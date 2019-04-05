.globl main
main:
movq $14, %r10
jmp end
end:
movq %r10, %rax
retq

