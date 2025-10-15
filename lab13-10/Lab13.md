# Lab 13
## Objective
* Create and use a script to automate analysis with Virtual machine

## old script
[old](vmauto-old.py)

## New script
[new](vmauto-new.py)

## Usage
### Vmware
```
python vm_auto.py vmware --vmx "/path/to/Win10.vmx" start
python vm_auto.py vmware --vmx "/path/to/Win10.vmx" revert "Clean Snapshot"
python vm_auto.py vmware --vmx "/path/to/Win10.vmx" --user vbox --pass secret exec "C:\Windows\System32\notepad.exe"
python vm_auto.py vmware --vmx "/path/to/Win10.vmx" screenshot C:\temp\shot.png
python vm_auto.py vmware --vmx "/path/to/Win10.vmx" find-mem
```
### Virtual Box
```
python vm_auto.py vbox --vm "Win10-Lab" check
python vm_auto.py vbox --vm "Win10-Lab" start --headless --boot-wait 15
python vm_auto.py vbox --vm "Win10-Lab" revert "Clean"
python vm_auto.py vbox --vm "Win10-Lab" --user demo --pass secret exec "C:\\Windows\\System32\\notepad.exe"

```

