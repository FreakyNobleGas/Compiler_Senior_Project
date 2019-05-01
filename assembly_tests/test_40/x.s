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
subq $304, %rsp
jmp next
next:
movq $0, %rdx
movq $10, 8(%rsp)
movq 8(%rsp), %rax
movq %rax, 16(%rsp)
addq %rdx, 16(%rsp)
movq 16(%rsp), %rax
movq %rax, 24(%rsp)
movq 24(%rsp), %rdx
movq 24(%rsp), %rcx
movq $6, 32(%rsp)
movq 32(%rsp), %rax
movq %rax, 40(%rsp)
addq %rcx, 40(%rsp)
movq 40(%rsp), %rax
movq %rax, 48(%rsp)
movq 48(%rsp), %r9
movq 48(%rsp), %rcx
movq $6, 56(%rsp)
movq 56(%rsp), %rax
movq %rax, 64(%rsp)
addq %rcx, 64(%rsp)
movq 64(%rsp), %rax
movq %rax, 72(%rsp)
movq 72(%rsp), %r8
movq 72(%rsp), %rcx
movq $9, 80(%rsp)
movq 80(%rsp), %rax
movq %rax, 88(%rsp)
addq %rcx, 88(%rsp)
movq 88(%rsp), %rax
movq %rax, 96(%rsp)
movq 96(%rsp), %rdi
movq 96(%rsp), %rcx
movq $6, 104(%rsp)
movq 104(%rsp), %rax
movq %rax, 112(%rsp)
addq %rcx, 112(%rsp)
movq 112(%rsp), %rax
movq %rax, 120(%rsp)
movq 120(%rsp), %rsi
movq 120(%rsp), %rax
movq %rax, 128(%rsp)
movq $8, 136(%rsp)
movq 136(%rsp), %rax
movq %rax, 144(%rsp)
movq 128(%rsp), %rax
addq %rax, 144(%rsp)
movq 144(%rsp), %rax
movq %rax, 152(%rsp)
movq 152(%rsp), %rax
movq %rax, 160(%rsp)
movq 152(%rsp), %rax
movq %rax, 168(%rsp)
movq $1, 176(%rsp)
movq 176(%rsp), %rax
movq %rax, 184(%rsp)
movq 168(%rsp), %rax
addq %rax, 184(%rsp)
movq 184(%rsp), %rcx
movq %rcx, 192(%rsp)
movq %rcx, 200(%rsp)
movq $5, 208(%rsp)
movq 208(%rsp), %rax
movq %rax, 216(%rsp)
movq 200(%rsp), %rax
addq %rax, 216(%rsp)
movq 216(%rsp), %rax
movq %rax, 224(%rsp)
movq 224(%rsp), %rax
movq %rax, 232(%rsp)
movq %rcx, 240(%rsp)
movq 240(%rsp), %rax
movq %rax, 248(%rsp)
movq 232(%rsp), %rax
addq %rax, 248(%rsp)
movq 248(%rsp), %rax
movq %rax, 256(%rsp)
movq 192(%rsp), %rax
addq %rax, 256(%rsp)
movq 256(%rsp), %rax
movq %rax, 264(%rsp)
movq 160(%rsp), %rax
addq %rax, 264(%rsp)
movq 264(%rsp), %rax
movq %rax, 272(%rsp)
addq %rsi, 272(%rsp)
movq 272(%rsp), %rax
movq %rax, 280(%rsp)
addq %rdi, 280(%rsp)
movq 280(%rsp), %rax
movq %rax, 288(%rsp)
addq %r8, 288(%rsp)
movq 288(%rsp), %rax
movq %rax, 296(%rsp)
addq %r9, 296(%rsp)
movq 296(%rsp), %rax
movq %rax, 304(%rsp)
addq %rdx, 304(%rsp)
movq 304(%rsp), %rax
jmp end
end:
addq $304, %rsp
popq %r15
popq %r14
popq %r13
popq %r12
popq %rbp
retq


