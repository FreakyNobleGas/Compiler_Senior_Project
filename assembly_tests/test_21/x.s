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
movq $10, 32(%rsp)
movq 32(%rsp), 40(%rsp)
movq 40(%rsp), 48(%rsp)
movq 48(%rsp), 56(%rsp)
addq 24(%rsp), 56(%rsp)
movq 56(%rsp), %rax
jmp end
end:
subq $16, %rsp
popq %rbp
retq


