.globl main
begin:
pushq %rbp
movq %rsp, %rbp
addq $16, %rsp
jmp next
next:
movq $5, 8(%rsp)
movq 8(%rsp), %rax
movq %rax, 16(%rsp)
movq 16(%rsp), %rax
movq %rax, 24(%rsp)
movq $5, 32(%rsp)
movq $5, 40(%rsp)
movq 40(%rsp), %rax
movq %rax, 48(%rsp)
movq 32(%rsp), %rax
addq %rax, 48(%rsp)
movq 48(%rsp), %rax
movq %rax, 56(%rsp)
movq 56(%rsp), %rax
movq %rax, 64(%rsp)
movq 56(%rsp), %rax
movq %rax, 72(%rsp)
movq 72(%rsp), %rax
movq %rax, 80(%rsp)
movq 64(%rsp), %rax
addq %rax, 80(%rsp)
movq 80(%rsp), %rax
movq %rax, 88(%rsp)
movq 24(%rsp), %rax
addq %rax, 88(%rsp)
movq 88(%rsp), %rax
movq %rax, %rax
jmp end
end:
subq $16, %rsp
popq %rbp
retq


