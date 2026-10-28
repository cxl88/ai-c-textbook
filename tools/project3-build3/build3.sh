#!/bin/bash
# 一键生成项目三第三稿：清洁版、带批注回复版、预览 PDF、修改意见、审计说明、配套资源。用法：bash build3.sh [程序目录]
# 插图与运行截图另行生成：python3 figs.py / cons3.py + shot.js（见 README.txt）
set -e
cd "$(dirname "$0")"
CODE=${1:-/root/cstudy/p3code}
V5="/mnt/project-files/textbook/v5/项目一-搭建个人专属档案-修订稿v5（清洁版）.docx"
rm -rf build && mkdir build && unzip -q "$V5" -d build/t && cp -r build/t build/tp && cp -r build/t build/ta
python3 content3.py build/t "$CODE" fig
python3 pack2.py build/t build/p3.docx
# 带批注回复版的底稿：正文相同，放好作者 16 条批注的锚点
python3 content3.py build/ta "$CODE" fig build/anchors.json >/dev/null
python3 pack2.py build/ta build/p3a.docx >/dev/null
# 预览 PDF：代码行尾注释前的空格按 LibreOffice 的替代字体重算（只影响空格个数），其余与 p3.docx 相同
CODE_LATIN_EM=0.602 CODE_WEAK_SP=0.3727 python3 content3.py build/tp "$CODE" fig >/dev/null
python3 pack2.py build/tp build/p3.docx.pv >/dev/null
cd build && mkdir pv && mv p3.docx.pv pv/p3.docx && timeout 300 soffice --headless --convert-to pdf --outdir . pv/p3.docx >/dev/null 2>&1 && pdfinfo p3.pdf | grep Pages
cd ..
# 带批注回复版：作者 16 条原批注 + 逐条回复
rm -rf build/ta2 && mkdir build/ta2 && (cd build/ta2 && unzip -q ../p3a.docx)
python3 replies3.py build/ta2 author_comments.xml
(cd build/ta2 && rm -f ../p3c.docx && zip -q -X -r ../p3c.docx '[Content_Types].xml' && zip -q -X -r ../p3c.docx . -x '[Content_Types].xml')
for f in p3 p3c; do (cd /mnt/skills/public/docx/scripts && python3 office/validate.py "$OLDPWD/build/$f.docx" | tail -2); done
# 修改意见与处理说明（含参考答案）、师生体验审计、配套资源
[ -f notes3.py ] && python3 notes3.py build/notes3.docx fig/nums.json
[ -f audit3.py ] && python3 audit3.py build/audit3.docx fig/nums.json
[ -f res3.py ] && python3 res3.py "$CODE" fig build/res3.zip
true
