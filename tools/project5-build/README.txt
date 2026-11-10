项目五生成脚本（初稿，2026-11-10）
底稿：客户框架 docs/requirements/5项目五 判断场景分支路径.docx（8 条批注，另附“综合示例要点”参考图）。
以项目一 v5 清洁版 docx 为版式模板：p3lib.py（取自项目二修订稿、项目三第三稿，另加 switch/case/break/default 的高亮）复制各类版式块，换上新内容。
content5.py：正文（改书稿就改这里）；图、表、例题按出现顺序自动编号（FIGS/TABS/EXS），正文用 fg()/tb()/ex() 引用，写出 fig/nums.json。
  数据表格设为表头行跨页重复、行不拆分，8 行以内的短表整表不跨页；题干与后面的程序框同页（kn）。
figs5.py（载入 base4.py）：17 幅插图（HTML/SVG，shot.js 截成 4 倍图）。
cons5.py：由实测输出 .wout 拼出运行结果截图：按顺序把 .in 中的各行插在输出中各个“：”的后面，并加下划线。
notes5.py《编写说明与参考答案》：答案中的运行结果从实测输出读取并断言核对，不符时报错，不会生成文档。
audit5.py《师生体验审计与优化说明》；res5.py 配套资源 zip（学生用/教师用分组、待补充练习、程序验证记录、插图原图、图片许可）。
程序：code/project05/book（书中程序 39 个），code/project05/check（答案核对、参考答案、错误示范 34 个）。
  注意：程序名不要以 if_ 开头——wrun.sh 生成的批处理中，“if exist if_x.exe ...”会被 cmd 当作 if 命令解析出错。

重新生成（在 home-server 的生成环境容器中运行，见 tools/build-env/；仓库挂载为 /work）：
  1. 改了程序后重跑（check 目录同理）：
     tools/build-env/run.sh bash -c 'cd code/project05/book && CODE_DIR=$PWD bash /work/tools/project5-build/wrun.sh $(ls *.c | sed "s/\.c$//")'
  2. 一键生成：tools/build-env/run.sh bash -c 'cd tools/project5-build && FIGS=1 bash build5.sh'
     输出在 build/：p5.docx 清洁版、p5.pdf 预览（LibreOffice 渲染）、notes5.docx、audit5.docx、res5.zip。
  3. 检查注释对齐：python3 tools/cmtchk.py build/p5.pdf （应输出 groups off by >2.5pt: 0）
依赖：python3（lxml、Pillow、python-docx、pypdf）、Node + Playwright、LibreOffice Writer、Noto Sans CJK 字体（生成环境容器中都已安装）。
