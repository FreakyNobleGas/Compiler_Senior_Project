.globl main
begin:
pushq %rbp
movq %rsp, %rbp
addq $16, %rsp
jmp next
next:
movq $7, %rax
movq $10, 8(%rsp)
movq 8(%rsp), 16(%rsp)
addq %rax, 16(%rsp)
movq 16(%rsp), 24(%rsp)
movq 24(%rsp), %rax
movq 24(%rsp), %rdx
movq $5, 32(%rsp)
movq 32(%rsp), 40(%rsp)
addq %rdx, 40(%rsp)
movq 40(%rsp), 48(%rsp)
movq 48(%rsp), %rdi
movq 48(%rsp), %rdx
movq $9, 56(%rsp)
movq 56(%rsp), 64(%rsp)
addq %rdx, 64(%rsp)
movq 64(%rsp), 72(%rsp)
movq 72(%rsp), %rsi
movq 72(%rsp), %rdx
movq $2, 80(%rsp)
movq 80(%rsp), 88(%rsp)
addq %rdx, 88(%rsp)
movq 88(%rsp), %rcx
movq %rcx, %rcx
movq %rcx, 96(%rsp)
movq $3, 104(%rsp)
movq 104(%rsp), 112(%rsp)
addq 96(%rsp), 112(%rsp)
movq 112(%rsp), 120(%rsp)
movq 120(%rsp), %rdx
movq %rcx, 128(%rsp)
movq 128(%rsp), 136(%rsp)
addq %rdx, 136(%rsp)
movq 136(%rsp), 144(%rsp)
addq %rcx, 144(%rsp)
movq 144(%rsp), 152(%rsp)
addq %rsi, 152(%rsp)
movq 152(%rsp), 160(%rsp)
addq %rdi, 160(%rsp)
movq 160(%rsp), 168(%rsp)
addq %rax, 168(%rsp)
movq 168(%rsp), %rax
jmp end
end:
subq $16, %rsp
popq %rbp
retq


