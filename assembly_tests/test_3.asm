globl .main
main:
movq $50, %R10
negq %R10
movq %R10, %rax
retq
