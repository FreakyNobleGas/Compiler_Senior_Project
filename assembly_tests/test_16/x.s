.globl main
main:
movq $5, (_u)
movq (_u), (y)
movq (y), (_u1)
movq $5, (_u2)
movq $5, (_u3)
movq (_u3), (_u4)
addq (_u2), (_u4)
movq (_u4), (y1)
movq (y1), (_u5)
movq (y1), (_u6)
movq (_u6), (_u7)
addq (_u5), (_u7)
movq (_u7), (_u8)
addq (_u1), (_u8)
movq (_u8), %rax
jmp end
end:
retq

