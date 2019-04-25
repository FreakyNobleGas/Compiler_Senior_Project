.globl main
begin:
pushq %rbp
movq %rsp, %rbp
pushq %r12
pushq %r13
pushq %r14
pushq %r15
subq $16, %rsp
jmp next
next:
movq $5, 8(%rsp)
movq 8(%rsp), %rax
movq %rax, 16(%rsp)
movq 16(%rsp), %rax
movq %rax, 24(%rsp)
movq $10, 32(%rsp)
movq 32(%rsp), %rax
movq %rax, 40(%rsp)
movq 40(%rsp), %rax
movq %rax, 48(%rsp)
movq 48(%rsp), %rax
movq %rax, 56(%rsp)
movq 24(%rsp), %rax
addq %rax, 56(%rsp)
movq 56(%rsp), %rax
movq %rax, %rax
jmp end
end:
addq $16, %rsp
popq %r15
popq %r14
popq %r13
popq %r12
popq %rbp
retq


