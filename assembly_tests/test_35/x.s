.globl main
begin:
pushq %rbp
movq %rsp, %rbp
pushq %r12
pushq %r13
pushq %r14
pushq %r15
subq $96, %rsp
jmp next
next:
movq $30, 8(%rsp)
movq 8(%rsp), 16(%rsp)
movq 16(%rsp), %rax
movq $10, 24(%rsp)
movq 24(%rsp), 32(%rsp)
movq 32(%rsp), %rdx
movq $5, %rcx
movq $5, 40(%rsp)
movq 40(%rsp), 48(%rsp)
addq %rcx, 48(%rsp)
movq 48(%rsp), 56(%rsp)
movq 56(%rsp), %rcx
movq 56(%rsp), 64(%rsp)
movq 64(%rsp), 72(%rsp)
addq %rcx, 72(%rsp)
movq 72(%rsp), 80(%rsp)
addq %rdx, 80(%rsp)
movq 80(%rsp), 88(%rsp)
addq %rax, 88(%rsp)
movq 88(%rsp), %rax
jmp end
end:
addq $96, %rsp
popq %r15
popq %r14
popq %r13
popq %r12
popq %rbp
retq


