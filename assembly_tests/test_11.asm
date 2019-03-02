globl .main
main:
pushq $80
pushq $100
popq %R10
popq %R11
subq %R10, %R11
movq %R11, %rax
retq
