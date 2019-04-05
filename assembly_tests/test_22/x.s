.globl main
begin:
pushq %rbp
movq %rsp, %rbp
addq $16, %rsp
jmp next
next:
movq $5, 8(%rsp)
movq 8(%rsp), 16(%rsp)
movq 16(%rsp), 24(%rsp)
movq $5, 32(%rsp)
movq $5, 40(%rsp)
movq 40(%rsp), 48(%rsp)
addq 32(%rsp), 48(%rsp)
movq 48(%rsp), 56(%rsp)
movq 56(%rsp), 64(%rsp)
movq 56(%rsp), 72(%rsp)
movq 72(%rsp), 80(%rsp)
addq 64(%rsp), 80(%rsp)
movq 80(%rsp), 88(%rsp)
addq 24(%rsp), 88(%rsp)
movq 88(%rsp), %rax
jmp end
end:
subq $16, %rsp
popq %rbp
retq


