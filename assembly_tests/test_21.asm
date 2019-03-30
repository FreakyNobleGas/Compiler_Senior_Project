globl .main
main:
movq $5, %rsp(8)
movq %rsp(8), %rsp(16)
movq %rsp(16), %rsp(24)
movq $10, %rsp(32)
movq %rsp(32), %rsp(40)
movq %rsp(40), %rsp(48)
movq %rsp(48), %rsp(56)
addq %rsp(24), %rsp(56)
movq %rsp(56), %rax
jmp end:
addq $16, %rsp
popq %rbp
retq

