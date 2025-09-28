# Lab 06 Public AV Scanners (VirusTotal, JoeSandbox)
<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->

- [Lab 06 Public AV Scanners (VirusTotal, JoeSandbox)](#lab-06-public-av-scanners-virustotal-joesandbox)
   * [Objective ](#objective)
   * [requirement](#requirement)
- [Lab Walkthrough](#lab-walkthrough)

<!-- TOC end -->
## Objective 
* using public AV scanner

## requirement
* Sample [malware](https://wildfire.paloaltonetworks.com/publicapi/test/pe)

# Lab Walkthrough

<img width="2880" height="1465" alt="image" src="https://github.com/user-attachments/assets/1e455cba-1d9c-4f7b-b54b-fff1b4fbef20" />

**Analyze**
* Tag:
  * `peexe`: PE file, .exe
  * `cve-2020-0601`: A spoofing vulnerability exists in the way Windows CryptoAPI (Crypt32.dll) validates Elliptic Curve Cryptography (ECC) certificates.An attacker could exploit the vulnerability by using a spoofed code-signing certificate to sign a malicious executable, making it appear the file was from a trusted, legitimate source, aka 'Windows CryptoAPI Spoofing Vulnerability'. [link](https://nvd.nist.gov/vuln/detail/cve-2020-0601)
  * `exploit`: Security vendor detect a exploit in vulnerability
* Popular threat label: trojan.bebloh/autog
* Thread categories: trojan, pua(Potentially Unwanted Application)
* Community score: 36/71 total of AV

**Detail**

<img width="2822" height="1117" alt="image" src="https://github.com/user-attachments/assets/81a175fd-c8b7-4167-a711-9c5c043c1269" />

**Relation**

<img width="1602" height="1273" alt="image" src="https://github.com/user-attachments/assets/a2da99dd-172c-4cd3-bbff-1d8f85f17b17" />

**Behavior**

<img width="2810" height="1340" alt="image" src="https://github.com/user-attachments/assets/d6cfe06d-91bc-4485-968f-335c23cd83f5" />





