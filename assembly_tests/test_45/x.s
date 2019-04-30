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
subq $48, %rsp
jmp next
next:
movq $1, %rdx
movq $4, 8(%rsp)
movq 8(%rsp), %rax
movq %rax, 16(%rsp)
addq %rdx, 16(%rsp)
movq 16(%rsp), %rax
movq %rax, 24(%rsp)
movq 24(%rsp), %rdx
movq 24(%rsp), %rax
movq %rax, 32(%rsp)
movq 32(%rsp), %rax
movq %rax, 40(%rsp)
addq %rdx, 40(%rsp)
movq 40(%rsp), %rax
jmp end
end:
addq $48, %rsp
popq %r15
popq %r14
popq %r13
popq %r12
popq %rbp
retq


