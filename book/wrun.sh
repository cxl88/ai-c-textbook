#!/bin/bash
# 用小熊猫C++自带的 Windows 版 GCC（wine）编译并运行指定程序，输出转为 UTF-8 存回 code/
B=$(cd "$(dirname "$0")" && pwd)/code
W=/root/cstudy/wb
export DISPLAY=:99 WINEPREFIX=/root/.wine64b WINEDEBUG=-all LANG=zh_CN.UTF-8 LC_ALL=zh_CN.UTF-8
rm -f $W/PARTDONE.txt
{
printf '@echo off\r\nset PATH=C:\\Program Files\\RedPanda-Cpp\\mingw64\\bin;%%PATH%%\r\ncd /d D:\\wb\r\n'
for n in "$@"; do
  sed 's/\r$//; s/$/\r/' $B/$n.c > $W/$n.c
  rm -f $W/$n.exe $W/$n.wout $W/$n.wdiag
  printf 'gcc.exe %s.c -o %s.exe -Wall -Werror=implicit-int -Werror=return-type -Werror=vla -g -pipe -finput-charset=UTF-8 -fexec-charset=GBK 2> %s.wdiag\r\n' $n $n $n
  case $n in bad_lab_run) ;; bad_*) continue;; esac
  if [ -f $B/$n.in ]; then sed 's/\r$//; s/$/\r/' $B/$n.in > $W/$n.in; printf 'if exist %s.exe %s.exe < %s.in > %s.wout\r\n' $n $n $n $n
  else printf 'if exist %s.exe %s.exe > %s.wout\r\n' $n $n $n; fi
done
printf 'echo done > D:\\wb\\PARTDONE.txt\r\n'
} > $W/part.bat
cd $W && timeout 400 wine cmd /c 'D:\wb\part.bat' > $W/part.log 2>&1
[ -f $W/PARTDONE.txt ] || { echo "BATCH DID NOT FINISH"; cat $W/part.log; exit 1; }
for n in "$@"; do
  [ -f $W/$n.wout ] && iconv -f gbk -t utf-8 $W/$n.wout | sed 's/\r$//' > $B/$n.wout
  sed 's/\r$//' $W/$n.wdiag > $B/$n.wdiag
  echo "=== $n  (diag $(wc -c < $B/$n.wdiag) bytes)"; [ -s $B/$n.wdiag ] && cat $B/$n.wdiag; [ -f $B/$n.wout ] && cat $B/$n.wout | head -40
done
