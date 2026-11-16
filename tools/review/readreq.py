# 读出客户框架 docx 的正文（含表格）和批注，批注范围用 ⟦c0 … c0⟧ 标在正文中。编写新项目前通读框架用。
# 用法：python -I tools/review/readreq.py 框架.docx（也可以是解包后的目录）
# 外来文件只用 zipfile 读取其中的 XML，不解包到磁盘。
import html
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
src = sys.argv[1]
if os.path.isdir(src):
    def rd(name):
        p = os.path.join(src, name)
        return open(p, encoding='utf8').read() if os.path.exists(p) else None
else:
    import zipfile
    z = zipfile.ZipFile(src)
    names = set(z.namelist())

    def rd(name):
        return z.read(name).decode('utf8') if name in names else None


def text(xml):
    return html.unescape(''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', xml)))


x = rd('word/document.xml')
body = x[x.index('<w:body>'):]
out = []
for m in re.finditer(r'<w:p[ >].*?</w:p>|<w:tbl>.*?</w:tbl>', body, re.S):
    blk = m.group(0)
    if blk.startswith('<w:tbl'):
        rows = [' | '.join(text(tc) for tc in re.findall(r'<w:tc>.*?</w:tc>', tr, re.S))
                for tr in re.findall(r'<w:tr[ >].*?</w:tr>', blk, re.S)]
        out.append('[表格] ' + ' // '.join(rows))
        continue
    s = re.sub(r'<w:commentRangeStart w:id="(\d+)"/>', r'⟦c\1 ', blk)
    s = re.sub(r'<w:commentRangeEnd w:id="(\d+)"/>', r' c\1⟧', s)
    t = html.unescape(''.join(a or b or c for a, b, c in re.findall(r'<w:t[^>]*>([^<]*)</w:t>|(⟦c\d+ )|( c\d+⟧)', s)))
    if t.strip():
        out.append(t)
print('\n'.join(out))
c = rd('word/comments.xml')
print('\n========== 批注' + ('' if c else '：无'))
for m in re.finditer(r'<w:comment\b([^>]*)>(.*?)</w:comment>', c or '', re.S):
    cid = re.search(r'w:id="(\d+)"', m.group(1)).group(1)
    au = re.search(r'w:author="([^"]*)"', m.group(1))
    print(f'c{cid}（{au.group(1) if au else ""}）：' + text(m.group(2)))
