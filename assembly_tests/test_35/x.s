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
subq $96, %rsp
jmp next
next:
movq $30, 8(%rsp)
movq 8(%rsp), %rax
movq %rax, 16(%rsp)
movq 16(%rsp), %rdx
movq $10, 24(%rsp)
movq 24(%rsp), %rax
movq %rax, 32(%rsp)
movq 32(%rsp), %rcx
movq $5, %rsi
movq $5, 40(%rsp)
movq 40(%rsp), %rax
movq %rax, 48(%rsp)
addq %rsi, 48(%rsp)
movq 48(%rsp), %rax
movq %rax, 56(%rsp)
movq 56(%rsp), %rsi
movq 56(%rsp), %rax
movq %rax, 64(%rsp)
movq 64(%rsp), %rax
movq %rax, 72(%rsp)
addq %rsi, 72(%rsp)
movq 72(%rsp), %rax
movq %rax, 80(%rsp)
addq %rcx, 80(%rsp)
movq 80(%rsp), %rax
movq %rax, 88(%rsp)
addq %rdx, 88(%rsp)
movq 88(%rsp), %rax
jmp end
end:
addq $96, %rsp
popq %r15
popq %r14
popq %r13
popq %r12
popq %rbp
retq


