.globl main
begin:
pushq %rbp
movq %rsp, %rbp
addq $16, %rsp
jmp next
next:
movq $3, 8(%rsp)
movq $1, 16(%rsp)
movq 16(%rsp), 24(%rsp)
addq 8(%rsp), 24(%rsp)
movq 24(%rsp), 32(%rsp)
movq 32(%rsp), 40(%rsp)
movq 32(%rsp), 48(%rsp)
movq $1, 56(%rsp)
movq 56(%rsp), 64(%rsp)
addq 48(%rsp), 64(%rsp)
movq 64(%rsp), 72(%rsp)
movq 72(%rsp), 80(%rsp)
movq 72(%rsp), 88(%rsp)
movq $7, 96(%rsp)
movq 96(%rsp), 104(%rsp)
addq 88(%rsp), 104(%rsp)
movq 104(%rsp), 112(%rsp)
movq 112(%rsp), 120(%rsp)
movq 72(%rsp), 128(%rsp)
movq 128(%rsp), 136(%rsp)
addq 120(%rsp), 136(%rsp)
movq 136(%rsp), 144(%rsp)
addq 80(%rsp), 144(%rsp)
movq 144(%rsp), 152(%rsp)
addq 40(%rsp), 152(%rsp)
movq 152(%rsp), %rax
jmp end
end:
subq $16, %rsp
popq %rbp
retq


