.globl main
main:
movq $30, (_u)
movq (_u), (y)
movq (y), (_u1)
movq $10, (_u2)
movq (_u2), (y1)
movq (y1), (_u3)
movq $5, (_u4)
movq $5, (_u5)
movq (_u5), (_u6)
addq (_u4), (_u6)
movq (_u6), (y2)
movq (y2), (_u7)
movq (y2), (_u8)
movq (_u8), (_u9)
addq (_u7), (_u9)
movq (_u9), (_u10)
addq (_u3), (_u10)
movq (_u10), (_u11)
addq (_u1), (_u11)
movq (_u11), %rax
jmp end
end:
retq

