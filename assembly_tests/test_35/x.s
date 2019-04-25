.globl main
main:
callq begin
movq %rax, %rdi
callq print_int
retq
begin:
pushq %rbp
movq %rsp, %rbp
pushq %r12
pushq %r13
pushq %r14
pushq %r15
addq $16, %rsp
jmp next
next:
movq $30, 8(%rsp)
movq 8(%rsp), %rax
movq %rax, 16(%rsp)
movq 16(%rsp), %rax
movq %rax, 24(%rsp)
movq $10, 32(%rsp)
movq 32(%rsp), %rax
movq %rax, 40(%rsp)
movq 40(%rsp), %rax
movq %rax, 48(%rsp)
movq $5, 56(%rsp)
movq $5, 64(%rsp)
movq 64(%rsp), %rax
movq %rax, 72(%rsp)
movq 56(%rsp), %rax
addq %rax, 72(%rsp)
movq 72(%rsp), %rax
movq %rax, 80(%rsp)
movq 80(%rsp), %rax
movq %rax, 88(%rsp)
movq 80(%rsp), %rax
movq %rax, 96(%rsp)
movq 96(%rsp), %rax
movq %rax, 104(%rsp)
movq 88(%rsp), %rax
addq %rax, 104(%rsp)
movq 104(%rsp), %rax
movq %rax, 112(%rsp)
movq 48(%rsp), %rax
addq %rax, 112(%rsp)
movq 112(%rsp), %rax
movq %rax, 120(%rsp)
movq 24(%rsp), %rax
addq %rax, 120(%rsp)
movq 120(%rsp), %rax
movq %rax, %rax
jmp end
end:
subq $16, %rsp
popq %r15
popq %r14
popq %r13
popq %r12
popq %rbp
retq


