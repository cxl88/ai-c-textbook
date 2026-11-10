项目四 开发顺序交互程序：程序与实测输出（小熊猫C++ 3.4 自带 GCC 11.5.0，Wine 中运行）
book/   书中直接引用的程序：14 个例题、ledger.c、ledger2.c、fix_scanf.c、技能训练和实训巩固的参考程序、fix_line.c，以及书中引用编译提示的错误示范（bad_ 开头）。tools/project4-build/build.sh 读这个目录。
check/  核对答案用的程序（cp*、q*、signin2 等）、fix_twice.c，以及其余错误示范。
.in/.in2… 为键盘输入；.wout/.wret/.wdiag 为实测输出、返回值和编译提示（bad_ 开头的程序只编译不运行）。
配套资源压缩包中的分组和改名（书中示例、参考答案、答案核对 hd_*、错误示范）由 tools/project4-build/prep_pack.py 生成。
