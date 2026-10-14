#!/bin/bash
# Linux GCC check: compile + run every .c; save .out (program output) and .diag (compiler messages)
cd "$(dirname "$0")"
for f in *.c; do
  n=${f%.c}
  gcc -std=c11 -Wall -fdiagnostics-color=never -o /tmp/lx_$n $f -lm 2> $n.lxdiag
  rc=$?
  if [ $rc -eq 0 ] && [[ $n != bad_* || $n == bad_lab_run ]]; then
    if [ -f $n.in ]; then /tmp/lx_$n < $n.in > $n.lxout; else /tmp/lx_$n > $n.lxout; fi
    echo "OK $n (diag lines: $(wc -l < $n.lxdiag))"
  else
    echo "FAILED-COMPILE $n rc=$rc"
  fi
done
