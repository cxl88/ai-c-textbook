#!/usr/bin/env python3
"""Body text of a docx in document order (TOC paragraphs skipped). usage: docxtext.py in.docx out.txt"""
import re, sys, zipfile
x = zipfile.ZipFile(sys.argv[1]).read('word/document.xml').decode('utf-8')
out = []
for p in re.findall(r'<w:p[ >].*?</w:p>', x, re.S):
    if re.search(r'<w:pStyle w:val="TOC\d"/>', p):
        continue
    s = []
    for m in re.finditer(r'<w:t(?: [^>]*)?>([^<]*)</w:t>|<w:tab/>|<w:br/>', p):
        s.append(m.group(1) if m.group(1) is not None else ' ')
    out.append(''.join(s))
import html
open(sys.argv[2], 'w', encoding='utf-8').write(html.unescape('\n'.join(out)))
