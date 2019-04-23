.globl main
begin:
pushq %rbp
movq %rsp, %rbp
addq $16, %rsp
jmp next
next:
movq $0, %rax
movq $0, 8(%rsp)
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
movq $5, 56(%rsp)
movq 56(%rsp), 64(%rsp)
addq %rdx, 64(%rsp)
movq 64(%rsp), 72(%rsp)
movq 72(%rsp), %rdi
movq 72(%rsp), %rdx
movq $5, 80(%rsp)
movq 80(%rsp), 88(%rsp)
addq %rdx, 88(%rsp)
movq 88(%rsp), 96(%rsp)
movq 96(%rsp), %rsi
movq 96(%rsp), %rdx
movq $1, 104(%rsp)
movq 104(%rsp), 112(%rsp)
addq %rdx, 112(%rsp)
movq 112(%rsp), 120(%rsp)
movq 120(%rsp), %rcx
movq 120(%rsp), 128(%rsp)
movq $9, 136(%rsp)
movq 136(%rsp), 144(%rsp)
addq 128(%rsp), 144(%rsp)
movq 144(%rsp), %rdx
movq %rdx, 152(%rsp)
movq %rdx, 160(%rsp)
movq $7, 168(%rsp)
movq 168(%rsp), 176(%rsp)
addq 160(%rsp), 176(%rsp)
movq 176(%rsp), 184(%rsp)
movq 184(%rsp), 192(%rsp)
movq %rdx, 200(%rsp)
movq 200(%rsp), 208(%rsp)
addq 192(%rsp), 208(%rsp)
movq 208(%rsp), 216(%rsp)
addq 152(%rsp), 216(%rsp)
movq 216(%rsp), 224(%rsp)
addq %rcx, 224(%rsp)
movq 224(%rsp), 232(%rsp)
addq %rsi, 232(%rsp)
movq 232(%rsp), 240(%rsp)
addq %rdi, 240(%rsp)
movq 240(%rsp), 248(%rsp)
addq %r8, 248(%rsp)
movq 248(%rsp), 256(%rsp)
addq %rax, 256(%rsp)
movq 256(%rsp), %rax
jmp end
end:
subq $16, %rsp
popq %rbp
retq


