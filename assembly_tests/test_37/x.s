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
movq $5, %rax
movq $8, 8(%rsp)
movq 8(%rsp), 16(%rsp)
addq %rax, 16(%rsp)
movq 16(%rsp), 24(%rsp)
movq 24(%rsp), %rax
movq 24(%rsp), %rdx
movq $10, 32(%rsp)
movq 32(%rsp), 40(%rsp)
addq %rdx, 40(%rsp)
movq 40(%rsp), 48(%rsp)
movq 48(%rsp), %rsi
movq 48(%rsp), %rdx
movq $3, 56(%rsp)
movq 56(%rsp), 64(%rsp)
addq %rdx, 64(%rsp)
movq 64(%rsp), %rcx
movq %rcx, %rcx
movq %rcx, %rdx
movq $1, 72(%rsp)
movq 72(%rsp), 80(%rsp)
addq %rdx, 80(%rsp)
movq 80(%rsp), 88(%rsp)
movq 88(%rsp), %rdx
movq %rcx, 96(%rsp)
movq 96(%rsp), 104(%rsp)
addq %rdx, 104(%rsp)
movq 104(%rsp), 112(%rsp)
addq %rcx, 112(%rsp)
movq 112(%rsp), 120(%rsp)
addq %rsi, 120(%rsp)
movq 120(%rsp), 128(%rsp)
addq %rax, 128(%rsp)
movq 128(%rsp), %rax
jmp end
end:
addq $16, %rsp
popq %r15
popq %r14
popq %r13
popq %r12
popq %rbp
retq


