.globl main
begin:
pushq %rbp
movq %rsp, %rbp
addq $16, %rsp
jmp next
next:
movq $7, 8(%rsp)
movq $7, 16(%rsp)
movq 16(%rsp), 24(%rsp)
addq 8(%rsp), 24(%rsp)
movq 24(%rsp), 32(%rsp)
movq 32(%rsp), 40(%rsp)
movq 32(%rsp), 48(%rsp)
movq $10, 56(%rsp)
movq 56(%rsp), 64(%rsp)
addq 48(%rsp), 64(%rsp)
movq 64(%rsp), 72(%rsp)
movq 72(%rsp), 80(%rsp)
movq 72(%rsp), 88(%rsp)
movq $9, 96(%rsp)
movq 96(%rsp), 104(%rsp)
addq 88(%rsp), 104(%rsp)
movq 104(%rsp), 112(%rsp)
movq 112(%rsp), 120(%rsp)
movq 112(%rsp), 128(%rsp)
movq $10, 136(%rsp)
movq 136(%rsp), 144(%rsp)
addq 128(%rsp), 144(%rsp)
movq 144(%rsp), 152(%rsp)
movq 152(%rsp), 160(%rsp)
movq 152(%rsp), 168(%rsp)
movq $10, 176(%rsp)
movq 176(%rsp), 184(%rsp)
addq 168(%rsp), 184(%rsp)
movq 184(%rsp), 192(%rsp)
movq 192(%rsp), 200(%rsp)
movq 192(%rsp), 208(%rsp)
movq $3, 216(%rsp)
movq 216(%rsp), 224(%rsp)
addq 208(%rsp), 224(%rsp)
movq 224(%rsp), 232(%rsp)
movq 232(%rsp), 240(%rsp)
movq 232(%rsp), 248(%rsp)
movq $9, 256(%rsp)
movq 256(%rsp), 264(%rsp)
addq 248(%rsp), 264(%rsp)
movq 264(%rsp), 272(%rsp)
movq 272(%rsp), 280(%rsp)
movq 232(%rsp), 288(%rsp)
movq 288(%rsp), 296(%rsp)
addq 280(%rsp), 296(%rsp)
movq 296(%rsp), 304(%rsp)
addq 240(%rsp), 304(%rsp)
movq 304(%rsp), 312(%rsp)
addq 200(%rsp), 312(%rsp)
movq 312(%rsp), 320(%rsp)
addq 160(%rsp), 320(%rsp)
movq 320(%rsp), 328(%rsp)
addq 120(%rsp), 328(%rsp)
movq 328(%rsp), 336(%rsp)
addq 80(%rsp), 336(%rsp)
movq 336(%rsp), 344(%rsp)
addq 40(%rsp), 344(%rsp)
movq 344(%rsp), %rax
jmp end
end:
subq $16, %rsp
popq %rbp
retq


