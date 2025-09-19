#!/usr/bin/env python3
# encoding: utf-8
#
# Tested on Linux (Ubuntu), Windows 10/11, and macOS
#
"""
clamav_to_yara.py

Original by Matthew Richard (2010-03-12)
Python 3 conversion & minor hardening by <you>.
"""

import os
import re
import sys
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Convert ClamAV hex signatures to YARA rules."
    )
    parser.add_argument(
        "-f", "--file", dest="filename", type=str, required=True, help="scanned FILENAME"
    )
    parser.add_argument(
        "-o", "--output-file", dest="outfile", type=str, required=True, help="output filename"
    )
    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", default=False, help="verbose"
    )
    parser.add_argument(
        "-s", "--search", dest="search", type=str, default="", help="search filter"
    )

    opts = parser.parse_args()

    if not os.path.isfile(opts.filename):
        parser.error(f"{opts.filename} does not exist")

    yara_rule = """
rule {rulename}
{{
strings:
{detects}
condition:
{conds}
}}

"""
    rules = {}
    output = ""

    # Read as text; ClamAV sigs are line-oriented ASCII. Use errors='replace' to be forgiving.
    with open(opts.filename, "r", encoding="utf-8", errors="replace") as fin:
        data = fin.readlines()

    if (opts.filename.endswith(".cvd") or opts.filename.endswith(".cld")) and data and data[0].startswith("ClamAV"):
        print("It seems you're passing a compressed database.")
        print("Try using sigtool -u to decompress first.")
        return

    print(f"[+] Read {len(data)} lines from {opts.filename}")

    # ClamAV signatures are one per line
    for raw_line in data:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        # signature format is: name:sigtype:offset:signature[:...]
        try:
            vals = line.split(":")
            if len(vals) < 4 or len(vals) > 6:
                print("**ERROR reading ClamAV signature file**")
                continue
            name = vals[0]
            sigtype = vals[1]
            offset = vals[2]
            signature = vals[3]
        except Exception:
            print("**ERROR reading ClamAV signature file**")
            continue

        # if specified, only parse rules that match a search criteria
        if opts.search not in name:
            continue

        # sanitize rule name for YARA compatibility
        # YARA allows [A-Za-z0-9_], cannot start with a number
        rulename = re.sub(r"(\W)", "_", name)
        rulename = re.sub(r"(^[0-9]{1,})", "", rulename) or "rule_" + str(abs(hash(name)) % (10**8))

        # if the rule doesn't exist, create a dict entry
        if rulename not in rules:
            rules[rulename] = []

        # handle the ClamAV style jumps

        # {-n} is n or less bytes  ->  {0-n}  ->  [0-n] in YARA
        signature = re.sub(r"(\{-(\d+)\})", r"{0-\g<2>}", signature)

        # {n-} is n or more bytes
        matches = re.findall(r"(\{(\d+)-\})", signature)
        if matches:
            for match in matches:
                start = int(match[1])
                jump_regex = re.compile(r"(\{(%d)-\})" % start)
                if start < 256:
                    signature = jump_regex.sub(r"[0-\g<2>]", signature)
                else:
                    # long jump not representable in a single hex jump -> split later with '*'
                    signature = jump_regex.sub("*", signature)

        # {n-m} is n to m bytes, must be <=255 and (m-n) < 256
        matches = re.findall(r"(\{(\d+)-(\d+)\})", signature)
        if matches:
            for match in matches:
                start = int(match[1])
                end = int(match[2])
                jump_regex = re.compile(r"(\{(%d)-(%d)\})" % (start, end))
                if (end - start) == 0:
                    if opts.verbose:
                        print("\t**Skip nothing, impossible!**")
                    signature = jump_regex.sub("", signature)
                elif (end - start) < 256 and end < 256:
                    signature = jump_regex.sub(r"[\g<2>-\g<3>]", signature)
                else:
                    signature = jump_regex.sub("*", signature)

        # {n} bytes -> [n] if n < 256, else '*'
        matches = re.findall(r"(\{(\d+)\})", signature)
        if matches:
            for match in matches:
                n = int(match[1])
                jump_regex = re.compile(r"(\{(%d)\})" % n)
                if n < 256:
                    signature = jump_regex.sub(r"[\g<2>]", signature)
                else:
                    signature = jump_regex.sub("*", signature)

        # translate the '*' operator into a pair of signatures with an 'and'
        # '*' means "arbitrary bytes between parts", which YARA hex cannot encode directly;
        # we instead create multiple hex strings and AND them in condition.
        if "*" in signature:
            for part in signature.split("*"):
                part = part.strip()
                if not part:
                    continue
                if part[0:1] != "(":
                    rules[rulename].append(part)
        else:
            sig = signature.strip()
            if sig and sig[0:1] != "(":
                rules[rulename].append(sig)

    # Build YARA text
    for rule, detects_list in rules.items():
        if not detects_list:
            if opts.verbose:
                print(f"\t**Found empty rule {rule}, skipping**")
            continue

        detects_lines = []
        cond_parts = []
        for idx, detect in enumerate(detects_list):
            detects_lines.append(f"\t$a{idx} = {{ {detect} }}")
            cond_parts.append(f"$a{idx}")

        detects = "\r\n".join(detects_lines) + "\r\n"
        conds = "\t" + " and ".join(cond_parts)

        output += yara_rule.format(rulename=rule, detects=detects, conds=conds)

    if output:
        print(f"\n[+] Wrote {len(rules)} rules to {opts.outfile}\n")
        with open(opts.outfile, "w", encoding="utf-8", errors="replace", newline="\n") as fout:
            fout.write(output)
    else:
        print("\n**Could not find any signatures to convert!!!**\n")


if __name__ == "__main__":
    print("\n" + "#" * 75)
    print("\tMalware Analyst's Cookbook - ClamAV to YARA Converter 0.0.1 (Py3)")
    print("#" * 75 + "\n")
    main()
