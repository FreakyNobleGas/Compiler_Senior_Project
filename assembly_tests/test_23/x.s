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
movq $30, 8(%rsp)
movq 8(%rsp), 16(%rsp)
movq 16(%rsp), 24(%rsp)
movq $10, 32(%rsp)
movq 32(%rsp), 40(%rsp)
movq 40(%rsp), 48(%rsp)
movq $5, 56(%rsp)
movq $5, 64(%rsp)
movq 64(%rsp), 72(%rsp)
addq 56(%rsp), 72(%rsp)
movq 72(%rsp), 80(%rsp)
movq 80(%rsp), 88(%rsp)
movq 80(%rsp), 96(%rsp)
movq 96(%rsp), 104(%rsp)
addq 88(%rsp), 104(%rsp)
movq 104(%rsp), 112(%rsp)
addq 48(%rsp), 112(%rsp)
movq 112(%rsp), 120(%rsp)
addq 24(%rsp), 120(%rsp)
movq 120(%rsp), %rax
jmp end
end:
addq $16, %rsp
popq %r15
popq %r14
popq %r13
popq %r12
popq %rbp
retq


