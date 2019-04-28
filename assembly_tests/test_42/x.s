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
subq $176, %rsp
jmp next
next:
movq $5, %rdx
movq $3, 8(%rsp)
movq 8(%rsp), %rax
movq %rax, 16(%rsp)
addq %rdx, 16(%rsp)
movq 16(%rsp), %rax
movq %rax, 24(%rsp)
movq 24(%rsp), %rdx
movq 24(%rsp), %rcx
movq $2, 32(%rsp)
movq 32(%rsp), %rax
movq %rax, 40(%rsp)
addq %rcx, 40(%rsp)
movq 40(%rsp), %rax
movq %rax, 48(%rsp)
movq 48(%rsp), %r8
movq 48(%rsp), %rcx
movq $0, 56(%rsp)
movq 56(%rsp), %rax
movq %rax, 64(%rsp)
addq %rcx, 64(%rsp)
movq 64(%rsp), %rax
movq %rax, 72(%rsp)
movq 72(%rsp), %rdi
movq 72(%rsp), %rcx
movq $7, 80(%rsp)
movq 80(%rsp), %rax
movq %rax, 88(%rsp)
addq %rcx, 88(%rsp)
movq 88(%rsp), %rsi
movq %rsi, %rsi
movq %rsi, 96(%rsp)
movq $2, 104(%rsp)
movq 104(%rsp), %rax
movq %rax, 112(%rsp)
movq 96(%rsp), %rax
addq %rax, 112(%rsp)
movq 112(%rsp), %rax
movq %rax, 120(%rsp)
movq 120(%rsp), %rcx
movq %rsi, 128(%rsp)
movq 128(%rsp), %rax
movq %rax, 136(%rsp)
addq %rcx, 136(%rsp)
movq 136(%rsp), %rax
movq %rax, 144(%rsp)
addq %rsi, 144(%rsp)
movq 144(%rsp), %rax
movq %rax, 152(%rsp)
addq %rdi, 152(%rsp)
movq 152(%rsp), %rax
movq %rax, 160(%rsp)
addq %r8, 160(%rsp)
movq 160(%rsp), %rax
movq %rax, 168(%rsp)
addq %rdx, 168(%rsp)
movq 168(%rsp), %rax
jmp end
end:
addq $176, %rsp
popq %r15
popq %r14
popq %r13
popq %r12
popq %rbp
retq


