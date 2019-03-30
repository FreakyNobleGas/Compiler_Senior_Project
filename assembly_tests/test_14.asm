globl .main
main:
movq $5, (_u)
movq (_u), (x)
movq (x), (_u1)
movq $8, (_u2)
movq (_u2), (_u3)
addq (_u1), (_u3)
movq (_u3), %rax
jmp end
end:
retq

