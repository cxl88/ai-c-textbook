项目四生成脚本（初稿，2026-10-15）
以项目一 v5 清洁版 docx 为版式模板：p3lib.py 复制其中各类版式块（标题、正文、代码框、AI 卡片、课堂验收等）换上新内容，与项目三第二稿同一套体例和栏目。
content4.py：正文（改书稿就改这里）；图、表、例题编号按出现顺序自动生成，正文用 fg()/tb()/ex() 引用，并写出 fig/nums.json 供 notes4.py、audit4.py、res4.py 使用。
figs4.py（载入 base4.py）：插图（HTML/SVG，shot.js 用 Playwright 截图）；cons4.py：由实测输出 .wout 拼出运行结果截图。
build.sh 一键：插图 → 运行截图 → 生成 docx → LibreOffice 渲染预览 PDF。用法：bash build.sh <code/project04/book 的绝对路径>
  build.sh 生成两份 docx：build/p4.docx 交付用；build/pv/p4.docx 只把代码行尾注释前的空格按 LibreOffice 的替代字体重算，用来渲染预览 PDF。
  代码排版：英文 Consolas 9 磅、汉字微软雅黑 10 磅，注释前的空格按字宽重算（p3lib.py 的 book_split，参数 CODE_LATIN_EM）；20 行以内的程序整段排，更长的只在空行处分段，每段至少 8 行。
notes4.py 生成《编写说明与参考答案》，audit4.py 生成《师生体验审计与优化说明》：python3 notes4.py 输出.docx fig/nums.json
配套资源：python3 prep_pack.py <book 目录> <check 目录> <新目录>（分 4 组整理 59 个程序）→ CODE_DIR=<新目录> bash wrun.sh <程序名…> → python3 res4.py <新目录> fig 输出.zip
tools/cmt.py：按编辑器列宽（汉字占 2 列）检查、对齐源程序的行尾注释；tools/cmtchk.py：检查预览 PDF 中的行尾注释是否对齐。
assets/fe：本项目用到的 Microsoft Fluent Emoji 3D 图标（MIT 许可，见目录内 LICENSE）；assets/ud：unDraw 插画 3 幅（主色已改为 #1D4F91，许可见目录内说明）。
程序验证：wrun.sh（Wine + 小熊猫C++ 3.4 自带 GCC 11.5.0，路径见脚本开头）。改了程序要先用 wrun.sh 重跑，运行结果截图由实测输出生成。
依赖：python3（lxml、Pillow、python-docx、pdfplumber）、Node + Playwright、LibreOffice Writer、Noto Sans CJK 字体。
