# Lab 12
## Objective
* Walkthrough Static analysis
* Deep dive to Dynamic analysis

## Requirement
* Win 2008 server
* Flarevm

## Lab Walkthrough
### Lab 1
First, we will walk through static analysis with `Pe-Bear` with `Lab11-01.exe`

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/d1aea8ef-1c1f-4ea3-896f-49bc42d1c853" />

Checking `import` section

<img width="1260" height="317" alt="image" src="https://github.com/user-attachments/assets/2f83e573-fb5f-480e-aae3-0528fbf2593c" />

We could see it import `KERNEL32.dll` and `ADVAPI32.dll`, let's look through it content

<img width="1304" height="316" alt="image" src="https://github.com/user-attachments/assets/724d5bfa-088b-41cc-b69f-a15d9ccda288" />

<img width="1290" height="287" alt="image" src="https://github.com/user-attachments/assets/6df356d0-e581-4163-982d-9b2d81a42cf0" />

As we can see, it seem to create and modify registry, also load resource to memory. Let's move to win2008 server to do a dynamic test with `procmon`

<img width="1918" height="1078" alt="image" src="https://github.com/user-attachments/assets/66200ad2-02db-4402-bbf8-c97e0b3c984b" />

As i go in detailed, we could see Registry has been set to `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\GinaDLL`, also create an `.dll` file

<img width="703" height="619" alt="image" src="https://github.com/user-attachments/assets/6944592e-3c0d-4865-9a61-2c071c8281c5" />

<img width="738" height="631" alt="image" src="https://github.com/user-attachments/assets/4c06d10e-010e-4333-be0f-c8b3d7ac4cb4" />

Section below just an lab tutorial but we can already check it from `pe-bear` but i will do it just in case.

`resource hacker`

<img width="1590" height="931" alt="image" src="https://github.com/user-attachments/assets/dafe868a-4bcf-4558-96b4-51a3d0cc10f0" />

<img width="1598" height="936" alt="image" src="https://github.com/user-attachments/assets/c8663195-b0b0-43a4-8cca-868e4777bbd7" />

<img width="1582" height="891" alt="image" src="https://github.com/user-attachments/assets/164653d5-242b-4d1e-9f42-faf6005e514c" />

`hashcalc`

<img width="585" height="571" alt="image" src="https://github.com/user-attachments/assets/22e82df0-fd87-4787-b9bc-a1bedabe3b8d" />

<img width="1292" height="395" alt="image" src="https://github.com/user-attachments/assets/11d439a1-b14e-4600-8301-8ef78aa3e1f1" />

### Lab 2
As always, i will examine `Lab12-01.exe` with `pe-bear`

<img width="1580" height="891" alt="image" src="https://github.com/user-attachments/assets/19388143-5c19-407c-9af8-b9050763ed57" />

Checking `import` section

<img width="1248" height="324" alt="image" src="https://github.com/user-attachments/assets/0ad0b95b-9e38-434c-b2ff-13ae07b0633c" />

we can see it import `KERNEL32.dll`, look at it

<img width="1212" height="291" alt="image" src="https://github.com/user-attachments/assets/9c301868-4a47-42da-b576-3e553fe8f963" />

we can see some special function such as `CreateRemoteThread`, `WriteProcessMemory` and `VirtualAllocEx` which use to allocate memory in another program, write to it memory and start a new thread in another process. Let's move to `string` section

<img width="1256" height="597" alt="image" src="https://github.com/user-attachments/assets/2149a959-b698-4321-881d-c2ff50da14c2" />

We could see 3 strings that are suspicious `Lab12-01.dll`, `psapi.dll` and `explorer.exe`. From here, i could give my assumption that it will try to allocate memory from `explorer.exe`. I will decompile it with `IDA`

<img width="1589" height="895" alt="image" src="https://github.com/user-attachments/assets/616fd6aa-75ca-48ba-b456-daac1e27cf11" />

After decompile it, we can see it load 3 function into `psapi.dll` which is to obfuscate us. To summarize it, 
```
clear buffers → load psapi.dll → get pointers to PSAPI functions → prepare to enumerate processes/modules and read module (image) names.
```
I will track `GetModuleBaseNameA` so i can see which process is watching and confirm my assumption

<img width="461" height="400" alt="image" src="https://github.com/user-attachments/assets/bf5f3337-2057-4069-83b6-db7678af2428" />

It track for `explorer.exe`
