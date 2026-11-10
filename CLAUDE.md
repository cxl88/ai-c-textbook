# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目性质

教材《人工智能助力C语言程序设计》（冯丽娜 编著，面向零基础的大一 / 高职一年级学生）的源文件仓库，不是软件产品。“代码”分两类：书中的 C 示例程序，以及把书稿生成为印刷 PDF / Word 的 Python、Node 脚本。没有单元测试，验证靠实测程序输出和排版检查脚本。各章进度和版本对应提交见 [README.md](README.md)，HTML 排版规格和自定义标签见 [book/README.md](book/README.md)。

## 每个项目在哪条线上

改哪一章，先确认它的现行底稿在哪：

| 章节 | 现行稿 | 生成脚本（改正文改这里） | 程序目录 |
| --- | --- | --- | --- |
| 项目一 | v5.1 Word（v4 HTML 印刷版为旧稿） | `tools/project1-v5-revise/`（在作者批注稿 docx 上用 `edit.py` 修订，`p1fix.py` 为 v5.1 统一序号） | `book/code/`（v4）、`code/project01-v5/` |
| 项目二 | 修订稿 Word（v4 HTML 印刷版为旧稿） | `tools/project2-build/content2.py` | `book/code/`（v4）、`code/project02/` |
| 项目三 | 第三稿 Word | `tools/project3-build3/content3.py`（`project3-build/` 是第二稿，保留不改） | `code/project03/{examples,answers}/` |
| 项目四 | 初稿 Word | `tools/project4-build/content4.py` | `code/project04/{book,check}/` |
| 附录A | v4 HTML | `book/parts/90_appx.html` | — |

两类流水线：

1. **HTML → 印刷 PDF（`book/`，v4）**：`parts/*.html` 用自定义标签写正文，`build.py` 预处理（代码高亮、运行窗口、自动编号 `⟦图…⟧`、不换行空格）→ Playwright/Chromium 打印 → `pdftotext` 读回页码回填目录和“第×页”、保证项目首页在奇数页 → pypdf 写 TrimBox/BleedBox、书签、合封面，另出电子阅读版。新增部分要加进 `build.py` 的 `BODY_PARTS`。`tools/word-export/` 从它的输出反向生成可编辑 Word（只是副本）。v5 起的 Word 稿都还没有并回 `book/parts/`。
2. **docx 模板拼装（项目二～四）**：以项目一 v5 清洁版 docx 为版式模板，`p3lib.py` 复制模板里的版式块（标题、代码框、AI 卡片、课堂验收、趣味小站等）换上新内容。各项目目录结构相同：
   - `contentN.py` 正文；图/表/例题编号由 `FIGS`/`TABS`/`EXS` 列表按出现顺序生成，正文用 `fg()`/`tb()`/`ex()` 引用，**不要手写编号**；写出 `fig/nums.json` 供说明文档使用。`A(批注号, 段落)` 标作者批注锚点。
   - `figs*.py`（HTML/SVG）+ `shot.js` 截图；`consN.py` 由 `.wout` 拼出运行结果截图，键盘输入加下划线。
   - `repliesN.py`（有作者批注的稿子才有）放回作者原批注（`author_comments.xml`）并逐条回复；`notesN.py` 修改意见/编写说明（含参考答案），`auditN.py` 师生体验审计，`resN.py` 配套资源 zip。
   - 预览 PDF 用另一份 docx 渲染，只按 LibreOffice 替代字体重算代码注释前的空格（`CODE_LATIN_EM`），其余与清洁版相同。
   - **`p3lib.py` 在各目录各有一份副本，版本不同**（project2-build 与 project3-build3 相同，project4-build、project3-build 较旧）。改版式块只改当前项目那份，别顺手同步到别的项目。

## 常用命令

```bash
# 字体（不入库，style.css 以 ../fonts/ 引用）
cd fonts && while read name url; do curl -sSfL -o "$name" "$url"; done < fonts-list.txt

# 印刷版（在 book/ 下）
python3 build.py                     # 输出 out/book.pdf、interior.pdf、cover_print.pdf、ebook.pdf
python3 build.py test 20_ch2a.html   # 只试排指定部分，输出 out/test.pdf（不回填页码）
node check.js out/body.html          # 内容溢出版心，应输出 OK
python3 gaps.py out/body.pdf 30      # 页底空白
python3 splitcheck.py                # 长表格、长程序跨页位置
python3 widths.py                    # 程序行宽

# 实测示例程序（改了 .c 或 .in 后必须重跑）；参数是不带 .c 的程序名
CODE_DIR=<程序目录> bash wrun.sh 程序名…   # WEXTRA=-Wconversion 附加选项

# Word 稿（在对应 tools/ 目录下，细节见各目录 README.txt）
bash build2.sh [程序目录]            # 项目二，默认 ../../code/project02；FIGS=1 强制重画插图
bash build3.sh /tmp/p3code           # 项目三，先把 examples/ 和 answers/ 复制到同一目录
bash build.sh <code/project04/book 的绝对路径>   # 项目四
python3 tools/cmtchk.py build/pN.pdf # 行尾注释对齐，应输出 groups off by >2.5pt: 0
```

**环境限制**：脚本写死了 Linux 沙箱路径：`/opt/node22/lib/node_modules/playwright`、Wine 工作目录 `/root/cstudy/wb` 和 `/root/.wine64b`、v5 模板 `/mnt/project-files/textbook/v5/…（清洁版）.docx`、docx 技能脚本 `/mnt/skills/public/docx/scripts`。`wrun.sh` 需要 Wine 和小熊猫C++ 3.4。在本机 Windows 上通常跑不起来；改路径前先确认用户要在哪里运行，无法重跑时要明说。依赖：Python 3（pypdf、Pillow、lxml、python-docx、pdfplumber）、Node + Playwright、poppler-utils、LibreOffice Writer、Noto 字体。

## 示例程序的约定

- 每个 `x.c` 配实测结果：`x.wout`/`x.wret`（输出、返回值）、`x.wdiag`（编译器提示，空文件=无提示）；`x.in`、`x.in2`… 是键盘输入，对应 `.wout2`/`.wret2`…。书中运行窗口、结果框都取自这些文件，**不要手写或手改结果文件**，必须由 `wrun.sh` 实测生成。
- 编译选项与小熊猫C++ 默认“MinGW-w64 GCC 11.5.0 64-bit Debug”一致（`-fexec-charset=gbk`，输出再转回 UTF-8）。
- `bad_` 开头：含编译错误或未定义行为，只编译不运行；`wc_` 开头：加 `-Wconversion` 的补充验证结果。
- 核对参考答案用的改动版程序：v4 在 `book/check/`，项目四在 `code/project04/check/`。配套资源包里的分组和改名由各项目的 `res*.py` / `prep_pack.py` 生成，仓库里不按资源包结构存放。
- 示例头文件尽量只用 `stdio.h`、`math.h`、`string.h`（`code/project01-v5/snake.c` 仅 Windows，展示用）。
- `<conwin ins="…">` 中多个输入用 `;;` 分隔，提示文字必须能在输出中找到。

## 版式硬性规格

- 成品 185×260 mm，四边出血 3 mm（PDF 191×266 mm）；主色 #1D4F91，2026-10-14 起确定四色印刷，彩色图标和插画可用；PDF 为 RGB，由印厂转 CMYK。
- 代码跨页：20 行以内的程序和“待补充”“待诊断”练习整段不跨页；21 行以上只在空行处分页、每段至少 8 行，续页加“文件名（续）”；**排不下就移页，不缩小字号**。HTML 版参数在 `build.py` 的 `LONG_CODE`/`MIN_CHUNK`/`LONG_TABLE`，docx 版在 `p3lib.py` 的 `book_split`。
- 行尾注释按编辑器列宽对齐（汉字占 2 列），用各目录 `tools/cmt.py`。
- 资源包版本号（`book/pack.py` 的 `VER`/`VER_TAG`/`BOOK_VER`）要与书中“本书使用说明·5. 配套资源”一起改。

## 体例

- 每个项目：项目首页 → 情境导入 → 三维目标 → 知识导图 → 任务（描述/分析/相关知识/课堂练习/实施/技能训练）→ 项目小结 → AI 升华；另有“学习分层（必会/跟着用/选学）”“课堂验收”“离开 AI 再做”。客户的各章框架在 `docs/requirements/`，作者批注稿在 `docs/author-drafts/`。
- 人物：新生林小禾、C老师（v4 及以前称林老师）、AI 助教小智。
- 科学性：结论要么有 C 标准依据，要么限定为“本书环境”；客户框架里技术上不成立的说法要改正，并在修改意见中说明理由。

## 产出与提交

- PDF、docx、zip 等成品不进 git，放 GitHub Releases 或项目文件夹（`textbook/项目N/…`）；`docs/**/*.docx` 例外，入库。修订说明放 `docs/history/`。
- 每一稿开分支、走 PR 合并到 `main`；提交信息用中文，写清项目、第几稿、按什么意见修订。
