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
subq $32, %rsp
jmp next
next:
movq $5, %rax
movq $5, %rdx
movq $5, 8(%rsp)
movq 8(%rsp), %rax
movq %rax, 16(%rsp)
addq %rdx, 16(%rsp)
movq 16(%rsp), %rax
movq %rax, 24(%rsp)
addq %rax, 24(%rsp)
movq 24(%rsp), %rax
jmp end
end:
addq $32, %rsp
popq %r15
popq %r14
popq %r13
popq %r12
popq %rbp
retq


