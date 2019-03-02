globl .main
main:
movq $14, %r10
jmp end:
movq %r10, %rax
retq

