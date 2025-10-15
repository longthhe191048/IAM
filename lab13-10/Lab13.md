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

## Testing
**Automated Script**
```
from vmauto import VMwareAuto
import os, time

vmx = r"C:\Users\WDchocopie\Desktop\Win2008Malware\Windows Server 2008 2.vmwarevm\Windows Server 2008 2.vmx"

vmw = VMwareAuto(vmx)
vmw.set_user("Administrator", "P@ssw0rd123!")  # non-empty password ✔

# Poll for explorer.exe using listProcessesInGuest()
def explorer_ready(timeout=180, poll=2):
    import time
    end = time.time() + timeout
    while time.time() < end:
        out = vmw._run_cmd("listProcessesInGuest", guest=True)[0]
        if "explorer.exe" in out.lower():
            return True
        time.sleep(poll)
    raise TimeoutError("No interactive desktop yet; auto-logon may not be configured.")

# 1) Start the VM
print(vmw.start())
explorer_ready(120)
print(vmw.suspend())
time.sleep(5)
print(vmw.start())
# 2) Wait a bit for the guest services to come up (Tools)
input("Continue?: ")
# 3) Run a program
print(vmw.winexec(r"C:\Windows\explorer.exe",r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Process Explorer.BAT", interactive=True, wait=True))
print(vmw.winexec(r"C:\Windows\System32\notepad.exe", interactive=False, wait=False))
input("Continue?: ")

# 4) Ensure the HOST folder exists before screenshot
os.makedirs(r"C:\temp", exist_ok=True)

# 5) Take a screenshot (host path). If this still fails, see note below to patch vmauto.
print(vmw.scrshot(r"C:\temp\shot.png"))

# 6) Suspend and list memory files (works as you already saw)
print(vmw.suspend())
print(vmw.findmem())

```
https://github.com/user-attachments/assets/976a4604-23af-4bba-8e51-50a30292233b

