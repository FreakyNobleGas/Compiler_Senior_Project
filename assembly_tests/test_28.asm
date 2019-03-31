globl .main
begin:
pushq %rbp
movq %rsp, %rbp
subq $16, %rsp
jmp main
main:
movq $5, %rsp(8)
movq %rsp(8), %rsp(16)
movq %rsp(16), %rsp(24)
movq $5, %rsp(32)
movq $5, %rsp(40)
movq %rsp(40), %rsp(48)
addq %rsp(32), %rsp(48)
movq %rsp(48), %rsp(56)
movq %rsp(56), %rsp(64)
movq %rsp(56), %rsp(72)
movq %rsp(72), %rsp(80)
addq %rsp(64), %rsp(80)
movq %rsp(80), %rsp(88)
addq %rsp(24), %rsp(88)
movq %rsp(88), %rax
jmp end
end:
addq $16, %rsp
popq %rbp
retq


