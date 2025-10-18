# Lab 16
## Objective
* Registry Forensics 
* Understand Registry of windows

## Knowledge 
* Registry - a Type of database store configuration of the OS (Operating System), Software, User, perhipirals,etc...
* a source of information if we need to gathering data
* malware can store some data to registry
* Registry is a combination of 'hives'
* Windows Registry component:
  * Keys
  * Subkeys
  * Values
* Common hives:
  * HKEY_CLASSES_ROOT
  * HKEY_CURRENT_USER
  * HKEY_LOCAL_MACHINE
  * HKEY_USERS
  * HKEY_CURRENT_CONFIG
* Common Registry file
  *HKLM  
    * SAM
    * SOFTWARE
    * SYSTEM
    * SECURITY
  * HKCU
    * NTuser.dat

<img width="1129" height="278" alt="image" src="https://github.com/user-attachments/assets/5b187d53-060c-4e4c-95ad-1dc998691e85" />
 
## Lab Walkthrough
This lab will try to retrieve data from hives and in this lab we will do it in 2 ways
## RegRipper
```
regripper -r NTUSER.DAT -a > ntuser.txt
```
or
```
regripper -r NTUSER.DAT -f ntuser > ntuser.txt
```
<img width="942" height="369" alt="image" src="https://github.com/user-attachments/assets/56ebe1d4-ac4c-4693-8407-d5efa327ed09" />

The same goes for other
## Eric Zimmerman tools
We can use this toolkit to extract information from hives. we can also create template to find exact information for us. I will try to retrieve User Activity
```
recmd -d .\ --bn "D:\Get-ZimmermanTools\net9\RECmd\BatchExamples\UserActivity.reb" --csv output.csv --json output.json
```
<img width="2483" height="1622" alt="image" src="https://github.com/user-attachments/assets/ebe195e7-1fef-4eff-8354-07a74d616a68" />

<img width="2190" height="718" alt="image" src="https://github.com/user-attachments/assets/2a5e9922-af73-41ae-ad2e-49b83d1929b4" />

## Reference
* [Windows Registry Analysis](https://blog.cyber5w.com/introducing-windows-registry)
* [What Is Windows Registry? Your Complete Guide](https://www.ninjaone.com/blog/what-is-windows-registry/)
