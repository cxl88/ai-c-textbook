#!/bin/bash
cd "$(dirname "$0")/tdir"
P=$'\e[1;32mstudent@lab\e[0m:\e[1;34m~\e[0m$ '
run(){ printf '%s%s\n' "$P" "$1"; eval "$1"; }
clear
run 'uname -sr'
run 'sqlite3 --version | cut -d" " -f1'
run 'python3 -VV'
run 'gcc hello.c -o hello && ./hello'
printf '%s' "$P"
sleep 30
