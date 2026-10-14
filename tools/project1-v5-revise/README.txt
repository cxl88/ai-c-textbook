项目一 v5 修订脚本（2026-10-12）
底稿：作者批注稿 搭建个人专属档案.docx（WPS 另存）。
build.sh：解包 → merge_runs → edit.py（全部改动）→ replies.py（批注回复）→ 打包、校验 → clean.py（清洁版）→ LibreOffice 渲染。
fig/：mkfigs.py 生成新图 HTML，shot.js 用 Playwright 截图；anim.py 生成预处理动画帧（再用 ffmpeg 合成）。
harn/：在 Linux 下按预设按键运行 snake.c 的绘图代码，截取图1-6 的画面。
依赖：docx 技能脚本（merge_runs、comment、validate）、book4/style.css 与 fonts/、Playwright、ffmpeg、python-docx。
图1-5 照片（2026-10-12 第二次修订）：edit.py 第三个参数 ph/ 是照片目录（p_auto/p_pv/p_robot/p_uav/p_cnc/p_sys.jpg），来源与许可见配套资源包“图1-5实物照片/图片来源与许可.txt”；term.sh 在 Xvfb 下用 xterm 截取系统软件一格的终端截图。
