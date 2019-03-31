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
movq %rsp(24), %rax
movq %rax, %rsp(32)
movq %rsp(16), %rax
addq %rax, %rsp(32)
movq %rsp(32), %rax
movq %rax, %rsp(40)
movq %rsp(8), %rax
addq %rax, %rsp(40)
movq %rsp(40), %rax
movq %rax, %rax
jmp end
end:
addq $16, %rsp
popq %rbp
retq


