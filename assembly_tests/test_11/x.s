.globl main
main:
pushq $80
pushq $100
popq %r10
popq %r11
subq %r10, %r11
movq %r11, %rax
retq
