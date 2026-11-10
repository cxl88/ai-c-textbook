#!/bin/bash
# 一键生成项目五 Word（清洁版）、预览 PDF、编写说明与参考答案、师生体验审计和配套资源。用法：bash build5.sh [程序目录]
set -e
cd "$(dirname "$0")"
CODE=${1:-$(pwd)/../../code/project05/book}
CHECK=${CHECK:-$(pwd)/../../code/project05/check}
V5=${V5:-"/mnt/project-files/textbook/v5/项目一-搭建个人专属档案-修订稿v5（清洁版）.docx"}
# 插图和运行结果图：fig/ 里没有图或设了 FIGS=1 时重新生成（改了插图或程序后用 FIGS=1）
if [ -n "$FIGS" ] || [ ! -f fig/f_scene.png ]; then
  mkdir -p fig && rm -rf fig/assets && cp -r assets fig/
  node shot.js fig/figs.html fig $(python3 figs5.py | tail -1)
  node shot.js fig/cons.html fig $(python3 cons5.py "$CODE" | tail -1)
fi
rm -rf build && mkdir build && unzip -q "$V5" -d build/t && cp -r build/t build/tp
python3 content5.py build/t "$CODE" fig
python3 pack5.py build/t build/p5.docx
# 预览 PDF：代码行尾注释前的空格按 LibreOffice 的替代字体重算（只影响空格个数），其余与 p5.docx 相同
CODE_LATIN_EM=0.602 CODE_WEAK_SP=0.3727 python3 content5.py build/tp "$CODE" fig >/dev/null
python3 pack5.py build/tp build/p5.docx.pv >/dev/null
cd build && mkdir pv && mv p5.docx.pv pv/p5.docx && timeout 300 soffice --headless --convert-to pdf --outdir . pv/p5.docx >/dev/null 2>&1 && pdfinfo p5.pdf | grep Pages
cd ..
# 编写说明与参考答案、师生体验审计、配套资源
[ -f notes5.py ] && python3 notes5.py build/notes5.docx fig/nums.json "$CODE" "$CHECK"
[ -f audit5.py ] && python3 audit5.py build/audit5.docx fig/nums.json
[ -f res5.py ] && python3 res5.py "$CODE" "$CHECK" fig build/res5.zip
true
