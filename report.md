# Malware Analysis report
<img width="1613" height="603" alt="image" src="https://github.com/user-attachments/assets/169a5113-a261-4938-8d04-59dd818b067a" />

## Objective
* Make a template for a report
* Understand the report

## Report Structure
* Summary
  * Description
  * Submitted Files
* [File 1]
  * tags
  * Detail (name, size, checksum, etc...)
  * Antivirus (if possible)
  * Yara Rules (if possible)
  * PE data
  * Relationship
  * packers
  * Description
  * Screenshot

## Understand reference report

* Brief description of the incident / malware being analyzed
* Impact summary
* Key findings
* Summary of recommended mitigations
<img width="1583" height="597" alt="image" src="https://github.com/user-attachments/assets/707c34ed-2476-4449-a0c7-a5801dd99ba1" />

An example:
```
[This malware] is a collection of actor binaries likely to be deployed by exploiting security vulnerabilities in Windows OS devices
```

How many file are included in this report

<img width="1143" height="677" alt="image" src="https://github.com/user-attachments/assets/9c1f7921-6307-4c56-bcc7-bdbba0335eb2" />

Their names and detail about it

<img width="1562" height="685" alt="image" src="https://github.com/user-attachments/assets/5c5ff036-8e82-4607-ae41-23eaf0e093e1" />

Which antivirus is detected and rules to detect it

<img width="1492" height="901" alt="image" src="https://github.com/user-attachments/assets/744d661f-46d2-4551-aeef-e34cb32c4a67" />

Analyze execution file

<img width="1568" height="1177" alt="image" src="https://github.com/user-attachments/assets/7cc8c4ce-b04d-4b17-b75b-cf769f379a38" />

and then write a description with a POC

<img width="1622" height="1227" alt="image" src="https://github.com/user-attachments/assets/2a823b2b-f02c-4a19-99c9-4f339e3e80e2" />

## Reference
[Malware Analysis Report](https://www.cisa.gov/sites/default/files/2023-06/mar-10365227.r1.v1.clear_.pdf)
