; build & run (32-bit):
; nasm -f elf32 cal.asm -o cal.o
; ld -m elf_i386 cal.o -o cal
; ./cal

SECTION .data
    num1        dd 5
    num2        dd 2
    result_add  dd 0
    result_sub  dd 0
    result_mul  dd 0
    result_div  dd 0
    nl          db 10

    msg_add     db 'Addition Result: ', 0
    len_add     equ $ - msg_add

    msg_sub     db 'Subtraction Result: ', 0
    len_sub     equ $ - msg_sub

    msg_mul     db 'Multiplication Result: ', 0
    len_mul     equ $ - msg_mul

    msg_div     db 'Division Result: ', 0
    len_div     equ $ - msg_div


SECTION .bss
    ; 10 digits + optional sign + NUL = 12 bytes is safe
    buffer      resb 12

SECTION .text
    global _start

_start:
    ; ----- Addition -----
    mov     eax, [num1]
    mov     ebx, [num2]
    add     eax, ebx
    mov     [result_add], eax

    ; ----- Subtraction -----
    mov     eax, [num1]
    mov     ebx, [num2]
    sub     eax, ebx
    mov     [result_sub], eax

    ; ----- Multiplication -----
    mov     eax, [num1]
    mov     ebx, [num2]
    imul    eax, ebx
    mov     [result_mul], eax

    ; ----- Division (unsigned) -----
    mov     eax, [num1]
    mov     ebx, [num2]
    xor     edx, edx        ; clear high part for DIV
    div     ebx             ; EAX = quotient, EDX = remainder
    mov     [result_div], eax

    ; ----- Print Results -----
    mov     eax, 4          ; syscall: sys_write
    mov     ebx, 1          ; file descriptor: stdout
    mov     ecx, msg_add        ; pointer to message
    mov     edx, len_add        ; message length
    int     0x80            ; call kernel
    mov     eax, [result_add]
    call    convert_and_print

    mov     eax, 4          ; syscall: sys_write
    mov     ebx, 1          ; file descriptor: stdout
    mov     ecx, msg_sub        ; pointer to message
    mov     edx, len_sub        ; message length
    int     0x80            ; call kernel
    mov     eax, [result_sub]
    call    convert_and_print
    
    mov     eax, 4          ; syscall: sys_write
    mov     ebx, 1          ; file descriptor: stdout
    mov     ecx, msg_mul        ; pointer to message
    mov     edx, len_mul        ; message length
    int     0x80            ; call kernel
    mov     eax, [result_mul]
    call    convert_and_print
    
    mov     eax, 4          ; syscall: sys_write
    mov     ebx, 1          ; file descriptor: stdout
    mov     ecx, msg_div        ; pointer to message
    mov     edx, len_div        ; message length
    int     0x80            ; call kernel
    mov     eax, [result_div]
    call    convert_and_print

    ; ----- Exit via Linux 32-bit syscall -----
    mov     eax, 1          ; sys_exit
    xor     ebx, ebx        ; status 0
    int     0x80

;------------------------------------------
; convert_and_print
;  In : EAX = unsigned number to print
;  Clobbers: EBX, ECX, EDX
;------------------------------------------
convert_and_print:
    push    eax                 ; save original (not strictly needed)
    mov     ecx, buffer + 11    ; write from end backward
    mov     byte [ecx], 0       ; NUL terminator
    dec     ecx

    cmp     eax, 0
    jne     .convert_loop
    mov     byte [ecx], '0'
    jmp     .print_string

.convert_loop:
    xor     edx, edx            ; clear high for div
    mov     ebx, 10
    div     ebx                 ; EAX = EAX/10, EDX = remainder
    add     dl, '0'             ; make ASCII digit
    mov     [ecx], dl
    dec     ecx
    test    eax, eax
    jne     .convert_loop

    inc     ecx                 ; now ECX points to first digit

.print_string:
    ; write number
    mov     eax, 4              ; sys_write
    mov     ebx, 1              ; stdout
    mov     edx, buffer + 11
    sub     edx, ecx            ; length = end - start
    int     0x80

    ; write newline
    mov     eax, 4
    mov     ebx, 1
    mov     ecx, nl
    mov     edx, 1
    int     0x80

    pop     eax
    ret
