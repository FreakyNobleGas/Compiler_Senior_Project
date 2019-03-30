globl .main
begin:
pushq %rbp
movq %rsp, %rbp
subq $16, %rsp
jmp main
main:
movq $5, %rsp(8)
movq $5, %rsp(16)
movq $5, %rsp(24)
movq %rsp(24), %rsp(32)
addq %rsp(16), %rsp(32)
movq %rsp(32), %rsp(40)
addq %rsp(8), %rsp(40)
movq %rsp(40), %rax
jmp end
end:
addq $16, %rsp
popq %rbp
retq


