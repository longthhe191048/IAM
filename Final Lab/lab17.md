# Lab 17:  Using Kernel Debugging Commands with WinDbg
## Objective
* Practice using simple WinDbg commands

## Requirement
* WinDBG
* LiveKD

## knowledge
LiveKD allows you to run the Kd and Windbg Microsoft kernel debuggers, which are part of the Debugging Tools for Windows package, locally on a live system

## Lab Walkthrough
Start `livekd` with this command
```
livekd -w
```

<img width="2264" height="1422" alt="image" src="https://github.com/user-attachments/assets/da619954-f534-49fd-a0b2-3a9992bd0e35" />

listing all loaded module with this command and find if there is `NT` module
```
lm
```

<img width="2544" height="1417" alt="image" src="https://github.com/user-attachments/assets/63087132-7e44-4634-8462-943ea76acce2" />

I will check the module in the memory with this command

```
dd nt
```
**Explaination:**
* `d` = Display memory
* `d` = DWORD -> 4 bytes
* `nt` = Module name

<img width="880" height="359" alt="image" src="https://github.com/user-attachments/assets/efda7451-4104-4b1a-8c67-5cc7dd7b766d" />

Showing with ASCII
```
da nt
```

<img width="2548" height="193" alt="image" src="https://github.com/user-attachments/assets/b286c769-4fa3-4587-abc7-a87af33b539d" />


Checking DOS Stub by going to `0x4C`
```
da nt+4c
```

<img width="854" height="207" alt="image" src="https://github.com/user-attachments/assets/2cb3f6ec-1513-4b8d-afb4-7c1063fb141d" />

Now i will go and search for function in this module. The command to list all function is
```
x nt!*
```

<img width="2554" height="1285" alt="image" src="https://github.com/user-attachments/assets/62cffd94-8d80-4023-82e7-61cd2b578438" />

To go deeper, i want to check if there is any `CreateProcess` function calling from winapi32
```
x nt!*CreateProcess*
```

<img width="1677" height="807" alt="image" src="https://github.com/user-attachments/assets/3e88b4a9-388b-4e03-8a6e-c65054c645cf" />

Disassemble the function

```
u nt!NtCreateProcess
```

<img width="981" height="335" alt="image" src="https://github.com/user-attachments/assets/4fa3d840-ab95-4510-8cb6-4757223010a7" />

<img width="1216" height="666" alt="image" src="https://github.com/user-attachments/assets/7de61f6d-d159-410e-b5bf-c8837cdf8998" />

