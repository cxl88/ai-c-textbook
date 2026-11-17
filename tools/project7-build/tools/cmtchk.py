# 预览 PDF 中检查行尾注释 // 的横坐标：同一组（相邻行）应对齐
import pdfplumber, sys
from collections import defaultdict
pdf = pdfplumber.open(sys.argv[1])
bad = 0
for pn, pg in enumerate(pdf.pages, 1):
    lines = defaultdict(list)
    for c in pg.chars:
        lines[round(c['top'], 0)].append(c)
    rows = []
    for top in sorted(lines):
        cs = sorted(lines[top], key=lambda c: c['x0'])
        txt = ''.join(c['text'] for c in cs)
        k = txt.find('//')
        if k > 0 and txt[:k].strip() and 'DejaVuSansMono' in cs[0]['fontname']:
            rows.append((top, cs[k]['x0'], txt))
    # 分组：相邻行（间距 < 25pt）
    grp = []
    for r in rows:
        if grp and r[0] - grp[-1][-1][0] < 25:
            grp[-1].append(r)
        else:
            grp.append([r])
    for g in grp:
        xs = [r[1] for r in g]
        if len(g) > 1 and max(xs) - min(xs) > 2.5:
            bad += 1
            print(f'p{pn}', [round(x - min(xs), 1) for x in xs], g[xs.index(max(xs))][2][:50])
print('groups off by >2.5pt:', bad)
