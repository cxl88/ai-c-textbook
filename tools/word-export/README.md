# Word 可编辑版生成脚本（v4）

从排版源文件（排版源文件v4.zip 解压后 `python3 build.py` 得到的 out/body.html、out/front.html、out/cover_print.pdf）生成可编辑 .docx。
Word 文件只是可编辑副本；改稿仍以排版源文件为准，改完重新生成。

## 依赖
- Node 22，Playwright（Chromium），docx 9.7.1（脚本里写的是 /opt/node22/lib/node_modules/docx，路径不同就改 require）
- LibreOffice Writer（`apt-get install -y libreoffice-writer`；只有 libreoffice-core 时打不开 docx），只用于预览和回读页码
- Python 3，Pillow；docx 技能的 validate.py 需要 `pip install defusedxml`
- render.py 引用 docx 技能的 scripts/office/soffice.py，路径不同就改第 4 行
- 预览字体替代：fonts.conf.preview 放到 ~/.config/fontconfig/fonts.conf（Consolas 用 JetBrains Mono 代替，比 Consolas 宽；代码字号按 0.6 em 估宽，两种字体都不折行）

## 步骤（B=排版工程目录，W=本目录）
1. 抽取：`node extract.js $B/out/body.html "$(cat cfg_body.json)" $W/body.json $W/img`；front 同理（cfg_front.json → front.json）
2. 封面和篇章页底图（Pillow）：
   - cover_print.pdf 用 pdftoppm -r 300 转 PNG，裁掉 3 mm 出血（185×260 mm）存 img/cover.jpg（quality 92）
   - img/b000.png、b061.png、f000.png（3 倍分辨率整页截图）裁掉 3 mm 出血存 *_trim.jpg
3. 第一遍：删除 pages.json → `node build_docx.js out/p1.docx` → `python3 post.py out/p1.docx out/p1p.docx 8390` → validate.py → `python3 render.py $PWD/out/p1p.docx $PWD/out/`（必须绝对路径）
4. 回读页码：`python3 mkpages.py out/p1p.pdf out/p1.meta.json pages.json`（目录 19 条、“见第×页” 6 处）
5. 第二遍：`node build_docx.js out/p2.docx` → post.py → validate.py → render.py；再跑一次 mkpages.py 到另一个文件，和 pages.json 一致才算稳定
6. 核对文字：`node textcheck.js $B/out/front.html cfg_front.json tc_front.txt`、body 同理，合并后 `python3 tdiff.py tc_html.txt tc_docx.txt`（tc_docx.txt 用 docxtext.py 生成）。预期差异只有：目录标题、篇章页底图里的装饰文字和页脚的学时行、图题（检查时随图隐藏）、“第…页”和重排后的页码、代码续页标题（Word 里改为重复标题行）
7. 逐页看：pdftoppm -r 50 + sheets.py 拼缩略图

## 版式要点
- 185×260 mm，对称页边距（内 20、外 17、上 21、下 20、页眉 12、页脚 10 mm），奇偶页不同页眉
- 封面后留空白页；扉页起罗马页码，前言、使用说明、目录从奇数页起；项目一篇章页从 1 起
- 标题只用样式，不带直接格式（Word 更新目录时会把标题里的直接格式带进目录）；任务编号是字符样式“任务标签”；附录标题是“附录标题”样式（大纲级别 1），目录域 `TOC \h \o "1-2" \u \z`
- 正文段落用“正文首行缩进”样式，和样式相同的字体字号颜色不写在文字上
- 程序：20 行以内整段不分页；21 行以上只在空行处分页、每段至少 8 行，标题行设为重复标题行
