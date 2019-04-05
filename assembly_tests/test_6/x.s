.globl main
main:
pushq (Hello World)
pushq $80
popq %rax
popq %rax
retq
