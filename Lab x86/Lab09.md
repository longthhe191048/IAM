# Lab 09: Using Jasmin to run x86 Assembly Code
## Objective
* To practice writing and running basic x86 assembly code, using the Jasmin interpreter

## Requirement
* Java

## Lab Walkthrough 
First install Jasmin [here](http://sourceforge.net/projects/tum-jasmin/files/)

<img width="1915" height="1079" alt="image" src="https://github.com/user-attachments/assets/6575faa2-7c36-4e0e-b1eb-459d5b6af2bd" />

Next, open Jasmin and click on `new file`

<img width="1595" height="948" alt="image" src="https://github.com/user-attachments/assets/fdeabf37-aa8c-4c9e-b3d9-603635a1e1d5" />

Let's do something like code below to see what's changes in register
```
mov eax, 4
mov ebx, 6
```
<img width="346" height="368" alt="image" src="https://github.com/user-attachments/assets/4f97ce94-3c36-4847-815b-9bb3c2d6803b" />

Storing to memory
```
mov [eax], ebx
mov ecx, eax
add ecx, ebx
mov [eax+4], ecx
```

<img width="1592" height="401" alt="image" src="https://github.com/user-attachments/assets/f861bd64-c70c-44d8-906e-ac14be9f7f01" />

Using stack

```
mov eax, 4
mov ebx, 6
push eax
push ebx
```
<img width="514" height="471" alt="image" src="https://github.com/user-attachments/assets/0c102c9a-a638-4ef6-8b85-faf79142ef7e" />
<img width="383" height="195" alt="image" src="https://github.com/user-attachments/assets/f75cf750-d317-47e2-ba20-cb3bbb8b4a32" />

```
 mov eax, 4
 mov ebx, 6
 push eax
 push ebx
 pop ecx
```
<img width="1594" height="941" alt="image" src="https://github.com/user-attachments/assets/127b9241-ca81-4122-87e7-2c0bfaa29528" />

