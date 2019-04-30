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
subq $256, %rsp
jmp next
next:
movq $9, %rdx
movq $10, 8(%rsp)
movq 8(%rsp), %rax
movq %rax, 16(%rsp)
addq %rdx, 16(%rsp)
movq 16(%rsp), %rax
movq %rax, 24(%rsp)
movq 24(%rsp), %rdx
movq 24(%rsp), %rcx
movq $5, 32(%rsp)
movq 32(%rsp), %rax
movq %rax, 40(%rsp)
addq %rcx, 40(%rsp)
movq 40(%rsp), %rax
movq %rax, 48(%rsp)
movq 48(%rsp), %r9
movq 48(%rsp), %rcx
movq $1, 56(%rsp)
movq 56(%rsp), %rax
movq %rax, 64(%rsp)
addq %rcx, 64(%rsp)
movq 64(%rsp), %rax
movq %rax, 72(%rsp)
movq 72(%rsp), %r8
movq 72(%rsp), %rcx
movq $6, 80(%rsp)
movq 80(%rsp), %rax
movq %rax, 88(%rsp)
addq %rcx, 88(%rsp)
movq 88(%rsp), %rax
movq %rax, 96(%rsp)
movq 96(%rsp), %rdi
movq 96(%rsp), %rcx
movq $5, 104(%rsp)
movq 104(%rsp), %rax
movq %rax, 112(%rsp)
addq %rcx, 112(%rsp)
movq 112(%rsp), %rax
movq %rax, 120(%rsp)
movq 120(%rsp), %rsi
movq 120(%rsp), %rax
movq %rax, 128(%rsp)
movq $1, 136(%rsp)
movq 136(%rsp), %rax
movq %rax, 144(%rsp)
movq 128(%rsp), %rax
addq %rax, 144(%rsp)
movq 144(%rsp), %rcx
movq %rcx, 152(%rsp)
movq %rcx, 160(%rsp)
movq $3, 168(%rsp)
movq 168(%rsp), %rax
movq %rax, 176(%rsp)
movq 160(%rsp), %rax
addq %rax, 176(%rsp)
movq 176(%rsp), %rax
movq %rax, 184(%rsp)
movq 184(%rsp), %rax
movq %rax, 192(%rsp)
movq %rcx, 200(%rsp)
movq 200(%rsp), %rax
movq %rax, 208(%rsp)
movq 192(%rsp), %rax
addq %rax, 208(%rsp)
movq 208(%rsp), %rax
movq %rax, 216(%rsp)
movq 152(%rsp), %rax
addq %rax, 216(%rsp)
movq 216(%rsp), %rax
movq %rax, 224(%rsp)
addq %rsi, 224(%rsp)
movq 224(%rsp), %rax
movq %rax, 232(%rsp)
addq %rdi, 232(%rsp)
movq 232(%rsp), %rax
movq %rax, 240(%rsp)
addq %r8, 240(%rsp)
movq 240(%rsp), %rax
movq %rax, 248(%rsp)
addq %r9, 248(%rsp)
movq 248(%rsp), %rax
movq %rax, 256(%rsp)
addq %rdx, 256(%rsp)
movq 256(%rsp), %rax
jmp end
end:
addq $256, %rsp
popq %r15
popq %r14
popq %r13
popq %r12
popq %rbp
retq


