.globl main
main:
movq $15, %r10
movq %r10, %r11
addq %r10, %r11
movq %r11, %rax
retq
