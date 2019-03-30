globl .main
main:
movq $5, (_u)
movq $5, (_u1)
movq (_u1), (_u2)
addq (_u), (_u2)
movq (_u2), %rax
jmp end
end:
retq

