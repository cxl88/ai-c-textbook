#!/bin/bash
# 用小熊猫C++ 自带的 Windows 版 GCC（在 Wine 中）编译并运行 code/ 下的程序，结果转为 UTF-8 存回 code/：
#   name.wdiag        编译器提示（空文件表示没有任何提示）
#   name.wout / .wret 运行输出 / 返回值；有 name.in 时用它作键盘输入
#   name.wout2 …      还有 name.in2、name.in3 … 时，逐个作为输入再运行，结果依次存为 .wout2/.wret2 …
# 以 bad_ 开头的程序含有编译错误或“未定义行为”，只编译、不运行。
# 编译选项与小熊猫C++ 3.4 默认的“MinGW-w64 GCC 11.5.0 64-bit Debug”配置相同；WEXTRA 可临时附加选项（如 -Wconversion）。
B=${CODE_DIR:-$(cd "$(dirname "$0")" && pwd)/code}
W=/root/cstudy/wb
export DISPLAY=:99 WINEPREFIX=/root/.wine64b WINEDEBUG=-all LANG=zh_CN.UTF-8 LC_ALL=zh_CN.UTF-8
rm -f $W/PARTDONE.txt
inputs() { for f in $B/$1.in $B/$1.in[2-9]; do [ -f "$f" ] && { s=${f##*.in}; echo "${s:-@}"; }; done; }   # @ 代表 name.in
{
printf '@echo off\r\nset PATH=C:\\Program Files\\RedPanda-Cpp\\mingw64\\bin;%%PATH%%\r\ncd /d D:\\wb\r\n'
for n in "$@"; do
  sed 's/\r$//; s/$/\r/' $B/$n.c > $W/$n.c
  rm -f $W/$n.exe $W/$n.wout* $W/$n.wret* $W/$n.wdiag
  printf 'gcc.exe %s.c -o %s.exe -finput-charset=UTF-8 -fexec-charset=gbk -g3 -fno-ms-extensions -pipe -Wall -Werror=implicit-int -Werror=return-type -Werror=vla%s 2> %s.wdiag\r\n' $n $n "${WEXTRA:+ $WEXTRA}" $n
  case $n in bad_*) continue;; esac
  ins=$(inputs $n)
  if [ -z "$ins" ]; then
    printf 'if exist %s.exe %s.exe > %s.wout\r\nif exist %s.exe echo %%ERRORLEVEL%% > %s.wret\r\n' $n $n $n $n $n
  else
    for s in $ins; do
      [ "$s" = @ ] && s=
      sed 's/\r$//; s/$/\r/' $B/$n.in$s > $W/$n.in$s
      printf 'if exist %s.exe %s.exe < %s.in%s > %s.wout%s\r\nif exist %s.exe echo %%ERRORLEVEL%% > %s.wret%s\r\n' $n $n $n "$s" $n "$s" $n $n "$s"
    done
  fi
done
printf 'echo done > D:\\wb\\PARTDONE.txt\r\n'
} > $W/part.bat
cd $W && timeout 600 wine cmd /c 'D:\wb\part.bat' > $W/part.log 2>&1
[ -f $W/PARTDONE.txt ] || { echo "BATCH DID NOT FINISH"; cat $W/part.log; exit 1; }
for n in "$@"; do
  rm -f $B/$n.wout $B/$n.wout[2-9] $B/$n.wret $B/$n.wret[2-9]
  sed 's/\r$//' $W/$n.wdiag > $B/$n.wdiag
  echo "=== $n  (diag $(wc -c < $B/$n.wdiag) bytes)"; [ -s $B/$n.wdiag ] && cat $B/$n.wdiag
  for o in $W/$n.wout $W/$n.wout[2-9]; do
    [ -f "$o" ] || continue
    s=${o##*.wout}
    iconv -f gbk -t utf-8 "$o" | sed 's/\r$//' > $B/$n.wout$s
    tr -d ' \r' < $W/$n.wret$s > $B/$n.wret$s
    echo "--- run${s:-1} (返回值 $(cat $B/$n.wret$s))"; head -40 $B/$n.wout$s
  done
done
