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
movq $3, %rdx
movq $4, 8(%rsp)
movq 8(%rsp), %rax
movq %rax, 16(%rsp)
addq %rdx, 16(%rsp)
movq 16(%rsp), %rax
movq %rax, 24(%rsp)
movq 24(%rsp), %rdx
movq 24(%rsp), %rcx
movq $10, 32(%rsp)
movq 32(%rsp), %rax
movq %rax, 40(%rsp)
addq %rcx, 40(%rsp)
movq 40(%rsp), %rsi
movq %rsi, %rsi
movq %rsi, %rcx
movq $3, 48(%rsp)
movq 48(%rsp), %rax
movq %rax, 56(%rsp)
addq %rcx, 56(%rsp)
movq 56(%rsp), %rax
movq %rax, 64(%rsp)
movq 64(%rsp), %rcx
movq %rsi, 72(%rsp)
movq 72(%rsp), %rax
movq %rax, 80(%rsp)
addq %rcx, 80(%rsp)
movq 80(%rsp), %rax
movq %rax, 88(%rsp)
addq %rsi, 88(%rsp)
movq 88(%rsp), %rax
movq %rax, 96(%rsp)
addq %rdx, 96(%rsp)
movq 96(%rsp), %rax
jmp end
end:
addq $96, %rsp
popq %r15
popq %r14
popq %r13
popq %r12
popq %rbp
retq


