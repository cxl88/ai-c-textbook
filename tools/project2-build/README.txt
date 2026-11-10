项目二生成脚本（修订稿，2026-10-19）
底稿为作者冯丽娜的新稿（docs/author-drafts/2项目二 读懂身边多样数据（作者新稿，含批注）.docx），按其中 16 条批注修订。
以项目一 v5 清洁版 docx 为版式模板：p3lib.py 复制其中各类版式块（标题、正文、代码框、AI 卡片、课堂验收等）换上新内容，与项目三第二稿、项目四同一套体例和栏目。
content2.py：正文（改书稿就改这里）；图、表、例题编号按出现顺序自动生成，正文用 fg()/tb()/ex() 引用，并写出 fig/nums.json 供 notes2.py、audit2.py、res2.py 使用。
figs2.py（载入 base4.py）：插图（HTML/SVG，shot.js 用 Playwright 截图）；cons2.py：由实测输出 .wout 拼出运行结果截图；author_fig/：取自作者新稿的 3 幅插图（图2-5～图2-7）。
pack2.py：打包 docx，加奇数页页眉“项目二 读懂身边多样数据”、首页不显示页眉，并把模板样式表中元素的顺序调成 OOXML 规定的顺序（模板经 WPS 保存后顺序不对，校验不过）。
replies2.py：放回作者 16 条原批注（author_comments.xml，取自作者新稿）并逐条加回复，生成带批注回复版；用到 docx 技能的 comment.py 和 office/validate.py（/mnt/skills/public/docx/scripts）。
notes2.py 生成《修改意见与处理说明（含参考答案）》，audit2.py 生成《师生体验审计与优化说明》，res2.py 生成配套资源 zip（程序分 4 组：书中程序、参考答案、答案核对、错误示范 bad_）。
build2.sh 一键：插图和运行截图（fig/ 里没有图或设 FIGS=1 时）→ 清洁版、带批注回复版 docx → LibreOffice 渲染预览 PDF → 校验 → 修改意见、审计说明、配套资源。
  用法：bash build2.sh [程序目录的绝对路径]，默认 ../../code/project02；版式模板路径用环境变量 V5 指定（默认是项目文件夹中的 v5 清洁版）。输出在 build/。
  预览 PDF 另用一份 docx 渲染，只把代码行尾注释前的空格按 LibreOffice 的替代字体重算（CODE_LATIN_EM=0.602），其余与清洁版相同。
tools/cmt.py：按编辑器列宽（汉字占 2 列）检查、对齐源程序的行尾注释；tools/cmtchk.py：检查预览 PDF 中的行尾注释是否对齐（应输出 groups off by >2.5pt: 0）。
assets/fe：本项目用到的 Microsoft Fluent Emoji 3D 图标（MIT 许可，见目录内 LICENSE）。
程序验证：CODE_DIR=<程序目录> bash wrun.sh <程序名…>（Wine + 小熊猫C++ 3.4 自带 GCC 11.5.0，路径见脚本开头；bad_ 开头的只编译）。改了程序要先重跑，再 FIGS=1 bash build2.sh。
依赖：python3（lxml、Pillow、python-docx、pdfplumber）、Node + Playwright、LibreOffice Writer、Noto Sans CJK 字体。
