.globl main
begin:
pushq %rbp
movq %rsp, %rbp
pushq %r12
pushq %r13
pushq %r14
pushq %r15
subq $64, %rsp
jmp next
next:
movq $3, %rdx
movq $9, 8(%rsp)
movq 8(%rsp), %rax
movq %rax, 16(%rsp)
addq %rdx, 16(%rsp)
movq 16(%rsp), %rdx
movq %rdx, %rdx
movq %rdx, %rcx
movq $1, 24(%rsp)
movq 24(%rsp), %rax
movq %rax, 32(%rsp)
addq %rcx, 32(%rsp)
movq 32(%rsp), %rax
movq %rax, 40(%rsp)
movq 40(%rsp), %rcx
movq %rdx, 48(%rsp)
movq 48(%rsp), %rax
movq %rax, 56(%rsp)
addq %rcx, 56(%rsp)
movq 56(%rsp), %rax
movq %rax, 64(%rsp)
addq %rdx, 64(%rsp)
movq 64(%rsp), %rax
jmp end
end:
addq $64, %rsp
popq %r15
popq %r14
popq %r13
popq %r12
popq %rbp
retq


