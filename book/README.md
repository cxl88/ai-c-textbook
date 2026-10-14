# 排版源文件（印刷版，项目一～项目二）

由本文件夹可以重新生成《人工智能助力C语言程序设计-第一至二章-印刷版.pdf》以及印刷分文件。

## 规格

- 成品尺寸 185 mm × 260 mm（正度 16 开），四边出血 3 mm，PDF 页面 191 mm × 266 mm；TrimBox / BleedBox 已写入每一页。
- 版心 148 mm × 219 mm；从成品边算起，订口 20 mm、切口 17 mm、天头 21 mm、地脚 20 mm；正文 10.5 pt 思源宋体（Noto Serif SC），标题思源黑体（Noto Sans SC），代码 JetBrains Mono。
- 用色：主色深蓝 #1D4F91 及其深浅色，加黑、灰。PDF 为 RGB，交印刷厂前需由印厂转 CMYK 并出数码样确认。
- 项目首页和附录从右页（奇数页）起排；前置部分页码用罗马数字，正文页码从 1 开始；全书为偶数页。

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
| code/ | 书中全部程序（.c）、自动输入（.in）、在 Windows 版 GCC 中实际运行得到的结果（.wout）和编译器提示（.wdiag） |
| img/ | 小熊猫C++ 界面截图（已裁切） |
| build.py | 组装 HTML → Chromium 打印 PDF → 读回页码填目录和“见第×页” → 加封面、写页面框和书签 |
| render.js / check.js | Chromium 打印；检查是否有内容溢出版心 |
| gaps.py / sheet.py | 排版检查：统计每页底部空白；生成缩略图 |
| wrun.sh | 用小熊猫C++ 自带的 MinGW-w64 GCC 11.5.0（在 Wine 中）编译运行 code/ 下的程序，更新 .wout / .wdiag |
| prep_img.py | 从原始截图裁切出 img/ 中的图片（原始截图未随附） |

## 生成方法

1. 安装 Python 3（pypdf、Pillow）、Node.js 与 Playwright（Chromium）、poppler-utils（pdftotext、pdftoppm）。
2. 按 fonts-list.txt 下载字体，放在本文件夹上一级的 fonts/ 目录中（即 `../fonts/`）。
3. 运行 `python3 build.py`，输出在 out/：
   - book.pdf：完整版（封面 + 封二空白 + 前置部分 + 正文）
   - interior.pdf：内文（交印刷厂）
   - cover_print.pdf：封面（交印刷厂）
4. 改稿后建议运行 `node check.js out/body.html`（应显示 OK）和 `python3 gaps.py out/body.pdf 30`。
5. 修改了程序后，用 wrun.sh 重新运行（需要 Wine 和小熊猫C++，路径在脚本开头），书中的运行窗口会自动使用新结果。

## 自定义标签（在 parts/*.html 中使用）

- `<code-file src="x.c" title="…" ln/>`：插入 code/x.c，带行号；加 `bad` 表示含错误的灰底代码。
- `<snip title="…">…</snip>`：插入一段代码。
- `<conwin src="x" dir="project02" ins="提示|输入"/>`：按 x.wout 画 Windows 运行窗口，`ins` 中的输入内容加下划线；`notrailer` 表示不画最下面的“进程退出……”。
- `<out src="x"/>`、`<diag src="x"/>`：运行结果框、编译器提示框。
- `<tocmark level="1|2" text="…" odd="1"/>`：目录项（odd 表示必须从右页起排）；`<anchor id="…"/>` 与 `<pref to="…"/>`：自动页码引用。
