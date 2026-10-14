项目三生成脚本（第二稿，2026-10-14）
以项目一 v5 清洁版 docx 为版式模板：p3lib.py 复制其中各类版式块（标题、正文、代码框、AI 卡片、课堂验收等）换上新内容，保证与 v5 样式一致；第二稿新增“趣味小站”“课堂活动”两种框（沿用 v5 的提示框和课堂练习框，换彩色图标）。
content.py：正文（改书稿就改这里）；图表编号按出现顺序自动生成，正文用 fg()/tb() 引用，并写出 fig/nums.json 供 notes.py、audit.py 使用。
figs.py：流程图与插图（HTML/SVG，shot.js 用 Playwright 截图），末尾载入 figs_new.py（第二稿重画和新增的图）。
cons.py：由实测输出 .wout 拼出运行结果截图。
build.sh 一键：插图 → 运行截图 → 生成 docx → LibreOffice 渲染预览 PDF。
notes.py 生成《编写说明与参考答案》，audit.py 生成《师生体验审计与优化说明》：python3 notes.py 输出.docx fig/nums.json
assets/fe：Microsoft Fluent Emoji 3D 图标（MIT 许可，见目录内 LICENSE）；assets/ud：unDraw 插画（主色已改为 #1D4F91，许可见目录内说明）。
程序验证：wrun.sh（Wine + 小熊猫C++ 3.4 自带 GCC 11.5.0，路径见脚本开头）。
依赖：python3（lxml、Pillow、python-docx）、Node + Playwright、LibreOffice Writer、Noto Sans CJK 字体。
