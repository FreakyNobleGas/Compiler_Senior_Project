.globl main
main:
movq $50, %r10
negq %r10
movq %r10, %rax
retq
