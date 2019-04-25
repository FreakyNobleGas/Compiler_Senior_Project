.globl main
main:
callq begin
movq %rax, %rdi
callq print_int
retq
begin:
pushq %rbp
movq %rsp, %rbp
pushq %r12
pushq %r13
pushq %r14
pushq %r15
subq $72, %rsp
jmp next
next:
movq $5, 8(%rsp)
movq 8(%rsp), 16(%rsp)
movq 16(%rsp), %rax
movq $5, %rdx
movq $5, 24(%rsp)
movq 24(%rsp), 32(%rsp)
addq %rdx, 32(%rsp)
movq 32(%rsp), 40(%rsp)
movq 40(%rsp), %rdx
movq 40(%rsp), 48(%rsp)
movq 48(%rsp), 56(%rsp)
addq %rdx, 56(%rsp)
movq 56(%rsp), 64(%rsp)
addq %rax, 64(%rsp)
movq 64(%rsp), %rax
jmp end
end:
addq $72, %rsp
popq %r15
popq %r14
popq %r13
popq %r12
popq %rbp
retq


