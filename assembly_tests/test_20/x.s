.globl main
begin:
pushq %rbp
movq %rsp, %rbp
pushq %r12
pushq %r13
pushq %r14
pushq %r15
subq $16, %rsp
jmp next
next:
movq $5, 8(%rsp)
movq 8(%rsp), 16(%rsp)
movq 16(%rsp), 24(%rsp)
movq $8, 32(%rsp)
movq 32(%rsp), 40(%rsp)
addq 24(%rsp), 40(%rsp)
movq 40(%rsp), %rax
jmp end
end:
addq $16, %rsp
popq %r15
popq %r14
popq %r13
popq %r12
popq %rbp
retq


