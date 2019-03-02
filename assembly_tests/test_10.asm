globl .main
main:
movq $15, %R10
movq %R10, %R11
addq %R10, %R11
movq %R11, %rax
retq
