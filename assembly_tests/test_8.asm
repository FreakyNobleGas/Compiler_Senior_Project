globl .main
main:
pushq %rbp
movq %rsp, %rbp
subq $16, %rsp
jmp start
start:
movq $10, %rbp(-8)
negq %rbp(-8)
movq %rbp(-8), %rax
addq $52, %rax
jmp conclusion
conclusion:
addq $16, %rsp
popq %rbp
retq


