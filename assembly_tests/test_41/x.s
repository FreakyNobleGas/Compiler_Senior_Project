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
subq $128, %rsp
jmp next
next:
movq $4, %rdx
movq $0, 8(%rsp)
movq 8(%rsp), %rax
movq %rax, 16(%rsp)
addq %rdx, 16(%rsp)
movq 16(%rsp), %rax
movq %rax, 24(%rsp)
movq 24(%rsp), %rdx
movq 24(%rsp), %rcx
movq $10, 32(%rsp)
movq 32(%rsp), %rax
movq %rax, 40(%rsp)
addq %rcx, 40(%rsp)
movq 40(%rsp), %rax
movq %rax, 48(%rsp)
movq 48(%rsp), %rdi
movq 48(%rsp), %rcx
movq $5, 56(%rsp)
movq 56(%rsp), %rax
movq %rax, 64(%rsp)
addq %rcx, 64(%rsp)
movq 64(%rsp), %rsi
movq %rsi, %rsi
movq %rsi, %rcx
movq $0, 72(%rsp)
movq 72(%rsp), %rax
movq %rax, 80(%rsp)
addq %rcx, 80(%rsp)
movq 80(%rsp), %rax
movq %rax, 88(%rsp)
movq 88(%rsp), %rcx
movq %rsi, 96(%rsp)
movq 96(%rsp), %rax
movq %rax, 104(%rsp)
addq %rcx, 104(%rsp)
movq 104(%rsp), %rax
movq %rax, 112(%rsp)
addq %rsi, 112(%rsp)
movq 112(%rsp), %rax
movq %rax, 120(%rsp)
addq %rdi, 120(%rsp)
movq 120(%rsp), %rax
movq %rax, 128(%rsp)
addq %rdx, 128(%rsp)
movq 128(%rsp), %rax
jmp end
end:
addq $128, %rsp
popq %r15
popq %r14
popq %r13
popq %r12
popq %rbp
retq


