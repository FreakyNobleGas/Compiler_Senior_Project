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
subq $208, %rsp
jmp next
next:
movq $4, %rdx
movq $10, 8(%rsp)
movq 8(%rsp), %rax
movq %rax, 16(%rsp)
addq %rdx, 16(%rsp)
movq 16(%rsp), %rax
movq %rax, 24(%rsp)
movq 24(%rsp), %rdx
movq 24(%rsp), %rcx
movq $0, 32(%rsp)
movq 32(%rsp), %rax
movq %rax, 40(%rsp)
addq %rcx, 40(%rsp)
movq 40(%rsp), %rax
movq %rax, 48(%rsp)
movq 48(%rsp), %r8
movq 48(%rsp), %rcx
movq $7, 56(%rsp)
movq 56(%rsp), %rax
movq %rax, 64(%rsp)
addq %rcx, 64(%rsp)
movq 64(%rsp), %rax
movq %rax, 72(%rsp)
movq 72(%rsp), %rdi
movq 72(%rsp), %rcx
movq $1, 80(%rsp)
movq 80(%rsp), %rax
movq %rax, 88(%rsp)
addq %rcx, 88(%rsp)
movq 88(%rsp), %rax
movq %rax, 96(%rsp)
movq 96(%rsp), %rsi
movq 96(%rsp), %rcx
movq $0, 104(%rsp)
movq 104(%rsp), %rax
movq %rax, 112(%rsp)
addq %rcx, 112(%rsp)
movq 112(%rsp), %rcx
movq %rcx, %rcx
movq %rcx, 120(%rsp)
movq $0, 128(%rsp)
movq 128(%rsp), %rax
movq %rax, 136(%rsp)
movq 120(%rsp), %rax
addq %rax, 136(%rsp)
movq 136(%rsp), %rax
movq %rax, 144(%rsp)
movq 144(%rsp), %rax
movq %rax, 152(%rsp)
movq %rcx, 160(%rsp)
movq 160(%rsp), %rax
movq %rax, 168(%rsp)
movq 152(%rsp), %rax
addq %rax, 168(%rsp)
movq 168(%rsp), %rax
movq %rax, 176(%rsp)
addq %rcx, 176(%rsp)
movq 176(%rsp), %rax
movq %rax, 184(%rsp)
addq %rsi, 184(%rsp)
movq 184(%rsp), %rax
movq %rax, 192(%rsp)
addq %rdi, 192(%rsp)
movq 192(%rsp), %rax
movq %rax, 200(%rsp)
addq %r8, 200(%rsp)
movq 200(%rsp), %rax
movq %rax, 208(%rsp)
addq %rdx, 208(%rsp)
movq 208(%rsp), %rax
jmp end
end:
addq $208, %rsp
popq %r15
popq %r14
popq %r13
popq %r12
popq %rbp
retq

