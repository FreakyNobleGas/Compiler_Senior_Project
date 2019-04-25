.globl main
main:
callq begin
movq %rax, %rdi
callq print_int
retq
begin:
pushq %rbp
movq %rsp, %rbp
addq $24, %rsp
jmp next
next:
movq $5, %rax
movq $5, 8(%rsp)
movq 8(%rsp), %rax
movq %rax, 16(%rsp)
addq %rax, 16(%rsp)
movq 16(%rsp), %rax
movq %rax, %rax
jmp end
end:
subq $24, %rsp
popq %rbp
retq


