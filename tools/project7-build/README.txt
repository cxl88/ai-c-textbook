项目七生成脚本（初稿，2026-11-17）
底稿：客户框架 docs/requirements/7项目七 构建批量信息数组.docx（8 条批注）。
以项目一 v5 清洁版 docx 为版式模板：p3lib.py（与项目六初稿相同，含 switch/case/break/default/continue 的高亮）复制各类版式块，换上新内容。
content7.py：正文（改书稿就改这里）；图、表、例题按出现顺序自动编号（FIGS/TABS/EXS），正文用 fg()/tb()/ex() 引用，写出 fig/nums.json。
  数据表格设为表头行跨页重复、行不拆分，8 行以内的短表整表不跨页；题干与后面的程序框同页（kn）。
figs7.py（载入 base4.py）：16 幅插图（HTML/SVG，shot.js 截成 4 倍图）；图中的电压、状态与程序的测试数据相同。
cons7.py：由实测输出 .wout 拼出运行结果截图：把 .in 中的各行依次插在输出中各个“提示”（全角冒号“：”）的后面，并加下划线。
notes7.py《编写说明与参考答案》：答案中的运行结果、书中引用的编译器提示都从实测记录读取并断言核对，不符时报错，不会生成文档。
audit7.py《师生体验审计与优化说明》；res7.py 配套资源 zip（学生用/教师用分组、待补充练习、程序验证记录、插图原图、图片许可）。
wrun.sh：与项目六相同，另外把键盘输入 .in 在运行时由 UTF-8 转为 GBK——与在运行窗口中用中文输入法输入汉字时程序读到的字节相同
  （任务四要输入“支路正常”等汉字状态文本）。项目七没有死循环程序，wcap.sh 未使用（保留以便后续项目沿用）。
程序：code/project07/book（书中程序 41 个），code/project07/check（答案核对、参考答案、错误示范 46 个）。
  注意：程序名不要以 if_、for_ 等 cmd 内部命令开头——wrun.sh 生成的批处理会把它们当作命令解析出错。

重新生成（在 home-server 的生成环境容器中运行，见 tools/build-env/；仓库挂载为 /work）：
  1. 改了程序后重跑（check 目录同理）：
     tools/build-env/run.sh bash -c 'cd code/project07/book && CODE_DIR=$PWD bash /work/tools/project7-build/wrun.sh $(ls *.c | sed "s/\.c$//")'
     tools/build-env/run.sh bash -c 'cd code/project07/check && CODE_DIR=$PWD bash /work/tools/project7-build/wrun.sh $(ls *.c | sed "s/\.c$//")'
  2. 一键生成：tools/build-env/run.sh bash -c 'cd tools/project7-build && FIGS=1 bash build7.sh'
     输出在 build/：p7.docx 清洁版、p7.pdf 预览（LibreOffice 渲染）、notes7.docx、audit7.docx、res7.zip。
  3. 检查注释对齐：python3 tools/cmtchk.py build/p7.pdf （应输出 groups off by >2.5pt: 0）
依赖：python3（lxml、Pillow、python-docx、pypdf）、Node + Playwright、LibreOffice Writer、Noto Sans CJK 字体（生成环境容器中都已安装）。
