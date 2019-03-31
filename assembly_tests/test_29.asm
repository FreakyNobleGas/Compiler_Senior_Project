globl .main
begin:
pushq %rbp
movq %rsp, %rbp
subq $16, %rsp
jmp main
main:
movq $30, %rsp(8)
movq %rsp(8), %rax
movq %rax, %rsp(16)
movq %rsp(16), %rax
movq %rax, %rsp(24)
movq $10, %rsp(32)
movq %rsp(32), %rax
movq %rax, %rsp(40)
movq %rsp(40), %rax
movq %rax, %rsp(48)
movq $5, %rsp(56)
movq $5, %rsp(64)
movq %rsp(64), %rax
movq %rax, %rsp(72)
movq %rsp(56), %rax
addq %rax, %rsp(72)
movq %rsp(72), %rax
movq %rax, %rsp(80)
movq %rsp(80), %rax
movq %rax, %rsp(88)
movq %rsp(80), %rax
movq %rax, %rsp(96)
movq %rsp(96), %rax
movq %rax, %rsp(104)
movq %rsp(88), %rax
addq %rax, %rsp(104)
movq %rsp(104), %rax
movq %rax, %rsp(112)
movq %rsp(48), %rax
addq %rax, %rsp(112)
movq %rsp(112), %rax
movq %rax, %rsp(120)
movq %rsp(24), %rax
addq %rax, %rsp(120)
movq %rsp(120), %rax
movq %rax, %rax
jmp end
end:
addq $16, %rsp
popq %rbp
retq


