# win32api
## Overview
* Win32 API(Windows Application Program Interface) is a collection of function and data structure that Windows operating systems provide for applications to interact with the operating system.
* Allows to managing windows, accessing hardware, interacting with system components, and handling user input.

<img width="693" height="699" alt="image" src="https://github.com/user-attachments/assets/f1daf30e-58b6-40f6-8ffe-6e941575d94c" />

**Explaination**
* User mode:
  * No direct access to hardware
  * Access to “owned” memory location
* Kernel mode:
  * Direct access to hardware
  * Access to entire physical memory

  ## Key component of Win32 API
  * Function:
    * creating windows
    * reading file
    * handling input
    * etc...
* Constant:
  * error code
  * message identifier
  * etc...
* Data type:
  * device contexts
  * strings

## Specified: Kernel32.dll
Kernel32.dll is a DLL file to manage system memory, input/output operations and interrupts. This file is loaded into a protective memory space when Windows starts up in an effort to prevent other applications from taking over this space.

**Key function**

1\. Process and Thread Management:
* CreateProcess: Creates a new process and its primary thread.   
* ExitProcess: Terminates a process and all its threads.   
* CreateThread: Creates a new thread in the calling process.   
* ExitThread: Exits a thread.
* GetCurrentProcess: Retrieves a pseudohandle for the current process.  
* GetCurrentThread: Retrieves a pseudohandle for the current thread.
  
2\. Memory Management:
* VirtualFree: Releases or decommits a region of pages within the virtual address space of the calling process.    
* GlobalAlloc: Allocates memory from the global heap.   
* GlobalFree: Frees memory allocated from the global heap.
    
3\. Input/Output (I/O) Operations:
* ReadFile: Reads data from a file or input/output (I/O) device.  
* WriteFile: Writes data to a file or I/O device. 
* CreateFile: Creates or opens a file or I/O device.  
* CloseHandle: Closes an open object handle.

4\. Synchronization:
* CreateMutex: Creates or opens a named or unnamed mutex object.
* CreateEvent: Creates or opens a named or unnamed event object.
* WaitForSingleObject: Waits until the specified object is in the signaled state or the time-out interval elapses.
* WaitForMultipleObjects: Waits until one or all of the specified objects are in the signaled state or the time-out interval elapses.
  
5\. System Information:
* GetVersion: Returns the version number of the operating system.
* GetSystemTime: Retrieves the current system date and time.
* GetTickCount: Retrieves the number of milliseconds that have elapsed since the system was started.

**Kernel32.dll with malware**
* Process Injection
* Persistence
* Evasion
* Data Exfiltration
* Privilege Escalation

## Example
I've coded and convert code into a PE file that use kernel32.dll to create process and call `notepad.exe`.
```
import time
import win32con
import win32process
import win32api
# Path or command line of the program to launch
cmd = r"notepad.exe"  # change to test program you trust

si = win32process.STARTUPINFO()   # default STARTUPINFO
# CREATE_SUSPENDED: process created but primary thread not running
hProcess, hThread, pid, tid = win32process.CreateProcess(
    None,            # appName
    cmd,             # commandLine
    None,            # processAttributes
    None,            # threadAttributes
    False,           # bInheritHandles
    win32con.CREATE_SUSPENDED,   # dwCreationFlags
    None,            # newEnvironment
    None,            # currentDirectory
    si               # startupInfo
)


# sleep for 60s
time.sleep(60)

# Resume the primary thread 
win32process.ResumeThread(hThread)
# Close handles
win32api.CloseHandle(hThread)
win32api.CloseHandle(hProcess)
```
Now i will pretend this is an malicious file that need to analyze. First i will look it in `PE_Bear`

<img width="1895" height="1350" alt="image" src="https://github.com/user-attachments/assets/cfc3121a-ff01-419b-be8b-1238784953e1" />

Look at `String` section, we can see it was created with python

<img width="1900" height="1353" alt="image" src="https://github.com/user-attachments/assets/541f65fe-60e1-48a1-a4f9-539c0c2ada7c" />

Look at `Import` section

<img width="2880" height="1800" alt="image" src="https://github.com/user-attachments/assets/30817b98-6425-4d12-a3ac-d6f707ba5407" />

we can see it import:
* USER32.dll
* COMCTL32.dll
* KERNEL32.dll
* ADVAPI32.dll
* GDI32.dll

I will look in KERNEL32.dll

<img width="2206" height="575" alt="image" src="https://github.com/user-attachments/assets/352ab6c9-c3a6-4540-95e3-59d059303193" />

There is a `CreateProcessW` which mean it create some type of process. Look back in `String` 

<img width="2192" height="930" alt="image" src="https://github.com/user-attachments/assets/abdb0235-2bb0-499a-970a-a7906f10dd34" />

Run program and use `procmon` to watch the process

<img width="2539" height="1505" alt="image" src="https://github.com/user-attachments/assets/47bbe2d2-fc5e-49ff-834c-aa7d4c0f0b0c" />

<img width="2555" height="1543" alt="image" src="https://github.com/user-attachments/assets/8f7b9bef-6907-4e22-ae1f-56b945e656f8" />

open `task manager`

<img width="1030" height="899" alt="image" src="https://github.com/user-attachments/assets/afdc449c-43fd-4821-bb11-de357ec16260" />

## Reference
* [Malware Analysis and Reverse Engineering](https://medium.com/@makt96/malware-analysis-and-reverse-engineering-understanding-windows-internals-such-as-win32-api-to-3c0b1cfd6122)
* [The Most Commonly Exploited Windows APIs](https://johndcyber.com/the-most-commonly-exploited-windows-apis-a-security-professionals-guide-d53acf201034)
