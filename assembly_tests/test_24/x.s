.globl main
begin:
pushq %rbp
movq %rsp, %rbp
addq $16, %rsp
jmp next
next:
movq $5, 8(%rsp)
movq $5, 16(%rsp)
movq 16(%rsp), %rax
movq %rax, 24(%rsp)
movq 8(%rsp), %rax
addq %rax, 24(%rsp)
movq 24(%rsp), %rax
movq %rax, %rax
jmp end
end:
subq $16, %rsp
popq %rbp
retq


