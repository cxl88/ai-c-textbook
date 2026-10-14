#!/usr/bin/env python3
"""Page numbers for the TOC and the page references, read back from a LibreOffice render.
usage: mkpages.py rendered.pdf build.meta.json pages.json
Display page = physical page - physical page of the first project heading + 1 (the projects restart at 1)."""
import json, re, subprocess, sys
pdf, meta_p, out_p = sys.argv[1:4]
meta = json.load(open(meta_p, encoding='utf-8'))
txt = subprocess.run(['pdfinfo', '-dests', pdf], capture_output=True, text=True, check=True).stdout
phys = {}
for line in txt.splitlines()[1:]:
    m = re.match(r'\s*(\d+)\s+\[.*\]\s+"(.*)"\s*$', line)
    if m:
        phys[m.group(2)] = int(m.group(1))
enc = lambda n: n.replace('_', '5F')   # LibreOffice writes '_' in destination names as 5F
names = [e['href'] for e in meta['toc']] + meta['refs']
missing = [n for n in names if enc(n) not in phys]
assert not missing, missing
base = phys[enc(meta['toc'][0]['href'])]
bm = {n: phys[enc(n)] - base + 1 for n in names}
json.dump({'bm': bm, 'source': pdf}, open(out_p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for e in meta['toc']:
    print('%4d  %s' % (bm[e['href']], e['title']))
for r in meta['refs']:
    print('%4d  %s' % (bm[r], r))
