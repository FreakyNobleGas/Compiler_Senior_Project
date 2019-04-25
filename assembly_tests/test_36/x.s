.globl main
begin:
pushq %rbp
movq %rsp, %rbp
pushq %r12
pushq %r13
pushq %r14
pushq %r15
addq $408, %rsp
jmp next
next:
movq $2, %rax
movq $9, 8(%rsp)
movq 8(%rsp), 16(%rsp)
addq %rax, 16(%rsp)
movq 16(%rsp), 24(%rsp)
movq 24(%rsp), %rax
movq 24(%rsp), %rdx
movq $1, 32(%rsp)
movq 32(%rsp), 40(%rsp)
addq %rdx, 40(%rsp)
movq 40(%rsp), 48(%rsp)
movq 48(%rsp), %r8
movq 48(%rsp), %rdx
movq $9, 56(%rsp)
movq 56(%rsp), 64(%rsp)
addq %rdx, 64(%rsp)
movq 64(%rsp), 72(%rsp)
movq 72(%rsp), %rdi
movq 72(%rsp), %rdx
movq $6, 80(%rsp)
movq 80(%rsp), 88(%rsp)
addq %rdx, 88(%rsp)
movq 88(%rsp), 96(%rsp)
movq 96(%rsp), %rsi
movq 96(%rsp), %rdx
movq $0, 104(%rsp)
movq 104(%rsp), 112(%rsp)
addq %rdx, 112(%rsp)
movq 112(%rsp), 120(%rsp)
movq 120(%rsp), %rcx
movq 120(%rsp), 128(%rsp)
movq $2, 136(%rsp)
movq 136(%rsp), 144(%rsp)
addq 128(%rsp), 144(%rsp)
movq 144(%rsp), 152(%rsp)
movq 152(%rsp), 160(%rsp)
movq 152(%rsp), 168(%rsp)
movq $3, 176(%rsp)
movq 176(%rsp), 184(%rsp)
addq 168(%rsp), 184(%rsp)
movq 184(%rsp), 192(%rsp)
movq 192(%rsp), 200(%rsp)
movq 192(%rsp), 208(%rsp)
movq $1, 216(%rsp)
movq 216(%rsp), 224(%rsp)
addq 208(%rsp), 224(%rsp)
movq 224(%rsp), 232(%rsp)
movq 232(%rsp), 240(%rsp)
movq 232(%rsp), 248(%rsp)
movq $9, 256(%rsp)
movq 256(%rsp), 264(%rsp)
addq 248(%rsp), 264(%rsp)
movq 264(%rsp), %rdx
movq %rdx, 272(%rsp)
movq %rdx, 280(%rsp)
movq $0, 288(%rsp)
movq 288(%rsp), 296(%rsp)
addq 280(%rsp), 296(%rsp)
movq 296(%rsp), 304(%rsp)
movq 304(%rsp), 312(%rsp)
movq %rdx, 320(%rsp)
movq 320(%rsp), 328(%rsp)
addq 312(%rsp), 328(%rsp)
movq 328(%rsp), 336(%rsp)
addq 272(%rsp), 336(%rsp)
movq 336(%rsp), 344(%rsp)
addq 240(%rsp), 344(%rsp)
movq 344(%rsp), 352(%rsp)
addq 200(%rsp), 352(%rsp)
movq 352(%rsp), 360(%rsp)
addq 160(%rsp), 360(%rsp)
movq 360(%rsp), 368(%rsp)
addq %rcx, 368(%rsp)
movq 368(%rsp), 376(%rsp)
addq %rsi, 376(%rsp)
movq 376(%rsp), 384(%rsp)
addq %rdi, 384(%rsp)
movq 384(%rsp), 392(%rsp)
addq %r8, 392(%rsp)
movq 392(%rsp), 400(%rsp)
addq %rax, 400(%rsp)
movq 400(%rsp), %rax
jmp end
end:
subq $408, %rsp
popq %r15
popq %r14
popq %r13
popq %r12
popq %rbp
retq


