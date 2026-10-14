项目三生成脚本（2026-10-14）
以项目一 v5 清洁版 docx 为版式模板：p3lib.py 复制其中各类版式块（标题、正文、代码框、AI 卡片、课堂验收等）换上新内容，保证与 v5 样式一致。
content.py：正文（改书稿就改这里）；figs.py：流程图与插图（HTML/SVG，shot.js 用 Playwright 截图）；cons.py：由实测输出 .wout 拼出运行结果截图。
build.sh 一键：插图 → 运行截图 → 生成 docx → LibreOffice 渲染预览 PDF。notes.py 生成《编写说明与参考答案》。
程序验证：wrun.sh（Wine + 小熊猫C++ 3.4 自带 GCC 11.5.0，路径见脚本开头）。
依赖：python3（lxml、Pillow、python-docx）、Node + Playwright、LibreOffice Writer、Noto Sans CJK 字体。
