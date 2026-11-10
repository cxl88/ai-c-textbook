#!/bin/bash
# 一键生成项目四 Word 与预览 PDF。用法：bash build.sh [程序目录]
set -e
cd "$(dirname "$0")"
CODE=${1:-/root/cstudy/p4code}
V5="/mnt/project-files/textbook/v5/项目一-搭建个人专属档案-修订稿v5（清洁版）.docx"
mkdir -p fig && rm -rf fig/assets && cp -r assets fig/assets
python3 figs4.py > /tmp/figids && NODE_PATH=/opt/node22/lib/node_modules node shot.js fig/figs.html fig $(cat /tmp/figids)
python3 cons4.py "$CODE" > /tmp/conids && NODE_PATH=/opt/node22/lib/node_modules node shot.js fig/cons.html fig $(cat /tmp/conids)
rm -rf build && mkdir build && unzip -q "$V5" -d build/t && cp -r build/t build/tp
python3 content4.py build/t "$CODE" fig
python3 pack.py build/t build/p4.docx
# 预览 PDF：代码行尾注释前的空格按 LibreOffice 的替代字体重算（只影响空格个数），其余与 p4.docx 相同
CODE_LATIN_EM=0.602 CODE_WEAK_SP=0.3727 python3 content4.py build/tp "$CODE" fig >/dev/null
python3 pack.py build/tp build/p4.docx.pv >/dev/null
cd build && mkdir pv && mv p4.docx.pv pv/p4.docx && timeout 300 soffice --headless --convert-to pdf --outdir . pv/p4.docx >/dev/null 2>&1 && pdfinfo p4.pdf | grep Pages
