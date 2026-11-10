# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目性质

《人工智能助力C语言程序设计》（冯丽娜 编著）教材的排版与生成工程，不是软件产品。仓库里的“代码”分两类：书中的 C 示例程序，以及把书稿生成为印刷 PDF / Word 的 Python、Node 脚本。成品 PDF、docx、zip 不进 git（见 `.gitignore`），放 GitHub Releases；`docs/**/*.docx`（客户章节模板、修改意见）例外，入库。各章进度与版本对应提交见 `README.md`。

## 三条并存的生成流水线

各章所处阶段不同，用的工具链也不同，改哪一章先确认它在哪条线上：

1. **`book/`：HTML → PDF 印刷版（v4，项目一、项目二、附录A）**
   `parts/*.html` 写正文 → `build.py` 预处理（代码高亮、运行窗口、自动编号、不换行空格）→ `render.js` 用 Playwright/Chromium 打印 → `pdftotext` 读回页码，回填目录和“详见第×页”，保证项目首页落在奇数页 → pypdf 写 TrimBox/BleedBox、书签、合并封面 → 另出电子阅读版。新增章节要把文件名加进 `build.py` 的 `BODY_PARTS`。
2. **`tools/project1-v5-revise/`、`tools/project3-build/`：直接生成 Word（v5 起的新稿）**
   项目一 v5 是在作者批注稿 docx 上用脚本修订；项目三以项目一 v5 清洁版 docx 为版式模板，`p3lib.py` 复制模板里的版式块（标题、正文、代码框、AI 卡片等）再填新内容。改项目三书稿改 `content.py`（图表编号按出现顺序自动生成，用 `fg()`/`tb()` 引用）；插图在 `figs.py`/`figs_new.py`（HTML/SVG，`shot.js` 截图），运行截图由 `cons.py` 从 `.wout` 拼出。v5 的项目一尚未并回 `book/parts/`。
3. **`tools/word-export/`：从 `book/` 的排版结果反向生成可编辑 Word（v4）**。Word 只是副本，改稿以排版源文件为准。

## 常用命令

```bash
# 字体（不入库，style.css 以 ../fonts/ 引用）
cd fonts && while read name url; do curl -sSfL -o "$name" "$url"; done < fonts-list.txt

# 印刷版完整构建，输出 book/out/：book.pdf、interior.pdf、cover_print.pdf、ebook.pdf
cd book && python3 build.py
# 快速试排指定部分（不回填目录页码），输出 out/test.pdf
python3 build.py test 20_ch2a.html

# 改稿后的排版检查
node check.js out/body.html          # 内容是否溢出版心，应显示 OK
python3 gaps.py out/body.pdf 30      # 每页底部空白
python3 splitcheck.py                # 长表格、长程序在哪里跨页
python3 widths.py                    # 程序行宽不超出版心

# 重跑示例程序（需 Wine + 小熊猫C++，路径写死在脚本开头 /root/cstudy/wb、/root/.wine64b）
bash wrun.sh club zone               # 参数是不带 .c 的程序名；CODE_DIR 改目录，WEXTRA=-Wconversion 附加选项

# 项目三 Word + 预览 PDF（参数为程序目录，默认 /root/cstudy/p3code；仓库内对应 code/project03/ 的 examples 与 answers）
bash tools/project3-build/build.sh <程序目录>
```

依赖：Python 3（pypdf、Pillow；项目三另需 lxml、python-docx）、Node（环境里在 `/opt/node22`）+ Playwright、poppler-utils、LibreOffice Writer。资源包 `book/pack.py` 的完整流程（三个重跑目录、版本号 `VER`/`VER_TAG`/`BOOK_VER` 须与书中“本书使用说明·5. 配套资源”同步）见 `book/README.md`。

注意：`tools/project3-build/build.sh` 引用的 v5 模板 docx（`/mnt/project-files/...`）、`/root/cstudy/` 下的 Wine 工作目录都不在仓库里，当前环境不一定有。

## 程序与运行结果的约定

- 书中出现的每个运行结果、编译提示都来自实测：`x.c` 配 `x.in`（键盘输入，`.in2`… 为多次运行），`wrun.sh` 用 Windows 版 MinGW-w64 GCC 11.5.0（小熊猫C++ 3.4 默认 Debug 配置，`-fexec-charset=gbk`）跑出 `.wout`/`.wret`/`.wdiag`（UTF-8 存回）。**不要手写或手改这些结果文件**；改了 `.c` 必须重跑，排版会自动用新结果。无法重跑时要明说。
- `bad_` 开头的程序含编译错误或未定义行为，只编译不运行；`wc_` 开头的是加 `-Wconversion` 的补充验证结果。
- `book/check/` 是为核对参考答案改动过一处的程序，进入程序验证记录的“补充验证”。
- 示例头文件尽量只用 `stdio.h`、`math.h`、`string.h`（`code/project01-v5/snake.c` 仅 Windows，展示用）。

## `book/parts/*.html` 自定义标签

- `<code-file src="x.c" title="…" ln/>` 插入 `code/x.c`（`ln` 行号，`bad` 灰底错误代码）；`<snip title="…">…</snip>` 内联代码。
- `<conwin src="x" ins="提示|输入"/>` 按 `x.wout` 画 Windows 运行窗口，`ins` 里的输入加下划线（多个用 `;;` 分隔，提示文字必须在输出中能找到）；`notrailer` 不画“进程退出”行。
- `<out src="x"/>`、`<diag src="x"/>` 运行结果框、编译器提示框。
- `<tocmark level="1|2" text="…" odd="1"/>` 目录项；`<anchor id="…"/>` + `<pref to="…"/>` 自动页码引用。
- `⟦图…⟧`、`⟦表…⟧`、`⟦例…⟧` 自动编号：写在 `<b>` 中是定义（图题、表题），其余是引用。

## 版式硬性规格（改排版时不可破坏）

- 成品 185×260 mm，四边出血 3 mm（PDF 191×266 mm）；正文 Noto Serif SC 10.5 pt，代码 JetBrains Mono 约 9 pt；主色 #1D4F91 加黑灰；PDF 为 RGB，由印厂转 CMYK（2026-10-14 已确认按四色印刷，项目三第二稿的彩色图标、插画可原样使用）。
- 代码跨页（`build.py` 的 `LONG_CODE`/`MIN_CHUNK`/`LONG_TABLE`）：20 行以内的程序和“待补充”“待诊断”练习整段不跨页；21 行以上只在空行处分页、每段至少 8 行，续页加“文件名（续）”；**排不下就移页，不靠缩小字号**。少于 5 行的表格和供填写的表格不跨页。
- 项目首页、附录从奇数页起；全书偶数页。

## 体例

读者是基础弱的大一学生：通俗、贴近生活、任务融合知识点。每个项目：项目首页 → 情境导入 → 三维目标 → 知识导图 → 任务（描述/分析/相关知识/课堂练习/实施/技能训练）→ 项目小结 → AI 升华；v3 起加“学习分层”“课堂验收”“离开 AI 再做”。人物固定为新生小禾、林老师、AI 助教小智。客户给的各章框架在 `docs/requirements/`，历次修订说明在 `docs/history/`。
