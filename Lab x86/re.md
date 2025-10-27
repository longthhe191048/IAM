# Reverse program in c
## hello world
```
#include<stdio.h>

int main(){
    printf("hello world!");
    return 0;
}
```
<img width="2880" height="1800" alt="image" src="https://github.com/user-attachments/assets/5a8cd558-3fb2-483a-8aab-8c66c043bad8" />


## cal
```
#include<stdio.h>

int a = 5;
int b = 2;

int main(){
    printf("Additional result: %d\n", 5 + 2);
    printf("Subtraction result: %d\n", a - b);
    printf("Multiplication result: %d\n", a * b);
    printf("Division result: %d\n", a / b);
    return 0;
}
```
<img width="2876" height="1795" alt="image" src="https://github.com/user-attachments/assets/1ff55bd6-ec16-4865-b976-a7ec63fd4b56" />


## cmp
```
#include<stdio.h>

void print_greater(){
    printf("The first number is greater than the second number.\n");
}

void print_lesser(){
    printf("The first number is less than the second number.\n");
}

int main(){
    int a = 10;
    int b = 20;
    if(a > b){
        print_greater();
    } else {
        print_lesser();
    }
    return 0;
}


```

<img width="2879" height="1800" alt="image" src="https://github.com/user-attachments/assets/42a4ae46-b9a8-45c7-8968-84ce5189ce25" />

<img width="1555" height="1092" alt="image" src="https://github.com/user-attachments/assets/c0f5d933-20c5-46ca-9c63-2fe30fd0803c" />

**prologue**

```
push    ebp
mov     ebp, esp
push    ebx
```

**Epilogue**

```
leave
retn
```

Explaination why it's `leave` [here](https://board.flatassembler.net/topic.php?t=10409), in short:

```
; leave =
mov  esp, ebp
pop  ebp  
```

## loop
```
#include<stdio.h>  

int main(){  
    int i;
    printf("For: \n");  
    for(i=1; i<=5; i++){  
        printf("%d\n", i);  
    }  
    printf("While: \n");
    i = 1;
    while(i <= 5){  
        printf("%d\n", i);  
        i++;  
    }
    printf("Do-While: \n");
    i = 1;
    do{
        printf("%d\n", i);  
        i++;  
    } while(i <= 5);
    return 0;  
}
```
<img width="1226" height="1037" alt="image" src="https://github.com/user-attachments/assets/d4eda11a-63e4-400e-b314-a875a20b2aed" />

<img width="1883" height="1093" alt="image" src="https://github.com/user-attachments/assets/6c221233-cffa-4f88-8d44-aa04346aaf69" />

<img width="945" height="1050" alt="image" src="https://github.com/user-attachments/assets/41d01e90-c35c-4050-8768-99133f545091" />

<img width="1088" height="932" alt="image" src="https://github.com/user-attachments/assets/823a10c8-7c80-45a1-94af-94184de6225f" />

**Detecting loop in asm**

<img width="1765" height="880" alt="image" src="https://github.com/user-attachments/assets/568f045b-4c4f-4f4d-a769-89b850fc406c" />

init counter
```
mov     [ebp+var_C], 1
```

jump and compare
```
jmp     short loc_80491C7

loc_80491C7:
cmp     [ebp+var_C], 5
jle     short loc_80491AE
```

add to counter
```
add     [ebp+var_C], 1
```

## Func
```
#include<stdio.h>

void printNumbers(){
    int a = 1, b = 5;
    for(int i = a; i <= b; i++){
        printf("%d\n", i);
    }
}

void printHello(){
    printf("Hello, World!\n");
}

void printSum(int a, int b){
    int sum = a + b;
    printf("Sum: %d\n", sum);
}

int main(){
    printNumbers();
    printHello();
    printSum(3, 7);
    return 0;
}
```
Compile with `gcc -m32 -no-pie func.c -o func`

<img width="1099" height="810" alt="image" src="https://github.com/user-attachments/assets/f4c72b53-b89d-4aa4-976d-1ff4d96565a9" />

**Function without epilogue**
```
call    printNumbers
call    printHello
```

**Function with epilogue**
```
call    printSum
add     esp, 10h
```

Compile with `gcc -m32 -no-pie -O2 func.c -o func_o2`

<img width="1129" height="822" alt="image" src="https://github.com/user-attachments/assets/36125065-250f-457b-8d11-7cda3d25e700" />

**Function without prologue**
```
public printHello
printHello proc near
; __unwind {
push    ebx
call    __x86_get_pc_thunk_bx
add     ebx, (offset _GLOBAL_OFFSET_TABLE_ - $)
sub     esp, 14h
```

