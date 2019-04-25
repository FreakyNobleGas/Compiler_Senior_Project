.globl main
begin:
pushq %rbp
movq %rsp, %rbp
pushq %r12
pushq %r13
pushq %r14
pushq %r15
addq $72, %rsp
jmp next
next:
movq $6, %rax
movq $4, 8(%rsp)
movq 8(%rsp), 16(%rsp)
addq %rax, 16(%rsp)
movq 16(%rsp), %rax
movq %rax, %rax
movq %rax, %rdx
movq $0, 24(%rsp)
movq 24(%rsp), 32(%rsp)
addq %rdx, 32(%rsp)
movq 32(%rsp), 40(%rsp)
movq 40(%rsp), %rdx
movq %rax, 48(%rsp)
movq 48(%rsp), 56(%rsp)
addq %rdx, 56(%rsp)
movq 56(%rsp), 64(%rsp)
addq %rax, 64(%rsp)
movq 64(%rsp), %rax
jmp end
end:
subq $72, %rsp
popq %r15
popq %r14
popq %r13
popq %r12
popq %rbp
retq


