.globl main
begin:
pushq %rbp
movq %rsp, %rbp
pushq %r12
pushq %r13
pushq %r14
pushq %r15
subq $360, %rsp
jmp next
next:
movq $4, %rax
movq $8, 8(%rsp)
movq 8(%rsp), 16(%rsp)
addq %rax, 16(%rsp)
movq 16(%rsp), 24(%rsp)
movq 24(%rsp), %rax
movq 24(%rsp), %rdx
movq $3, 32(%rsp)
movq 32(%rsp), 40(%rsp)
addq %rdx, 40(%rsp)
movq 40(%rsp), 48(%rsp)
movq 48(%rsp), %r8
movq 48(%rsp), %rdx
movq $1, 56(%rsp)
movq 56(%rsp), 64(%rsp)
addq %rdx, 64(%rsp)
movq 64(%rsp), 72(%rsp)
movq 72(%rsp), %rdi
movq 72(%rsp), %rdx
movq $2, 80(%rsp)
movq 80(%rsp), 88(%rsp)
addq %rdx, 88(%rsp)
movq 88(%rsp), 96(%rsp)
movq 96(%rsp), %rsi
movq 96(%rsp), %rdx
movq $5, 104(%rsp)
movq 104(%rsp), 112(%rsp)
addq %rdx, 112(%rsp)
movq 112(%rsp), 120(%rsp)
movq 120(%rsp), %rcx
movq 120(%rsp), 128(%rsp)
movq $9, 136(%rsp)
movq 136(%rsp), 144(%rsp)
addq 128(%rsp), 144(%rsp)
movq 144(%rsp), 152(%rsp)
movq 152(%rsp), 160(%rsp)
movq 152(%rsp), 168(%rsp)
movq $8, 176(%rsp)
movq 176(%rsp), 184(%rsp)
addq 168(%rsp), 184(%rsp)
movq 184(%rsp), 192(%rsp)
movq 192(%rsp), 200(%rsp)
movq 192(%rsp), 208(%rsp)
movq $4, 216(%rsp)
movq 216(%rsp), 224(%rsp)
addq 208(%rsp), 224(%rsp)
movq 224(%rsp), %rdx
movq %rdx, 232(%rsp)
movq %rdx, 240(%rsp)
movq $9, 248(%rsp)
movq 248(%rsp), 256(%rsp)
addq 240(%rsp), 256(%rsp)
movq 256(%rsp), 264(%rsp)
movq 264(%rsp), 272(%rsp)
movq %rdx, 280(%rsp)
movq 280(%rsp), 288(%rsp)
addq 272(%rsp), 288(%rsp)
movq 288(%rsp), 296(%rsp)
addq 232(%rsp), 296(%rsp)
movq 296(%rsp), 304(%rsp)
addq 200(%rsp), 304(%rsp)
movq 304(%rsp), 312(%rsp)
addq 160(%rsp), 312(%rsp)
movq 312(%rsp), 320(%rsp)
addq %rcx, 320(%rsp)
movq 320(%rsp), 328(%rsp)
addq %rsi, 328(%rsp)
movq 328(%rsp), 336(%rsp)
addq %rdi, 336(%rsp)
movq 336(%rsp), 344(%rsp)
addq %r8, 344(%rsp)
movq 344(%rsp), 352(%rsp)
addq %rax, 352(%rsp)
movq 352(%rsp), %rax
jmp end
end:
addq $360, %rsp
popq %r15
popq %r14
popq %r13
popq %r12
popq %rbp
retq


