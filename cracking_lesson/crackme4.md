# Crack me 4 Write Up
## Objective
* Crack it to extend beyond 30 days
* In the About screen – also extend it to beyond 30 days
<img width="1456" height="1328" alt="image" src="https://github.com/user-attachments/assets/211e8b63-175b-41d9-b3fa-7ec37b005591" />

## Write Up
Fristly, i installed the challenge file, make a backup and run it

<img width="2537" height="1509" alt="image" src="https://github.com/user-attachments/assets/b8a43651-7f02-40e6-b9e8-a1e7db59992e" />

Disassemble with `IDA` and look at `WinMain`

<img width="2541" height="1510" alt="image" src="https://github.com/user-attachments/assets/2a1f3f1c-5e61-4128-917f-a44a4617b891" />

we can see 2 register holding 2 variable: `ecx = 0x1e` and `eax = lt.systemtime` or our time in the machine, after that it calculate the remaining days by `sub` instruction. So i decided to modified it like below
```
add     ecx, ecx
```
This should result in `30 + 30 = 60 days`

<img width="2000" height="1042" alt="image" src="https://github.com/user-attachments/assets/a09f9153-0d19-487c-acdf-ee481e463e4c" />

Patch the program and run

<img width="929" height="481" alt="image" src="https://github.com/user-attachments/assets/8adc2037-facb-482b-98c6-71cb981e8c40" />
