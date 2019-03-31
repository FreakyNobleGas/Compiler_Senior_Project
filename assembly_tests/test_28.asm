globl .main
begin:
pushq %rbp
movq %rsp, %rbp
subq $16, %rsp
jmp main
main:
movq $5, %rsp(8)
movq %rsp(8), %rax
movq %rax, %rsp(16)
movq %rsp(16), %rax
movq %rax, %rsp(24)
movq $5, %rsp(32)
movq $5, %rsp(40)
movq %rsp(40), %rax
movq %rax, %rsp(48)
movq %rsp(32), %rax
addq %rax, %rsp(48)
movq %rsp(48), %rax
movq %rax, %rsp(56)
movq %rsp(56), %rax
movq %rax, %rsp(64)
movq %rsp(56), %rax
movq %rax, %rsp(72)
movq %rsp(72), %rax
movq %rax, %rsp(80)
movq %rsp(64), %rax
addq %rax, %rsp(80)
movq %rsp(80), %rax
movq %rax, %rsp(88)
movq %rsp(24), %rax
addq %rax, %rsp(88)
movq %rsp(88), %rax
movq %rax, %rax
jmp end
end:
addq $16, %rsp
popq %rbp
retq


