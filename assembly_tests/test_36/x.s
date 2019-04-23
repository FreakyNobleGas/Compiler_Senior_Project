.globl main
begin:
pushq %rbp
movq %rsp, %rbp
addq $16, %rsp
jmp next
next:
movq $9, %rax
movq $10, 8(%rsp)
movq 8(%rsp), 16(%rsp)
addq %rax, 16(%rsp)
movq 16(%rsp), 24(%rsp)
movq 24(%rsp), %rax
movq 24(%rsp), 32(%rsp)
movq 32(%rsp), 40(%rsp)
addq %rax, 40(%rsp)
movq 40(%rsp), %rax
jmp end
end:
subq $16, %rsp
popq %rbp
retq


