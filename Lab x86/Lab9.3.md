# Lab 9.3  Disassembling C on Windows
## Objective
* Write a C program
* Examine in IDA

## Requirement
* A 32bit C compiler - I juse Mingw
* IDA

# Lab Walkthrough
Create a C code like below. Can use any example
```
// Compile: gcc -m32 a.c -no-pie -o a.out
#include <stdio.h>

int a = 1; //global variable/

int main() {
    int b = 2; //local variable
    printf("longthhe191048: %d\n", a); //global variable
    printf("longthhe191048: %d\n", b); //local variable
    return 0;
}
```
<img width="768" height="411" alt="image" src="https://github.com/user-attachments/assets/fbf95c7f-bd47-4ae7-a580-c553068241b4" />

<img width="516" height="93" alt="image" src="https://github.com/user-attachments/assets/aaa39390-8004-45f1-9091-fcb3fcc0c93c" />

Checking the script

<img width="295" height="91" alt="image" src="https://github.com/user-attachments/assets/b924ef47-a6fa-433e-a988-5c65cdb5646f" />

Open it in IDA, choose the right processor type

<img width="1094" height="703" alt="image" src="https://github.com/user-attachments/assets/7b497ef0-3d3b-4e22-96f6-d5b480f1b809" />

Here we have all the function in the program

<img width="440" height="338" alt="image" src="https://github.com/user-attachments/assets/57b65dd8-a1b7-4e91-a93c-98f7d209111c" />

Let's look at `main`

<img width="670" height="745" alt="image" src="https://github.com/user-attachments/assets/aa5b4432-bac1-4df4-a5e9-5dcf4f1df0c9" />

First, we can see this program use `cdecl`

<img width="600" height="87" alt="image" src="https://github.com/user-attachments/assets/6d83e7c5-8542-4b6d-a493-0bd8479c4130" />

Next we can see `printf` function with their param pass in the stack

<img width="504" height="185" alt="image" src="https://github.com/user-attachments/assets/398c2113-094a-441f-8d68-6a15410184d7" />

Local variable

<img width="440" height="73" alt="image" src="https://github.com/user-attachments/assets/28544483-7bd7-4257-bfd2-83b9237294f1" />

Global Variable

<img width="399" height="91" alt="image" src="https://github.com/user-attachments/assets/5d2921d2-2626-41f7-8e40-e8d547531d25" />

<img width="650" height="66" alt="image" src="https://github.com/user-attachments/assets/569a44c2-93bd-4cd4-b19a-be84f18e30c4" />


