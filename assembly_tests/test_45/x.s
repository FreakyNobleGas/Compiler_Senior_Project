.globl main
begin:
pushq %rbp
movq %rsp, %rbp
pushq %r12
pushq %r13
pushq %r14
pushq %r15
subq $104, %rsp
jmp next
next:
movq $7, %rax
movq $7, 8(%rsp)
movq 8(%rsp), 16(%rsp)
addq %rax, 16(%rsp)
movq 16(%rsp), 24(%rsp)
movq 24(%rsp), %rax
movq 24(%rsp), %rdx
movq $7, 32(%rsp)
movq 32(%rsp), 40(%rsp)
addq %rdx, 40(%rsp)
movq 40(%rsp), %rcx
movq %rcx, %rcx
movq %rcx, %rdx
movq $8, 48(%rsp)
movq 48(%rsp), 56(%rsp)
addq %rdx, 56(%rsp)
movq 56(%rsp), 64(%rsp)
movq 64(%rsp), %rdx
movq %rcx, 72(%rsp)
movq 72(%rsp), 80(%rsp)
addq %rdx, 80(%rsp)
movq 80(%rsp), 88(%rsp)
addq %rcx, 88(%rsp)
movq 88(%rsp), 96(%rsp)
addq %rax, 96(%rsp)
movq 96(%rsp), %rax
jmp end
end:
addq $104, %rsp
popq %r15
popq %r14
popq %r13
popq %r12
popq %rbp
retq


