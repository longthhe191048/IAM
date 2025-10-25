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
