#!/usr/bin/env python3
"""
VM automation helper for VMware (vmrun) and VirtualBox (vboxapi).

Features:
- List VMs / Start / Stop / Suspend / Revert snapshot
- Run a program in the guest
- Copy files to/from the guest (VMware)
- Screenshot (VMware)
- Locate .vmem (host-side physical memory file) for suspended VMware VMs

Requirements:
- VMware Workstation/Fusion: vmrun available (on PATH or default locations)
- VirtualBox + VirtualBox SDK: 'vboxapi' module available
"""

import argparse
import os
import sys
import time
import glob
import shutil
import subprocess
from typing import List, Tuple, Optional

# Known vmrun locations
VMRUN_CANDIDATES = {
    # macOS Fusion
    "/Applications/VMware Fusion.app/Contents/Library/vmrun": "fusion",
    "/Library/Application Support/VMware Fusion/vmrun": "fusion",
    # Linux Workstation
    "/usr/bin/vmrun": "ws",
    "/usr/local/bin/vmrun": "ws",
    # Windows Workstation
    r"C:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe": "ws",
    r"C:\Program Files\VMware\VMware Workstation\vmrun.exe": "ws",
}

def pinfo(msg: str) -> None:
    print(f"[INFO] {msg}")

def perror(msg: str) -> None:
    print(f"[ERROR] {msg}", file=sys.stderr)


# ----------------------------- VirtualBox -----------------------------

class VBoxAuto:
    """VirtualBox automation via vboxapi (VirtualBox SDK)."""

    def __init__(self, machine_id_or_name: str):
        self.machine = machine_id_or_name
        self.ctx = {}
        self.mach = None

    def _get_machines(self):
        return self.ctx["global"].getArray(self.ctx["vb"], "machines")

    def check(self) -> bool:
        try:
            from vboxapi import VirtualBoxManager  # provided by VirtualBox SDK
        except ImportError:
            perror("VirtualBox SDK not found. Install VirtualBox and its SDK to get 'vboxapi'.")
            return False

        vbm = VirtualBoxManager(None, None)
        self.ctx = {
            "global": vbm,
            "const": vbm.constants,
            "vb": vbm.vbox,
            "mgr": vbm.mgr,
        }

        # Resolve machine by name or UUID
        for m in self._get_machines():
            if m.name == self.machine or m.id == self.machine:
                self.mach = m
                break

        if self.mach is None:
            perror(f"Cannot find the machine: {self.machine}")
            return False

        pinfo(f"Using {self.mach.name} (uuid: {self.mach.id})")
        pinfo(f"Session state: {self._enum_name('SessionState', self.mach.sessionState)}")
        pinfo(f"Machine state: {self._enum_name('MachineState', self.mach.state)}")
        return True

    def _enum_name(self, enum: str, elem) -> str:
        try:
            all_vals = self.ctx["const"].all_values(enum)
            for name, value in all_vals.items():
                if str(elem) == str(value):
                    return name
        except Exception:
            pass
        return str(elem)

    def list(self) -> None:
        try:
            for m in self._get_machines():
                print(
                    f"{m.name:<24} {m.id} "
                    f"(state:{self._enum_name('MachineState', m.state)}/"
                    f"{self._enum_name('SessionState', m.sessionState)})"
                )
        except Exception:
            perror("No machines. Did you call check() first?")

    def start(self, headless: bool = False, boot_wait: int = 20) -> None:
        vb = self.ctx["vb"]
        session = self.ctx["mgr"].getSessionObject(vb)
        type_str = "headless" if headless else "gui"

        pinfo(f"Starting VM ({type_str})...")
        p = vb.openRemoteSession(session, self.mach.id, type_str, "")
        while not p.completed:
            p.waitForCompletion(1000)
            self.ctx["global"].waitForEvents(0)

        if int(p.resultCode) == 0:
            session.close()
            pinfo(f"Waiting {boot_wait} seconds to boot...")
            time.sleep(boot_wait)
        else:
            perror("Cannot start machine!")

    def _open_session(self):
        return self.ctx["global"].openMachineSession(self.mach.id)

    def _close_session(self, session):
        self.ctx["global"].closeMachineSession(session)
        time.sleep(2)

    def stop(self) -> None:
        session = self._open_session()
        pinfo("Powering down the system...")
        try:
            session.console.powerDown()
            time.sleep(3)
        finally:
            self._close_session(session)

    def suspend(self) -> None:
        session = self._open_session()
        pinfo("Saving machine state (suspend)...")
        try:
            session.console.saveState()
            time.sleep(3)
        finally:
            self._close_session(session)

    def revert(self, snapshot_name: str) -> None:
        session = self._open_session()
        pinfo(f"Reverting to snapshot '{snapshot_name}'")
        try:
            snap = session.machine.findSnapshot(snapshot_name)
            session.console.restoreSnapshot(snap)
            time.sleep(3)
        finally:
            self._close_session(session)

    def winexec(self, exe_path: str, user: str, passwd: str, args: List[str]) -> None:
        """Execute a program in the guest (requires Guest Additions + credentials)."""
        session = self._open_session()
        try:
            pinfo(f"Executing in guest: {exe_path} {' '.join(args) if args else ''}")
            env = []
            # executeProcess signature differs per platform; VirtualBox SDK handles it
            ret = session.console.guest.executeProcess(
                exe_path, 0, [exe_path] + (args or []), env, user, passwd, 0
            )
            # On Windows hosts, ret can be a tuple containing pid at index 3; otherwise index 1
            pid = ret[3] if os.name == "nt" and len(ret) > 3 else ret[1] if len(ret) > 1 else ret
            pinfo(f"Process ID: {pid}")
        finally:
            self._close_session(session)


# ------------------------------ VMware ------------------------------

class VMwareAuto:
    """VMware automation via vmrun."""

    def __init__(self, vmx_path: str, vmrun_path: Optional[str] = None):
        self.vmx = vmx_path
        if not os.path.isfile(self.vmx):
            raise FileNotFoundError(f"Cannot find .vmx file: {vmx_path}")

        self.vmrun, self.vmtype = self._find_vmrun(vmrun_path)
        self.user = None
        self.passwd = None
        pinfo(f"Found vmrun ({self.vmtype}) at: {self.vmrun}")

    def _find_vmrun(self, override: Optional[str]) -> Tuple[str, str]:
        if override:
            if os.path.isfile(override):
                return override, ("ws" if os.name != "posix" else "fusion")
            raise FileNotFoundError(f"vmrun not found at {override}")
        # search known locations then PATH
        for path, vmtype in VMRUN_CANDIDATES.items():
            if os.path.isfile(path):
                return path, vmtype
        vmrun_on_path = shutil.which("vmrun")
        if vmrun_on_path:
            # Best-effort type detection
            vmtype = "ws" if os.name in ("nt", "posix") else "fusion"
            return vmrun_on_path, vmtype
        raise FileNotFoundError("vmrun not found. Install VMware Workstation/Fusion, or supply --vmrun.")

    def set_user(self, user: str, passwd: str) -> None:
        self.user = user
        self.passwd = passwd

    def _run_cmd(self, cmd: str, args: List[str] = None, guest: bool = False) -> Tuple[str, str]:
        args = args or []
        pargs = [self.vmrun, "-T", self.vmtype]
        if guest:
            if not self.user or not self.passwd:
                raise RuntimeError("Guest credentials not set. Call set_user(user, passwd).")
            pargs += ["-gu", self.user, "-gp", self.passwd]
        pargs += [cmd, self.vmx] + args

        pinfo("Executing: " + " ".join(pargs))
        proc = subprocess.Popen(pargs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        out, _ = proc.communicate()
        return out, ""  # vmrun writes everything to stdout

    # High-level ops
    def list(self) -> str:
        out, _ = subprocess.Popen([self.vmrun, "list"], stdout=subprocess.PIPE, text=True).communicate()
        return out

    def start(self) -> str:
        return self._run_cmd("start")[0]

    def stop(self) -> str:
        return self._run_cmd("stop")[0]

    def suspend(self) -> str:
        return self._run_cmd("suspend")[0]

    def revert(self, snapshot_name: str) -> str:
        return self._run_cmd("revertToSnapshot", [snapshot_name])[0]

    def screenshot(self, out_file: str) -> str:
        return self._run_cmd("captureScreen", [out_file], guest=True)[0]

    def copy_to_vm(self, host_src: str, guest_dst: str) -> str:
        if not os.path.isfile(host_src):
            raise FileNotFoundError(f"Host source file not found: {host_src}")
        return self._run_cmd("copyFileFromHostToGuest", [host_src, guest_dst], guest=True)[0]

    def copy_to_host(self, guest_src: str, host_dst: str) -> str:
        return self._run_cmd("copyFileFromGuestToHost", [guest_src, host_dst], guest=True)[0]

    def winexec(self, file_path: str, args: str = "") -> str:
        # -interactive/-activeWindow helps when guest has UI
        vm_args = ["-noWait", "-interactive", "-activeWindow", file_path]
        if args:
            vm_args.append(args)
        return self._run_cmd("runProgramInGuest", vm_args, guest=True)[0]

    def find_memory_files(self) -> List[str]:
        """Return non-snapshot .vmem files next to the .vmx (for suspended VMs)."""
        base = os.path.dirname(self.vmx)
        mems = glob.glob(os.path.join(base, "*.vmem"))
        mems = [m for m in mems if "Snapshot" not in m]
        return mems


# ------------------------------- CLI --------------------------------

def make_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="VM automation for VMware/VirtualBox")
    sub = p.add_subparsers(dest="provider", required=True, help="vmware or vbox")

    # VMware
    p_vm = sub.add_parser("vmware", help="VMware vmrun operations")
    p_vm.add_argument("--vmx", required=True, help="Path to .vmx file")
    p_vm.add_argument("--vmrun", help="Path to vmrun (optional)")
    p_vm.add_argument("--user", help="Guest username (for guest ops)")
    p_vm.add_argument("--pass", dest="passwd", help="Guest password (for guest ops)")

    vm_actions = p_vm.add_subparsers(dest="action", required=True)
    vm_actions.add_parser("start")
    vm_actions.add_parser("stop")
    vm_actions.add_parser("suspend")
    rv = vm_actions.add_parser("revert"); rv.add_argument("snapshot")
    ls = vm_actions.add_parser("list")  # lists running VMs (global)
    sc = vm_actions.add_parser("screenshot"); sc.add_argument("outfile")
    tovm = vm_actions.add_parser("copy-to-vm"); tovm.add_argument("src"); tovm.add_argument("dst")
    tohost = vm_actions.add_parser("copy-to-host"); tohost.add_argument("src"); tohost.add_argument("dst")
    ex = vm_actions.add_parser("exec"); ex.add_argument("exe"); ex.add_argument("args", nargs=argparse.REMAINDER)
    mem = vm_actions.add_parser("find-mem")

    # VirtualBox
    p_vb = sub.add_parser("vbox", help="VirtualBox vboxapi operations")
    p_vb.add_argument("--vm", required=True, help="VM name or UUID")
    p_vb.add_argument("--headless", action="store_true")
    p_vb.add_argument("--boot-wait", type=int, default=20)
    p_vb.add_argument("--user", help="Guest username (for guest exec)")
    p_vb.add_argument("--pass", dest="passwd", help="Guest password (for guest exec)")

    vb_actions = p_vb.add_subparsers(dest="action", required=True)
    vb_actions.add_parser("check")
    vb_actions.add_parser("list")
    vb_actions.add_parser("start")
    vb_actions.add_parser("stop")
    vb_actions.add_parser("suspend")
    rv2 = vb_actions.add_parser("revert"); rv2.add_argument("snapshot")
    ex2 = vb_actions.add_parser("exec"); ex2.add_argument("exe"); ex2.add_argument("args", nargs=argparse.REMAINDER)

    return p

def main(argv: List[str]) -> int:
    parser = make_parser()
    args = parser.parse_args(argv)

    if args.provider == "vmware":
        try:
            vmw = VMwareAuto(args.vmx, args.vmrun)
            if args.user and args.passwd:
                vmw.set_user(args.user, args.passwd)

            if args.action == "start":
                print(vmw.start())
            elif args.action == "stop":
                print(vmw.stop())
            elif args.action == "suspend":
                print(vmw.suspend())
            elif args.action == "revert":
                print(vmw.revert(args.snapshot))
            elif args.action == "list":
                print(subprocess.Popen(["vmrun", "list"], stdout=subprocess.PIPE, text=True).communicate()[0])
            elif args.action == "screenshot":
                print(vmw.screenshot(args.outfile))
            elif args.action == "copy-to-vm":
                print(vmw.copy_to_vm(args.src, args.dst))
            elif args.action == "copy-to-host":
                print(vmw.copy_to_host(args.src, args.dst))
            elif args.action == "exec":
                print(vmw.winexec(args.exe, " ".join(args.args)))
            elif args.action == "find-mem":
                files = vmw.find_memory_files()
                print("\n".join(files) if files else "(none)")
        except Exception as e:
            perror(str(e))
            return 1

    elif args.provider == "vbox":
        vb = VBoxAuto(args.vm)
        if args.action in ("check", "list", "start", "stop", "suspend", "revert", "exec"):
            if not vb.check():
                return 1

        if args.action == "check":
            return 0
        elif args.action == "list":
            vb.list()
        elif args.action == "start":
            vb.start(headless=bool(args.headless), boot_wait=args.boot_wait)
        elif args.action == "stop":
            vb.stop()
        elif args.action == "suspend":
            vb.suspend()
        elif args.action == "revert":
            vb.revert(args.snapshot)
        elif args.action == "exec":
            if not (args.user and args.passwd):
                perror("Guest credentials required for exec. Provide --user and --pass.")
                return 1
            vb.winexec(args.exe, args.user, args.passwd, args.args)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
