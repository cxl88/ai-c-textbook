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
def f_scene():
    st = [('核验录取信息', '报到大厅'), ('核对专业班级', '学院迎新点'), ('领取校园一卡通\n与新生物资', '物资发放点'),
          ('办理入住登记', '宿舍楼值班室'), ('领取宿舍钥匙', '宿舍楼值班室'), ('确认床位信息', '宿舍房间'), ('录入学籍信息', '学籍登记处')]
    W, H = 520, 196
    out = []
    pos = [(16 + i * 128, 18) for i in range(4)] + [(16 + (3 - i) * 128, 112) for i in range(3)]
    for i, ((t, where), (x, y)) in enumerate(zip(st, pos)):
        out.append(f'<rect x="{x}" y="{y}" width="104" height="66" rx="5" fill="{BG}" stroke="{L}" stroke-width="1"/>')
        out.append(f'<circle cx="{x + 14}" cy="{y + 14}" r="9" fill="{C}"/>' + mtext(x + 14, y + 14, str(i + 1), 10, '#fff', 700))
        out.append(mtext(x + 56, y + 36, t, 10.2, D, 700))
        out.append(mtext(x + 56, y + 57, where, 8.4, '#666'))
    ar = []
    for i in range(3):
        x = 16 + i * 128 + 104
        ar.append(f'<path d="M{x + 3},51 L{x + 21},51" stroke="{M}" stroke-width="1.6" marker-end="url(#ar)"/>')
    ar.append(f'<path d="M{16 + 3 * 128 + 52},87 L{16 + 3 * 128 + 52},109" stroke="{M}" stroke-width="1.6" marker-end="url(#ar)"/>')
    for i in range(2):
        x = 16 + (3 - i) * 128
        ar.append(f'<path d="M{x - 3},145 L{x - 21},145" stroke="{M}" stroke-width="1.6" marker-end="url(#ar)"/>')
    # 完成
    x = 16
    out.append(f'<path d="M{x + 128 - 3},145 L{x + 128 - 21},145" stroke="{M}" stroke-width="1.6" marker-end="url(#ar)"/>'.replace(f'M{x + 128 - 3}', f'M{x + 128 - 3}'))
    out = out[:-1]
    out.append(f'<rect x="20" y="118" width="96" height="54" rx="27" fill="#fff" stroke="{C}" stroke-width="1.4"/>' + mtext(68, 138, '报到完成', 11, D, 700) + mtext(68, 157, '开启大学生活', 8.6, '#666'))
    ar.append(f'<path d="M{16 + 128 - 3},145 L{120},145" stroke="{M}" stroke-width="1.6" marker-end="url(#ar)"/>')
    return f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">{MK}{"".join(ar)}{"".join(out)}</svg>'


figs['f_scene'] = f_scene()


# ------------------------------------------------------------------ 图3-2 知识导图
def kmap():
    tasks = [("任务一 认知算法与执行步骤", ["程序 = 算法 + 数据结构", "算法的概念：解决问题的方法和步骤", "算法举例：累加求和、判断闰年、辗转相除", "算法的五个特征", "算法的表示：自然语言、流程图", "任务实施：梳理新生报到流程"]),
             ("任务二 辨析程序三大控制结构", ["顺序结构：从上到下依次执行", "选择结构：按条件选一条路走", "循环结构：条件满足就重复执行", "结构化程序设计：自顶向下、逐步细化", "任务实施：组合三种结构检测电阻"]),
             ("AI升华 用算法特征检验 AI 程序", ["用算法特征检查 AI 的答案", "手动跟踪循环，找出死循环"])]
    y = 14
    centers, lines, texts, dots = [], [], [], []
    for name, leaves in tasks:
        ys = [y + 20 * i for i in range(len(leaves))]
        c = (ys[0] + ys[-1]) / 2
        centers.append(c)
        for ly, t in zip(ys, leaves):
            lines.append(f'<path d="M318 {c} C330 {c} 330 {ly} 344 {ly}"/>')
            texts.append(f'<text x="349" y="{ly + 3.4}">{esc(t)}</text>')
            dots.append(f'<circle cx="344" cy="{ly}" r="1.8"/>')
        y = ys[-1] + 30
    H = y - 14
    mid = (centers[0] + centers[-1]) / 2
    for c in centers:
        lines.append(f'<path d="M128 {mid} C150 {mid} 150 {c} 168 {c}"/>')
    boxes = []
    for (name, _), c in zip(tasks, centers):
        boxes.append(f'<rect x="168" y="{c - 15}" width="150" height="30" rx="3" fill="{BG}" stroke="{C}" stroke-width="0.8"/><text x="243" y="{c + 3.6}" fill="{D}">{esc(name)}</text>')
    return f'''<svg viewBox="0 0 540 {H}" width="540" height="{H}" font-family="{FONT}">
<g stroke="#9DB3D3" stroke-width="1.3" fill="none">{''.join(lines)}</g>
<rect x="8" y="{mid - 25}" width="120" height="50" rx="4" fill="{C}"/>
<text x="68" y="{mid - 4}" fill="#fff" font-size="13" font-weight="700" text-anchor="middle">项目三</text>
<text x="68" y="{mid + 14}" fill="#fff" font-size="10.5" text-anchor="middle">梳理程序执行逻辑</text>
<g font-size="9.6" font-weight="700" text-anchor="middle">{''.join(boxes)}</g>
<g font-size="9.4" fill="#1F1F1F">{''.join(texts)}</g>
<g fill="{C}">{''.join(dots)}</g></svg>'''


figs['f_kmap'] = kmap()


# ------------------------------------------------------------------ 图3-3 程序 = 算法 + 数据结构
def f_prog():
    W, H = 520, 210
    out = []

    def card(x, y, w, h, title, body, dark=False):
        f, tc, bc = (C, '#fff', '#fff') if dark else (BG, D, '#1F1F1F')
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{f}" stroke="{C}" stroke-width="1"/>')
        out.append(mtext(x + w / 2, y + 15, title, 10.2, tc, 700))
        out.append(f'<line x1="{x + 8}" y1="{y + 26}" x2="{x + w - 8}" y2="{y + 26}" stroke="{"#fff" if dark else L}" stroke-width="0.8"/>')
        out.append(mtext(x + w / 2, y + 26 + (h - 26) / 2, body, 9, bc))

    def sym(x, y, s):
        out.append(mtext(x, y, s, 20, C, 700))

    out.append(mtext(14, 18, '做菜', 10, '#666', 700, 'start'))
    card(14, 26, 140, 74, '食材（数据）', '番茄 2 个、鸡蛋 3 个\n盐、油')
    sym(168, 63, '+')
    card(182, 26, 168, 74, '菜谱（算法）', '① 打蛋　② 炒蛋盛出\n③ 炒番茄　④ 倒回鸡蛋、加盐')
    sym(364, 63, '=')
    card(378, 26, 128, 74, '一道菜', '番茄炒蛋', True)
    out.append(mtext(14, 120, '编程', 10, '#666', 700, 'start'))
    card(14, 128, 140, 74, '数据（项目二已学）', '成绩 c、math、eng\n总分 total、平均分 avg')
    sym(168, 165, '+')
    card(182, 128, 168, 74, '算法（本项目学习）', '① 输入三门成绩　② 求总分\n③ 求平均分　④ 输出结果')
    sym(364, 165, '=')
    card(378, 128, 128, 74, '程序', 'avg.c\n（见例3-1）', True)
    return f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">{"".join(out)}</svg>'


figs['f_prog'] = f_prog()


# ------------------------------------------------------------------ 图3-4 交换两杯饮料
def f_swap():
    W, H = 520, 150
    out = [MK]
    cola, juice = D, L

    def cup(x, y, name, fill, label):
        # 杯子：上宽下窄的梯形
        out.append(f'<path d="M{x},{y} L{x + 36},{y} L{x + 31},{y + 46} L{x + 5},{y + 46} Z" fill="#fff" stroke="#555" stroke-width="1.1"/>')
        if fill:
            out.append(f'<path d="M{x + 1.6},{y + 12} L{x + 34.4},{y + 12} L{x + 30.6},{y + 45} L{x + 5.4},{y + 45} Z" fill="{fill}"/>')
        out.append(mtext(x + 18, y + 58, name, 9, D, 700))
        out.append(mtext(x + 18, y + 71, label, 8.2, '#555'))

    titles = ['开始', '第 1 步：A 倒入 C', '第 2 步：B 倒入 A', '第 3 步：C 倒入 B']
    states = [(cola, juice, None), (None, juice, cola), (juice, None, cola), (juice, cola, None)]
    for i, (t, (a, b, c)) in enumerate(zip(titles, states)):
        x0 = 8 + i * 130
        out.append(f'<rect x="{x0}" y="8" width="120" height="132" rx="4" fill="#FAFBFD" stroke="{L}" stroke-width="0.9"/>')
        out.append(mtext(x0 + 60, 24, t, 9.6, D, 700))
        nm = lambda f: '可乐' if f == cola else ('果汁' if f == juice else '空')
        cup(x0 + 4, 44, 'A 杯', a, nm(a))
        cup(x0 + 42, 44, 'B 杯', b, nm(b))
        cup(x0 + 80, 44, 'C 杯', c, nm(c))
    for i in range(3):
        x = 8 + i * 130 + 120
        out.append(f'<path d="M{x + 1},74 L{x + 9},74" stroke="{M}" stroke-width="1.5" marker-end="url(#ar)"/>')
    return f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">{"".join(out)}</svg>'


figs['f_swap'] = f_swap()


# ------------------------------------------------------------------ 图3-5 算法的五个特征
def icon(kind):
    s = f'<svg viewBox="0 0 40 40" width="40" height="40">'
    if kind == 'finite':
        s += f'<circle cx="20" cy="20" r="18" fill="{BG}"/><path d="M11 22a9 9 0 1 1 9 9" fill="none" stroke="{C}" stroke-width="2.6"/><path d="M20 27v8l5-4z" fill="{C}"/><rect x="24" y="24" width="11" height="11" rx="2" fill="{D}"/><path d="M27 29.5h5" stroke="#fff" stroke-width="2"/>'
    elif kind == 'definite':
        s += f'<circle cx="20" cy="20" r="18" fill="{BG}"/><circle cx="20" cy="20" r="11" fill="none" stroke="{C}" stroke-width="2.4"/><circle cx="20" cy="20" r="5" fill="none" stroke="{C}" stroke-width="2.4"/><circle cx="20" cy="20" r="1.8" fill="{D}"/>'
    elif kind == 'feasible':
        s += f'<circle cx="20" cy="20" r="18" fill="{BG}"/><path d="M12 21l6 6 11-13" fill="none" stroke="{C}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>'
    elif kind == 'input':
        s += f'<circle cx="20" cy="20" r="18" fill="{BG}"/><rect x="21" y="11" width="11" height="18" rx="2" fill="none" stroke="{C}" stroke-width="2.2"/><path d="M7 20h12" stroke="{C}" stroke-width="2.4"/><path d="M15 15l5 5-5 5" fill="none" stroke="{C}" stroke-width="2.4"/>'
    else:
        s += f'<circle cx="20" cy="20" r="18" fill="{BG}"/><rect x="8" y="11" width="11" height="18" rx="2" fill="none" stroke="{C}" stroke-width="2.2"/><path d="M21 20h12" stroke="{C}" stroke-width="2.4"/><path d="M28 15l5 5-5 5" fill="none" stroke="{C}" stroke-width="2.4"/>'
    return s + '</svg>'


def f_feat():
    items = [('finite', '有穷性', '步骤有限，能在有限时间内结束', '洗发水说明“涂抹、冲洗、重复”，没说重复几次，照做就停不下来'),
             ('definite', '确定性', '每一步含义明确，不会有两种理解', '“加盐适量”：多少算适量？不同的人做法不同'),
             ('feasible', '可行性', '每一步都能实际做到', '“用 10 除以 0”“1 秒内从宿舍跑到图书馆”都做不到'),
             ('input', '有零个或多个输入', '从外界获得要处理的数据', '求平均分要先输入成绩；打印“欢迎新生”则不需要输入'),
             ('output', '有一个或多个输出', '至少给出一个结果', '算了半天却不显示平均分，这个算法就没有意义')]
    cards = []
    for k, t, d, ex in items:
        cards.append(f'<div class="fc"><div class="fh">{icon(k)}<b>{t}</b></div><div class="fd">{d}</div><div class="fx"><span>反例</span>{ex}</div></div>')
    return '<div class="feat">' + ''.join(cards) + '</div>'


figs['f_feat'] = f_feat()


# ------------------------------------------------------------------ 图3-6 流程图常用符号
def f_sym():
    W, H = 520, 196
    rows = [('起止框', '表示算法的开始和结束', 'term'), ('输入输出框', '表示输入数据或输出结果', 'io'), ('处理框', '表示计算、赋值等处理', 'proc'),
            ('判断框', '根据条件是否成立，选择一个出口', 'dec'), ('流程线', '表示执行的先后顺序', 'line'), ('连接点', '把画在不同位置的流程线连接起来', 'conn')]
    out = [MK]
    for i, (n, d, k) in enumerate(rows):
        col, row = i % 2, i // 2
        x0, y0 = 8 + col * 258, 8 + row * 62
        out.append(f'<rect x="{x0}" y="{y0}" width="248" height="54" rx="4" fill="#FAFBFD" stroke="{L}" stroke-width="0.9"/>')
        cx, cy = x0 + 48, y0 + 27
        if k == 'term':
            out.append(f'<rect x="{cx - 34}" y="{cy - 12}" width="68" height="24" rx="12" fill="#fff" stroke="{C}" stroke-width="1.4"/>')
        elif k == 'io':
            out.append(f'<polygon points="{cx - 28},{cy - 12} {cx + 36},{cy - 12} {cx + 28},{cy + 12} {cx - 36},{cy + 12}" fill="{BG}" stroke="{C}" stroke-width="1.3"/>')
        elif k == 'proc':
            out.append(f'<rect x="{cx - 34}" y="{cy - 12}" width="68" height="24" rx="2" fill="{C}"/>')
        elif k == 'dec':
            out.append(f'<polygon points="{cx},{cy - 18} {cx + 36},{cy} {cx},{cy + 18} {cx - 36},{cy}" fill="{BG}" stroke="{C}" stroke-width="1.3"/>')
        elif k == 'line':
            out.append(f'<path d="M{cx - 30},{cy - 8} L{cx + 4},{cy - 8} L{cx + 4},{cy + 10} L{cx + 30},{cy + 10}" fill="none" stroke="{M}" stroke-width="1.5" marker-end="url(#ar)"/>')
        else:
            out.append(f'<circle cx="{cx}" cy="{cy}" r="11" fill="#fff" stroke="{C}" stroke-width="1.4"/>')
        out.append(mtext(x0 + 100, y0 + 18, n, 10.4, D, 700, 'start'))
        out.append(mtext(x0 + 100, y0 + 37, d, 8.8, '#333', 400, 'start'))
    return f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">{"".join(out)}</svg>'


figs['f_sym'] = f_sym()


# ------------------------------------------------------------------ 图3-7 三个示例流程图
def f_three():
    fa = FC(158, 330, 9.6)
    x = 79
    fa.term('s', x, 20, '开始', 64, 22)
    fa.proc('i', x, 70, 'c = 86，math = 92\neng = 78', 140, 34)
    fa.proc('t', x, 124, 'total = c+math+eng', 140, 26)
    fa.proc('a', x, 172, 'avg = total / 3', 140, 26)
    fa.io('o', x, 222, '输出 total、avg', 138, 26)
    fa.term('e', x, 272, '结束', 64, 22)
    for a, b in [('s', 'i'), ('i', 't'), ('t', 'a'), ('a', 'o'), ('o', 'e')]:
        fa.v(a, b)

    fb = FC(170, 330, 9.6)
    x = 85
    fb.term('s', x, 20, '开始', 64, 22)
    fb.io('i', x, 66, '输入成绩 score', 124, 26)
    fb.dec('d', x, 124, 'score >= 60?', 112, 50)
    fb.io('y', 40, 190, '输出“及格”', 76, 26)
    fb.io('n', 130, 190, '输出“不及格”', 80, 26)
    fb.term('e', x, 272, '结束', 64, 22)
    fb.v('s', 'i')
    fb.v('i', 'd')
    fb.line([fb.p('d', 'l'), (40, 124), fb.p('y', 't')])
    fb.line([fb.p('d', 'r'), (130, 124), fb.p('n', 't')])
    fb.line([fb.p('y', 'b'), (40, 232), (x, 232)], False)
    fb.line([fb.p('n', 'b'), (130, 232), (x, 232)], False)
    fb.line([(x, 232), fb.p('e', 't')])
    fb.label(28, 116, '是')
    fb.label(142, 116, '否')

    fc = FC(178, 330, 9.6)
    x = 96
    fc.term('s', x, 20, '开始', 64, 22)
    fc.proc('i', x, 64, 'sum = 0，i = 1', 116, 26)
    fc.dec('d', x, 120, 'i <= 100?', 104, 48)
    fc.proc('a', x, 178, 'sum = sum + i', 112, 26)
    fc.proc('b', x, 222, 'i = i + 1', 112, 26)
    fc.io('o', x, 272, '输出 sum', 96, 24)
    fc.term('e', x, 302 + 4, '结束', 60, 20)
    fc.v('s', 'i')
    fc.v('i', 'd')
    fc.v('d', 'a')
    fc.v('a', 'b')
    fc.line([fc.p('b', 'l'), (16, 222), (16, 92), (x, 92)])
    fc.line([fc.p('d', 'r'), (164, 120), (164, 250), (x, 250), fc.p('o', 't')])
    fc.v('o', 'e')
    fc.label(108, 152, '是', 'start')
    fc.label(156, 112, '否')
    fa_s, fb_s, fc_s = fa.svg(), fb.svg(), fc.svg()
    # (c) 图注放在下方单独一行，避免与“结束”重叠
    return f'<div class="row3"><div>{fa_s}<div class="cap">（a）顺序：求平均分</div></div><div>{fb_s}<div class="cap">（b）选择：判断是否及格</div></div><div>{fc_s}<div class="cap">（c）循环：求 1+2+…+100</div></div></div>'


figs['f_three'] = f_three()


# ------------------------------------------------------------------ 图3-8 新生报到流程图
def f_reg():
    f = FC(330, 560, 10)
    x = 190
    f.term('s', x, 20, '开始', 70, 24)
    f.proc('a', x, 66, '核验录取信息', 150, 28)
    f.dec('d', x, 126, '信息无误？', 124, 50)
    f.proc('fix', 58, 126, '到咨询台更正', 96, 28)
    f.proc('b', x, 190, '核对专业班级', 150, 28)
    f.proc('c', x, 238, '领取一卡通和新生物资', 170, 28)
    f.proc('g', x, 286, '到宿舍楼办理入住登记', 170, 28)
    f.proc('h', x, 334, '领取宿舍钥匙', 150, 28)
    f.proc('i', x, 382, '确认床位信息', 150, 28)
    f.proc('j', x, 430, '到学籍登记处录入学籍信息', 190, 28)
    f.io('o', x, 480, '输出：报到完成', 150, 28)
    f.term('e', x, 530, '结束', 70, 24)
    for a, b in [('s', 'a'), ('a', 'd'), ('d', 'b'), ('b', 'c'), ('c', 'g'), ('g', 'h'), ('h', 'i'), ('i', 'j'), ('j', 'o'), ('o', 'e')]:
        f.v(a, b)
    f.line([f.p('d', 'l'), f.p('fix', 'r')])
    f.line([f.p('fix', 't'), (58, 66), f.p('a', 'l')])
    f.label(116, 116, '否')
    f.label(202, 162, '是', 'start')
    return f.svg()


figs['f_reg'] = f_reg()


# ------------------------------------------------------------------ 图3-9 训练 1：饮水机加热（待补全）
def f_train1():
    f = FC(300, 330, 10)
    x = 170
    f.term('s', x, 20, '开始', 70, 24)
    f.proc('a', x, 64, '接通电源', 130, 28)
    f.proc('m', x, 112, '①', 130, 28, blank=True)
    f.dec('d', x, 170, '水温 < 95 ℃？', 132, 50)
    f.proc('h', x, 232, '②', 130, 28, blank=True)
    f.proc('o', x + 0, 300 - 6, '③', 130, 28, blank=True)
    f.v('s', 'a')
    f.v('a', 'm')
    f.v('m', 'd')
    f.v('d', 'h')
    f.line([f.p('h', 'l'), (40, 232), (40, 88), (x, 88)])
    f.line([f.p('d', 'r'), (270, 170), (270, 264), (x, 264), f.p('o', 't')])
    f.label(182, 204, '是', 'start')
    f.label(258, 160, '否')
    return f.svg()


figs['f_train1'] = f_train1()


# ------------------------------------------------------------------ 图3-10 顺序结构
def f_seq():
    g = FC(150, 200, 10)
    x = 75
    g.line([(x, 8), (x, 50)])
    g.proc('a', x, 66, 'A', 90, 30)
    g.proc('b', x, 132, 'B', 90, 30)
    g.v('a', 'b')
    g.line([g.p('b', 'b'), (x, 190)])

    h = FC(350, 200, 10)
    h.term('s', 62, 20, '开始', 64, 22)
    h.proc('1', 62, 62, '取出课本', 96, 26)
    h.proc('2', 62, 106, '取出签字笔', 96, 26)
    h.proc('3', 62, 150, '取出笔记本', 96, 26)
    h.proc('4', 182, 62, '取出水杯', 96, 26)
    h.proc('5', 182, 106, '摆放在课桌上', 96, 26)
    h.proc('6', 182, 150, '打开实训计算机', 96, 26)
    h.proc('7', 302, 62, '等候上课', 96, 26)
    h.term('e', 302, 106, '结束', 64, 22)
    for a, b in [('s', '1'), ('1', '2'), ('2', '3'), ('4', '5'), ('5', '6'), ('7', 'e')]:
        h.v(a, b)
    h.line([h.p('3', 'b'), (62, 180), (122, 180), (122, 36), (182, 36), h.p('4', 't')])
    h.line([h.p('6', 'b'), (182, 180), (242, 180), (242, 36), (302, 36), h.p('7', 't')])
    return f'<div class="row2"><div>{g.svg()}<div class="cap">（a）一般形式</div></div><div>{h.svg()}<div class="cap">（b）上课前的准备</div></div></div>'


figs['f_seq'] = f_seq()


# ------------------------------------------------------------------ 图3-11 选择结构
def f_sel():
    a = FC(170, 240, 10)
    x = 85
    a.line([(x, 6), (x, 30)])
    a.dec('d', x, 56, '条件', 96, 46)
    a.proc('A', 34, 120, 'A', 56, 28)
    a.proc('B', 136, 120, 'B', 56, 28)
    a.line([a.p('d', 'l'), (34, 56), a.p('A', 't')])
    a.line([a.p('d', 'r'), (136, 56), a.p('B', 't')])
    a.line([a.p('A', 'b'), (34, 164), (136, 164), a.p('B', 'b')], False)
    a.line([(x, 164), (x, 194)])
    a.label(28, 46, '成立')
    a.label(148, 46, '不成立')

    b = FC(150, 240, 10)
    x = 75
    b.line([(x, 6), (x, 30)])
    b.dec('d', x, 56, '条件', 96, 46)
    b.proc('A', x, 120, 'A', 56, 28)
    b.v('d', 'A')
    b.line([b.p('d', 'r'), (138, 56), (138, 164), (x, 164)], False)
    b.line([b.p('A', 'b'), (x, 194)])
    b.label(86, 90, '成立', 'start')
    b.label(126, 46, '不成立')

    c = FC(220, 240, 9.6)
    x = 110
    c.term('s', x, 16, '开始', 60, 20)
    c.io('i', x, 50, '输入账号、密码', 128, 24)
    c.dec('d', x, 100, '账号正确并且\n密码正确？', 136, 52)
    c.io('y', 48, 160, '登录成功', 82, 24)
    c.io('n', 172, 160, '提示错误', 82, 24)
    c.term('e', x, 216, '结束', 60, 20)
    c.v('s', 'i')
    c.v('i', 'd')
    c.line([c.p('d', 'l'), (48, 100), c.p('y', 't')])
    c.line([c.p('d', 'r'), (172, 100), c.p('n', 't')])
    c.line([c.p('y', 'b'), (48, 190), (172, 190), c.p('n', 'b')], False)
    c.line([(x, 190), c.p('e', 't')])
    c.label(36, 92, '是')
    c.label(184, 92, '否')
    return f'<div class="row3"><div>{b.svg()}<div class="cap">（a）单分支</div></div><div>{a.svg()}<div class="cap">（b）双分支</div></div><div>{c.svg()}<div class="cap">（c）登录教学平台</div></div></div>'


figs['f_sel'] = f_sel()


# ------------------------------------------------------------------ 图3-12 循环结构
def f_loop():
    a = FC(160, 262, 10)
    x = 80
    a.line([(x, 6), (x, 28)])
    a.dec('d', x, 54, '条件', 96, 46)
    a.proc('A', x, 124, 'A（循环体）', 104, 28)
    a.v('d', 'A')
    a.line([a.p('A', 'b'), (x, 156), (14, 156), (14, 18), (x, 18)])
    a.line([a.p('d', 'r'), (148, 54), (148, 186), (x, 186), (x, 206)])
    a.label(90, 88, '成立', 'start')
    a.label(136, 44, '不成立')

    b = FC(160, 262, 10)
    x = 80
    b.line([(x, 6), (x, 40)])
    b.proc('A', x, 56, 'A（循环体）', 104, 28)
    b.dec('d', x, 126, '条件', 96, 46)
    b.v('A', 'd')
    b.line([b.p('d', 'l'), (14, 126), (14, 24), (x, 24)])
    b.line([b.p('d', 'b'), (x, 206)])
    b.label(26, 138, '成立')
    b.label(92, 166, '不成立', 'start')

    c = FC(200, 262, 9.4)
    x = 112
    c.term('s', x, 12, '开始', 56, 18)
    c.proc('i', x, 42, 'sum = 0，i = 1', 116, 22)
    c.dec('d', x, 84, 'i <= 5?', 92, 40)
    c.io('r', x, 130, '读入第 i 次测量值 r', 140, 22)
    c.proc('a', x, 162, 'sum = sum + r', 112, 22)
    c.proc('b', x, 192, 'i = i + 1', 112, 22)
    c.io('o', x, 228, '输出 sum / 5', 104, 22)
    c.v('s', 'i')
    c.v('i', 'd')
    c.v('d', 'r')
    c.v('r', 'a')
    c.v('a', 'b')
    c.line([c.p('b', 'l'), (34, 192), (34, 61), (x, 61)])
    c.line([c.p('d', 'r'), (190, 84), (190, 210), (x, 210), c.p('o', 't')])
    c.label(122, 110, '是', 'start')
    c.label(178, 76, '否')
    return f'<div class="row3"><div>{a.svg()}<div class="cap">（a）当型：先判断后执行</div></div><div>{b.svg()}<div class="cap">（b）直到型：先执行后判断</div></div><div>{c.svg()}<div class="cap">（c）测量电阻 5 次求平均（当型）</div></div></div>'


figs['f_loop'] = f_loop()


# ------------------------------------------------------------------ 图3-13 自顶向下、逐步细化
def f_topdown():
    W, H = 540, 236
    f = FC(W, H, 9.4)
    f.box('r', 290, 26, '逐个检测 5 个标称 100 Ω 的电阻（95～105 Ω 为合格），\n统计合格个数和不合格个数', 330, 40, C, C, '#fff', 700)
    f.box('a', 140, 98, '① 准备：合格数 ok、不合格数 bad\n都清零，从第 1 个电阻开始', 176, 38, BG, C, D, 700, size=8.8)
    f.box('b', 324, 98, '② 逐个检测：对第 1～5 个\n电阻做同样的检测', 160, 38, BG, C, D, 700, size=8.8)
    f.box('c', 470, 98, '③ 输出：合格数\n和不合格数', 108, 38, BG, C, D, 700, size=8.8)
    f.box('b1', 136, 176, '读入第 i 个\n电阻的阻值 r', 96, 36, size=8.8)
    f.box('b2', 242, 176, '判断 r 是否在\n95～105 Ω 之间', 104, 36, size=8.8)
    f.box('b3', 356, 176, '合格：ok 加 1\n不合格：bad 加 1', 112, 36, size=8.8)
    f.box('b4', 470, 176, 'i 加 1，准备\n检测下一个', 100, 36, size=8.8)
    for k in 'abc':
        x = f.n[k][0]
        f.line([(290, 46), (290, 62), (x, 62), (x, 78)])
    for k in ['b1', 'b2', 'b3', 'b4']:
        x = f.n[k][0]
        f.line([(324, 117), (324, 138), (x, 138), (x, 157)])
    f.note(6, 26, '第 1 层\n问题', 'start', 8.6)
    f.note(6, 98, '第 2 层\n大步骤', 'start', 8.6)
    f.note(6, 176, '第 3 层\n细化 ②', 'start', 8.6)
    f.note(290, 220, '第 3 层的 4 小步要对 5 个电阻各做一遍：用循环；“合格还是不合格”要分两种情况：用选择', 'middle', 8.8, D)
    return f.svg()


figs['f_topdown'] = f_topdown()


# ------------------------------------------------------------------ 电阻检测流程图（组合）
def f_resist():
    f = FC(380, 512, 9.8)
    x = 190
    f.term('s', x, 18, '开始', 64, 22)
    f.proc('i', x, 58, 'ok = 0，bad = 0，i = 1', 176, 26)
    f.dec('d', x, 112, 'i <= 5?', 104, 46)
    f.io('r', x, 166, '读入第 i 个阻值 r', 140, 26)
    f.dec('q', x, 226, 'r >= 95 并且\nr <= 105?', 150, 56)
    f.io('y', 92, 284, '输出“合格”', 112, 26)
    f.proc('y2', 92, 328, 'ok = ok + 1', 112, 26)
    f.io('n', 290, 284, '输出“不合格”', 116, 26)
    f.proc('n2', 290, 328, 'bad = bad + 1', 116, 26)
    f.proc('b', x, 390, 'i = i + 1', 110, 26)
    f.io('o', x, 452, '输出 ok 和 bad', 140, 26)
    f.term('e', x, 494, '结束', 64, 22)
    f.v('s', 'i')
    f.v('i', 'd')
    f.v('d', 'r')
    f.v('r', 'q')
    f.v('y', 'y2')
    f.v('n', 'n2')
    f.line([f.p('q', 'l'), (92, 226), f.p('y', 't')])
    f.line([f.p('q', 'r'), (290, 226), f.p('n', 't')])
    f.line([f.p('y2', 'b'), (92, 358), (290, 358), f.p('n2', 'b')], False)
    f.line([(x, 358), f.p('b', 't')])
    f.line([f.p('b', 'l'), (16, 390), (16, 84), (x, 84)])
    f.line([f.p('d', 'r'), (368, 112), (368, 422), (x, 422), f.p('o', 't')])
    f.v('o', 'e')
    f.label(200, 140, '是', 'start')
    f.label(356, 104, '否')
    f.label(102, 216, '是')
    f.label(276, 216, '否')
    f.note(24, 98, '循环', 'start', 9, M)
    f.note(190, 306, '选择', 'middle', 9, M)
    return f.svg()


figs['f_resist'] = f_resist()


# ------------------------------------------------------------------ 图3-15 技能训练：图书馆借书（待补全）
def f_train2():
    f = FC(330, 360, 10)
    x = 190
    f.term('s', x, 18, '开始', 64, 22)
    f.proc('a', x, 60, '在检索机上查到索书号', 168, 28)
    f.proc('b', x, 108, '到书架按索书号找书', 168, 28)
    f.dec('d', x, 168, '①', 120, 48)
    f.proc('y', x, 232, '在自助借还机上借书', 168, 28)
    f.proc('n', 52, 232, '②', 92, 28, blank=True)
    f.io('o', x, 284, '③', 150, 28)
    f.term('e', x, 334, '结束', 64, 22)
    f.v('s', 'a')
    f.v('a', 'b')
    f.v('b', 'd')
    f.v('d', 'y')
    f.v('y', 'o')
    f.v('o', 'e')
    f.line([f.p('d', 'l'), (52, 168), f.p('n', 't')])
    f.line([f.p('n', 'b'), (52, 312), (x, 312)])
    f.label(202, 202, '是', 'start')
    f.label(118, 158, '否')
    return f.svg()


figs['f_train2'] = f_train2()


# ------------------------------------------------------------------ 课堂练习图标（与原有图标同风格）
figs['ico_practice'] = f'''<svg viewBox="0 0 54 54" width="54" height="54"><rect x="1" y="1" width="52" height="52" rx="10" fill="{C}"/>
<path d="M16 38l3-9 15-15 6 6-15 15z" fill="#fff"/><path d="M16 38l3-9 6 6z" fill="{L}"/><path d="M31 17l6 6" stroke="{C}" stroke-width="2"/></svg>'''

exec(open('figs_new.py', encoding='utf8').read())

CSS = f'''
body {{ margin:0; background:#fff; font-family:{FONT}; }}
.fig {{ display:inline-block; padding:6px; background:#fff; margin:10px; }}
.row2, .row3 {{ display:flex; align-items:flex-start; gap:6px; }}
.cap {{ text-align:center; font-size:10px; color:{D}; font-weight:700; margin-top:-4px; }}
.feat {{ width:520px; display:grid; grid-template-columns:repeat(5,1fr); gap:6px; }}
.fc {{ border:1px solid {L}; border-top:3px solid {C}; border-radius:4px; padding:6px 6px 8px; background:#fff; }}
.fh {{ display:flex; flex-direction:column; align-items:center; gap:3px; }}
.fh b {{ color:{D}; font-size:10px; white-space:nowrap; text-align:center; }}
.fd {{ font-size:9px; color:#1F1F1F; margin:5px 0 6px; line-height:1.45; min-height:39px; }}
.fx {{ font-size:8.4px; color:#444; line-height:1.45; background:{BG}; padding:4px 5px; border-radius:3px; min-height:62px; }}
.fx span {{ display:inline-block; background:{D}; color:#fff; font-size:7.6px; padding:0 3px; border-radius:2px; margin-right:3px; }}
'''

with open('fig/figs.html', 'w', encoding='utf8') as fh:
    fh.write(f'<!doctype html><meta charset="utf-8"><style>{CSS}{CSS2}</style><body>')
    for k, v in figs.items():
        fh.write(f'<div class="fig" id="{k}">{v}</div>\n')
print(' '.join(figs))
