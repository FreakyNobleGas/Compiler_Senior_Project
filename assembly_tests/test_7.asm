globl .main
main:
movq $14, %R10
jmp end:
movq %R10, %rax
retq

