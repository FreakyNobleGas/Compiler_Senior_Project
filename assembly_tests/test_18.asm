globl .main
begin:
pushq %rbp
movq %rsp, %rbp
subq $16, %rsp
jmp main
main:
movq $5, %rsp(8)
movq $5, %rsp(16)
movq %rsp(16), %rsp(24)
addq %rsp(8), %rsp(24)
movq %rsp(24), %rax
jmp end
end:
addq $16, %rsp
popq %rbp
retq


