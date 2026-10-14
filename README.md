# 人工智能助力C语言程序设计

冯丽娜　编著。面向大一学生的 C 语言教材：情景贴近生活、任务融合知识点、全书结合 AI 助学。成书按印刷厂标准排版（185×260 mm 成品、3 mm 出血、字体嵌入）。

## 进度

| 章节 | 状态 | 说明 |
| --- | --- | --- |
| 项目一 搭建个人专属档案 | 已成稿（v4 印刷版）；作者新稿 v5 修订中 | v5 把项目一合并为两个任务，修订稿为 Word（见 Release `v5`），尚未并回排版源文件 |
| 项目二 读懂身边多样数据 | 已成稿（v4 印刷版） | 三个任务，6 号楼 203 实训室主线 |
| 附录A ASCII 字符集 | 已成稿 | |
| 项目三 梳理程序执行逻辑 | 初稿（Word，2026-10-14） | 按客户框架两个任务：认知程序算法与执行步骤、辨析程序三大控制结构；版式套用项目一 v5，成品见 Release / 项目文件夹 textbook/项目三 |
| 项目四及以后 | 未开始 | 沿用同一套体例与工具链 |

签印刷终稿前仍需：学校资源平台地址、机房试教、原尺寸打印检查、数码样。

## 目录结构

```
book/                 排版工程（最新为 v4）：build.py、style.css、检查脚本
  parts/              各章 HTML 源文件（00_front 前言目录、10_ch1 项目一、20_ch2a/b/c 项目二、90_appx 附录、cover 封面）
  code/               书中全部示例程序 .c，及在 Windows GCC 实测的输出（.wout/.wret/.wdiag）
  check/              核对参考答案用的改动版程序
  img/                界面截图
code/project01-v5/    v5 配套的点餐小程序 canteen.c 与贪吃蛇 snake.c（snake.c 仅 Windows，展示用）
code/project03/       项目三示例程序（examples/）与参考答案程序（answers/），含实测输出 .wout/.wret/.wdiag
fonts/                字体（不入库，见 fonts/README.md）
tools/
  word-export/        由排版结果生成可编辑 Word 版（v4）
  project1-v5-revise/ 对作者批注稿项目一的 v5 修订脚本
  project3-build/     项目三 Word 生成脚本（以 v5 清洁版为版式模板，build.sh 一键生成）
docs/
  requirements/       客户给的章节模板（项目一、项目二、项目三）
  history/            各版修订说明、v5 修改意见与处理说明
```

新增章节：在 `book/parts/` 加 `30_ch3.html`（`build.py` 里的 `BODY_PARTS` 加上文件名），程序放进 `book/code/`，用 `<code-file src="x.c" .../>` 引用。标签和规格全部写在 [book/README.md](book/README.md)。

## 重建 PDF

1. 安装 Python 3（pypdf、Pillow）、Node.js + Playwright（Chromium）、poppler-utils。
2. 按 [fonts/README.md](fonts/README.md) 下载字体到 `fonts/`。
3. `cd book && python3 build.py`，输出在 `book/out/`：`book.pdf` 完整版、`interior.pdf` 内文、`cover_print.pdf` 封面、`ebook.pdf` 电子阅读版。
4. 检查：`node check.js out/body.html`、`python3 gaps.py out/body.pdf 30`、`python3 splitcheck.py`、`python3 widths.py`。
5. 改了示例程序：用 `wrun.sh`（Wine + 小熊猫C++ 自带 GCC 11.5.0）重跑；资源包用 `pack.py` 生成。详见 book/README.md。

## 体例与规格要点

- 读者基础弱：通俗、贴近现实、任务融合知识点；示例头文件尽量只用 stdio.h、math.h、string.h。
- 每个项目：项目首页 → 情境导入 → 三维目标 → 知识导图 → 任务（描述/分析/相关知识/课堂练习/实施/技能训练）→ 项目小结 → AI 升华；v3 起加“学习分层”“课堂验收”“离开 AI 再做”。
- 配色：主色 #1D4F91 加黑灰；正文 Noto Serif SC 10.5 pt，代码 JetBrains Mono 约 9 pt；项目首页从奇数页起。
- 代码跨页：20 行以内整段，更长的只在空行处分页；不靠缩小字号。
- 人物：新生小禾、林老师、AI 助教小智。

## 版本

成品 PDF、Word 不进 git，放在 [Releases](../../releases)；每版源文件对应下表中的提交（可用 `git checkout <提交>` 取回该版源文件）。

| 版本 | 提交 | 内容 |
| --- | --- | --- |
| v2 | `970197d` | 第一至二章印刷版（98 页含封面） |
| v3 | `6ceb987` | 按审读意见修订：科学性勘误、学习分层、课堂验收、资源入口 |
| v4 | `8542094` | 教师试教稿：补交资源、选择题勘误、AI 纠错先只编译再运行、EOF 提示、代码分页；118 页；含教师用《参考答案与评分说明》和可编辑 Word 版 |
| v5 | `8d558d7` | 项目一按作者批注修订（Word 修订稿、清洁版、预览 PDF、修改意见、配套资源）；排版源文件仍为 v4 |

各版详细说明见 `docs/history/`。
