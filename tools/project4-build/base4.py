# 项目三插图：生成 figs.html（每张图一个 id），再用 shot.js 截成 PNG
# 配色只用主色系：#1D4F91 主色、#153A6B 深、#4A75AE 中、#C5D3E7 浅线、#E8EEF7 浅底，加黑灰
import html

C, D, M, L, BG = '#1D4F91', '#153A6B', '#4A75AE', '#C5D3E7', '#E8EEF7'
FONT = "'Noto Sans CJK SC','Noto Sans SC',sans-serif"
MONO = "'DejaVu Sans Mono','Noto Sans Mono CJK SC',monospace"

MK = f'''<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{M}"/></marker></defs>'''


def esc(s):
    return html.escape(s)


def mtext(x, y, s, size=10.5, fill='#1F1F1F', weight=400, anchor='middle', lh=1.3, mono=False):
    """多行文字，以 y 为整体中线"""
    lines = s.split('\n')
    y0 = y - (len(lines) - 1) * size * lh / 2 + size * 0.36
    fam = f' font-family="{MONO}"' if mono else ''
    out = []
    for i, ln in enumerate(lines):
        out.append(f'<text x="{x}" y="{y0 + i * size * lh:.1f}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}"{fam}>{esc(ln)}</text>')
    return ''.join(out)


class FC:
    """简易流程图：节点以中心坐标定位"""

    def __init__(self, w, h, size=10.5):
        self.w, self.h, self.size = w, h, size
        self.n = {}
        self.el = []
        self.ln = []

    def _add(self, k, x, y, w, h):
        self.n[k] = (x, y, w, h)

    def term(self, k, x, y, s, w=80, h=26):
        self._add(k, x, y, w, h)
        self.el.append(f'<rect x="{x - w / 2}" y="{y - h / 2}" width="{w}" height="{h}" rx="{h / 2}" fill="#fff" stroke="{C}" stroke-width="1.4"/>' + mtext(x, y, s, self.size, D, 700))

    def proc(self, k, x, y, s, w=130, h=28, blank=False):
        self._add(k, x, y, w, h)
        if blank:
            self.el.append(f'<rect x="{x - w / 2}" y="{y - h / 2}" width="{w}" height="{h}" rx="2" fill="#fff" stroke="{C}" stroke-width="1.2" stroke-dasharray="4 3"/>' + mtext(x, y, s, self.size, D, 700))
        else:
            self.el.append(f'<rect x="{x - w / 2}" y="{y - h / 2}" width="{w}" height="{h}" rx="2" fill="{C}"/>' + mtext(x, y, s, self.size, '#fff', 700))

    def io(self, k, x, y, s, w=140, h=28):
        self._add(k, x, y, w, h)
        o = 9
        pts = f'{x - w / 2 + o},{y - h / 2} {x + w / 2},{y - h / 2} {x + w / 2 - o},{y + h / 2} {x - w / 2},{y + h / 2}'
        self.el.append(f'<polygon points="{pts}" fill="{BG}" stroke="{C}" stroke-width="1.3"/>' + mtext(x, y, s, self.size, D, 700))

    def dec(self, k, x, y, s, w=130, h=50):
        self._add(k, x, y, w, h)
        pts = f'{x},{y - h / 2} {x + w / 2},{y} {x},{y + h / 2} {x - w / 2},{y}'
        self.el.append(f'<polygon points="{pts}" fill="{BG}" stroke="{C}" stroke-width="1.3"/>' + mtext(x, y, s, self.size, D, 700))

    def box(self, k, x, y, s, w=130, h=28, fill='#fff', stroke=C, color=D, weight=400, dash=False, size=None):
        self._add(k, x, y, w, h)
        da = ' stroke-dasharray="4 3"' if dash else ''
        self.el.append(f'<rect x="{x - w / 2}" y="{y - h / 2}" width="{w}" height="{h}" rx="2" fill="{fill}" stroke="{stroke}" stroke-width="1.1"{da}/>' + mtext(x, y, s, size or self.size, color, weight))

    def p(self, k, side):
        x, y, w, h = self.n[k]
        return {'t': (x, y - h / 2), 'b': (x, y + h / 2), 'l': (x - w / 2, y), 'r': (x + w / 2, y)}[side]

    def line(self, pts, arrow=True):
        d = 'M' + ' L'.join(f'{a:.1f},{b:.1f}' for a, b in pts)
        mk = ' marker-end="url(#ar)"' if arrow else ''
        self.ln.append(f'<path d="{d}" fill="none" stroke="{M}" stroke-width="1.4"{mk}/>')

    def v(self, a, b):
        self.line([self.p(a, 'b'), self.p(b, 't')])

    def label(self, x, y, s, anchor='middle', size=None):
        self.el.append(mtext(x, y, s, size or self.size * 0.95, D, 700, anchor))

    def note(self, x, y, s, anchor='start', size=None, fill='#4D4D4D'):
        self.el.append(mtext(x, y, s, size or self.size * 0.9, fill, 400, anchor))

    def svg(self, extra=''):
        return f'<svg viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}" font-family="{FONT}">{MK}{"".join(self.ln)}{"".join(self.el)}{extra}</svg>'


figs = {}


# ------------------------------------------------------------------ 图3-1 报到流程（情境）
# 项目三第二稿新增与重画的插图（由 figs.py 末尾载入）
# 图标：微软 Fluent Emoji 3D（MIT 许可），assets/fe；插画：unDraw（免费商用、无需署名），assets/ud，主色已改为 #1D4F91
# 版式元素仍只用主色系和黑灰；彩色只出现在图标和插画里


def img(name, x, y, s, h=None):
    return f'<image href="assets/fe/{name}.png" x="{x}" y="{y}" width="{s}" height="{h or s}"/>'


def ud(name, x, y, w, h):
    return f'<image href="assets/ud/{name}.svg" x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet"/>'


def svgwrap(W, H, body, defs=''):
    return f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">{MK}{defs}{body}</svg>'


# ------------------------------------------------------------------ 角色头像（与书中小禾、C老师、小智头像同款，可变表情）
def eyes(x, y, r, mood, col):
    dx, ey = r * 0.34, y + r * 0.02
    if mood == 'dizzy':
        out = ''
        for sx in (x - dx, x + dx):
            out += f'<path d="M{sx - r*0.12},{ey} a{r*0.12},{r*0.12} 0 1 1 {r*0.12},{r*0.12} a{r*0.08},{r*0.08} 0 1 1 -{r*0.04},-{r*0.12}" fill="none" stroke="{col}" stroke-width="{r*0.06}"/>'
        return out
    if mood == 'happy':
        return ''.join(f'<path d="M{sx - r*0.11},{ey + r*0.04} q{r*0.11},-{r*0.16} {r*0.22},0" fill="none" stroke="{col}" stroke-width="{r*0.08}" stroke-linecap="round"/>' for sx in (x - dx, x + dx))
    rr = r * (0.11 if mood == 'shock' else 0.09)
    return ''.join(f'<circle cx="{sx}" cy="{ey}" r="{rr}" fill="{col}"/>' for sx in (x - dx, x + dx))


def mouth(x, y, r, mood, col):
    my = y + r * 0.38
    if mood in ('shock', 'dizzy'):
        return f'<ellipse cx="{x}" cy="{my}" rx="{r*0.1}" ry="{r*0.13}" fill="{col}"/>'
    if mood == 'happy':
        return f'<path d="M{x - r*0.24},{my - r*0.06} q{r*0.24},{r*0.34} {r*0.48},0 z" fill="{col}"/>'
    if mood == 'think':
        return f'<path d="M{x - r*0.16},{my} l{r*0.3},-{r*0.05}" stroke="{col}" stroke-width="{r*0.07}" stroke-linecap="round"/>'
    return f'<path d="M{x - r*0.22},{my - r*0.04} q{r*0.22},{r*0.2} {r*0.44},0" fill="none" stroke="{col}" stroke-width="{r*0.08}" stroke-linecap="round"/>'


def av_he(x, y, r, mood='smile'):
    """小禾：浅蓝脸、深蓝头发"""
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{BG}" stroke="{C}" stroke-width="{r*0.07}"/>'
            f'<path d="M{x - r*0.97},{y - r*0.12} A{r},{r} 0 0 1 {x + r*0.97},{y - r*0.12} Q{x + r*0.5},{y - r*0.42} {x - r*0.2},{y - r*0.38} Q{x - r*0.7},{y - r*0.34} {x - r*0.97},{y - r*0.12} z" fill="{C}"/>'
            f'<path d="M{x + r*0.55},{y - r*0.8} q{r*0.3},-{r*0.14} {r*0.42},{r*0.08} q-{r*0.2},-{r*0.02} -{r*0.3},{r*0.1} z" fill="{C}"/>'
            + eyes(x, y, r, mood, C) + mouth(x, y, r, mood, C))


def av_zhi(x, y, r, mood='smile'):
    """小智：蓝色机器人"""
    return (f'<line x1="{x}" y1="{y - r*0.75}" x2="{x}" y2="{y - r*1.05}" stroke="{M}" stroke-width="{r*0.08}"/>'
            f'<circle cx="{x}" cy="{y - r*1.1}" r="{r*0.13}" fill="{L}" stroke="{M}" stroke-width="{r*0.05}"/>'
            f'<rect x="{x - r*1.02}" y="{y - r*0.3}" width="{r*0.2}" height="{r*0.55}" rx="{r*0.06}" fill="{M}"/>'
            f'<rect x="{x + r*0.82}" y="{y - r*0.3}" width="{r*0.2}" height="{r*0.55}" rx="{r*0.06}" fill="{M}"/>'
            f'<rect x="{x - r*0.85}" y="{y - r*0.75}" width="{r*1.7}" height="{r*1.4}" rx="{r*0.38}" fill="{C}"/>'
            f'<rect x="{x - r*0.62}" y="{y - r*0.5}" width="{r*1.24}" height="{r*0.88}" rx="{r*0.22}" fill="{D}"/>'
            f'<rect x="{x - r*0.38}" y="{y + r*0.72}" width="{r*0.76}" height="{r*0.24}" rx="{r*0.08}" fill="{D}"/>'
            + eyes(x, y - r*0.1, r * 0.9, mood, L) + mouth(x, y - r*0.18, r * 0.8, mood, L))


def bubble(x, y, w, h, text, tail, size=9.2, fill='#fff', stroke=C, color='#1F1F1F', weight=400):
    """对话气泡；tail = (尖端x, 尖端y)"""
    tx, ty = tail
    cx = min(max(tx, x + 12), x + w - 12)
    if ty > y + h:
        tp = f'M{cx - 6},{y + h - 0.5} L{tx},{ty} L{cx + 6},{y + h - 0.5}'
    elif ty < y:
        tp = f'M{cx - 6},{y + 0.5} L{tx},{ty} L{cx + 6},{y + 0.5}'
    else:
        cy = min(max(ty, y + 10), y + h - 10)
        ex = x + 0.5 if tx < x else x + w - 0.5
        tp = f'M{ex},{cy - 5} L{tx},{ty} L{ex},{cy + 5}'
    return (f'<path d="{tp}" fill="{fill}" stroke="{stroke}" stroke-width="1"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{fill}" stroke="{stroke}" stroke-width="1"/>'
            f'<path d="{tp}" fill="{fill}" stroke="none" transform="translate(0,0)"/>'
            + mtext(x + w / 2, y + h / 2, text, size, color, weight))


# ------------------------------------------------------------------ 图：新生报到闯关地图（重画情境图）
