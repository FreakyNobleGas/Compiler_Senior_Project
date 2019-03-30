globl .main
main:
movq $5, (_u)
movq $5, (_u1)
movq $5, (_u2)
movq (_u2), (_u3)
addq (_u1), (_u3)
movq (_u3), (_u4)
addq (_u), (_u4)
movq (_u4), %rax
jmp end
end:
retq

