.globl main
begin:
pushq %rbp
movq %rsp, %rbp
addq $16, %rsp
jmp next
next:
movq $5, 8(%rsp)
movq 8(%rsp), %rax
movq %rax, 16(%rsp)
movq 16(%rsp), %rax
movq %rax, 24(%rsp)
movq $8, 32(%rsp)
movq 32(%rsp), %rax
movq %rax, 40(%rsp)
movq 24(%rsp), %rax
addq %rax, 40(%rsp)
movq 40(%rsp), %rax
movq %rax, %rax
jmp end
end:
subq $16, %rsp
popq %rbp
retq


