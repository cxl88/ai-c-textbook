项目六生成脚本（初稿，2026-11-15）
底稿：客户框架 docs/requirements/6项目六 编写重复操作流程.docx（5 条批注）。
以项目一 v5 清洁版 docx 为版式模板：p3lib.py（与项目五初稿相同，含 switch/case/break/default 的高亮）复制各类版式块，换上新内容。
content6.py：正文（改书稿就改这里）；图、表、例题按出现顺序自动编号（FIGS/TABS/EXS），正文用 fg()/tb()/ex() 引用，写出 fig/nums.json。
  数据表格设为表头行跨页重复、行不拆分，8 行以内的短表整表不跨页；题干与后面的程序框同页（kn）。
figs6.py（载入 base4.py）：16 幅插图（HTML/SVG，shot.js 截成 4 倍图）。
cons6.py：由实测输出 .wout 拼出运行结果截图：把 .in 中的各行依次插在输出中各个“提示”的后面，并加下划线；
  任务二、三的输出本身含“状态：”，所以提示按程序给出正则（PROMPT）。停不下来的程序用限时运行记录 .wcap 截取开头几行（CAPS）。
notes6.py《编写说明与参考答案》：答案中的运行结果从实测输出（死循环取限时运行记录）读取并断言核对，不符时报错，不会生成文档。
audit6.py《师生体验审计与优化说明》；res6.py 配套资源 zip（学生用/教师用分组、待补充练习、程序验证记录、插图原图、图片许可）。
wcap.sh：限时运行“停不下来”的程序（默认 5 秒后强制结束），保存开头的输出 .wcap 和运行记录 .wcapret，作为死循环的实测依据。
程序：code/project06/book（书中程序 34 个），code/project06/check（答案核对、参考答案、错误示范 38 个）。
  注意：程序名不要以 if_、for_ 等 cmd 内部命令开头——wrun.sh 生成的批处理会把它们当作命令解析出错。

重新生成（在 home-server 的生成环境容器中运行，见 tools/build-env/；仓库挂载为 /work）：
  1. 改了程序后重跑（check 目录同理）；死循环要在同一个容器中接着用 wcap.sh 限时运行（容器用完即删，可执行文件不保留）：
     tools/build-env/run.sh bash -c 'cd code/project06/book && CODE_DIR=$PWD bash /work/tools/project6-build/wrun.sh $(ls *.c | sed "s/\.c$//") && CODE_DIR=$PWD bash /work/tools/project6-build/wcap.sh bad_wsemi lamp1 ai_a'
     tools/build-env/run.sh bash -c 'cd code/project06/check && CODE_DIR=$PWD bash /work/tools/project6-build/wrun.sh $(ls *.c | sed "s/\.c$//") && CODE_DIR=$PWD bash /work/tools/project6-build/wcap.sh bad_nobrace bad_wcont'
     限时运行的输出行数每次略有不同；notes6.py 核对书中“120 多万行”“80 多万行”的说法，超出范围时要改正文。
  2. 一键生成：tools/build-env/run.sh bash -c 'cd tools/project6-build && FIGS=1 bash build6.sh'
     输出在 build/：p6.docx 清洁版、p6.pdf 预览（LibreOffice 渲染）、notes6.docx、audit6.docx、res6.zip。
  3. 检查注释对齐：python3 tools/cmtchk.py build/p6.pdf （应输出 groups off by >2.5pt: 0）
依赖：python3（lxml、Pillow、python-docx、pypdf）、Node + Playwright、LibreOffice Writer、Noto Sans CJK 字体（生成环境容器中都已安装）。
