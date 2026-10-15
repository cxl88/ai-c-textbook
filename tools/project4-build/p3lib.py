# 项目三 Word 生成工具：以项目一 v5 清洁版为模板，复制其中各类版式块（标题、正文、代码框、AI 卡片等），
# 换上新内容，保证与 v5 的样式、字号、配色完全一致。
import copy
import os
import unicodedata
import re
import shutil
from lxml import etree
from PIL import Image

NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
      'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
      'w14': 'http://schemas.microsoft.com/office/word/2010/wordml'}
W = '{%s}' % NS['w']
R_ = '{%s}' % NS['r']
XS = '{http://www.w3.org/XML/1998/namespace}space'
TEXTW = 5324475  # 版心宽（EMU），148 mm
FIGW = 520       # 插图 HTML 中 520 px = 版心宽


class Doc:
    def __init__(self, d):
        self.d = d
        self.doc = etree.parse(f'{d}/word/document.xml')
        self.body = self.doc.getroot().find(W + 'body')
        self.T = [k for k in self.body]
        self.rels = etree.parse(f'{d}/word/_rels/document.xml.rels')
        self.out = []
        self.docpr = 9000
        self.imgn = 0

    # ------------------------------------------------------------ 基础
    def clone(self, i):
        e = copy.deepcopy(self.T[i])
        for b in e.findall('.//' + W + 'bookmarkStart') + e.findall('.//' + W + 'bookmarkEnd'):
            b.getparent().remove(b)
        for x in e.iter():
            x.attrib.pop('{%s}paraId' % NS['w14'], None)
            x.attrib.pop('{%s}textId' % NS['w14'], None)
        return e

    def add(self, e):
        self.out.append(e)
        return e

    def finish(self, extra_media=()):
        sect = self.body.find(W + 'sectPr')
        for k in list(self.body):
            self.body.remove(k)
        n = 100
        for e in self.out:
            for dp in e.iter('{%s}docPr' % NS['wp']):
                n += 1
                dp.set('id', str(n))
                dp.set('name', f'图片 {n}')
                for c in dp.getparent().iter('{%s}cNvPr' % NS['pic']):
                    c.set('id', str(n))
            for t in e.iter(W + 't'):
                if t.text and t.text != t.text.strip():
                    t.set(XS, 'preserve')
            self.body.append(e)
        self.body.append(sect)
        self.doc.write(f'{self.d}/word/document.xml', xml_declaration=True, encoding='UTF-8', standalone=True)
        self.rels.write(f'{self.d}/word/_rels/document.xml.rels', xml_declaration=True, encoding='UTF-8', standalone=True)

    # ------------------------------------------------------------ 图片
    def add_image(self, png):
        self.imgn += 1
        ext = png.rsplit('.', 1)[-1].lower()
        name = f'p3_{self.imgn:02d}.{ext}'
        shutil.copy(png, f'{self.d}/word/media/{name}')
        root = self.rels.getroot()
        ids = [int(x.get('Id')[3:]) for x in root if x.get('Id', '').startswith('rId') and x.get('Id')[3:].isdigit()]
        rid = f'rId{max(ids) + 1}'
        el = etree.SubElement(root, '{http://schemas.openxmlformats.org/package/2006/relationships}Relationship')
        el.set('Id', rid)
        el.set('Type', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image')
        el.set('Target', f'media/{name}')
        return rid

    def set_drawing(self, dr, png, cx):
        iw, ih = Image.open(png).size
        cy = int(cx * ih / iw)
        ext = dr.find('.//{%s}extent' % NS['wp'])
        ext.set('cx', str(cx))
        ext.set('cy', str(cy))
        aext = dr.find('.//{%s}xfrm/{%s}ext' % (NS['a'], NS['a']))
        aext.set('cx', str(cx))
        aext.set('cy', str(cy))
        dr.find('.//{%s}blip' % NS['a']).set(R_ + 'embed', self.add_image(png))
        for e in dr.iter('{%s}docPr' % NS['wp'], '{%s}cNvPr' % NS['pic']):
            self.docpr += 1
            e.set('id', str(self.docpr))
            e.set('name', f'图片 {self.docpr}')


# ------------------------------------------------------------ 文字块（run）
def rpr(ascii=None, ea=None, color=None, sz=None, b=False, shd=None, u=None, bdr=None, spc=None):
    p = etree.Element(W + 'rPr')
    if ascii or ea:
        f = etree.SubElement(p, W + 'rFonts')
        f.set(W + 'hint', 'eastAsia')
        if ascii:
            for k in ('ascii', 'hAnsi', 'cs'):
                f.set(W + k, ascii)
        if ea:
            f.set(W + 'eastAsia', ea)
    if b:
        etree.SubElement(p, W + 'b')
        etree.SubElement(p, W + 'bCs')
    if color:
        etree.SubElement(p, W + 'color').set(W + 'val', color)
    if spc:  # 字符间距，单位 1/20 磅
        etree.SubElement(p, W + 'spacing').set(W + 'val', str(spc))
    if sz:
        etree.SubElement(p, W + 'sz').set(W + 'val', str(sz))
        etree.SubElement(p, W + 'szCs').set(W + 'val', str(sz))
    if u:
        e = etree.SubElement(p, W + 'u')
        e.set(W + 'val', u)
        e.set(W + 'color', '4D4D4D')
    if bdr:
        e = etree.SubElement(p, W + 'bdr')
        for k, v in (('val', 'single'), ('color', bdr), ('sz', '4'), ('space', '0')):
            e.set(W + k, v)
    if shd:
        e = etree.SubElement(p, W + 'shd')
        e.set(W + 'val', 'clear')
        e.set(W + 'color', 'auto')
        e.set(W + 'fill', shd)
    return p


def run(text, **kw):
    r = etree.Element(W + 'r')
    if kw:
        r.append(rpr(**kw))
    parts = text.split('\t')
    for i, s in enumerate(parts):
        if i:
            etree.SubElement(r, W + 'tab')
        if s:
            t = etree.SubElement(r, W + 't')
            t.text = s
            t.set(XS, 'preserve')
    return r


SONG = dict(ascii='Times New Roman', ea='宋体')
HEI = dict(ascii='Arial', ea='微软雅黑')
CTX = {
    # 上下文：普通、加粗、行内代码
    'body': (dict(), dict(HEI, b=True), dict(ascii='Consolas', ea='微软雅黑', color='153A6B', sz=19, shd='E8EEF7')),
    'list': (dict(SONG, color='1F1F1F', sz=21), dict(HEI, b=True, color='1F1F1F', sz=21), dict(ascii='Consolas', ea='微软雅黑', color='153A6B', sz=19, shd='E8EEF7')),
    'cell': (dict(SONG, color='1F1F1F', sz=18), dict(HEI, b=True, color='1F1F1F', sz=18), dict(ascii='Consolas', ea='微软雅黑', color='153A6B', sz=17, shd='E8EEF7')),
    'box': (dict(SONG, color='1F1F1F', sz=19), dict(HEI, b=True, color='1F1F1F', sz=19), dict(ascii='Consolas', ea='微软雅黑', color='153A6B', sz=17, shd='E8EEF7')),
    'desc': (dict(SONG, color='1F1F1F', sz=21), dict(HEI, b=True, color='1F1F1F', sz=21), dict(ascii='Consolas', ea='微软雅黑', color='153A6B', sz=19, shd='E8EEF7')),
    'dlg': (dict(SONG, color='1F1F1F', sz=20), dict(HEI, b=True, color='1F1F1F', sz=20), dict(ascii='Consolas', ea='微软雅黑', color='153A6B', sz=18, shd='E8EEF7')),
    'ai': (dict(HEI, color='1F1F1F', sz=19), dict(HEI, b=True, color='153A6B', sz=19), dict(ascii='Consolas', ea='微软雅黑', color='153A6B', sz=17, shd='E8EEF7')),
    'bubu': (dict(HEI, color='FFFFFF', sz=18), dict(HEI, b=True, color='FFFFFF', sz=18), dict(ascii='Consolas', ea='微软雅黑', color='FFFFFF', sz=17)),
    'buba': (dict(HEI, color='1F1F1F', sz=18), dict(HEI, b=True, color='153A6B', sz=18), dict(ascii='Consolas', ea='微软雅黑', color='153A6B', sz=17, shd='E8EEF7')),
    'small': (dict(HEI, color='4D4D4D', sz=17), dict(HEI, b=True, color='4D4D4D', sz=17), dict(ascii='Consolas', ea='微软雅黑', color='153A6B', sz=16)),
    'q': (dict(SONG, color='1F1F1F', sz=19), dict(HEI, b=True, color='1F1F1F', sz=19), dict(ascii='Consolas', ea='微软雅黑', color='153A6B', sz=17, shd='E8EEF7')),
    'opt': (dict(SONG, color='333333', sz=19), dict(HEI, b=True, color='333333', sz=19), dict(ascii='Consolas', ea='微软雅黑', color='153A6B', sz=17, shd='E8EEF7')),
}


def runs(text, ctx):
    """**粗体**、`代码`、[[占位]]（AI 话术中由学生替换的部分）、__填空__"""
    base, bold, code = CTX[ctx]
    out = []
    for seg in re.split(r'(\*\*.+?\*\*|`.+?`|\[\[.+?\]\]|__+)', text):
        if not seg:
            continue
        if seg.startswith('**'):
            out.append(run(seg[2:-2], **bold))
        elif seg.startswith('`'):
            out.append(run(seg[1:-1], **code))
        elif seg.startswith('[['):
            out.append(run(' ' + seg[2:-2] + ' ', **dict(base, color='1D4F91', u='dotted')))
        elif seg.startswith('__'):
            out.append(run('　' * (len(seg) // 2), **dict(base, u='single')))
        else:
            out.append(run(seg, **base))
    return out


def clear_runs(p):
    for k in list(p):
        if k.tag != W + 'pPr':
            p.remove(k)
    return p


def fill(p, text, ctx):
    clear_runs(p)
    for r in runs(text, ctx):
        p.append(r)
    return p


def cell_paras(tc):
    return tc.findall(W + 'p')


def set_cell(tc, texts, ctx, tpl=None):
    """把单元格里的段落换成 texts（每项一段），段落格式取 tpl 或单元格首段"""
    ps = cell_paras(tc)
    tpl = tpl if tpl is not None else ps[0]
    for p in ps:
        tc.remove(p)
    for t in texts:
        p = clear_runs(copy.deepcopy(tpl))
        if isinstance(t, list):
            for r in t:
                p.append(r)
        else:
            fill(p, t, ctx)
        tc.append(p)


# ------------------------------------------------------------ C 代码高亮（与 v5 代码框配色一致）
KW = r'\b(int|float|double|char|void|while|for|do|if|else|return)\b'
FN = r'\b(printf|scanf|main|getchar|putchar|pow|fflush)\b'


def cjk_split(s):
    return re.findall(r'[⺀-￿]+|[^⺀-￿]+', s)


def code_runs(line, state):
    out = []

    def emit(s, color, b=False):
        for ch in cjk_split(s):
            sz = 20 if ord(ch[0]) >= 0x2e80 else 18
            out.append(run(ch, ascii='Consolas', ea='微软雅黑', color=color, sz=sz, b=b))

    i = 0
    while i < len(line):
        if state['cm']:
            j = line.find('*/', i)
            if j < 0:
                emit(line[i:], '7B8594')
                return out
            emit(line[i:j + 2], '7B8594')
            state['cm'] = False
            i = j + 2
            continue
        rest = line[i:]
        if rest.startswith('/*'):
            state['cm'] = True
            continue
        if rest.startswith('//'):
            emit(rest, '7B8594')
            return out
        if rest.startswith('#'):
            m = re.match(r'#[^/]*', rest)
            emit(m.group(0), '1D4F91')
            i += len(m.group(0))
            continue
        if rest.startswith('"'):
            m = re.match(r'"(\\.|[^"\\])*"', rest)
            emit(m.group(0), '3F6FA6')
            i += len(m.group(0))
            continue
        m = re.match(KW, rest)
        if m:
            emit(m.group(0), '1D4F91', True)
            i += len(m.group(0))
            continue
        m = re.match(FN, rest)
        if m:
            emit(m.group(0), '153A6B')
            i += len(m.group(0))
            continue
        m = re.match(r'[A-Za-z_]\w*|\d+(\.\d+)?|\s+|.', rest)
        emit(m.group(0), '1A1A1A')
        i += len(m.group(0))
    return out


# 书中代码：英文字符用 Consolas 9 磅（字宽 0.55em），汉字和全角符号用微软雅黑 10 磅（见 code_runs），①等用微软雅黑 9 磅。
# 生成预览 PDF 时 LibreOffice 用 DejaVu Sans Mono（0.602em）代替 Consolas（build.sh 另生成一份预览用 docx）。
LATIN_EM = float(os.environ.get('CODE_LATIN_EM', '0.5498'))
# 汉字后面紧跟的空格：Word 用 Consolas 排（1 列）；LibreOffice 按前一个字符的文种改用中文字体，只有约 0.37 列
WEAK_SP = float(os.environ.get('CODE_WEAK_SP', '1'))


def _vw(s, r):
    """IDE 中的列数：汉字和全角符号占 r 列（源程序按 r = 2 对齐）"""
    return sum(r if unicodedata.east_asian_width(ch) in 'WF' else 1 for ch in s)


def _bw(s):
    """书中的宽度，以一个英文字符的宽度为 1 列"""
    w, prev = 0, ''
    for ch in s:
        if ord(ch) >= 0x2e80:
            w += 10 / 9 / LATIN_EM
        elif 0x2460 <= ord(ch) <= 0x24ff:
            w += 1 / LATIN_EM
        elif ch == ' ' and prev and ord(prev) >= 0x2460:
            w += WEAK_SP
            ch = prev  # 连续的空格同样处理
        else:
            w += 1
        prev = ch
    return w


def book_split(ln):
    """源程序按 IDE 习惯（汉字占 2 列）对齐行尾注释。代码部分含汉字时，排进书中要按书中字体重算注释前的空白：
    返回 (代码, 空格数, 每个空格加宽的磅数×20, 注释)；不需要调整时返回 None"""
    q, i = None, 0
    while i < len(ln):
        c = ln[i]
        if q:
            if c == '\\':
                i += 2
                continue
            if c == q:
                q = None
        elif c in '"\'':
            q = c
        elif ln.startswith('//', i):
            code = ln[:i].rstrip()
            if not code.strip() or _bw(code) == len(code):
                return None
            gap = _vw(ln[:i], 2) - _bw(code)  # 注释前应留的宽度（列）
            n = max(2, round(gap))
            spc = round((gap - n) * LATIN_EM * 9 * 20 / n) if gap > 2 else 0
            return code, n, spc, ln[i:]
        i += 1
    return None


def code_paras(tpl_p, src, numbers=True, start=1, wd=None, state=None):
    """start：首行的行号（摘录程序片段时与完整程序的行号一致）；wd、state 供分段排版时各段共用"""
    lines = src if isinstance(src, list) else src.rstrip('\n').split('\n')
    wd = wd or len(str(start + len(lines) - 1))
    state = state if state is not None else {'cm': False}
    ps = []
    for n, ln in enumerate(lines, start):
        p = clear_runs(copy.deepcopy(tpl_p))
        if numbers:
            p.append(run(str(n).rjust(wd) + '  ', ascii='Consolas', ea='微软雅黑', color='98A3B3', sz=18))
        sp = book_split(ln)
        if sp:
            code, n_sp, spc, cm = sp
            for r in code_runs(code, state):
                p.append(r)
            p.append(run(' ' * n_sp, ascii='Consolas', ea='微软雅黑', color='1A1A1A', sz=18, spc=spc or None))
            for r in code_runs(cm, state):
                p.append(r)
        else:
            for r in code_runs(ln, state):
                p.append(r)
        ps.append(p)
    return ps


def code_chunks(lines, maxlen=20, minlen=8):
    """长程序按空行分段：空行归入上一段，每段至少 minlen 行。
    在所有分法中选“最长一段最短”的（换页时页底留白最少），同样短时段数多者优先，再同样时前段长者优先。"""
    if len(lines) <= maxlen:
        return [lines]
    segs, cur = [], []
    for ln in lines:
        cur.append(ln)
        if not ln.strip():
            segs.append(cur)
            cur = []
    if cur:
        segs.append(cur)
    m = len(segs)
    best = {m: (0, 0, ())}  # best[i]：从第 i 段起到末尾的最优分法 (最长段, -段数, 各组起点)
    for i in range(m - 1, -1, -1):
        cand = []
        n = 0
        for j in range(i, m):
            n += len(segs[j])
            if n >= minlen and j + 1 in best:
                mx, neg, cuts = best[j + 1]
                cand.append((max(n, mx), neg - 1, -n, (i,) + cuts))
        if cand:
            c = min(cand)
            best[i] = (c[0], c[1], c[3])
    if 0 not in best:
        return [lines]
    cuts = best[0][2] + (m,)
    return [sum(segs[cuts[k]:cuts[k + 1]], []) for k in range(len(cuts) - 1)]


# ------------------------------------------------------------ 版式块（模板序号取自 v5 清洁版）
class Book(Doc):
    def title(self, s):
        p = clear_runs(self.clone(0))
        p.append(run(s, sz=32))
        return self.add(p)

    def sec(self, s, before=None):
        p = clear_runs(self.clone(1))
        if before:
            p.find(W + 'pPr/' + W + 'spacing').set(W + 'before', str(before))
        p.append(run(s))
        return self.add(p)

    def task(self, no, name):
        p = self.clone(17)
        rs = p.findall(W + 'r')
        rs[0].find(W + 't').text = f' {no} '
        rs[2].find(W + 't').text = name
        return self.add(p)

    def sub(self, s):
        return self.add(fill(self.clone(18), s, 'body'))

    def h1(self, s):
        return self.add(fill(self.clone(23), s, 'body'))

    def h2(self, s):
        return self.add(fill(self.clone(25), s, 'body'))

    def p(self, s):
        return self.add(fill(self.clone(24), s, 'body'))

    def bul(self, s):
        return self.add(fill(self.clone(33), s, 'list'))

    def lead(self, label, s):
        return self.add(fill(self.clone(45), f'**{label}**{s}', 'list'))

    def spacer(self):
        return self.add(self.clone(7))

    def note(self, s):
        return self.add(fill(self.clone(5), s, 'small'))

    def note2(self, s):
        """表下注（与 v5 表1-6 注一致）"""
        return self.add(fill(self.clone(154), s, 'small'))

    def fig(self, png, cap, frac=None, css_w=None):
        """frac：占版心宽比例；css_w：按 HTML 像素（520 = 版心宽）"""
        p = self.clone(3)
        if frac is None:
            w = Image.open(png).size[0] / 4
            frac = (css_w or w) / FIGW
        self.set_drawing(p.find('.//' + W + 'drawing'), png, int(TEXTW * min(frac, 1)))
        self.add(p)
        if cap:
            self.cap(cap)

    def cap(self, s):
        p = clear_runs(self.clone(4))
        no, _, txt = s.partition(' ')
        p.append(run(no, **HEI, b=True, color='153A6B', sz=18))
        p.append(run('  ', **HEI, sz=18))
        p.append(run(txt, **HEI, color='4D4D4D', sz=18))
        return self.add(p)

    def tcap(self, s):
        p = clear_runs(self.clone(82))
        no, _, txt = s.partition(' ')
        p.append(run(no, **HEI, b=True, color='153A6B', sz=18))
        p.append(run('  ', **HEI, sz=18))
        p.append(run(txt, **HEI, color='4D4D4D', sz=18))
        return self.add(p)

    def runimg(self, png, label='运行结果：'):
        if label:
            lp = fill(self.clone(97), f'**{label}**', 'body')
            lp.find(W + 'pPr').insert(1, etree.Element(W + 'keepNext'))
            self.add(lp)
        p = self.clone(98)
        sp = p.find(W + 'pPr/' + W + 'spacing')
        sp.set(W + 'line', '240')
        sp.set(W + 'lineRule', 'auto')
        w = Image.open(png).size[0] / 4 * 0.86
        self.set_drawing(p.find('.//' + W + 'drawing'), png, int(TEXTW * w / FIGW))
        return self.add(p)

    def say(self, who, s):
        i = {'小禾': 6, 'C老师': 8, '小智': 10}[who]
        t = self.clone(i)
        tc = t.findall('.//' + W + 'tc')[2]
        set_cell(tc, [[run(who + '：', **HEI, b=True, color='153A6B', sz=20)] + runs(s, 'dlg')], 'dlg')
        self.add(t)
        self.spacer()

    def goals(self, k, a, s):
        t = self.clone(13)
        tcs = t.findall('.//' + W + 'tc')
        for tc, title, items in ((tcs[0], '知识目标', k), (tcs[2], '能力目标', a), (tcs[4], '素养目标', s)):
            ps = cell_paras(tc)
            head, tpl = ps[0], ps[1]
            set_cell(tc, [], 'cell')
            tc.append(head)
            for it in items:
                tc.append(fill(copy.deepcopy(tpl), it, 'cell'))
        for p in t.iter(W + 'p'):
            pass
        return self.add(t)

    def desc(self, s):
        t = self.clone(19)
        set_cell(t.find('.//' + W + 'tc'), s if isinstance(s, list) else [s], 'desc')
        return self.add(t)

    def step(self, tag, s):
        p = self.clone(73)
        rs = p.findall(W + 'r')
        rs[0].find(W + 't').text = f'  {tag}  '
        for r in rs[2:]:
            p.remove(r)
        p.append(run(s, **HEI, b=True, color='153A6B', sz=21))
        return self.add(p)

    def ex(self, no, s):
        p = clear_runs(self.clone(95))
        p.append(run(no, **HEI, b=True, color='1F1F1F', sz=21))
        for r in runs('　' + s, 'desc'):
            p.append(r)
        return self.add(p)

    def code(self, src, title=None, start=1):
        """程序框。20 行以内整段排（不跨页）；更长的程序按空行分成若干段（每段至少 8 行），
        每段是一个不可拆分的表格行，只在段与段之间换页，换页后自动重复标题行（与 v4 的跨页规则一致）。
        代码行不设“与下段同页”（标题行保留），运行结果可以排到下一页，避免页底大片空白。"""
        lines = src.rstrip('\n').split('\n')
        if title:
            t = self.clone(175)
            tr = t.findall(W + 'tr')
            set_cell(tr[0].find(W + 'tc'), [[run(title, **HEI, b=True, color='153A6B', sz=16)]], 'cell')
            row = tr[1]
        else:
            t = self.clone(96)
            row = t.findall(W + 'tr')[0]
        tc = row.find(W + 'tc')
        tpl = cell_paras(tc)[0]
        wd = len(str(start + len(lines) - 1))
        state = {'cm': False}
        parts = code_chunks(lines) if title else [lines]
        n = start
        for k, part in enumerate(parts):
            r = copy.deepcopy(row) if k else row
            c = r.find(W + 'tc')
            for p in cell_paras(c):
                c.remove(p)
            ps = code_paras(tpl, part, start=n, wd=wd, state=state)
            for p in ps:  # 行内段落不设“与下段同页”，否则 Word、LibreOffice 会把整个程序框连同后文一起推到下一页
                kn = p.find(W + 'pPr/' + W + 'keepNext')
                if kn is not None:
                    kn.getparent().remove(kn)
            for p in ps:
                c.append(p)
            if k:
                mar = c.find(W + 'tcPr/' + W + 'tcMar/' + W + 'top')
                if mar is not None:
                    mar.set(W + 'w', '0')
                t.append(r)
            n += len(part)
        return self.add(t)

    def table(self, header, rows, widths, heights=420, ctx='cell', head_ctx=None):
        """heights：数据行的最小行高（缇），可为列表；项目四默认 420，比 v5 模板的 737 紧凑"""
        t = self.clone(83)
        trs = t.findall(W + 'tr')
        total = sum(int(g.get(W + 'w')) for g in t.find(W + 'tblGrid'))
        ws = [int(total * w / sum(widths)) for w in widths]
        ws[-1] = total - sum(ws[:-1])
        grid = t.find(W + 'tblGrid')
        for g in list(grid):
            grid.remove(g)
        for w in ws:
            etree.SubElement(grid, W + 'gridCol').set(W + 'w', str(w))
        htr, btr = trs[0], trs[1]
        hc, bc = htr.find(W + 'tc'), btr.find(W + 'tc')
        for tr in trs:
            t.remove(tr)

        def mkrow(tpl_tr, tpl_tc, cells, head, h=None):
            tr = copy.deepcopy(tpl_tr)
            for tc in tr.findall(W + 'tc'):
                tr.remove(tc)
            if h:
                trpr = tr.find(W + 'trPr')
                if trpr is None:
                    trpr = etree.SubElement(tr, W + 'trPr')
                    tr.insert(0, trpr)
                e = trpr.find(W + 'trHeight')
                if e is None:
                    e = etree.SubElement(trpr, W + 'trHeight')
                e.set(W + 'val', str(h))
                e.set(W + 'hRule', 'atLeast')
            for w, c in zip(ws, cells):
                tc = copy.deepcopy(tpl_tc)
                tc.find(W + 'tcPr/' + W + 'tcW').set(W + 'w', str(w))
                if head:
                    set_cell(tc, [[run(c, **HEI, b=True, color='153A6B', sz=18)]], 'cell')
                else:
                    set_cell(tc, c if isinstance(c, list) else [c], ctx)
                tr.append(tc)
            t.append(tr)

        mkrow(htr, hc, header, True)
        for i, r in enumerate(rows):
            mkrow(btr, bc, r, False, heights[i] if isinstance(heights, list) else heights)
        return self.add(t)

    def _box(self, i, title, items, ctx='box', icon=None, note=None, numbered=False):
        t = self.clone(i)
        tc = t.find('.//' + W + 'tc')
        ps = cell_paras(tc)
        head, tpl = ps[0], ps[1]
        hr = [r for r in head.findall(W + 'r') if r.find(W + 't') is not None]
        hr[0].find(W + 't').text = title
        for r in hr[1:]:
            if note is not None and r.find(W + 't').text and r is hr[-1]:
                r.find(W + 't').text = note
            elif note is None:
                head.remove(r)
        if icon:
            self.set_drawing(head.find('.//' + W + 'drawing'), icon,
                             int(head.find('.//{%s}extent' % NS['wp']).get('cx')))
        for p in ps:
            tc.remove(p)
        tc.append(head)
        for k, it in enumerate(items, 1):
            p = copy.deepcopy(tpl)
            if numbered:
                ppr = p.find(W + 'pPr')
                n = ppr.find(W + 'numPr')
                if n is not None:
                    ppr.remove(n)
                ind = ppr.find(W + 'ind')
                if ind is None:
                    ind = etree.SubElement(ppr, W + 'ind')
                ind.set(W + 'left', '300')
                ind.set(W + 'hanging', '300')
                it = f'{k}．' + it
            tc.append(fill(p, it, ctx))
        self.add(t)
        self.spacer()

    def check(self, items):
        self._box(86, '课堂验收', items, note='由老师或同伴当场检查')

    def practice(self, items, icon):
        self._box(86, '课堂练习', items, icon=icon, note='先独立完成，再同桌互查', numbered=True)

    def tip(self, title, items):
        self._box(140, title, items)

    def warn(self, title, items):
        self._box(133, title, items)

    def aisum(self, title, items):
        self._box(217, title, items)

    def aicard(self, title, lines, tip=None, tool='DeepSeek / 豆包'):
        t = self.clone(69)
        trs = t.findall(W + 'tr')
        hp = cell_paras(trs[0].find(W + 'tc'))[0]
        hr = [r for r in hp.findall(W + 'r') if r.find(W + 't') is not None]
        hr[0].find(W + 't').text = title
        hr[-1].find(W + 't').text = tool
        tc = trs[1].find(W + 'tc')
        ps = cell_paras(tc)
        tpl, tipp = ps[0], ps[-1]
        for p in ps:
            tc.remove(p)
        for tag, s in lines:
            p = clear_runs(copy.deepcopy(tpl))
            p.append(run(f' {tag} ', **HEI, color='153A6B', sz=15, bdr='C5D3E7', shd='E8EEF7'))
            p.append(run(' ', **HEI, sz=15))
            for r in runs(s, 'ai'):
                p.append(r)
            tc.append(p)
        if tip:
            tc.append(fill(clear_runs(copy.deepcopy(tipp)), tip, 'small'))
        self.add(t)
        self.spacer()

    def aidlg(self, msgs, note='编写整理的示例，实际回答会有所不同'):
        """msgs：[('u', 文字), ('a', [段落…])]"""
        t = self.clone(77)
        trs = t.findall(W + 'tr')
        hp = cell_paras(trs[0].find(W + 'tc'))[0]
        hr = [r for r in hp.findall(W + 'r') if r.find(W + 't') is not None]
        hr[-1].find(W + 't').text = note
        tc = trs[1].find(W + 'tc')
        kids = [k for k in tc if k.tag != W + 'tcPr']
        utpl, sp, atpl = kids[0], kids[1], kids[2]
        for k in kids:
            tc.remove(k)
        for i, (who, s) in enumerate(msgs):
            if i:
                tc.append(copy.deepcopy(sp))
            tb = copy.deepcopy(utpl if who == 'u' else atpl)
            cells = tb.findall('.//' + W + 'tc')
            bub = cells[1] if who == 'u' else cells[2]
            paras = s if isinstance(s, list) else [s]
            set_cell(bub, paras, 'bubu' if who == 'u' else 'buba')
            for e in tb.iter('{%s}docPr' % NS['wp'], '{%s}cNvPr' % NS['pic']):
                self.docpr += 1
                e.set('id', str(self.docpr))
            tc.append(tb)
        tc.append(copy.deepcopy(sp))
        self.add(t)
        self.spacer()

    def train(self, label, s):
        p = clear_runs(self.clone(180))
        p.append(run(label, **HEI, b=True, color='1F1F1F', sz=21))
        for r in runs(s, 'desc'):
            p.append(r)
        return self.add(p)

    def line(self, s):
        """填写行（与 v5 训练 1 的“填写：①___”一致）"""
        return self.add(fill(self.clone(184), s, 'desc'))

    def q(self, s):
        return self.add(fill(self.clone(219), s, 'q'))

    def opts(self, *xs):
        return self.add(fill(self.clone(222), '\t'.join(xs), 'opt'))

    def pagebreak(self):
        p = etree.Element(W + 'p')
        r = etree.SubElement(p, W + 'r')
        etree.SubElement(r, W + 'br').set(W + 'type', 'page')
        return self.add(p)


# ------------------------------------------------------------ 第二稿新增：趣味栏目
def _fun(self, title, items, icon):
    """趣味小站：沿用“小智提示”底色框，换成彩色图标"""
    self._box(140, title, items, icon=icon)


def _activity(self, title, items, icon, note):
    """课堂活动 / 小游戏：沿用“课堂练习”边框框，换成彩色图标"""
    self._box(86, title, items, icon=icon, note=note, numbered=True)


Book.fun = _fun
Book.activity = _activity
