项目三第三稿生成脚本（2026-10-28，底稿为作者冯丽娜的项目三修改稿，按 16 条批注修订）
作者原稿在 docs/author-drafts/，修改意见与处理说明在 docs/history/。第二稿的脚本在 tools/project3-build/，未改动。

以项目一 v5 清洁版 docx 为版式模板：p3lib.py 复制其中各类版式块（标题、正文、代码框、AI 卡片、课堂验收、趣味小站等）换上新内容。
content3.py：正文（改书稿就改这里）；图、表、例题按出现顺序自动编号（FIGS/TABS/EXS 列表），正文用 fg()/tb()/ex() 引用，写出 fig/nums.json；A(批注号, 段落) 标出作者 16 条批注的锚点。
figs.py：流程图与插图（HTML/SVG，shot.js 用 Playwright 截成 4 倍图），末尾载入 figs_new.py（第二、三稿重画和新增的图）。
cons3.py：由实测输出 .wout 拼出运行结果截图，键盘输入加下划线。
replies3.py：把作者的 16 条原批注（author_comments.xml）放回带批注回复版，并在每条下面挂一条回复。
notes3.py《修改意见与处理说明（含参考答案）》，audit3.py《师生体验审计与优化说明》，res3.py《配套资源》压缩包。
tools/cmt.py：按编辑器列宽（汉字占 2 列）对齐源程序的行尾注释；tools/cmtchk.py：检查预览 PDF 中行尾注释是否对齐。
wrun.sh：在 Wine 中用小熊猫C++ 3.4 自带的 GCC 11.5.0 编译运行程序（编译选项与默认 Debug 配置相同），路径见脚本开头。
assets/fe：Microsoft Fluent Emoji 3D 图标（MIT 许可）；assets/ud：unDraw 插画（主色已改为 #1D4F91），许可见各目录。

重新生成（Linux；python3 与 lxml、Pillow、python-docx，Node + Playwright，LibreOffice，Noto Sans CJK 字体）
  0. 程序放到同一个目录：mkdir -p /tmp/p3code && cp ../../code/project03/examples/* ../../code/project03/answers/* /tmp/p3code/
     改了程序后重新运行：CODE_DIR=/tmp/p3code bash wrun.sh <程序名…>   （生成 .wdiag/.wout/.wret）
  1. 插图：mkdir -p fig && cp -r assets fig/ && python3 figs.py && node shot.js fig/figs.html fig <图的 id…>
     运行结果图：python3 cons3.py /tmp/p3code && node shot.js fig/cons.html fig <上一步打印的 id…>
  2. 全部文档：bash build3.sh /tmp/p3code   （模板路径写在 build3.sh 中）。输出在 build/：
     p3.docx 清洁版、p3c.docx 带批注回复版、p3.pdf 预览、notes3.docx、audit3.docx、res3.zip。
     预览 PDF 另用一份按 LibreOffice 替代字体重算注释空格的 docx 生成，与清洁版只差代码注释前的空格个数。
     批注回复用到 docx 技能中的 comment.py 和 office/validate.py（/mnt/skills/public/docx/scripts）。
  3. 检查注释对齐：python3 tools/cmtchk.py build/p3.pdf   （应输出 groups off by >2.5pt: 0）
