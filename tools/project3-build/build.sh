#!/bin/bash
# 一键生成项目三 Word 与预览 PDF。用法：bash build.sh 程序目录
set -e
cd "$(dirname "$0")"
CODE=${1:-/root/cstudy/p3code}
V5="/mnt/project-files/textbook/v5/项目一-搭建个人专属档案-修订稿v5（清洁版）.docx"
python3 figs.py > /tmp/figids && NODE_PATH=/opt/node22/lib/node_modules node shot.js fig/figs.html fig $(cat /tmp/figids)
python3 cons.py > /tmp/conids && NODE_PATH=/opt/node22/lib/node_modules node shot.js fig/cons.html fig $(cat /tmp/conids)
rm -rf build && mkdir build && unzip -q "$V5" -d build/t
python3 content.py build/t "$CODE" fig
python3 pack.py build/t build/p3.docx
cd build && timeout 300 soffice --headless --convert-to pdf p3.docx >/dev/null 2>&1 && pdfinfo p3.pdf | grep Pages
