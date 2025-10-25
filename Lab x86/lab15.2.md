# Reverse Engineering with IDA Pro Freeware 
## Objective
*  You will use IDA Pro Free to disassemble and analyze Windows executable files.

## Requirement
* Windows machine with IDA
* File from the lab

## Lab walkthrogh
### 12.1
Open file in IDA, choose the correct decompiler\

<img width="1200" height="785" alt="image" src="https://github.com/user-attachments/assets/d585f590-8abe-4852-b371-3b4a430c1554" />

Look at the function name, i found `_main`

<img width="2880" height="1800" alt="image" src="https://github.com/user-attachments/assets/a32dae66-675f-4a58-8f5b-78b2901e451d" />

Navigate to function `_main_0` 

<img width="2879" height="1800" alt="image" src="https://github.com/user-attachments/assets/252d8349-35fb-4cd5-9b80-bd36987322c1" />

we could see some strings here. We can guess the password as look at below it some function said we found the password. Let's test it

<img width="1103" height="539" alt="image" src="https://github.com/user-attachments/assets/c441fa1d-690a-4d00-94da-886e52e91b59" />

## 12.2
Reproduce the same process as in [12.1](#12.1)

<img width="2256" height="1032" alt="image" src="https://github.com/user-attachments/assets/3cc9701a-221f-44e9-89bf-f0cc8e16f3d1" />

Test the answer

<img width="1446" height="485" alt="image" src="https://github.com/user-attachments/assets/4d751eee-d383-43ca-aefa-900a4d3c9b70" />

## 12.3
Reproduce the same process as in [12.1](#12.1)

<img width="1377" height="969" alt="image" src="https://github.com/user-attachments/assets/58ba15b6-dc55-491c-9416-2b83f4ebb498" />

We see it check if there is any argument

<img width="1215" height="890" alt="image" src="https://github.com/user-attachments/assets/3bb3a66a-f53f-4c7e-a872-537a665d0b48" />

Look down, we can see in this lab need 2 argument

<img width="2193" height="1173" alt="image" src="https://github.com/user-attachments/assets/7852c161-171a-42f1-92cd-55080b0eb1ad" />

Test both argument

<img width="1344" height="705" alt="image" src="https://github.com/user-attachments/assets/c7c86f1d-68d2-482e-ade3-fa007f158b5a" />

## 12.4
Reproduce the same process as in [12.1](#12.1)

<img width="2879" height="1787" alt="image" src="https://github.com/user-attachments/assets/d0c52219-83a9-4205-8ee3-c96a81ab62df" />

We could see we need to run command with name of the application `game3.exe`

<img width="2880" height="1767" alt="image" src="https://github.com/user-attachments/assets/5e59e8cb-cd74-4d30-aca3-5a090a2c846d" />

Testing the answer

<img width="1368" height="884" alt="image" src="https://github.com/user-attachments/assets/4596b33e-ba21-40f8-936b-28c4f1f496d5" />

