#!/bin/bash
# 一键生成项目二 Word（清洁版、带批注回复版）、预览 PDF、修改意见、审计说明和配套资源。用法：bash build2.sh [程序目录]
set -e
cd "$(dirname "$0")"
CODE=${1:-$(pwd)/../../code/project02}
V5=${V5:-"/mnt/project-files/textbook/v5/项目一-搭建个人专属档案-修订稿v5（清洁版）.docx"}
# 插图和运行结果图：fig/ 里没有图或设了 FIGS=1 时重新生成（改了插图或程序后用 FIGS=1）
if [ -n "$FIGS" ] || [ ! -f fig/f_scene.png ]; then
  mkdir -p fig && rm -rf fig/assets && cp -r assets fig/ && cp author_fig/*.png fig/
  node shot.js fig/figs.html fig $(python3 figs2.py | tail -1)
  node shot.js fig/cons.html fig $(python3 cons2.py "$CODE" | tail -1)
fi
rm -rf build && mkdir build && unzip -q "$V5" -d build/t && cp -r build/t build/tp && cp -r build/t build/ta
python3 content2.py build/t "$CODE" fig
python3 pack2.py build/t build/p2.docx
# 带批注回复版的底稿：正文相同，放好作者 16 条批注的锚点
python3 content2.py build/ta "$CODE" fig build/anchors.json >/dev/null
python3 pack2.py build/ta build/p2a.docx >/dev/null
# 预览 PDF：代码行尾注释前的空格按 LibreOffice 的替代字体重算（只影响空格个数），其余与 p2.docx 相同
CODE_LATIN_EM=0.602 CODE_WEAK_SP=0.3727 python3 content2.py build/tp "$CODE" fig >/dev/null
python3 pack2.py build/tp build/p2.docx.pv >/dev/null
cd build && mkdir pv && mv p2.docx.pv pv/p2.docx && timeout 300 soffice --headless --convert-to pdf --outdir . pv/p2.docx >/dev/null 2>&1 && pdfinfo p2.pdf | grep Pages
cd ..
# 带批注回复版：作者 16 条原批注 + 逐条回复
rm -rf build/ta2 && mkdir build/ta2 && (cd build/ta2 && unzip -q ../p2a.docx)
python3 replies2.py build/ta2 author_comments.xml
(cd build/ta2 && rm -f ../p2c.docx && zip -q -X -r ../p2c.docx '[Content_Types].xml' && zip -q -X -r ../p2c.docx . -x '[Content_Types].xml')
for f in p2 p2c; do (cd /mnt/skills/public/docx/scripts && python3 office/validate.py "$OLDPWD/build/$f.docx" | tail -2); done
# 修改意见与处理说明（含参考答案）、师生体验审计、配套资源
python3 notes2.py build/notes2.docx fig/nums.json
python3 audit2.py build/audit2.docx fig/nums.json
python3 res2.py "$CODE" fig build/res2.zip
