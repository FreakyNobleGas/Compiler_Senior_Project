.globl main
begin:
pushq %rbp
movq %rsp, %rbp
pushq %r12
pushq %r13
pushq %r14
pushq %r15
subq $312, %rsp
jmp next
next:
movq $7, %rax
movq $10, 8(%rsp)
movq 8(%rsp), 16(%rsp)
addq %rax, 16(%rsp)
movq 16(%rsp), 24(%rsp)
movq 24(%rsp), %rax
movq 24(%rsp), %rdx
movq $7, 32(%rsp)
movq 32(%rsp), 40(%rsp)
addq %rdx, 40(%rsp)
movq 40(%rsp), 48(%rsp)
movq 48(%rsp), %r8
movq 48(%rsp), %rdx
movq $3, 56(%rsp)
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
movq $4, 104(%rsp)
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
movq $8, 176(%rsp)
movq 176(%rsp), 184(%rsp)
addq 168(%rsp), 184(%rsp)
movq 184(%rsp), %rdx
movq %rdx, 192(%rsp)
movq %rdx, 200(%rsp)
movq $2, 208(%rsp)
movq 208(%rsp), 216(%rsp)
addq 200(%rsp), 216(%rsp)
movq 216(%rsp), 224(%rsp)
movq 224(%rsp), 232(%rsp)
movq %rdx, 240(%rsp)
movq 240(%rsp), 248(%rsp)
addq 232(%rsp), 248(%rsp)
movq 248(%rsp), 256(%rsp)
addq 192(%rsp), 256(%rsp)
movq 256(%rsp), 264(%rsp)
addq 160(%rsp), 264(%rsp)
movq 264(%rsp), 272(%rsp)
addq %rcx, 272(%rsp)
movq 272(%rsp), 280(%rsp)
addq %rsi, 280(%rsp)
movq 280(%rsp), 288(%rsp)
addq %rdi, 288(%rsp)
movq 288(%rsp), 296(%rsp)
addq %r8, 296(%rsp)
movq 296(%rsp), 304(%rsp)
addq %rax, 304(%rsp)
movq 304(%rsp), %rax
jmp end
end:
addq $312, %rsp
popq %r15
popq %r14
popq %r13
popq %r12
popq %rbp
retq


