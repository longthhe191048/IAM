; build & run (32-bit):
; nasm -f elf32 helloworld.asm -o helloworld.o
; gcc -m32 helloworld.o -o helloworld -nostartfiles -no-pie 
; or run with:
; nasm -f elf32 helloworld.asm -o helloworld.o
; ld -m elf_i386 helloworld.o -o helloworld
SECTION .data
    msg     db      'Hello World!', 0xA, 0x0  ; our string with newline
    len equ $ - msg                           ; length of our string

SECTION .text
    global _start
_start:
    ; write our string to stdout
    mov     eax, 4          ; syscall: sys_write
    mov     ebx, 1          ; file descriptor: stdout
    mov     ecx, msg        ; pointer to message
    mov     edx, len        ; message length
    int     0x80            ; call kernel
    ; exit
    mov     eax, 1          ; syscall: sys_exit
    xor     ebx, ebx        ; exit code 0
    int     0x80            ; call kernel