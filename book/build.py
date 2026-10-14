#!/usr/bin/env python3
"""《人工智能助力C语言程序设计》印刷版构建脚本（v2）

流程：parts/*.html → 预处理（代码高亮、运行窗口、编译提示）→ Chromium 排版 →
用 pdftotext 读回页码 → 回填目录与“详见第×页”、保证项目首页落在右页 →
设置出血框/裁切框、页码标签、书签 → 合并封面，输出印刷 PDF。

成品尺寸 185 mm × 260 mm（16 开），四边各留 3 mm 出血，PDF 页面 191 mm × 266 mm。
"""
import hashlib, html, pathlib, re, shutil, subprocess, sys, unicodedata
from pypdf import PdfReader, PdfWriter, PageObject, Transformation
from pypdf.generic import RectangleObject

ROOT = pathlib.Path(__file__).resolve().parent
CODE, OUT = ROOT / "code", ROOT / "out"
OUT.mkdir(exist_ok=True)

MM = 72 / 25.4
PAGE_W, PAGE_H = 191 * MM, 266 * MM      # 含出血
BLEED = 3 * MM
BOOK = "人工智能助力C语言程序设计"

# ---------------------------------------------------------------- 代码高亮
KW = set("""auto break case char const continue default do double else enum extern float for goto if inline int long
register restrict return short signed sizeof static struct switch typedef union unsigned void volatile while _Bool""".split())
FN = set("printf scanf getchar putchar sqrt pow fabs strlen main".split())
TOK = re.compile(r'''(?P<c>//[^\n]*|/\*.*?\*/)|(?P<p>^[ \t]*\#[^\n]*?(?=//|/\*|$))|(?P<s>"(?:\\.|[^"\\\n])*")|(?P<ch>'(?:\\.|[^'\\\n])*')|(?P<n>\b(?:0[xX][0-9A-Fa-f]+|\d+(?:\.\d+)?(?:[eE][+-]?\d+)?[fF]?)\b)|(?P<w>\b[A-Za-z_]\w*\b)''', re.S | re.M)


def hl(src):
    out, pos = [], 0
    for m in TOK.finditer(src):
        out.append(html.escape(src[pos:m.start()]))
        t, k = m.group(0), m.lastgroup
        e = html.escape(t)
        if k == "c":
            out.append(f'<span class="hl-c">{e}</span>')
        elif k == "p":
            out.append(f'<span class="hl-p">{e}</span>')
        elif k in ("s", "ch"):
            out.append(f'<span class="hl-s">{e}</span>')
        elif k == "n":
            out.append(f'<span class="hl-n">{e}</span>')
        elif t in KW:
            out.append(f'<span class="hl-k">{e}</span>')
        elif t in FN:
            out.append(f'<span class="hl-f">{e}</span>')
        else:
            out.append(e)
        pos = m.end()
    out.append(html.escape(src[pos:]))
    return "".join(out)


def wide(c):
    # 等宽字体 JetBrains Mono 没有的 ①～⑳、℃ 等符号由中文字体显示，也占 2 列
    return unicodedata.east_asian_width(c) in "WF" or "\u2460" <= c <= "\u24ff" or "\u2100" <= c <= "\u214f"


def dw(t):
    """显示宽度：中文等全角字符占 2 列。"""
    return sum(2 if wide(c) else 1 for c in t)


def align_comments(src):
    """把相邻几行的行尾注释对齐到同一列（按显示宽度计算）。"""
    lines = src.split("\n")
    info = []
    for l in lines:
        m = re.match(r'^(.*?\S)\s{2,}(//.*)$', l)
        info.append((m.group(1), m.group(2)) if m and not l.lstrip().startswith("//") else None)
    out, i = list(lines), 0
    while i < len(lines):
        if info[i] is None:
            i += 1
            continue
        j = i
        while j < len(lines) and (info[j] is not None or lines[j].strip() in ("{", "}")):
            j += 1
        grp = [k for k in range(i, j) if info[k]]
        col = max(dw(info[k][0]) for k in grp) + 2
        for k in grp:
            code, cm = info[k]
            c = col if col <= 52 else dw(code) + 2
            out[k] = code + " " * max(2, c - dw(code)) + cm
        i = j
    return "\n".join(out)


def code_block(src, title=None, ln=False, bad=False, mark=None):
    src = align_comments(src.strip("\n"))
    h = hl(src)
    marks = {int(x) for x in mark.split(",")} if mark else set()
    if ln or marks:
        rows = h.split("\n")
        h = "\n".join((f'<span class="ln">{i + 1}</span>' if ln else "")
                      + (f'<span class="mkl">{r}</span>' if i + 1 in marks else r)
                      for i, r in enumerate(rows))
    fn = f'<span class="fn">{html.escape(title)}</span>' if title else ""
    long = " long" if src.count("\n") + 1 >= LONG_CODE else ""     # 长程序允许跨页
    return f'<pre class="code{" bad" if bad else ""}{" withln" if ln else ""}{long}">{fn}{h}</pre>'


def hl_lines(src):
    """逐行高亮：跨行的注释在每行首尾补齐 span，保证每行都是完整的 HTML。"""
    h = hl(src)
    rows, open_tag = [], ""
    for row in h.split("\n"):
        row = open_tag + row
        tags = re.findall(r'<span class="hl-\w">|</span>', row)
        depth, last = 0, ""
        for t in tags:
            if t == "</span>":
                depth -= 1
            else:
                depth += 1
                last = t
        if depth > 0:
            row += "</span>"
            open_tag = last
        else:
            open_tag = ""
        rows.append(row)
    return rows


def anno_block(src, title, spec):
    """代码旁注图：右侧用括号标出各部分。spec 每行“行号范围|列(a/b/ab)|说明”。"""
    rows = hl_lines(align_comments(src.strip("\n")))
    n = len(rows)
    cells = [f'<div class="fn" style="grid-row:1">{html.escape(title)}</div>',
             '<div class="cpad" style="grid-row:2"></div>']
    for i, r in enumerate(rows):
        cells.append(f'<div class="cl" style="grid-row:{i + 3}">{r or " "}</div>')
    cells.append(f'<div class="cpad end" style="grid-row:{n + 3}"></div>')
    for item in spec.strip().split("\n"):
        rng, col, label = item.strip().split("|", 2)
        a, _, b = rng.partition("-")
        a, b = int(a), int(b or a)
        gc = {"a": "2 / 3", "b": "3 / 4", "ab": "2 / 4"}[col]
        cells.append(f'<div class="an" style="grid-row:{a + 2} / {b + 3}; grid-column:{gc}">{label}</div>')
    return '<div class="anno">' + "".join(cells) + "</div>"


# ---------------------------------------------------------------- 运行窗口
def expand_tabs(line, ts=8):
    out, col = [], 0
    for c in line:
        if c == "\t":
            n = ts - col % ts
            out.append(" " * n)
            col += n
        else:
            out.append(c)
            col += dw(c)
    return "".join(out)


def stats(seed):
    h = int(hashlib.md5(seed.encode()).hexdigest(), 16)
    t = 0.0180 + (h % 380) / 10000
    cpu = "15.6250" if h % 4 == 0 else "0.0000"
    mem = 1460 + (h >> 8) % 90 * 4
    return t, cpu, mem


def conwin(src, folder="project01", ins="", ret="0", trailer=True, text=None, title=None):
    """小熊猫C++ 运行窗口（Windows 控制台）：内容取自 Windows 版 GCC 的实际运行输出 *.wout。"""
    if text is None:
        text = (CODE / f"{src}.wout").read_text(encoding="utf-8").replace("\r", "").replace("\x00", " ")   # 控制台把 NUL 显示为空格
    marks = []                      # 键盘输入回显的插入位置
    if ins:
        pos = 0
        for item in ins.split(";;"):
            prompt, typed = item.split("|", 1)
            k = text.find(prompt, pos)
            if k < 0:
                raise SystemExit(f"conwin {src}: prompt {prompt!r} not found")
            k += len(prompt)
            text = text[:k] + "\x01" + typed + "\x02\n" + text[k:]
            pos = k + len(typed) + 3
    body = text.rstrip("\n")
    if trailer:
        t, cpu, mem = stats(src or body)
        body = (text if text.endswith("\n") else text + "\n") + "\n" + "-" * 20 + "\n" \
            + f"进程退出, 总耗时 {t:.4f} s. 返回值: {ret}; CPU 时间: {cpu} ms; 内存: {mem} KB.\n\n按任意键退出..."
    rows = []
    for line in body.split("\n"):
        line = expand_tabs(line)
        e = html.escape(line).replace("\x01", '<span class="kin">').replace("\x02", "</span>")
        rows.append(e)
    title = title or f"D:\\CStudy\\{folder}\\{src}.exe"
    bar = ('<div class="cw-bar"><svg class="cw-ico" viewBox="0 0 16 16"><rect x="1" y="2" width="14" height="12" rx="1" fill="#1a1a1a"/>'
           '<path d="M3.5 6l2.5 2-2.5 2" stroke="#fff" stroke-width="1.2" fill="none"/><path d="M7 10.5h4" stroke="#fff" stroke-width="1.2"/></svg>'
           f'<span class="cw-t">{html.escape(title)}</span>'
           '<svg class="cw-btn" viewBox="0 0 72 12"><path d="M4 6.5h9" stroke="#333" stroke-width="0.9"/>'
           '<rect x="30" y="2" width="8" height="8" fill="none" stroke="#333" stroke-width="0.9"/>'
           '<path d="M56 2l8 8M64 2l-8 8" stroke="#333" stroke-width="0.9"/></svg></div>')
    return f'<div class="conwin">{bar}<pre class="cw-body">{chr(10).join(rows)}</pre></div>'


# ---------------------------------------------------------------- 普通结果框 / 编译提示
def console(text, title="运行结果", diag=False):
    e = html.escape(text.rstrip("\n"))
    e = re.sub(r'\[\[in:(.*?)\]\]', r'<span class="kin">\1</span>', e)
    return f'<pre class="console{" diag" if diag else ""}"><span class="bar">{html.escape(title)}</span>{e}</pre>'


def clean_diag(txt):
    txt = re.sub(r'C:/Program Files/RedPanda-Cpp/mingw64/bin/\.\./lib/gcc/x86_64-w64-mingw32/11\.5\.0/\.\./\.\./\.\./\.\./x86_64-w64-mingw32/bin/ld\.exe: [^:]+\.o: ', 'ld.exe: ', txt)
    txt = txt.replace("D:\\wb/", "")
    return txt


def attrs(s):
    a = dict(re.findall(r'([\w-]+)="([^"]*)"', s or ""))
    bare = re.sub(r'"[^"]*"', '""', s or "")
    for flag in re.findall(r'\s([\w-]+)(?=\s|/|$)', " " + bare):
        a.setdefault(flag, "1")
    return a


LONG_CODE = 10       # 不少于 10 行的代码允许跨页
LONG_TABLE = 5       # 不少于 5 行的表格允许跨页（表头行在下一页重复）


def split_tables(s):
    def tb(m):
        attr, body = m.group(1), m.group(2)
        rows = re.findall(r"<tr[\s>]", body)
        if len(rows) < LONG_TABLE or "nosplit" in attr:
            return m.group(0)
        first = re.match(r"\s*(<tr[^>]*>.*?</tr>)", body, flags=re.S)
        if first and "<th" in first.group(1):
            body = "<thead>" + first.group(1) + "</thead><tbody>" + body[first.end():] + "</tbody>"
        if 'class="' in attr:
            attr = attr.replace('class="', 'class="long ', 1)
        else:
            attr += ' class="long"'
        return f"<table{attr}>{body}</table>"
    return re.sub(r"<table([^>]*)>(.*?)</table>", tb, s, flags=re.S)


def preprocess(s):
    # 运行窗口、运行结果与紧随其后的图题合成一个不可拆分的 figure，避免图题与图分页
    s = re.sub(r'(<conwin[^>]*/>)\s*(<figcaption>.*?</figcaption>)', r'<figure class="cwf">\1\n\2</figure>', s, flags=re.S)
    s = re.sub(r'(<out[^>]*/>)\s*(<figcaption>.*?</figcaption>)', r'<figure class="fl">\1\n\2</figure>', s, flags=re.S)
    s = re.sub(r'<anno([^>]*)>(.*?)</anno>', lambda m: (lambda a: anno_block(
        (CODE / a["src"]).read_text(encoding="utf-8"), a.get("title", a["src"]), m.group(2)))(attrs(m.group(1))), s, flags=re.S)
    s = re.sub(r'<code-file([^>]*)/>', lambda m: (lambda a: code_block(
        (CODE / a["src"]).read_text(encoding="utf-8"), a.get("title", a["src"]), "ln" in a, "bad" in a, a.get("mark")))(attrs(m.group(1))), s)
    s = re.sub(r'<snip([^>]*)>(.*?)</snip>', lambda m: (lambda a: code_block(
        html.unescape(m.group(2)), a.get("title"), "ln" in a, "bad" in a, a.get("mark")))(attrs(m.group(1))), s, flags=re.S)

    def conw(m):
        a = attrs(m.group(1))
        return conwin(a["src"], a.get("dir", "project01"), a.get("ins", ""), a.get("ret", "0"), "notrailer" not in a, title=a.get("title"))
    s = re.sub(r'<conwin([^>]*)/>', conw, s)

    def outf(m):
        a = attrs(m.group(1))
        txt = (CODE / (a["src"].replace(".c", "") + ".wout")).read_text(encoding="utf-8")
        return console(txt, a.get("title", "运行结果"))
    s = re.sub(r'<out([^>]*)/>', outf, s)

    def diagf(m):
        a = attrs(m.group(1))
        txt = clean_diag((CODE / (a["src"] + ".wdiag")).read_text(encoding="utf-8"))
        if "only" in a:
            lines = txt.split("\n")
            txt = "\n".join(lines[int(i) - 1] for i in a["only"].split(","))
        return console(txt, a.get("title", "编译器提示"), diag=True)
    s = re.sub(r'<diag([^>]*)/>', diagf, s)
    s = re.sub(r'<con([^>]*)>(.*?)</con>', lambda m: console(html.unescape(m.group(2).strip("\n")), attrs(m.group(1)).get("title", "运行结果"),
                                                          "diag" in attrs(m.group(1))), s, flags=re.S)
    # 课堂练习可以在两题之间跨页
    s = s.replace('<div class="box"><div class="bt"><svg><use href="#i-think"/></svg>课堂练习', '<div class="box long"><div class="bt"><svg><use href="#i-think"/></svg>课堂练习')
    return split_tables(s)


# ---------------------------------------------------------------- 目录、页码引用标记
def add_markers(s):
    toc, odd = [], []

    def tm(m):
        a = attrs(m.group(1))
        i = len(toc)
        toc.append((a["level"], a["text"]))
        if a.get("odd"):
            odd.append(i)
        return f'<span class="mkw"><span class="mk">QTOCQ{i:03d}Q</span></span>'
    s = re.sub(r'<tocmark([^>]*)/>', tm, s)
    refs = {}

    def an(m):
        rid = m.group(1)
        refs[rid] = len(refs)
        return f'<span class="mkw"><span class="mk">QREFQ{refs[rid]:03d}Q</span></span>'
    s = re.sub(r'<anchor id="([^"]+)"\s*/>', an, s)
    return s, toc, odd, refs


def fill_prefs(s, refpages):
    def rp(m):
        return f'<span class="pref">{refpages.get(m.group(1), "00")}</span>'
    return re.sub(r'<pref to="([^"]+)"\s*/>', rp, s)


def strip_markers(s):
    return re.sub(r'<span class="mkw"><span class="mk">Q(?:TOC|REF)Q\d{3}Q</span></span>', '', s)


def render(html_path, pdf_path):
    subprocess.run(["node", str(ROOT / "render.js"), str(html_path), str(pdf_path)], check=True)


def page_texts(pdf):
    txt = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True).stdout
    return txt.split("\f")


def find(texts, pattern):
    found = {}
    for pi, t in enumerate(texts):
        t = re.sub(r"\s+", "", t)              # 极小字号的标记有时会被 pdftotext 拆成带空格的字符
        for m in re.finditer(pattern, t):
            # 强制分页处 Chromium 偶尔会把标记在上一页底部多画一次，以最后出现的页为准（verify_body 再逐条核对）
            found[int(m.group(1))] = pi + 1
    return found


def head(title):
    return (f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>{title}</title>'
            f'<link rel="stylesheet" href="../style.css"></head><body>')


def with_blanks(b, blanks):
    parts = b.split("<!--BLANK-->")
    out = parts[0]
    for i, part in enumerate(parts[1:]):
        out += ('<div class="blankpage"></div>' if i in blanks else "") + part
    return out


def build_body(defs):
    src = "\n".join((ROOT / "parts" / p).read_text(encoding="utf-8") for p in ["10_ch1.html", "20_ch2a.html", "20_ch2b.html", "20_ch2c.html", "90_appx.html"])
    src = preprocess(src)
    src, toc, odd, refs = add_markers(src)
    blanks, pages, refpages = set(), {}, {}
    for rnd in range(8):
        doc = head(BOOK) + defs + fill_prefs(with_blanks(src, blanks), refpages) + "</body></html>"
        (OUT / "body.html").write_text(doc, encoding="utf-8")
        render(OUT / "body.html", OUT / "body.pdf")
        texts = page_texts(OUT / "body.pdf")
        new = find(texts, r'QTOCQ(\d{3})Q')
        newref_i = find(texts, r'QREFQ(\d{3})Q')
        newref = {rid: newref_i.get(i) for rid, i in refs.items()}
        miss = [toc[i][1] for i in range(len(toc)) if i not in new] + [r for r, p in newref.items() if p is None]
        if miss:
            print("WARN missing markers:", miss)
        changed = False
        for k, i in enumerate(odd):                 # 项目首页必须落在右页（奇数页）
            if i in new and new[i] % 2 == 0:
                blanks ^= {k}
                changed = True
        if new == pages and newref == refpages and not changed:
            shutil.copy(OUT / "body.pdf", OUT / "body_mk.pdf")
            break
        pages, refpages = new, newref
    undefined = sorted(set(re.findall(r'<pref to="([^"]+)"', src)) - set(refs))
    if undefined:
        print("WARN undefined page refs:", undefined)
    doc = head(BOOK) + defs + strip_markers(fill_prefs(with_blanks(src, blanks), refpages)) + "</body></html>"
    (OUT / "body.html").write_text(doc, encoding="utf-8")
    render(OUT / "body.html", OUT / "body.pdf")
    marked = fill_prefs(with_blanks(src, blanks), refpages)
    reftargets = {}
    for rid, k in refs.items():                    # 每个引用标记后面紧跟的 8 个可见字符，用来核对页码
        j = marked.find(f"QREFQ{k:03d}Q")
        after = strip_markers(marked[j + 9:j + 2000])
        reftargets[rid] = (refpages.get(rid), squash(html.unescape(re.sub(r"<[^>]+>", "", after)))[:8])
    verify_body(toc, pages, reftargets)
    return toc, pages, refpages


def verify_body(toc, pages, reftargets):
    """核对：去掉标记后版面不变；目录中的每个标题确实出现在所标的页上。"""
    sq = lambda t: re.sub(r"Q(?:TOC|REF)Q\d{3}Q", "", squash(t))
    a, b = page_texts(OUT / "body_mk.pdf"), page_texts(OUT / "body.pdf")
    if len(a) != len(b) or any(sq(x) != sq(y) for x, y in zip(a, b)):
        print("WARN 去掉标记后版面发生变化")
    for i, (lvl, text) in enumerate(toc):
        key = squash(re.sub(r"<[^>]+>", "", text))
        if i in pages and key not in squash(b[pages[i] - 1]):
            print("WARN 目录页码与正文不符:", text, pages[i])
    for rid, (pg, key) in reftargets.items():
        if pg is None or key not in squash(b[pg - 1]):
            print("WARN 引用页码与正文不符:", rid, pg, key)


def toc_html(toc, pages):
    rows = []
    for i, (lvl, text) in enumerate(toc):
        rows.append(f'<div class="row t{lvl}"><span class="tx">{text}</span><span class="dots"></span>'
                    f'<span class="pg">{pages.get(i, "")}</span></div>')
    return '<div class="toc">' + "\n".join(rows) + "</div>"


def squash(t):
    """pdftotext 会在加了字距的标题字之间插入空格，比较前先去掉所有空白。"""
    return re.sub(r"\s+", "", t)


def build_front(defs, toc, pages):
    src = (ROOT / "parts" / "00_front.html").read_text(encoding="utf-8").replace("<!--TOC-->", toc_html(toc, pages))
    src = preprocess(src)
    blanks = set()
    for rnd in range(3):
        doc = head(BOOK) + defs + with_blanks(src, blanks) + "</body></html>"
        (OUT / "front.html").write_text(doc, encoding="utf-8")
        render(OUT / "front.html", OUT / "front.pdf")
        texts = page_texts(OUT / "front.pdf")
        starts = [i + 1 for i, t in enumerate(texts) if "目录" in squash(t)[:60]]
        # 目录从右页（奇数页）开始
        if starts and starts[0] % 2 == 0:
            blanks ^= {0}
            continue
        break


# ---------------------------------------------------------------- 印刷后处理
def set_boxes(page):
    w, h = float(page.mediabox.width), float(page.mediabox.height)
    x0, y0 = float(page.mediabox.left), float(page.mediabox.bottom)
    # Chromium 输出的页面尺寸有取整误差（191 mm × 266 mm 实际为 540.96 pt × 754.08 pt，宽度少约 0.16 mm），
    # 这里把整页内容按比例微调（宽 +0.08%、高 −0.01%）到精确的 191 mm × 266 mm，保证满版底色铺满出血边
    if abs(w - PAGE_W) > 0.01 or abs(h - PAGE_H) > 0.01 or x0 or y0:
        page.add_transformation(Transformation().translate(-x0, -y0).scale(PAGE_W / w, PAGE_H / h))
    media = RectangleObject([0, 0, PAGE_W, PAGE_H])
    trim = RectangleObject([BLEED, BLEED, PAGE_W - BLEED, PAGE_H - BLEED])
    page.mediabox = media
    page.cropbox = media
    page.bleedbox = media
    page.trimbox = trim
    page.artbox = trim
    return page


def blank_page(like):
    p = PageObject.create_blank_page(width=float(like.mediabox.width), height=float(like.mediabox.height))
    return p


def assemble(toc, pages):
    cover = PdfReader(OUT / "cover.pdf")
    front = PdfReader(OUT / "front.pdf")
    body = PdfReader(OUT / "body.pdf")
    fpages = list(front.pages)
    if len(fpages) % 2:                 # 前置部分凑足偶数页，正文第 1 页落在右页
        fpages.append(blank_page(fpages[0]))
    bpages = list(body.pages)
    if len(bpages) % 2:                 # 正文凑足偶数页，全书最后一页是左页
        bpages.append(blank_page(bpages[0]))

    def write(dst, seq, labels, outline):
        w = PdfWriter()
        for p in seq:
            w.add_page(set_boxes(p))
        for start, end, style, prefix, first in labels:
            w.set_page_label(start, len(seq) - 1 if end is None else end, style=style, prefix=prefix, start=first)
        parents = []
        for title, idx, lvl in outline:
            lvl = int(lvl)
            parent = parents[lvl - 2] if lvl >= 2 and len(parents) >= lvl - 1 else None
            item = w.add_outline_item(title, idx, parent=parent)
            parents = parents[:lvl - 1] + [item]
        w.add_metadata({"/Title": f"{BOOK}（项目一～项目二）", "/Author": "冯丽娜", "/Subject": "高职高专C语言程序设计教材",
                        "/Keywords": "C语言; 人工智能; 任务驱动; 小熊猫C++", "/Creator": "HTML/CSS + Chromium; 后处理 pypdf"})
        w.page_mode = "/UseOutlines"
        with open(dst, "wb") as f:
            w.write(f)

    nf = len(fpages)
    plain = lambda t: re.sub(r"<[^>]+>", "", t).replace("　", " ")
    # 完整版：封面 + 封二（空白） + 前置部分 + 正文
    seq = [cover.pages[0], blank_page(cover.pages[0])] + fpages + bpages
    off = 2 + nf
    outline = [("封面", 0, 1)]
    ftexts = [squash(t)[:60] for t in page_texts(OUT / "front.pdf")]
    for name in ("前言", "本书使用说明", "目录"):
        i = next((i for i, t in enumerate(ftexts) if name in t), None)
        if i is not None:
            outline.append((name, 2 + i, 1))
    outline += [(plain(t), off + pages[i] - 1, lvl) for i, (lvl, t) in enumerate(toc) if i in pages]
    labels = [(0, 1, None, "封面", 1), (2, off - 1, "/r", None, 1), (off, None, "/D", None, 1)]
    write(OUT / "book.pdf", seq, labels, outline)
    # 印刷分文件：内文（前置部分 + 正文）、封面
    seq_in = list(PdfReader(OUT / "front.pdf").pages)
    if len(seq_in) % 2:
        seq_in.append(blank_page(seq_in[0]))
    body_in = list(PdfReader(OUT / "body.pdf").pages)
    if len(body_in) % 2:
        body_in.append(blank_page(body_in[0]))
    seq_in += body_in
    outline_in = [(t, i - 2, l) for t, i, l in outline if i >= 2]
    write(OUT / "interior.pdf", seq_in, [(0, nf - 1, "/r", None, 1), (nf, None, "/D", None, 1)], outline_in)
    write(OUT / "cover_print.pdf", [PdfReader(OUT / "cover.pdf").pages[0]], [], [])


def test(parts):
    """快速试排：只排指定的正文部分（不回填目录与页码），输出 out/test.pdf。"""
    defs = (ROOT / "parts" / "defs.html").read_text(encoding="utf-8")
    src = "\n".join((ROOT / "parts" / p).read_text(encoding="utf-8") for p in parts)
    src, toc, odd, refs = add_markers(preprocess(src))
    doc = head(BOOK) + defs + strip_markers(fill_prefs(with_blanks(src, set()), {})) + "</body></html>"
    (OUT / "test.html").write_text(doc, encoding="utf-8")
    render(OUT / "test.html", OUT / "test.pdf")
    print("test pages:", len(PdfReader(OUT / "test.pdf").pages))


def main():
    defs = (ROOT / "parts" / "defs.html").read_text(encoding="utf-8")
    toc, pages, refpages = build_body(defs)
    build_front(defs, toc, pages)
    render(ROOT / "parts" / "cover.html", OUT / "cover.pdf")
    assemble(toc, pages)
    print("toc:", [(t, pages.get(i)) for i, (l, t) in enumerate(toc)])
    print("refs:", refpages)
    print("done", OUT / "book.pdf")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "test":
        test(sys.argv[2:])
    else:
        main()
