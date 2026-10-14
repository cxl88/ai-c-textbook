# 排版源文件（第四版 v4，项目一～项目二）

由本文件夹可以重新生成 v4 的印刷版 PDF、印刷分文件、电子阅读版，以及配套资源包和程序验证记录。

## 规格

- 成品尺寸 185 mm × 260 mm（正度 16 开），四边出血 3 mm，PDF 页面 191 mm × 266 mm；TrimBox / BleedBox 已写入每一页。
- 版心 148 mm × 219 mm；从成品边算起，订口 20 mm、切口 17 mm、天头 21 mm、地脚 20 mm；正文 10.5 pt 思源宋体（Noto Serif SC），标题思源黑体（Noto Sans SC）。
- 代码：中文 10.8 pt，英文等宽字 JetBrains Mono 按 83.34% 缩放，实际约 9 pt（小五号）；运行窗口 10 pt。程序行不超出版心（widths.py 检查）。
- 用色：主色深蓝 #1D4F91 及其深浅色，加黑、灰。PDF 为 RGB，交印刷厂前需由印厂转 CMYK 并出数码样确认。
- 项目首页和附录从右页（奇数页）起排；前置部分页码用罗马数字，正文页码从 1 开始；全书为偶数页。
- 跨页规则（build.py 开头的 LONG_CODE、MIN_CHUNK、LONG_TABLE）：20 行以内的程序和待补充、待诊断的练习整段不跨页（排不下就整段移到下一页，不缩小字号）；21 行以上的程序只在空行处（程序的段落之间）分页，每段至少 8 行，排到新页开头的段自动加“文件名（续）”；少于 5 行的表格和供填写的表格不跨页，长表跨页时表头重复、两边各至少 2 行。
- 正文中数字与单位（380 V）、“第 5 行”这类序数、简短算式之间自动改用不换行空格（build.py 的 keep_together）。

## 文件

| 路径 | 作用 |
| --- | --- |
| parts/00_front.html | 扉页、前言、本书使用说明、目录（目录由程序自动填页码） |
| parts/10_ch1.html | 项目一 |
| parts/20_ch2a.html、20_ch2b.html、20_ch2c.html | 项目二的任务一、任务二、任务三（含项目小结、AI 升华） |
| parts/90_appx.html | 附录A ASCII 字符集 |
| parts/cover.html | 封面（正封） |
| parts/defs.html | 小智、小禾、林老师头像和栏目图标（SVG） |
| style.css | 全书版式 |
| code/ | 书中全部程序（.c）、键盘输入（.in）、在 Windows 版 GCC 中实际运行得到的结果（.wout/.wret）和编译器提示（.wdiag）；wc_ 开头的是加 -Wconversion 的补充验证结果 |
| img/ | 小熊猫C++ 界面截图（已裁切、局部放大） |
| build.py | 组装 HTML → Chromium 打印 PDF → 读回页码填目录和“第×页” → 加封面、写页面框和书签 → 生成电子阅读版 |
| pack.py | 生成配套资源包（学生用、教师用）、版本说明和程序验证记录 |
| teacher_doc.py | 生成教师用《参考答案与评分说明》（A4 PDF，由 pack.py 调用；页码、图表编号和程序结果都从排好的正文和运行结果中读取） |
| check/ | 为核对参考答案而改动过一处的程序（如年龄改为 19、输入 Z、输入结束）及其运行结果，进入程序验证记录的“补充验证” |
| render.js / check.js | Chromium 打印；检查是否有内容溢出版心 |
| gaps.py / splitcheck.py / widths.py / sheet.py | 排版检查：每页底部空白；长表格、长程序在哪里跨页；程序行宽；缩略图 |
| wrun.sh | 用小熊猫C++ 3.4 自带的 MinGW-w64 GCC 11.5.0（在 Wine 中）编译运行程序，更新 .wout / .wret / .wdiag |
| prep_img.py | 从原始截图裁切出 img/ 中的图片（原始截图未随附） |

## 生成方法

1. 安装 Python 3（pypdf、Pillow）、Node.js 与 Playwright（Chromium）、poppler-utils（pdftotext、pdftoppm）。
2. 按 fonts-list.txt 下载字体，放在本文件夹上一级的 fonts/ 目录中（即 `../fonts/`）。
3. 运行 `python3 build.py`，输出在 out/：
   - book.pdf：完整版（封面 + 封二空白 + 前置部分 + 正文）
   - interior.pdf：内文（交印刷厂）
   - cover_print.pdf：封面（交印刷厂）
   - ebook.pdf：电子阅读版（裁去出血、去掉空白页，目录和“第×页”可点击，页码标签与印刷版一致）
4. 改稿后运行 `node check.js out/body.html`（应显示 OK）、`python3 gaps.py out/body.pdf 30`、`python3 splitcheck.py`、`python3 widths.py`。
5. 修改了程序后，用 wrun.sh 重新运行（需要 Wine 和小熊猫C++，路径在脚本开头），书中的运行窗口会自动使用新结果。
6. 资源包与程序验证记录：把 code/ 中的 .c、.in 文件复制到一个新目录，用 `CODE_DIR=该目录 bash wrun.sh 程序名…` 全部重新运行；
   再把 convert、fix205、lab_draft2、overflow 复制到另一个目录，用 `WEXTRA=-Wconversion` 运行；
   再把 check/ 中的 .c、.in 文件复制到第三个目录，同样用 wrun.sh 全部运行；
   然后 `python3 pack.py 第一个目录 第二个目录 第三个目录`，输出在 out/pack/（pack.py 会先核对重新运行的结果与排版用的结果、check/ 中保存的结果是否一致）。
   资源版本号在 pack.py 开头的 VER、VER_TAG、BOOK_VER，书中“本书使用说明·5. 配套资源”写明了对应的版本，两处要一起改。

## 自定义标签（在 parts/*.html 中使用）

- `<code-file src="x.c" title="…" ln/>`：插入 code/x.c，带行号；加 `bad` 表示含错误的灰底代码。
- `<snip title="…">…</snip>`：插入一段代码（标题含“待补充”“待诊断”的练习不跨页）。
- `<conwin src="x" dir="project02" ins="提示|输入"/>`：按 x.wout 画 Windows 运行窗口，`ins` 中的输入内容加下划线；`notrailer` 表示不画最下面的“进程退出……”。
- `<out src="x"/>`、`<diag src="x"/>`：运行结果框、编译器提示框。
- `<tocmark level="1|2" text="…" odd="1"/>`：目录项（odd 表示必须从右页起排）；`<anchor id="…"/>` 与 `<pref to="…"/>`：自动页码引用。
- `⟦图…⟧`、`⟦表…⟧`、`⟦例…⟧`：自动编号；写在 `<b>` 中的是定义（图题、表题），其余是引用。
