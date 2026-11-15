# 项目六插图：生成 fig/figs.html（每张图一个 id），再用 shot.js 截成 PNG
# 版式元素只用主色系：#1D4F91 主色、#153A6B 深、#4A75AE 中、#C5D3E7 浅线、#E8EEF7 浅底，加黑灰；
# 强调用红色 #D0312D（与项目四、五相同）；彩色只出现在图标（Fluent Emoji，MIT）和指示灯的灯色里
exec(open('base4.py', encoding='utf8').read())

figs = {}
RED = '#D0312D'
GRN, GLOW = '#2FAE5F', '#BFEBD0'     # 正常点亮
YEL = '#F2B705'                       # 闪烁异常
OFF, OFF2 = '#5D636C', '#3A3F47'      # 短路不亮
# 循环四个组成部分的标注色
K1, K2, K3, K4 = C, '#2F8F5B', RED, '#B86E00'


def chip(x, y, w, h, s, fill=C, color='#fff', size=9, weight=700, rx=None, stroke='none', mono=False):
    rx = h / 2 if rx is None else rx
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1"/>'
            + mtext(x + w / 2, y + h / 2, s, size, color, weight, mono=mono))


def arrow(pts, color=M, width=1.4, dash=False):
    d = 'M' + ' L'.join(f'{a:.1f},{b:.1f}' for a, b in pts)
    da = ' stroke-dasharray="4 3"' if dash else ''
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" marker-end="url(#ar)"{da}/>'


def rarrow(pts, width=1.5, dash=False):
    """红色箭头（箭头也是红色）"""
    d = 'M' + ' L'.join(f'{a:.1f},{b:.1f}' for a, b in pts)
    da = ' stroke-dasharray="4 3"' if dash else ''
    return f'<path d="{d}" fill="none" stroke="{RED}" stroke-width="{width}" marker-end="url(#arr)"{da}/>'


REDMK = f'<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{RED}"/></marker></defs>'


def seg(pts, color=M, width=1.4, dash=False):
    d = 'M' + ' L'.join(f'{a:.1f},{b:.1f}' for a, b in pts)
    da = ' stroke-dasharray="4 3"' if dash else ''
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"{da}/>'


def code_lines(x, y, lines, size=9.6, lh=15, color='#1F1F1F'):
    return ''.join(f'<text x="{x}" y="{y + i * lh}" font-size="{size}" fill="{color}" font-family="{MONO}" xml:space="preserve">{esc(s)}</text>'
                   for i, s in enumerate(lines))


def num(x, y, k, fill=RED, r=7.5, size=9):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>' + mtext(x, y, str(k), size, '#fff', 700)


def led(x, y, st, r=10):
    """指示灯：1 正常点亮（绿色、外发光），2 闪烁异常（黄色、放射线），0 短路不亮（深灰）"""
    if st == 1:
        return (f'<circle cx="{x}" cy="{y}" r="{r * 1.6}" fill="{GLOW}" opacity="0.8"/>'
                f'<circle cx="{x}" cy="{y}" r="{r}" fill="{GRN}" stroke="#1E7A42" stroke-width="1"/>'
                f'<circle cx="{x - r * 0.35}" cy="{y - r * 0.35}" r="{r * 0.28}" fill="#fff" opacity="0.7"/>')
    if st == 2:
        rays = ''
        for k in range(8):
            import math
            a = k * math.pi / 4
            x1, y1 = x + math.cos(a) * r * 1.35, y + math.sin(a) * r * 1.35
            x2, y2 = x + math.cos(a) * r * 1.85, y + math.sin(a) * r * 1.85
            rays += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{YEL}" stroke-width="1.6" stroke-linecap="round"/>'
        return (rays + f'<circle cx="{x}" cy="{y}" r="{r}" fill="{YEL}" stroke="#B88A00" stroke-width="1"/>'
                f'<circle cx="{x - r * 0.35}" cy="{y - r * 0.35}" r="{r * 0.28}" fill="#fff" opacity="0.7"/>')
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{OFF}" stroke="{OFF2}" stroke-width="1"/>'
            f'<circle cx="{x - r * 0.35}" cy="{y - r * 0.35}" r="{r * 0.22}" fill="#fff" opacity="0.25"/>')


BOARD = [[1, 1, 2, 1], [1, 0, 1, 1], [2, 1, 1, 1]]   # 与任务二运行时输入的状态码相同


# ================================================================== 图6-1 情境：信号指示灯监测电路实训板
def f_scene():
    W, H = 520, 318
    o = [chip(12, 8, 236, 24, '信号指示灯监测电路实训板', size=10.5)]
    bx, by, bw, bh = 12, 40, 300, 238
    o.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="8" fill="{D}"/>')
    for k in range(7):                                   # 电路板走线
        yy = by + 22 + k * 34
        o.append(f'<path d="M{bx + 8},{yy} h40 l10,10 h{bw - 70}" fill="none" stroke="{M}" stroke-width="1" opacity="0.45"/>')
    cx0, cy0 = bx + 18, by + bh - 46                     # 单片机芯片：放在灯阵下方
    o.append(f'<rect x="{cx0}" y="{cy0}" width="70" height="32" rx="3" fill="#0B1F3A" stroke="#7F93B3" stroke-width="0.8"/>')
    for k in range(6):
        o.append(f'<rect x="{cx0 + 6 + k * 11}" y="{cy0 - 6}" width="4" height="6" fill="#B8C2CF"/>'
                 f'<rect x="{cx0 + 6 + k * 11}" y="{cy0 + 32}" width="4" height="6" fill="#B8C2CF"/>')
    o.append(mtext(cx0 + 35, cy0 + 16, '单片机', 8.6, '#fff', 700))
    xs, ys = [130, 178, 226, 274], [92, 140, 188]
    for j, x in enumerate(xs):
        o.append(mtext(x, by + 20, f'第{j + 1}列', 8.4, '#DCE6F5', 700))
    for i, y in enumerate(ys):
        o.append(mtext(104, y, f'第{i + 1}行', 8.4, '#DCE6F5', 700, 'end'))
        for j, x in enumerate(xs):
            o.append(led(x, y, BOARD[i][j]))
    o.append(seg([(cx0 + 70, cy0 + 16), (xs[0] - 20, cy0 + 16), (xs[0] - 20, ys[2] + 24)], '#7F93B3', 1, True))
    gx = 334
    o.append(chip(gx, 8, 176, 24, '状态码的规定', fill=BG, color=D, stroke=C, size=10))
    for k, (st, code, name) in enumerate([(0, '0', '短路不亮'), (1, '1', '正常点亮'), (2, '2', '闪烁异常')]):
        y = 60 + k * 40
        o.append(led(gx + 22, y, st, 9))
        o.append(chip(gx + 48, y - 11, 24, 22, code, fill=C, size=11, rx=4, mono=True))
        o.append(mtext(gx + 82, y, name, 10.5, '#1F1F1F', 700, 'start'))
    o.append(av_he(gx + 26, 246, 24, 'think'))
    o.append(bubble(gx + 58, 206, 120, 58, '12 盏灯，\n难道要把判断\n写 12 遍？', (gx + 52, 240), 9.2))
    o.append(mtext(bx + bw / 2, H - 12, '灯阵中各灯的状态与任务二运行时输入的状态码相同', 8.4, '#4D4D4D'))
    return svgwrap(W, H, ''.join(o))

figs['f_scene'] = f_scene()


# ================================================================== 图6-2 知识导图
def kmap():
    tasks = [("任务一 读取指示灯实时状态", ["循环结构示例：1+2+…+100", "循环的组成：初值、条件、循环体、修改", "while 语句及易错点（死循环）", "do…while 语句，与 while 的区别", "任务实施：持续读取，读到 0 结束"]),
             ("任务二 遍历灯阵的亮灭情况", ["for 语句：三个表达式的执行顺序", "for 语句的易错点", "循环嵌套：外层走一步，内层走一圈", "九九乘法表", "任务实施：先巡检一行，再巡检 3 行 4 列"]),
             ("任务三 控制监测指示灯流程", ["break：提前结束所在的那一层循环", "continue：结束本次循环", "break 与 continue 的比较", "典型示例：兔子数列、百钱买百鸡", "任务实施：闪烁跳过，短路终止"]),
             ("AI升华 让巡检程序停得下来", ["用错误输入检验 AI 给出的办法", "离开 AI 再做：防误报、查状态码"])]
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
<text x="68" y="{mid - 4}" fill="#fff" font-size="13" font-weight="700" text-anchor="middle">项目六</text>
<text x="68" y="{mid + 14}" fill="#fff" font-size="10.5" text-anchor="middle">编写重复操作流程</text>
<g font-size="9.6" font-weight="700" text-anchor="middle">{''.join(boxes)}</g>
<g font-size="9.4" fill="#1F1F1F">{''.join(texts)}</g>
<g fill="{C}">{''.join(dots)}</g></svg>'''


figs['f_kmap'] = kmap()


# ================================================================== 图6-3 为什么需要循环
def f_why():
    W, H = 520, 232
    o = []
    # 左：一条一条地写
    o.append(chip(10, 6, 236, 24, '不用循环：一条一条地写', fill=BG, color=D, stroke=C, size=10, rx=4))
    o.append(f'<rect x="10" y="38" width="236" height="150" rx="4" fill="#fff" stroke="{L}" stroke-width="1"/>')
    o.append(code_lines(26, 60, ['sum = 0;', 'sum = sum + 1;', 'sum = sum + 2;', 'sum = sum + 3;'], 10, 17))
    o.append(mtext(128, 136, '…… 还要写 96 行 ……', 9.4, '#7F7F7F'))
    o.append(code_lines(26, 166, ['sum = sum + 100;'], 10, 17))
    o.append(mtext(128, 204, '一共要写 101 条语句', 10, RED, 700))
    o.append(mtext(128, 222, '加到 1 万，就要写 10001 条', 9, '#4D4D4D'))
    # 右：用循环
    x0 = 274
    o.append(chip(x0, 6, 236, 24, '用循环：让计算机重复做', fill=C, size=10, rx=4))
    o.append(f'<rect x="{x0}" y="38" width="236" height="150" rx="4" fill="{BG}" stroke="{C}" stroke-width="1"/>')
    o.append(code_lines(x0 + 18, 60, ['sum = 0;', 'i = 1;', 'while (i <= 100)', '{', '    sum = sum + i;', '    i++;', '}'], 10, 17))
    o.append(f'<path d="M{x0 + 150},{150} C{x0 + 205},{150} {x0 + 205},{94} {x0 + 150},{94}" fill="none" stroke="{RED}" stroke-width="1.6" marker-end="url(#arr)"/>')
    o.append(mtext(x0 + 212, 122, '重复\n100 次', 9.4, RED, 700, 'start', 1.25))
    o.append(mtext(x0 + 118, 204, '7 行就够了', 10, C, 700))
    o.append(mtext(x0 + 118, 222, '加到 1 万，只要把 100 改成 10000', 9, '#4D4D4D'))
    o.append(arrow([(250, 113), (270, 113)], M, 1.6))
    return svgwrap(W, H, ''.join(o), REDMK)


figs['f_why'] = f_why()


# ================================================================== 图6-4 循环的组成
def f_parts():
    W, H = 520, 272
    o = []
    cx, lh = 20, 22
    code = ['sum = 0;', 'i = 1;', 'while (i <= 100)', '{', '    sum = sum + i;', '    i++;', '}']
    o.append(f'<rect x="10" y="10" width="236" height="170" rx="4" fill="{BG}" stroke="{C}" stroke-width="1"/>')
    o.append(code_lines(cx, 38, code, 11, lh))
    cw = 0.602 * 11                                 # 等宽字的字宽（11px）
    mid = lambda k: 34 + k * lh                     # 第 k 行文字的竖直中线
    boxes = [(1, K1, 1, 0, 5), (2, K2, 2, 7, 15), (3, K3, 4, 4, 18), (4, K4, 5, 4, 8)]
    ends = {}
    for k, col, line, c0, c1 in boxes:
        x0, x1 = cx + c0 * cw - 3, cx + c1 * cw + 3
        o.append(f'<rect x="{x0:.1f}" y="{mid(line) - 10}" width="{x1 - x0:.1f}" height="20" rx="3" fill="none" stroke="{col}" stroke-width="1.6"/>')
        ends[k] = (x1, mid(line))
    items = [(1, K1, '循环变量的初值', 'i = 1：从 1 开始', 34),
             (2, K2, '循环条件', 'i <= 100：终值是 100，\n条件成立才执行循环体', 82),
             (3, K3, '循环体', '每次要重复做的事：\nsum = sum + i;', 136),
             (4, K4, '循环变量的修改', 'i++：每次加 1，\n使条件最终不成立', 190)]
    for k, col, t1, t2, y in items:
        o.append(num(298, y, k, col))
        o.append(mtext(310, y, t1, 10, col, 700, 'start'))
        o.append(mtext(310, y + 18 + (6 if '\n' in t2 else 0), t2, 8.8, '#1F1F1F', 400, 'start', 1.3))
        ex, ey = ends[k]
        o.append(seg([(ex, ey), (288, y)], col, 1, True))
    o.append(f'<rect x="10" y="226" width="500" height="40" rx="4" fill="#fff" stroke="{L}" stroke-width="1"/>')
    o.append(mtext(260, 239, '循环次数：i 从 1 到 100，每次加 1，循环体执行 100 次', 9.6, D, 700))
    o.append(mtext(260, 256, 'sum = 0 是累加的“起点”，也要在循环之前写好', 9, '#4D4D4D'))
    return svgwrap(W, H, ''.join(o))

figs['f_parts'] = f_parts()


# ================================================================== 图6-5 while 语句
def f_while():
    W, H = 520, 236
    o = [f'<rect x="14" y="40" width="190" height="100" rx="4" fill="{BG}" stroke="{C}" stroke-width="1"/>']
    o.append(code_lines(30, 66, ['while (表达式)', '{', '    循环体', '}'], 11, 19, D))
    o.append(f'<rect x="72" y="54" width="82" height="17" rx="2" fill="none" stroke="{RED}" stroke-width="1.2"/>')
    o.append(f'<path d="M26,{80} h-6 V{136} h6" fill="none" stroke="{RED}" stroke-width="1.2"/>')
    o.append(mtext(14, 18, '①循环条件：写在圆括号中，非 0 为真；', 9, RED, 700, 'start'))
    o.append(mtext(14, 32, '　每次执行循环体之前都要判断一次', 9, RED, 700, 'start'))
    o.append(mtext(14, 160, '②循环体：多条语句要用花括号括起来；', 9, RED, 700, 'start'))
    o.append(mtext(14, 176, '　要有使条件最终不成立的语句', 9, RED, 700, 'start'))
    o.append(chip(14, 196, 120, 24, '先判断，后执行', fill=C, size=10, rx=4))
    f = FC(520, 236, 9.4)
    x = 366
    f.dec('d', x, 70, '表达式', 100, 46)
    f.proc('b', x, 138, '循环体', 90, 28)
    f.box('n', x, 214, 'while 后面的语句', 130, 24, fill='#fff')
    f.line([(x, 8), f.p('d', 't')])
    f.v('d', 'b')
    f.line([f.p('b', 'b'), (x, 170), (x - 86, 170), (x - 86, 30), (x, 30)])
    f.line([f.p('d', 'r'), (x + 96, 70), (x + 96, 190), (x, 190), f.p('n', 't')])
    f.label(x - 10, 106, '真（非 0）', 'end')
    f.label(x + 78, 60, '假（0）')
    f.note(x - 92, 100, '回到条件\n再判断', 'end', 8.4, '#4D4D4D')
    return svgwrap(W, H, ''.join(o) + ''.join(f.ln) + ''.join(f.el))


figs['f_while'] = f_while()


# ================================================================== 图6-6 while 与 do…while 的执行过程
def f_dowhile():
    f = FC(520, 262, 9.4)
    # （a）while
    x = 130
    f.dec('a1', x, 66, '条件', 84, 42)
    f.proc('a2', x, 130, '循环体', 84, 26)
    f.line([(x, 8), f.p('a1', 't')])
    f.v('a1', 'a2')
    f.line([f.p('a2', 'b'), (x, 158), (x - 72, 158), (x - 72, 30), (x, 30)])
    f.line([f.p('a1', 'r'), (x + 80, 66), (x + 80, 186), (x, 186), (x, 204)])
    f.label(x - 10, 99, '真', 'end')
    f.label(x + 64, 57, '假')
    f.note(x, 214, '出口', 'middle')
    # （b）do…while
    x = 390
    f.proc('b1', x, 60, '循环体', 84, 26)
    f.dec('b2', x, 124, '条件', 84, 42)
    f.line([(x, 8), f.p('b1', 't')])
    f.v('b1', 'b2')
    f.line([f.p('b2', 'l'), (x - 72, 124), (x - 72, 30), (x, 30)])
    f.line([f.p('b2', 'b'), (x, 204)])
    f.label(x - 54, 115, '真')
    f.label(x + 10, 158, '假', 'start')
    f.note(x, 214, '出口', 'middle')
    for cx, t1, t2 in ((130, '（a）while：先判断，后执行', '第一次条件就不成立时，循环体一次也不执行'),
                       (390, '（b）do…while：先执行，后判断', '不论条件是否成立，循环体至少执行一次')):
        f.el.append(mtext(cx, 236, t1, 10, D, 700) + mtext(cx, 254, t2, 8.8, RED if 'do' in t1 else '#4D4D4D'))
    return f.svg()


figs['f_dowhile'] = f_dowhile()


# ================================================================== 图6-7 任务一流程图
def f_flow1():
    f = FC(440, 352, 9.4)
    x = 170
    f.term('s', x, 18, '开始')
    f.proc('a', x, 58, 'n = 0', 110, 26)
    f.proc('b', x, 104, 'n++（准备读下一个灯）', 170, 26)
    f.io('c', x, 150, '输出提示，输入状态码 code', 200, 28)
    f.box('d', x, 204, '按 code 输出第 n 个灯的状态\n（1 正常点亮，2 闪烁异常，0 短路不亮）', 236, 42, fill=C, stroke=C, color='#fff', weight=700, size=9.2)
    f.dec('e', x, 270, 'code != 0', 120, 46)
    f.term('t', x, 334, '结束')
    for a_, b_ in (('s', 'a'), ('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e'), ('e', 't')):
        f.v(a_, b_)
    f.line([f.p('e', 'l'), (x - 140, 270), (x - 140, 104), f.p('b', 'l')])
    f.label(x + 10, 304, '否：读到 0', 'start')
    br = (f'<path d="M{x + 126},{91} h6 V{225} h-6" fill="none" stroke="{L}" stroke-width="1.2"/>'
          + mtext(x + 140, 150, '循环体\n（至少执行一次）', 9.2, C, 700, 'start', 1.3))
    br += mtext(x - 134, 242, '是：不是 0，\n继续监测', 8.8, RED, 700, 'start', 1.3)
    return f.svg(br)

figs['f_flow1'] = f_flow1()


# ================================================================== 图6-8 for 语句的执行过程
def f_for():
    W, H = 520, 266
    o = [f'<rect x="10" y="30" width="232" height="96" rx="4" fill="{BG}" stroke="{C}" stroke-width="1"/>']
    o.append(code_lines(18, 56, ['for (表达式1; 表达式2; 表达式3)', '{', '    循环体', '}'], 9.6, 18, D))
    o.append(num(64, 18, 1) + num(110, 18, 2) + num(157, 18, 4) + num(84, 88, 3))
    o.append(mtext(10, 146, '例：for (i = 1; i <= 100; i++)', 9.6, '#1F1F1F', 700, 'start', mono=True))
    for col, cxx, t in ((K1, 72.6, '初值'), (K2, 121.7, '条件'), (K4, 165.1, '修改')):
        o.append(chip(cxx - 19, 156, 38, 18, t, fill=col, size=8.8, rx=3))
    o.append(mtext(10, 196, '① 只在开始时执行一次；', 9, RED, 700, 'start'))
    o.append(mtext(10, 212, '② ③ ④ 反复执行，直到 ② 不成立', 9, RED, 700, 'start'))
    o.append(mtext(10, 236, '相当于：表达式1;  while (表达式2)', 9, '#4D4D4D', 400, 'start'))
    o.append(mtext(10, 252, '　　　　{ 循环体  表达式3; }', 9, '#4D4D4D', 400, 'start'))
    f = FC(520, 266, 9.2)
    x = 380
    f.proc('e1', x, 40, '表达式1', 100, 26)
    f.dec('e2', x, 100, '表达式2', 104, 44)
    f.proc('b', x, 160, '循环体', 90, 26)
    f.proc('e3', x, 206, '表达式3', 100, 26)
    f.box('n', x, 252, 'for 后面的语句', 120, 22, fill='#fff')
    f.line([(x, 4), f.p('e1', 't')])
    f.v('e1', 'e2')
    f.v('e2', 'b')
    f.v('b', 'e3')
    f.line([f.p('e3', 'l'), (x - 86, 206), (x - 86, 70), (x, 70)])
    f.line([f.p('e2', 'r'), (x + 84, 100), (x + 84, 232), (x, 232), f.p('n', 't')])
    f.label(x - 10, 134, '真', 'end')
    f.label(x + 66, 90, '假')
    marks = num(x - 66, 40, 1) + num(x - 68, 100, 2) + num(x - 60, 160, 3) + num(x + 68, 206, 4)
    return svgwrap(W, H, ''.join(o) + ''.join(f.ln) + ''.join(f.el) + marks)

figs['f_for'] = f_for()


# ================================================================== 图6-9 循环嵌套：外层走一步，内层走一圈
def f_nest():
    import math
    W, H = 520, 250
    o = []
    cx, cy, r = 112, 110, 76
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" stroke="{C}" stroke-width="3"/>')
    for k in range(12):
        a = k * math.pi / 6
        x1, y1 = cx + math.sin(a) * (r - 6), cy - math.cos(a) * (r - 6)
        x2, y2 = cx + math.sin(a) * (r - 14), cy - math.cos(a) * (r - 14)
        o.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{D}" stroke-width="2"/>')
    o.append(f'<line x1="{cx}" y1="{cy}" x2="{cx + 36}" y2="{cy}" stroke="{D}" stroke-width="6" stroke-linecap="round"/>')
    o.append(f'<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - 60}" stroke="{RED}" stroke-width="3" stroke-linecap="round"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="5" fill="{D}"/>')
    o.append(f'<path d="M{cx + 26},{cy - 56} A62,62 0 1 1 {cx - 4},{cy - 62}" fill="none" stroke="{RED}" stroke-width="1.4" stroke-dasharray="4 3" marker-end="url(#arr)"/>')
    o.append(mtext(cx, cy + r + 18, '时针走一格，分针走一圈', 10, D, 700))
    o.append(mtext(cx, cy + r + 36, '外层循环像时针，内层循环像分针', 9, '#4D4D4D'))
    # 右：灯阵的巡检顺序
    gx, gy, cw, ch = 286, 52, 50, 40
    o.append(mtext(gx + 2 * cw, 18, '内层循环：col 从 1 到 4', 9.4, RED, 700))
    o.append(rarrow([(gx + 6, 30), (gx + 4 * cw - 6, 30)]))
    o.append(mtext(gx - 30, gy + 1.5 * ch, '外层循环\nrow\n1→3', 9.4, D, 700, 'middle', 1.3))
    k = 0
    for i in range(3):
        for j in range(4):
            k += 1
            x, y = gx + j * cw, gy + i * ch
            o.append(f'<rect x="{x + 3}" y="{y + 3}" width="{cw - 6}" height="{ch - 6}" rx="4" fill="{BG}" stroke="{C}" stroke-width="1"/>')
            o.append(mtext(x + cw / 2, y + ch / 2 - 5, f'{i + 1}-{j + 1}', 10, D, 700, mono=True))
            o.append(mtext(x + cw / 2, y + ch / 2 + 9, f'第{k}个', 7.6, '#7F7F7F'))
            if j < 3:
                o.append(arrow([(x + cw - 3, y + ch / 2), (x + cw + 3, y + ch / 2)], RED, 1.2))
        if i < 2:
            o.append(seg([(gx + 4 * cw - 3, gy + i * ch + ch / 2), (gx + 4 * cw + 12, gy + i * ch + ch / 2),
                          (gx + 4 * cw + 12, gy + i * ch + ch + 1), (gx - 8, gy + i * ch + ch + 1)], D, 1.2, True)
                     + arrow([(gx - 8, gy + i * ch + ch + 1), (gx - 8, gy + (i + 1) * ch + ch / 2), (gx + 3, gy + (i + 1) * ch + ch / 2)], D, 1.2, True))
    o.append(mtext(gx + 2 * cw, gy + 3 * ch + 22, '外层每走一步（row 加 1），内层就走完一圈（col 从 1 到 4）', 8.8, '#1F1F1F'))
    o.append(mtext(gx + 2 * cw, gy + 3 * ch + 40, '内层循环体一共执行 3 × 4 = 12 次', 9.6, RED, 700))
    return svgwrap(W, H, ''.join(o), REDMK)


figs['f_nest'] = f_nest()


# ================================================================== 图6-10 任务二流程图（第二步）
def f_flow2():
    f = FC(470, 506, 9.2)
    x = 200
    f.term('s', x, 16, '开始')
    f.proc('a', x, 54, 'row = 1', 100, 24)
    f.dec('b', x, 102, 'row <= 3', 110, 44)
    f.io('c', x, 152, '输出第 row 行的输入提示', 190, 26)
    f.proc('d', x, 194, 'col = 1', 100, 24)
    f.dec('e', x, 240, 'col <= 4', 110, 44)
    f.io('g', x, 290, '输入状态码 code', 150, 26)
    f.box('h', x, 336, '按 code 输出第 row 行第 col 列的状态', 220, 28, fill=C, stroke=C, color='#fff', weight=700)
    f.proc('i', x, 382, 'col++', 90, 24)
    f.proc('r', x + 190, 240, 'row++', 76, 24)
    f.io('j', x, 448, '输出“灯阵全部巡检完毕！”', 200, 26)
    f.term('k', x, 490, '结束')
    for a_, b_ in (('s', 'a'), ('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e'), ('e', 'g'), ('g', 'h'), ('h', 'i')):
        f.v(a_, b_)
    f.line([f.p('i', 'l'), (x - 130, 382), (x - 130, 240), f.p('e', 'l')])
    f.line([f.p('e', 'r'), f.p('r', 'l')])
    f.line([f.p('r', 't'), (x + 190, 102), f.p('b', 'r')])
    f.line([f.p('b', 'l'), (x - 170, 102), (x - 170, 424), (x, 424), f.p('j', 't')])
    f.v('j', 'k')
    f.label(x - 10, 134, '是', 'end')
    f.label(x - 10, 270, '是', 'end')
    f.label(x + 76, 230, '否')
    f.label(x - 76, 92, '否')
    box = (f'<rect x="{x - 150}" y="{214}" width="{300}" height="{186}" rx="6" fill="none" stroke="{RED}" stroke-width="1.2" stroke-dasharray="5 3"/>'
           + mtext(x + 144, 390, '内层循环：逐列', 9, RED, 700, 'end'))
    box += (f'<rect x="{x - 186}" y="{76}" width="{420}" height="{334}" rx="8" fill="none" stroke="{C}" stroke-width="1" stroke-dasharray="2 3"/>'
            + mtext(x + 230, 88, '外层循环：逐行', 9, C, 700, 'end'))
    return f.svg(box)

figs['f_flow2'] = f_flow2()


# ================================================================== 图6-11 break 与 continue 的执行过程
def f_break():
    f = FC(520, 340, 9.0)
    extra = REDMK
    for x, word, fx in ((130, 'break', 122), (380, 'continue', 134)):
        p = word + '_'
        f.dec(p + 'c', x, 60, '循环条件', 96, 42)
        f.proc(p + 'a', x, 114, '循环体的前一部分', 130, 24)
        f.dec(p + 'i', x, 168, 'if (条件)', 96, 42)
        f.proc(p + 'b', x, 222, '循环体的后一部分', 130, 24)
        f.proc(p + 'e3', x, 262, 'i++（表达式3）', 120, 24)
        f.box(p + 'n', x, 318, '循环后面的语句', 120, 22, fill='#fff')
        f.line([(x, 18), f.p(p + 'c', 't')])
        f.v(p + 'c', p + 'a')
        f.v(p + 'a', p + 'i')
        f.v(p + 'i', p + 'b')
        f.v(p + 'b', p + 'e3')
        f.line([f.p(p + 'e3', 'l'), (x - 92, 262), (x - 92, 34), (x, 34)])
        f.line([f.p(p + 'c', 'r'), (x + fx, 60), (x + fx, 318), f.p(p + 'n', 'r')])
        f.label(x + fx - 16, 50, '假')
        f.label(x - 10, 198, '否', 'end')
        extra += mtext(x + 56, 158, '是', 9, RED, 700, 'start')
        extra += mtext(x, 6, f'（{"ab"[word == "continue"]}）{word}', 10, D, 700)
    x = 130
    extra += rarrow([(x + 48, 168), (x + 76, 168), (x + 76, 294), (x + 30, 294), (x + 30, 307)], 1.8)
    extra += mtext(x + 80, 200, 'break：\n结束整个\n循环', 8.8, RED, 700, 'start', 1.25)
    x = 380
    extra += rarrow([(x + 48, 168), (x + 76, 168), (x + 76, 262), (x + 62, 262)], 1.8)
    extra += mtext(x + 80, 206, 'continue：\n跳过后一\n部分，接着\n下一次', 8.4, RED, 700, 'start', 1.25)
    return f.svg(extra)

figs['f_break'] = f_break()


# ================================================================== 图6-12 break 只跳出一层
def f_breakout():
    W, H = 520, 268
    o = []
    for x0, title, ok in ((8, '（a）只用 break', False), (268, '（b）加上标志变量 stop', True)):
        o.append(mtext(x0 + 122, 12, title, 10, D, 700))
        o.append(f'<rect x="{x0}" y="26" width="244" height="188" rx="6" fill="#fff" stroke="{C}" stroke-width="1.2"/>')
        o.append(mtext(x0 + 8, 40, '外层：for (row = 1; row <= 3; row++)', 8.6, C, 700, 'start'))
        o.append(f'<rect x="{x0 + 14}" y="52" width="210" height="92" rx="5" fill="{BG}" stroke="{M}" stroke-width="1"/>')
        o.append(mtext(x0 + 22, 66, '内层：for (col = 1; col <= 4; col++)', 8.6, M, 700, 'start'))
        body = ['if (code == 0)', '{', '    stop = 1;  break;' if ok else '    break;', '}']
        o.append(code_lines(x0 + 28, 88, body, 9, 14, D))
        bx = x0 + 28 + len(body[2]) * 0.602 * 9 + 4             # 第一个 break; 的右端
        o.append(rarrow([(bx, 113), (x0 + 214, 113), (x0 + 214, 160), (x0 + 168 if ok else x0 + 150, 166)], 1.6))
        if ok:
            o.append(code_lines(x0 + 22, 170, ['if (stop == 1)', '    break;'], 9, 14, RED))
            o.append(rarrow([(x0 + 70, 188), (x0 + 70, 232)], 1.6))
            o.append(mtext(x0 + 78, 228, '跳出外层循环，结束巡检', 9, RED, 700, 'start'))
            o.append(mtext(x0 + 122, 254, '第二个 break 跳出外层循环', 9, '#1F1F1F', 700))
        else:
            o.append(mtext(x0 + 22, 166, '（内层循环之后）', 8.8, '#7F7F7F', 400, 'start'))
            o.append(rarrow([(x0 + 30, 176), (x0 + 30, 200), (x0 + 234, 200), (x0 + 234, 36), (x0 + 170, 36)], 1.4, True))
            o.append(mtext(x0 + 124, 192, '回到外层：row++，继续巡检', 8.4, RED, 700))
            o.append(mtext(x0 + 122, 236, 'break 只跳出内层循环，', 9, '#1F1F1F', 700))
            o.append(mtext(x0 + 122, 252, '外层循环还会继续', 9, RED, 700))
    return svgwrap(W, H, ''.join(o), REDMK)

figs['f_breakout'] = f_breakout()


# ================================================================== 图6-13 任务三流程图（内层循环体）
def f_flow3():
    f = FC(520, 456, 9.0)
    x, xl, xr = 236, 92, 420
    f.dec('e', x, 44, 'col <= 4', 108, 40)
    f.io('g', x, 96, '输入状态码 code', 150, 24)
    f.dec('z', x, 150, 'code == 0', 116, 42)
    f.io('z1', xr, 150, '输出“短路不亮”', 132, 24)
    f.proc('z2', xr, 196, 'stop = 1', 90, 22)
    f.dec('t', x, 216, 'code == 2', 116, 42)
    f.io('t1', xl, 268, '输出“闪烁异常”', 132, 24)
    f.io('n1', x, 280, '输出“正常点亮”', 132, 24)
    f.proc('i', x, 336, 'col++', 80, 22)
    f.box('q', xr, 300, '内层循环结束', 116, 24, fill='#fff', dash=True)
    f.dec('k', xr, 362, 'stop == 1', 110, 40)
    f.box('o1', xr, 430, '跳出外层循环', 110, 24, fill='#fff', stroke=RED, color=RED, weight=700)
    f.box('o2', x - 10, 430, 'row++，巡检下一行', 140, 24, fill='#fff', dash=True)
    f.line([(x, 8), f.p('e', 't')])
    f.v('e', 'g')
    f.v('g', 'z')
    f.line([f.p('z', 'r'), f.p('z1', 'l')])
    f.v('z1', 'z2')
    f.v('z', 't')
    f.line([f.p('t', 'l'), (xl, 216), f.p('t1', 't')])
    f.v('t', 'n1')
    f.line([f.p('n1', 'b'), f.p('i', 't')])
    f.line([f.p('i', 'l'), (10, 336), (10, 44), f.p('e', 'l')])
    f.line([f.p('e', 'r'), (xr + 76, 44), (xr + 76, 300), f.p('q', 'r')])
    f.v('q', 'k')
    f.v('k', 'o1')
    f.line([f.p('k', 'l'), (x - 10, 362), f.p('o2', 't')])
    f.label(x + 74, 141, '是')
    f.label(x + 10, 182, '否', 'start')
    f.label(x - 70, 207, '是')
    f.label(x + 10, 254, '否', 'start')
    f.label(x + 66, 35, '否')
    f.label(xr + 10, 394, '是', 'start')
    f.label(xr - 66, 353, '否')
    f.note(x + 6, 14, '（外层循环中，col = 1 之后）', 'start', 8.4, '#4D4D4D')
    f.note(18, 190, '内层\n循环', 'start', 8.8, M)
    extra = (REDMK + rarrow([(xl, 280), (xl, 318), (x - 20, 318), (x - 20, 325)], 1.6)
             + mtext(xl + 6, 302, 'continue', 8.6, RED, 700, 'start')
             + rarrow([f.p('z2', 'b'), (xr, 288)], 1.6)
             + mtext(xr + 6, 246, 'break：\n跳出内层', 8.6, RED, 700, 'start', 1.25))
    return f.svg(extra)

figs['f_flow3'] = f_flow3()


# ================================================================== 图6-14 兔子数列
def f_rabbit():
    W, H = 520, 178
    o = []
    nums = [1, 1, 2, 3, 5, 8]
    for k, n in enumerate(nums):
        x = 18 + k * 84
        o.append(f'<rect x="{x}" y="8" width="76" height="114" rx="6" fill="{BG}" stroke="{L}" stroke-width="1"/>')
        for q in range(n):
            ix, iy = x + 6 + (q % 3) * 22, 14 + (q // 3) * 22
            o.append(img('rabbit_face', ix, iy, 20))
        o.append(mtext(x + 38, 94, f'{n} 对', 12, D, 700))
        o.append(mtext(x + 38, 112, f'第 {k + 1} 个月', 8.8, '#4D4D4D'))
    a, b, c = (18 + k * 84 + 38 for k in (2, 3, 4))
    o.append(seg([(a, 124), (a, 134), (c, 134), (c, 124)], RED, 1.2) + seg([(b, 124), (b, 134)], RED, 1.2))
    o.append(mtext(b, 148, '2 + 3 = 5：每个月的对数等于前两个月之和', 9.4, RED, 700))
    o.append(mtext(260, 168, '（一个兔头代表一对兔子；每对兔子从出生后第 3 个月起，每个月生一对小兔子；兔子都不死亡）', 8.2, '#4D4D4D'))
    return svgwrap(W, H, ''.join(o))

figs['f_rabbit'] = f_rabbit()


# ================================================================== 图6-15 百钱买百鸡
def f_chick():
    W, H = 520, 186
    o = []
    for k, (icon, name, price) in enumerate((('rooster', '公鸡', '5 元 1 只'), ('chicken', '母鸡', '3 元 1 只'), ('baby_chick', '小鸡', '1 元 3 只'))):
        x = 22 + k * 166
        o.append(f'<rect x="{x}" y="8" width="144" height="118" rx="8" fill="{BG}" stroke="{C}" stroke-width="1"/>')
        o.append(img(icon, x + 44, 14, 56))
        o.append(mtext(x + 72, 88, name, 12, D, 700))
        o.append(mtext(x + 72, 110, price, 11, RED, 700))
    o.append(chip(60, 140, 400, 28, '用 100 元买 100 只鸡，三种鸡各买几只？', fill=C, size=11, rx=6))
    o.append(mtext(260, 182, '——南北朝时期《张丘建算经》中的“百鸡问题”', 8.8, '#4D4D4D'))
    return svgwrap(W, H, ''.join(o))


figs['f_chick'] = f_chick()


# ================================================================== 图6-16 AI 升华：四格漫画
def f_comic():
    W, H = 520, 330
    o = []
    PW, PH = 254, 158
    pos = [(4, 4), (262, 4), (4, 168), (262, 168)]
    for k, (x, y) in enumerate(pos, 1):
        o.append(f'<rect x="{x}" y="{y}" width="{PW}" height="{PH}" rx="8" fill="#fff" stroke="{C}" stroke-width="1.3"/>')
        o.append(f'<circle cx="{x + 14}" cy="{y + 14}" r="9" fill="{C}"/>' + mtext(x + 14, y + 14, str(k), 10, '#fff', 700))
    # 1 1 和 l
    x, y = 4, 4
    o.append(f'<rect x="{x + 28}" y="{y + 30}" width="56" height="64" rx="6" fill="{BG}" stroke="{C}"/>' + mtext(x + 56, y + 62, '1', 40, D, 700, mono=True))
    o.append(f'<rect x="{x + 100}" y="{y + 30}" width="56" height="64" rx="6" fill="{BG}" stroke="{RED}"/>' + mtext(x + 128, y + 62, 'l', 40, RED, 700, mono=True))
    o.append(mtext(x + 56, y + 108, '数字 1', 9, D, 700) + mtext(x + 128, y + 108, '小写字母 l', 9, RED, 700))
    o.append(av_he(x + 212, y + 118, 22, 'happy'))
    o.append(bubble(x + 168, y + 28, 80, 50, '第 2 盏灯\n输入 l……', (x + 208, y + 94), 8.8))
    o.append(mtext(x + 92, y + 140, '同学试用时，把 1 误输成了 l', 8.6, '#4D4D4D'))
    # 2 停不下来
    x, y = 262, 4
    o.append(f'<rect x="{x + 12}" y="{y + 28}" width="150" height="112" rx="4" fill="#0C0C0C"/>')
    for j, s in enumerate(['第3个灯正常点亮', '第4个灯正常点亮', '第5个灯正常点亮', '第6个灯正常点亮', '第7个灯正常点亮', '……']):
        o.append(f'<text x="{x + 18}" y="{y + 44 + j * 17}" font-size="8.6" fill="#CCCCCC" font-family="{MONO}">{esc(s)}</text>')
    o.append(arrow([(x + 150, y + 120), (x + 150, y + 40)], RED, 1.6))
    o.append(av_he(x + 212, y + 124, 22, 'shock'))
    o.append(bubble(x + 172, y + 30, 76, 46, '停不下来\n了！', (x + 208, y + 100), 9.4))
    # 3 原因
    x, y = 4, 168
    o.append(mtext(x + 28, y + 34, '缓冲区：', 9, D, 700, 'start'))
    for j, ch_ in enumerate(['l', '⏎']):
        o.append(f'<rect x="{x + 78 + j * 24}" y="{y + 22}" width="22" height="24" rx="2" fill="{BG}" stroke="{RED if j == 0 else C}" stroke-width="1.2"/>' + mtext(x + 89 + j * 24, y + 34, ch_, 11, RED if j == 0 else D, 700, mono=True))
    o.append(mtext(x + 16, y + 66, 'scanf 读不进 l，l 一直留在缓冲区；', 8.6, '#1F1F1F', 400, 'start'))
    o.append(mtext(x + 16, y + 82, 'code 还是上一次的 1，', 8.6, '#1F1F1F', 400, 'start'))
    o.append(mtext(x + 16, y + 98, '永远等不到 0——死循环！', 8.6, RED, 700, 'start'))
    o.append(av_zhi(x + 212, y + 124, 22, 'think'))
    o.append(img('magnifying_glass_tilted_left', x + 150, y + 104, 34))
    # 4 Ctrl+C，问 AI
    x, y = 262, 168
    o.append(av_he(x + 40, y + 126, 22, 'think'))
    o.append(bubble(x + 12, y + 28, 112, 54, '先按 Ctrl+C\n结束程序，\n再问问 AI！', (x + 42, y + 102), 8.8))
    o.append(av_zhi(x + 206, y + 126, 22, 'happy'))
    o.append(bubble(x + 134, y + 28, 114, 54, 'AI 的办法，\n也要用错误的\n输入试一试哦！', (x + 204, y + 102), 8.6))
    o.append(img('keyboard', x + 100, y + 108, 36))
    return svgwrap(W, H, ''.join(o))


figs['f_comic'] = f_comic()

# ------------------------------------------------------------------ 课堂练习图标（与项目三～五相同）
figs['ico_practice'] = f'''<svg viewBox="0 0 54 54" width="54" height="54"><rect x="1" y="1" width="52" height="52" rx="10" fill="{C}"/>
<path d="M16 38l3-9 15-15 6 6-15 15z" fill="#fff"/><path d="M16 38l3-9 6 6z" fill="{L}"/><path d="M31 17l6 6" stroke="{C}" stroke-width="2"/></svg>'''

CSS = f'''
body {{ margin:0; background:#fff; font-family:{FONT}; }}
.fig {{ display:inline-block; padding:6px; background:#fff; margin:10px; }}
'''

if __name__ == '__main__':
    import os
    os.makedirs('fig', exist_ok=True)
    with open('fig/figs.html', 'w', encoding='utf8') as fh:
        fh.write(f'<!doctype html><meta charset="utf-8"><style>{CSS}</style><body>')
        for k, v in figs.items():
            fh.write(f'<div class="fig" id="{k}">{v}</div>\n')
    print(' '.join(figs))
