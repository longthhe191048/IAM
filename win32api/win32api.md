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

## Reference
* [Malware Analysis and Reverse Engineering](https://medium.com/@makt96/malware-analysis-and-reverse-engineering-understanding-windows-internals-such-as-win32-api-to-3c0b1cfd6122)
* [The Most Commonly Exploited Windows APIs](https://johndcyber.com/the-most-commonly-exploited-windows-apis-a-security-professionals-guide-d53acf201034)
