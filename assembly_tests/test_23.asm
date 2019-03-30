globl .main
main:
movq $30, %rsp(8)
movq %rsp(8), %rsp(16)
movq %rsp(16), %rsp(24)
movq $10, %rsp(32)
movq %rsp(32), %rsp(40)
movq %rsp(40), %rsp(48)
movq $5, %rsp(56)
movq $5, %rsp(64)
movq %rsp(64), %rsp(72)
addq %rsp(56), %rsp(72)
movq %rsp(72), %rsp(80)
movq %rsp(80), %rsp(88)
movq %rsp(80), %rsp(96)
movq %rsp(96), %rsp(104)
addq %rsp(88), %rsp(104)
movq %rsp(104), %rsp(112)
addq %rsp(48), %rsp(112)
movq %rsp(112), %rsp(120)
addq %rsp(24), %rsp(120)
movq %rsp(120), %rax
jmp end:
addq $16, %rsp
popq %rbp
retq

