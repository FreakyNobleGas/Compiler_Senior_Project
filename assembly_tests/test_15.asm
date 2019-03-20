globl .main
main:
movq $5, (_u)
movq (_u), (x)
movq (x), (_u1)
movq $10, (_u2)
movq (_u2), (y)
movq (y), (_u3)
movq (_u3), (_u4)
addq (_u1), (_u4)
movq (_u4), %rax
jmp end:
retq

