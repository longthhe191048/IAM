# Lab 04
<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->

- [Lab 04](#lab-04)
   * [Objective](#objective)
   * [Prerequisite / Requirement](#prerequisite--requirement)
   * [Pre-lab knowledge](#pre-lab-knowledge)
   * [Lab walkthrough and definition](#lab-walkthrough-and-definition)
- [encoding: utf-8](#encoding-utf-8)
- [Tested on Linux (Ubuntu), Windows 10/11, and macOS](#tested-on-linux-ubuntu-windows-1011-and-macos)

<!-- TOC end -->
## Objective
* Install and understand `yara`
* Understand and convert code `clamav_to_yara.py` from `python2` to `python3`

## Prerequisite / Requirement
* Kali linux / any debian / linux VM
* Understand how to craft a signature file for clamav

## Pre-lab knowledge
* YARA is a tool aimed at helping malware researchers to identify and classify malware samples.
* Allowed to create descriptions of malware families based on textual or binary patterns
* Creating rules with wildcard, REGEX, etc...
* Difference between `yara` and `clamav`:
  * `clamav`: antivirus scanner
  * `yara`: write a rule for detection of malwares 

## Lab walkthrough and definition
1. First, run and update our package manager
```
sudo apt update
```
<img width="2880" height="1800" alt="image" src="https://github.com/user-attachments/assets/6ed92d0f-28e9-46a7-ab5e-4fb014070907" />

2. Install `yara` with our package manager
```
sudo apt install yara
```
<img width="1938" height="1015" alt="image" src="https://github.com/user-attachments/assets/ea07dbec-25d4-41e6-aa24-0e08d2d7ea69" />

3. We will download some of the material given by the lab
```
wget https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/clamsrch/package.01.ful.7z
curl -o clamav_to_yara.py https://raw.githubusercontent.com/mattulm/volgui/refs/heads/master/tools/clamav_to_yara.py
```
<img width="1946" height="1038" alt="image" src="https://github.com/user-attachments/assets/91d628a0-9b48-4913-99b6-f6ed175f5e9f" />

4. Unzip the 7z file
```
7z e package.01.ful.7z
```
<img width="1964" height="1000" alt="image" src="https://github.com/user-attachments/assets/4cf7af82-3d3c-4405-a036-489ccf194f47" />

5. Now we will analyze the `clamav_to_yara.py` file

This is the rule's format for `yara`
```
rule %s
{
strings:
%s
condition:
%s
}

```

This is the signature format for `clamav`
```
# name:sigtype:offset:signature
```

So in `clamav` signature, i can divide it into 4 part and match it to `yara` rules

```
rule <RuleName>
{
strings:
    $a0 = { <hex pattern 1> }
    $a1 = { <hex pattern 2> }
    ...
condition:
    $a0 and $a1 and $a2 ...
}
```
in this script, they also converted where wildcard in `clamav` to `yara` like below
| clamav | yara  |
| ------ | ----- |
| `{-n}`   | `[0-n]` |
| `{n-}`   | `[0-n]` |
| `{n-m}`  | `[n-m]` |
| `{n}`    | `[n]`   |
| `*` or any type above has more than 255 bytes      | `*`     |

**Naming rules**:
* convert any Non-alphanumerics to `_`
* leading digit remove

Example
```Trojan.longthhe191048:0:*:4D 5A {10} FF```
```
rule Trojan_longthhe191048
{
strings:
    $a0 = { 4D 5A [10] FF }
condition:
    $a0
}

```
convert the script to python3
```
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
```

<img width="1939" height="999" alt="image" src="https://github.com/user-attachments/assets/45ad2f3b-2c1f-4bd0-be67-b573c1af227d" />

and run the script 
```
sudo python clamav_to_yara_py3.py -f clamsrch.ndb -o clamsrch.yara
```

<img width="1338" height="590" alt="image" src="https://github.com/user-attachments/assets/004bc21d-310f-4ca9-811a-8facb8623dc2" />

let's check the `ndb` file and `yara` file and get one sample of them

`.ndb`
```
Erlang [32.big.AND]:0:*:9e3779b9{-20}3c6ef372{-20}daa66d2b{-20}78dde6e4{-20}1715609d{-20}b54cda56{-20}5384540f{-20}f1bbcdc8{-20}8ff34781{-20}2e2ac13a{-20}cc623af3{-20}6a99b4ac{-20}08d12e65{-20}a708a81e{-20}454021d7
```

`.yara`
```
rule Erlang__32_big_AND_
{
strings:
        $a0 = { 9e3779b9[0-20]3c6ef372[0-20]daa66d2b[0-20]78dde6e4[0-20]1715609d[0-20]b54cda56[0-20]5384540f[0-20]f1bbcdc8[0-20]8ff34781[0-20]2e2ac13a[0-20]cc623af3[0-20]6a99b4ac[0-20]08d12e65[0-20]a708a81e[0-20]454021d7 }

condition:
        $a0
}
```

6. Test `yara`
```
yara -r clamsrch.yara /home/kali
```
<img width="1941" height="993" alt="image" src="https://github.com/user-attachments/assets/a185b67b-d1a7-432b-9d5c-b569a9ed621a" />

7. Create custom rules for `yara`. I will get my previous example from [this](https://github.com/longthhe191048/IAM/blob/main/Lab_02%2B03/Lab02%2B03.md) lab

```
echo "IAM is the best" > "test"
```
and i have SHA1 + size of it using `sigtool`: `bc241de771d6e4ffcab98337e06cc3fa64262221:16:test`

i can craft something like this

```
import "hash"

rule test_sha1_16b
{
    condition:
        filesize == 16 and
        hash.sha1(0, filesize) == "bc241de771d6e4ffcab98337e06cc3fa64262221"
}
```
or this
```
rule longthhe191048_test{
    
    strings:
        $a = "IAM is the best"

    condition:
        $a
}
```

<img width="813" height="401" alt="image" src="https://github.com/user-attachments/assets/59e9971f-16af-4c93-afb6-1af10259d0d9" />

## Reference
* [Writing YARA rules](https://yara.readthedocs.io/en/stable/writingrules.html)
* [clamav_to_yara](https://github.com/mattulm/volgui/blob/master/tools/clamav_to_yara.py)
* [yara(git)](https://github.com/VirusTotal/yara)
* [yara(kali)](https://www.kali.org/tools/yara/)
* [yara module](https://yara.readthedocs.io/en/stable/modules.html)
* [What is the difference between YARA and CLAMAV?](https://security.stackexchange.com/questions/73676/what-is-the-difference-between-yara-and-clamav)
