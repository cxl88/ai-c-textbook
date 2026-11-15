#!/bin/bash
# 限时运行“停不下来”的程序（死循环），作为“程序不会自己结束”的实测证据。
#   先用 wrun.sh 编译（bad_ 开头的只编译、不运行，可执行文件留在 Wine 工作目录中），
#   再在 Wine 中运行 T 秒（默认 5 秒）后强制结束，只保存开头的输出。
# 用法：CODE_DIR=程序目录 [T=5] [LINES=30] bash wcap.sh 程序名…
#   name.cin      键盘输入（没有这个文件就不输入）
#   name.wcap     开头的 LINES 行输出（GBK 转为 UTF-8）
#   name.wcapret  “timeout 5s lines=N bytes=M”表示运行 5 秒仍未结束、被强制结束，此前共输出 N 行（M 字节）；否则为 exit=返回值
# 说明：输出写入文件时有缓冲，被强制结束时还没有写满一块的输出不会出现在记录中；
#       所以输出很少的死循环，记录中可能没有输出，以 timeout 为准。
B=${CODE_DIR:-$(cd "$(dirname "$0")" && pwd)/code}
W=/root/cstudy/wb
T=${T:-5}
LINES=${LINES:-30}
export DISPLAY=:99 WINEPREFIX=/root/.wine64b WINEDEBUG=-all LANG=zh_CN.UTF-8 LC_ALL=zh_CN.UTF-8
for n in "$@"; do
  [ -f "$W/$n.exe" ] || { echo "$n.exe 不存在：先用 wrun.sh 编译"; exit 1; }
  if [ -f "$B/$n.cin" ]; then sed 's/\r$//; s/$/\r/' "$B/$n.cin" > "$W/$n.cin"; else : > "$W/$n.cin"; fi
  ( cd "$W" && timeout "$T" wine "$n.exe" < "$n.cin" > "$n.cap" 2>/dev/null ); rc=$?
  total=$(wc -l < "$W/$n.cap"); bytes=$(wc -c < "$W/$n.cap")
  # 只取开头：最多 LINES 行、3000 字节（不换行的输出也不会太长）；截断处不完整的汉字由 iconv -c 丢弃
  head -n "$LINES" "$W/$n.cap" | head -c 3000 | iconv -f gbk -t utf-8 -c | sed 's/\r$//' > "$B/$n.wcap"
  if [ $rc -eq 124 ]; then st="timeout ${T}s"; else st="exit=$rc"; fi
  echo "$st lines=$total bytes=$bytes" > "$B/$n.wcapret"
  rm -f "$W/$n.cap"
  echo "=== $n: $(cat "$B/$n.wcapret")"; head -4 "$B/$n.wcap"
done
