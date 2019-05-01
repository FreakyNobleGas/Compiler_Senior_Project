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
subq $352, %rsp
jmp next
next:
movq $1, %rdx
movq $7, 8(%rsp)
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
movq $5, 56(%rsp)
movq 56(%rsp), %rax
movq %rax, 64(%rsp)
addq %rcx, 64(%rsp)
movq 64(%rsp), %rax
movq %rax, 72(%rsp)
movq 72(%rsp), %r8
movq 72(%rsp), %rcx
movq $2, 80(%rsp)
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
movq $0, 136(%rsp)
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
movq 184(%rsp), %rax
movq %rax, 192(%rsp)
movq 192(%rsp), %rax
movq %rax, 200(%rsp)
movq 192(%rsp), %rax
movq %rax, 208(%rsp)
movq $3, 216(%rsp)
movq 216(%rsp), %rax
movq %rax, 224(%rsp)
movq 208(%rsp), %rax
addq %rax, 224(%rsp)
movq 224(%rsp), %rcx
movq %rcx, 232(%rsp)
movq %rcx, 240(%rsp)
movq $9, 248(%rsp)
movq 248(%rsp), %rax
movq %rax, 256(%rsp)
movq 240(%rsp), %rax
addq %rax, 256(%rsp)
movq 256(%rsp), %rax
movq %rax, 264(%rsp)
movq 264(%rsp), %rax
movq %rax, 272(%rsp)
movq %rcx, 280(%rsp)
movq 280(%rsp), %rax
movq %rax, 288(%rsp)
movq 272(%rsp), %rax
addq %rax, 288(%rsp)
movq 288(%rsp), %rax
movq %rax, 296(%rsp)
movq 232(%rsp), %rax
addq %rax, 296(%rsp)
movq 296(%rsp), %rax
movq %rax, 304(%rsp)
movq 200(%rsp), %rax
addq %rax, 304(%rsp)
movq 304(%rsp), %rax
movq %rax, 312(%rsp)
movq 160(%rsp), %rax
addq %rax, 312(%rsp)
movq 312(%rsp), %rax
movq %rax, 320(%rsp)
addq %rsi, 320(%rsp)
movq 320(%rsp), %rax
movq %rax, 328(%rsp)
addq %rdi, 328(%rsp)
movq 328(%rsp), %rax
movq %rax, 336(%rsp)
addq %r8, 336(%rsp)
movq 336(%rsp), %rax
movq %rax, 344(%rsp)
addq %r9, 344(%rsp)
movq 344(%rsp), %rax
movq %rax, 352(%rsp)
addq %rdx, 352(%rsp)
movq 352(%rsp), %rax
jmp end
end:
addq $352, %rsp
popq %r15
popq %r14
popq %r13
popq %r12
popq %rbp
retq


