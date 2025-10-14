#!/usr/bin/env python3
"""
Modern Multi-AV Uploader with SQLite (VirusTotal v3, MetaDefender, Hybrid Analysis)

- Python 3.8+
- pip install requests

Env/API keys (export before running or pass via CLI):
  VT_API_KEY=...              # VirusTotal v3
  METADEFENDER_API_KEY=...    # OPSWAT MetaDefender Cloud
  HA_API_KEY=...              # Hybrid Analysis (Falcon Sandbox)
  HA_USER_AGENT=...           # e.g. "Falcon Sandbox"

Usage examples:
  python3 multiav.py --init
  python3 multiav.py -f sample.bin --vt --meta
  python3 multiav.py -f sample.bin --vt --meta --ha --overwrite
"""

import os
import sys
import time
import hashlib
import sqlite3
import argparse
from typing import Dict, List, Optional

import requests

DBNAME = "virus.db"
MAXWAIT = 60 * 10           # 10 minutes total wait per service
POLL_INTERVAL = 10          # 10s between polls
MAX_RETRIES = 3             # retry count for transient errors (per request)


# --------------------------- Helpers ---------------------------

def md5_bytes(b: bytes) -> str:
    return hashlib.md5(b).hexdigest()

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def read_file_bytes(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()

def safe_get(d: dict, *path, default=None):
    cur = d
    for p in path:
        if isinstance(cur, dict) and p in cur:
            cur = cur[p]
        else:
            return default
    return cur

def merge_detects(*maps: Dict[str, str]) -> Dict[str, str]:
    out = {}
    for m in maps:
        for k, v in (m or {}).items():
            if k and v:
                out[k] = v
    return out

def backoff_sleep(i: int):
    # 0 -> 1s, 1 -> 2s, 2 -> 4s (capped 10s)
    time.sleep(min(10, 2 ** max(0, i)))


# --------------------------- Database ---------------------------

def initdb():
    if os.path.isfile(DBNAME):
        print("File already exists, initialization not required.")
        return
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    # Enforce foreign keys
    cur.execute("PRAGMA foreign_keys = ON;")
    cur.executescript("""
        CREATE TABLE samples (
            id      INTEGER PRIMARY KEY,
            md5     TEXT NOT NULL UNIQUE,
            sha256  TEXT NOT NULL UNIQUE
        );

        CREATE TABLE detects (
            id       INTEGER PRIMARY KEY,
            sid      INTEGER NOT NULL,
            vendor   TEXT NOT NULL,
            name     TEXT NOT NULL,
            UNIQUE (sid, vendor),
            FOREIGN KEY (sid) REFERENCES samples(id) ON DELETE CASCADE
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("Success.")

def _db_connect():
    conn = sqlite3.connect(DBNAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def savetodb(filename: str, detects: Dict[str, str], force: bool = False):
    if not detects:
        print("Nothing to add, submission yielded no detections (or still pending).")
        return

    if not os.path.isfile(DBNAME):
        print(f"{DBNAME} does not exist, run --init first.")
        return

    data = read_file_bytes(filename)
    md5 = md5_bytes(data)
    sha256 = sha256_bytes(data)

    conn = _db_connect()
    cur = conn.cursor()

    # match by sha256 first (preferred), fallback to md5
    cur.execute("SELECT id FROM samples WHERE sha256=? OR md5=?", (sha256, md5))
    ids = [row[0] for row in cur.fetchall()]

    if ids and not force:
        id_list = ",".join(str(i) for i in ids)
        print(f"Sample already exists with ID(s): {id_list}. Use --overwrite to replace.")
        cur.close()
        conn.close()
        return
    elif ids and force:
        # Delete child rows first, then parent (or rely on FK cascade)
        qmarks = ",".join("?" * len(ids))
        cur.execute(f"DELETE FROM detects WHERE sid IN ({qmarks})", ids)
        cur.execute(f"DELETE FROM samples WHERE id IN ({qmarks})", ids)

    try:
        cur.execute("INSERT INTO samples (md5, sha256) VALUES (?, ?)", (md5, sha256))
        sid = cur.lastrowid
    except sqlite3.IntegrityError:
        # Likely an old DB without sha256; suggest re-init
        print("DB schema mismatch (likely missing sha256/constraints). Consider re-running with --init on a new DB.")
        cur.close()
        conn.close()
        return

    for vendor, name in detects.items():
        cur.execute("INSERT OR IGNORE INTO detects (sid, vendor, name) VALUES (?,?,?)", (sid, vendor, name))

    conn.commit()
    cur.close()
    conn.close()
    print(f"Saved {len(detects)} detections to DB (sample id={sid}).")


# --------------------------- HTTP wrapper ---------------------------

class Http:
    def __init__(self):
        self.s = requests.Session()

    def get(self, url, headers=None, timeout=30):
        for i in range(MAX_RETRIES):
            try:
                r = self.s.get(url, headers=headers, timeout=timeout)
                if r.status_code == 429:
                    backoff_sleep(i)
                    continue
                return r
            except requests.RequestException:
                backoff_sleep(i)
        return self.s.get(url, headers=headers, timeout=timeout)

    def post(self, url, headers=None, files=None, data=None, timeout=120):
        for i in range(MAX_RETRIES):
            try:
                r = self.s.post(url, headers=headers, files=files, data=data, timeout=timeout)
                if r.status_code == 429:
                    backoff_sleep(i)
                    continue
                return r
            except requests.RequestException:
                backoff_sleep(i)
        return self.s.post(url, headers=headers, files=files, data=data, timeout=timeout)


# --------------------------- Services ---------------------------

class VirusTotalV3:
    """VirusTotal v3: hash lookup, upload (incl. large-file flow), poll result.
    API docs: https://developers.virustotal.com/reference/overview
    """

    def __init__(self, api_key: Optional[str]):
        self.api_key = api_key
        self.http = Http()
        self.base = "https://www.virustotal.com/api/v3"

    def _headers(self):
        return {"x-apikey": self.api_key}

    def _upload(self, file_path: str):
        size = os.path.getsize(file_path)
        url = f"{self.base}/files"
        if size > 32 * 1024 * 1024:  # >32MB needs upload_url
            u = self.http.get(f"{self.base}/files/upload_url", headers=self._headers(), timeout=30)
            if u.status_code != 200:
                return u  # let caller handle
            url = u.json()["data"]
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f)}
            return self.http.post(url, headers=self._headers(), files=files, timeout=300)

    def submit(self, file_path: str) -> Dict[str, str]:
        if not self.api_key:
            print("[VT] Skipped: missing VT_API_KEY")
            return {}

        b = read_file_bytes(file_path)
        sha256hex = sha256_bytes(b)
        md5hex = md5_bytes(b)

        # 1) hash lookup (prefer sha256)
        try:
            r = self.http.get(f"{self.base}/files/{sha256hex}", headers=self._headers(), timeout=30)
            if r.status_code == 200:
                detects = self._extract_detections(r.json())
                if detects:
                    print("[VT] Found existing report.")
                    return detects
        except requests.RequestException as e:
            print(f"[VT] Hash lookup error: {e}")

        # 2) upload
        print("[VT] Uploading file...")
        try:
            r = self._upload(file_path)
            if r.status_code not in (200, 201):
                print(f"[VT] Upload failed: {r.status_code} {r.text[:200]}")
                return {}
            analysis_id = safe_get(r.json(), "data", "id")
            if not analysis_id:
                print("[VT] No analysis id returned.")
                return {}
        except requests.RequestException as e:
            print(f"[VT] Upload error: {e}")
            return {}

        # 3) poll analysis
        print("[VT] Polling analysis...")
        t0 = time.time()
        while time.time() - t0 < MAXWAIT:
            try:
                rr = self.http.get(f"{self.base}/analyses/{analysis_id}", headers=self._headers(), timeout=30)
                if rr.status_code == 200:
                    status = safe_get(rr.json(), "data", "attributes", "status")
                    if status == "completed":
                        # final report can lag; retry fetch a few times
                        for _ in range(6):  # up to ~60s
                            fr = self.http.get(f"{self.base}/files/{sha256hex}", headers=self._headers(), timeout=30)
                            if fr.status_code == 200:
                                detects = self._extract_detections(fr.json())
                                if detects or safe_get(fr.json(), "data", "attributes", "last_analysis_results"):
                                    return detects
                            time.sleep(10)
                        break
                time.sleep(POLL_INTERVAL)
            except requests.RequestException as e:
                print(f"[VT] Poll error: {e}")
                break
        print("[VT] Timed out waiting for verdict.")
        return {}

    @staticmethod
    def _extract_detections(j: dict) -> Dict[str, str]:
        """Map: engine_name -> result (only when category == malicious)."""
        out = {}
        stats = safe_get(j, "data", "attributes", "last_analysis_results", default={})
        if not isinstance(stats, dict):
            return out
        for engine, info in stats.items():
            cat = info.get("category")
            res = info.get("result")
            if cat == "malicious" and res:
                out[engine] = res
        return out


class MetaDefenderCloud:
    """OPSWAT MetaDefender Cloud
    Docs: https://metadefender.opswat.com/docs
    """

    def __init__(self, api_key: Optional[str]):
        self.api_key = api_key
        self.http = Http()
        self.base = "https://api.metadefender.com/v4"

    def _headers(self):
        return {"apikey": self.api_key}

    def submit(self, file_path: str) -> Dict[str, str]:
        if not self.api_key:
            print("[META] Skipped: missing METADEFENDER_API_KEY")
            return {}

        b = read_file_bytes(file_path)
        sha256hex = sha256_bytes(b)

        # 1) hash lookup (accepts md5/sha1/sha256)
        try:
            r = self.http.get(f"{self.base}/hash/{sha256hex}", headers=self._headers(), timeout=30)
            if r.status_code == 200:
                detects = self._extract_detections(r.json())
                if detects:
                    print("[META] Found existing report.")
                    return detects
        except requests.RequestException as e:
            print(f"[META] Hash lookup error: {e}")

        # 2) upload
        print("[META] Uploading file...")
        try:
            with open(file_path, "rb") as f:
                r = self.http.post(f"{self.base}/file", headers=self._headers(), files={"file": f}, timeout=300)
            if r.status_code not in (200, 201):
                print(f"[META] Upload failed: {r.status_code} {r.text[:200]}")
                return {}
            data_id = r.json().get("data_id")
            if not data_id:
                print("[META] No data_id returned.")
                return {}
        except requests.RequestException as e:
            print(f"[META] Upload error: {e}")
            return {}

        # 3) poll
        print("[META] Polling analysis...")
        t0 = time.time()
        while time.time() - t0 < MAXWAIT:
            try:
                rr = self.http.get(f"{self.base}/file/{data_id}", headers=self._headers(), timeout=30)
                if rr.status_code == 200:
                    j = rr.json()
                    status = safe_get(j, "scan_results", "scan_all_result_a", default="")
                    progress = safe_get(j, "scan_results", "progress_percentage", default=0)
                    if progress == 100 or status:
                        det = self._extract_detections(j)
                        return det
                time.sleep(POLL_INTERVAL)
            except requests.RequestException as e:
                print(f"[META] Poll error: {e}")
                break
        print("[META] Timed out waiting for verdict.")
        return {}

    @staticmethod
    def _extract_detections(j: dict) -> Dict[str, str]:
        out = {}
        engines = safe_get(j, "scan_results", "scan_details", default={})
        if not isinstance(engines, dict):
            return out
        for engine, info in engines.items():
            threat = info.get("threat_found")
            if threat and threat != "Clean":
                out[engine] = threat
        return out


class HybridAnalysis:
    """Hybrid Analysis (CrowdStrike Falcon Sandbox)
    Docs: https://www.hybrid-analysis.com/docs/api/v2
    Requires HA_API_KEY and HA_USER_AGENT header.
    """

    def __init__(self, api_key: Optional[str], user_agent: Optional[str]):
        self.api_key = api_key
        self.user_agent = user_agent
        self.http = Http()
        # Use apex domain to avoid redirect/TLS issues
        self.base = "https://hybrid-analysis.com/api/v2"

    def _headers(self):
        return {
            "api-key": self.api_key or "",
            "User-Agent": self.user_agent or "Falcon Sandbox",
            "accept": "application/json",
        }

    def submit(self, file_path: str) -> Dict[str, str]:
        if not self.api_key:
            print("[HA] Skipped: missing HA_API_KEY")
            return {}
        if not self.user_agent:
            print("[HA] Skipped: missing HA_USER_AGENT")
            return {}

        print("[HA] Uploading file for analysis...")
        try:
            with open(file_path, "rb") as f:
                files = {"file": (os.path.basename(file_path), f)}
                # 120 = Windows 10 64-bit (per docs)
                data = {"environment_id": "120"}  # NOTE: quick_scan removed (not accepted on your account/API)
                r = self.http.post(f"{self.base}/submit/file", headers=self._headers(), files=files, data=data, timeout=300)
            if r.status_code not in (200, 201):
                print(f"[HA] Upload failed: {r.status_code} {r.text[:200]}")
                return {}
            j = r.json()
            job_id = j.get("job_id")
            if not job_id:
                print("[HA] No job_id returned.")
                return {}
        except requests.RequestException as e:
            print(f"[HA] Upload error: {e}")
            return {}

        print("[HA] Polling job status...")
        t0 = time.time()
        while time.time() - t0 < MAXWAIT:
            try:
                rr = self.http.get(f"{self.base}/report/{job_id}/state", headers=self._headers(), timeout=30)
                if rr.status_code == 200:
                    state = rr.json().get("state")
                    if state in ("SUCCESS", "ERROR"):
                        break
                time.sleep(POLL_INTERVAL)
            except requests.RequestException as e:
                print(f"[HA] Poll error: {e}")
                break

        # fetch summary if available
        try:
            rep = self.http.get(f"{self.base}/report/{job_id}/summary", headers=self._headers(), timeout=30)
            if rep.status_code == 200:
                return self._extract_detections(rep.json())
        except requests.RequestException as e:
            print(f"[HA] Summary fetch error: {e}")
        return {}

    @staticmethod
    def _extract_detections(j: dict) -> Dict[str, str]:
        """
        Hybrid Analysis gives behaviors/signatures rather than AV vendor names.
        We map notable signature names under a "HybridAnalysis" pseudo-vendor.
        """
        out = {}
        sigs = j.get("signatures") or []
        names = [s.get("name") for s in sigs if s.get("name")]
        if names:
            out["HybridAnalysis"] = "; ".join(names[:10]) + (" ..." if len(names) > 10 else "")
        verdict = j.get("verdict")
        if verdict:
            out["HA_Verdict"] = verdict
        return out


# --------------------------- CLI ---------------------------

def main():
    ap = argparse.ArgumentParser(description="Modern Multi-AV Uploader (VT v3, MetaDefender, HybridAnalysis)")
    ap.add_argument("--init", action="store_true", help="initialize virus.db (creates schema with sha256 + FK cascade)")
    ap.add_argument("-o", "--overwrite", action="store_true", help="overwrite existing DB entry if sample MD5/SHA256 exists")
    ap.add_argument("-f", "--file", help="path to file to upload/analyze")
    ap.add_argument("--vt", action="store_true", help="use VirusTotal v3")
    ap.add_argument("--meta", action="store_true", help="use MetaDefender Cloud")
    ap.add_argument("--ha", action="store_true", help="use Hybrid Analysis")
    ap.add_argument("--vt-key", default=os.getenv("VT_API_KEY"), help="VirusTotal API key (env VT_API_KEY)")
    ap.add_argument("--meta-key", default=os.getenv("METADEFENDER_API_KEY"), help="MetaDefender API key (env METADEFENDER_API_KEY)")
    ap.add_argument("--ha-key", default=os.getenv("HA_API_KEY"), help="Hybrid Analysis API key (env HA_API_KEY)")
    ap.add_argument("--ha-ua", default=os.getenv("HA_USER_AGENT"), help="Hybrid Analysis User-Agent (env HA_USER_AGENT)")
    args = ap.parse_args()

    if args.init:
        initdb()
        return

    if not args.file:
        ap.error("You must supply --file")
    if not (args.vt or args.meta or args.ha):
        ap.error("You must choose at least one service: --vt/--meta/--ha")
    if not os.path.isfile(args.file):
        ap.error(f"{args.file} does not exist")

    all_detects: List[Dict[str, str]] = []

    if args.vt:
        vt = VirusTotalV3(args.vt_key)
        vt_detects = vt.submit(args.file)
        if vt_detects:
            print("[VT] Detections:")
            for k, v in vt_detects.items():
                print(f"  {k:30} => {v}")
        all_detects.append(vt_detects)

    if args.meta:
        meta = MetaDefenderCloud(args.meta_key)
        md_detects = meta.submit(args.file)
        if md_detects:
            print("[META] Detections:")
            for k, v in md_detects.items():
                print(f"  {k:30} => {v}")
        all_detects.append(md_detects)

    if args.ha:
        ha = HybridAnalysis(args.ha_key, args.ha_ua)
        ha_detects = ha.submit(args.file)
        if ha_detects:
            print("[HA] Findings:")
            for k, v in ha_detects.items():
                print(f"  {k:30} => {v}")
        all_detects.append(ha_detects)

    merged = merge_detects(*all_detects)
    if merged:
        savetodb(args.file, merged, force=args.overwrite)
    else:
        print("No detections to save (file may be clean or analyses still pending).")


if __name__ == "__main__":
    main()
