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
movq 8(%rsp), %rax
movq %rax, 16(%rsp)
movq 16(%rsp), %rdx
movq $5, %rcx
movq $5, 24(%rsp)
movq 24(%rsp), %rax
movq %rax, 32(%rsp)
addq %rcx, 32(%rsp)
movq 32(%rsp), %rax
movq %rax, 40(%rsp)
movq 40(%rsp), %rcx
movq 40(%rsp), %rax
movq %rax, 48(%rsp)
movq 48(%rsp), %rax
movq %rax, 56(%rsp)
addq %rcx, 56(%rsp)
movq 56(%rsp), %rax
movq %rax, 64(%rsp)
addq %rdx, 64(%rsp)
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


