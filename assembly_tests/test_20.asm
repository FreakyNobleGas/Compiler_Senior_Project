globl .main
main:
movq $5, %rsp(8)
movq %rsp(8), %rsp(16)
movq %rsp(16), %rsp(24)
movq $8, %rsp(32)
movq %rsp(32), %rsp(40)
addq %rsp(24), %rsp(40)
movq %rsp(40), %rax
jmp end:
addq $16, %rsp
popq %rbp
retq

