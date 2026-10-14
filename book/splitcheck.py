"""跨页检查：给长表格的每一行、长程序的每一段加隐形标记，渲染后统计它们落在哪一页。
用法：python3 splitcheck.py   （读取 out/body.html，输出每个跨页元素在各页的行数/段数，并标出可疑处）"""
import re, html, subprocess, collections
from pathlib import Path
ROOT = Path(__file__).parent
s = (ROOT / "out/body.html").read_text(encoding="utf-8")
names = {}
eid = 0

def mk(e, r):
    return f'<span class="mkw"><span class="mk">QSPQ{e:03d}{r:03d}Q</span></span>'

def label(seg):
    t = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", seg))).strip()
    return t[:34]

def tab(m):
    global eid
    eid += 1; e = eid
    head_, body = m.group(1), m.group(2)
    names[e] = ("表", label(body))
    k = [0]
    def tr(mm):
        k[0] += 1
        return mm.group(0) + mk(e, k[0])
    # 只给 tbody 中的行加标记：标记放进每行第一个单元格的开头
    tb = re.search(r"<tbody>(.*?)</tbody>", body, flags=re.S)
    if not tb:
        return m.group(0)
    nb = re.sub(r"<tr[^>]*>\s*<t[dh][^>]*>", tr, tb.group(1))
    return f"<table{head_}>" + body[:tb.start(1)] + nb + body[tb.end(1):] + "</table>"

s = re.sub(r'<table([^>]*class="long[^"]*"[^>]*)>(.*?)</table>', tab, s, flags=re.S)

def code(m):
    global eid
    eid += 1; e = eid
    names[e] = ("程序", label(m.group(0)[:300]))
    k = [0]
    def ck(mm):
        k[0] += 1
        return mm.group(0) + mk(e, k[0])
    return re.sub(r'<div class="ck">', ck, m.group(0))

s = re.sub(r'<div class="code[^"]*\blong\b[^"]*">.*?</div></div>', code, s, flags=re.S)
(ROOT / "dbg/split.html").write_text(s.replace('href="', 'href="../out/').replace('src="', 'src="../out/') if False else s, encoding="utf-8")
subprocess.run(["node", str(ROOT / "render.js"), str(ROOT / "dbg/split.html"), str(ROOT / "dbg/split.pdf")], check=True)
txt = subprocess.run(["pdftotext", "-layout", str(ROOT / "dbg/split.pdf"), "-"], capture_output=True, text=True).stdout.split("\f")
where = collections.defaultdict(lambda: collections.Counter())
for pi, t in enumerate(txt):
    t = re.sub(r"\s+", "", t)
    for m in re.finditer(r"QSPQ(\d{3})(\d{3})Q", t):
        where[int(m.group(1))][pi + 1] += 1
print("pages:", len(txt) - 1)
for e in sorted(names):
    kind, lab = names[e]
    c = where.get(e, {})
    if len(c) > 1:
        flag = "  <-- 只有 1 行" if kind == "表" and min(c.values()) < 2 else ""
        print(f"{kind} p{'/'.join(str(p) for p in sorted(c))} {dict(sorted(c.items()))}  {lab}{flag}")
missing = [e for e in names if e not in where]
print("未找到标记:", missing)
