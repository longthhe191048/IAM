SECTION .data
    msg_greater db "First number is greater than second.", 0
    len_msg_greater equ $ - msg_greater
    msg_less db "First number is less than second.", 0
    len_msg_less equ $ - msg_less

    a db 10
    b db 20

SECTION .text
    global _start

_start:
    ; Load values into registers
    mov al, [a]
    mov bl, [b]

    ; Compare the two values
    cmp al, bl

    ; Conditional jump based on comparison
    jg  first_greater
    jl  first_less

    ; Exit if they are equal (not handled in this example)
    jmp exit

first_greater:
    ; Print message for first greater
    mov eax, 4
    mov ebx, 1
    mov edx, len_msg_greater
    mov ecx, msg_greater
    int 0x80
    jmp exit

first_less: 
    ; Print message for first less
    mov eax, 4
    mov ebx, 1
    mov edx, len_msg_less
    mov ecx, msg_less
    int 0x80
    jmp exit

exit:
    ; Exit program
    mov eax, 1
    xor ebx, ebx
    int 0x80