"""检查代码块、运行结果、运行窗口在给定字号下的最大列数（中文占 2 列）。"""
import re, sys, html, pathlib
sys.path.insert(0, ".")
import build
from build import dw, align_comments, CODE, attrs, clean_diag, expand_tabs

PT = 72 / 25.4
TEXT_W = 148 * PT
def cols(width_pt, fs):           # 等宽字符宽 0.5em
    return int(width_pt / (0.5 * fs) + 1e-6)

CODE_FS = float(sys.argv[1]) if len(sys.argv) > 1 else 10.8
CON_FS = float(sys.argv[2]) if len(sys.argv) > 2 else 10
CW_FS = float(sys.argv[3]) if len(sys.argv) > 3 else 10
DIAG_FS = float(sys.argv[4]) if len(sys.argv) > 4 else 9.6

import os
GUT = float(os.environ.get("GUT", 2.1)); PADX = float(os.environ.get("PADX", 7)); CWW = float(os.environ.get("CWW", 0.96))
inner = TEXT_W - 2.9 - 2 * PADX
lim_code = cols(inner, CODE_FS); lim_code_ln = cols(inner - GUT * CODE_FS, CODE_FS)
half = (TEXT_W - 10) / 2 - 2.9 - 2 * PADX
lim_half = cols(half, CODE_FS)
lim_con = cols(TEXT_W - 19.2, CON_FS)
lim_cw = cols(TEXT_W * CWW - 15.2, CW_FS)
lim_diag = cols(TEXT_W - 19.2, DIAG_FS)
print(f"limits: code {lim_code}, code+ln {lim_code_ln}, half {lim_half}, console {lim_con}, conwin {lim_cw}, diag {lim_diag}")

bad = 0
for part in build.BODY_PARTS:
    s = (build.ROOT / "parts" / part).read_text(encoding="utf-8")
    # 两栏中的代码
    twos = [m.span() for m in re.finditer(r'<div class="two">.*?\n</div>', s, re.S)]
    def in_two(pos): return any(a <= pos < b for a, b in twos)
    for m in re.finditer(r'<code-file([^>]*)/>|<snip([^>]*)>(.*?)</snip>', s, re.S):
        if m.group(1) is not None:
            a = attrs(m.group(1)); src = (CODE / a["src"]).read_text(encoding="utf-8"); name = a["src"]
        else:
            a = attrs(m.group(2)); src = html.unescape(m.group(3)); name = "snip:" + (a.get("title") or src.split("\n")[0][:30])
        src = align_comments(src.strip("\n"))
        lim = lim_half if in_two(m.start()) else (lim_code_ln if "ln" in a else lim_code)
        for i, line in enumerate(src.split("\n"), 1):
            w = dw(expand_tabs(line))
            if w > lim:
                bad += 1; print(f"CODE {part} {name} L{i} w={w} > {lim}: {line}")
    for m in re.finditer(r'<out([^>]*)/>', s):
        a = attrs(m.group(1)); txt = (CODE / (a["src"].replace(".c", "") + ".wout" + a.get("run", ""))).read_text(encoding="utf-8")
        lim = lim_half if in_two(m.start()) else lim_con
        for line in txt.split("\n"):
            if dw(expand_tabs(line)) > lim: bad += 1; print(f"OUT {part} {a['src']} w={dw(line)} > {lim}: {line}")
    for m in re.finditer(r'<conwin([^>]*)/>', s):
        a = attrs(m.group(1))
        html_ = build.conwin(a["src"], a.get("dir", "project01"), a.get("ins", ""), a.get("ret"), "notrailer" not in a, title=a.get("title"), run=a.get("run", ""))
        body = re.search(r'<pre class="cw-body">(.*?)</pre>', html_, re.S).group(1)
        body = html.unescape(re.sub(r'<[^>]+>', '', body))
        for line in body.split("\n"):
            if dw(line) > lim_cw: bad += 1; print(f"CONWIN {part} {a['src']} w={dw(line)} > {lim_cw}: {line}")
    for m in re.finditer(r'<diag([^>]*)/>', s):
        a = attrs(m.group(1)); txt = clean_diag((CODE / (a["src"] + ".wdiag")).read_text(encoding="utf-8"))
        for line in txt.split("\n"):
            if "|" in line and dw(line) > lim_diag: bad += 1; print(f"DIAG {part} {a['src']} w={dw(line)} > {lim_diag}: {line}")
print("over-limit lines:", bad)
