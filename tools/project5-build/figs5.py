# 项目五插图：生成 fig/figs.html（每张图一个 id），再用 shot.js 截成 PNG
# 版式元素只用主色系：#1D4F91 主色、#153A6B 深、#4A75AE 中、#C5D3E7 浅线、#E8EEF7 浅底，加黑灰；
# 强调和“新增”用红色 #D0312D（与项目四相同）；彩色只出现在图标（Fluent Emoji，MIT）里
exec(open('base4.py', encoding='utf8').read())

figs = {}
RED = '#D0312D'


def chip(x, y, w, h, s, fill=C, color='#fff', size=9, weight=700, rx=None, stroke='none', mono=False):
    rx = h / 2 if rx is None else rx
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1"/>'
            + mtext(x + w / 2, y + h / 2, s, size, color, weight, mono=mono))


def arrow(pts, color=M, width=1.4, dash=False):
    d = 'M' + ' L'.join(f'{a:.1f},{b:.1f}' for a, b in pts)
    da = ' stroke-dasharray="4 3"' if dash else ''
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" marker-end="url(#ar)"{da}/>'


def seg(pts, color=M, width=1.4, dash=False):
    d = 'M' + ' L'.join(f'{a:.1f},{b:.1f}' for a, b in pts)
    da = ' stroke-dasharray="4 3"' if dash else ''
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"{da}/>'


def code_lines(x, y, lines, size=9.6, lh=15, color='#1F1F1F'):
    return ''.join(f'<text x="{x}" y="{y + i * lh}" font-size="{size}" fill="{color}" font-family="{MONO}" xml:space="preserve">{esc(s)}</text>'
                   for i, s in enumerate(lines))


# ================================================================== 图5-1 情境：光伏组件监测实训台
def f_scene():
    W, H = 520, 286
    o = [chip(10, 8, 200, 24, '光伏组件监测实训台', size=10.5)]
    o.append(img('sun', 16, 44, 46))
    # 光伏组件（6×4 片电池片）
    px, py, pw, ph = 70, 58, 132, 88
    o.append(f'<rect x="{px - 4}" y="{py - 4}" width="{pw + 8}" height="{ph + 8}" rx="3" fill="#B8C2CF"/>')
    for r in range(4):
        for c in range(6):
            o.append(f'<rect x="{px + c * 22 + 1}" y="{py + r * 22 + 1}" width="20" height="20" fill="{D}"/>'
                     f'<line x1="{px + c * 22 + 11}" y1="{py + r * 22 + 1}" x2="{px + c * 22 + 11}" y2="{py + r * 22 + 21}" stroke="{M}" stroke-width="0.6"/>')
    o.append(f'<line x1="{px + 40}" y1="{py + ph + 4}" x2="{px + 30}" y2="{py + ph + 34}" stroke="#7F8A99" stroke-width="3"/>'
             f'<line x1="{px + 92}" y1="{py + ph + 4}" x2="{px + 102}" y2="{py + ph + 34}" stroke="#7F8A99" stroke-width="3"/>')
    o.append(mtext(px + pw / 2, py + ph + 46, '光伏组件（额定工作电压 18 V）', 9, D, 700))
    # 电压表
    mx, my = 222, 74
    o.append(f'<rect x="{mx}" y="{my}" width="58" height="82" rx="8" fill="{C}"/>'
             f'<rect x="{mx + 6}" y="{my + 8}" width="46" height="24" rx="2" fill="#DCE9D8"/>'
             f'<text x="{mx + 29}" y="{my + 25}" font-size="11" font-weight="700" text-anchor="middle" font-family="{MONO}" fill="#1F1F1F">21.5V</text>'
             f'<circle cx="{mx + 29}" cy="{my + 54}" r="12" fill="{BG}"/><line x1="{mx + 29}" y1="{my + 54}" x2="{mx + 37}" y2="{my + 46}" stroke="{D}" stroke-width="2"/>'
             f'<circle cx="{mx + 17}" cy="{my + 74}" r="3" fill="#D0312D"/><circle cx="{mx + 41}" cy="{my + 74}" r="3" fill="#1F1F1F"/>')
    o.append(f'<path d="M{px + pw + 4},{py + 30} C{px + pw + 18},{py + 30} {mx - 10},{my + 100} {mx + 17},{my + 77}" fill="none" stroke="#D0312D" stroke-width="1.3"/>'
             f'<path d="M{px + pw + 4},{py + 60} C{px + pw + 12},{py + 70} {mx},{my + 110} {mx + 41},{my + 77}" fill="none" stroke="#1F1F1F" stroke-width="1.3"/>')
    o.append(mtext(mx + 29, my + 96, '电压表', 9, D, 700))
    o.append(av_he(46, 234, 26, 'think'))
    o.append(bubble(84, 200, 196, 46, '测得 21.5 V，属于哪种状态？\n要让程序自动判断！', (74, 226), 9))
    # 右：判定标准标尺
    gx, gw = 312, 40
    segs = [(('紧急', '过压'), '电压＞24 V\n紧急告警，立即停机保护', 'police_car_light', D, '#fff', 56),
            (('过压', '预警'), '21 V＜电压≤24 V\n及时核查组件与线路', 'warning', M, '#fff', 50),
            (('正常', '工作'), '15 V≤电压≤21 V\n组件稳定运行', 'check_mark_button', BG, D, 74),
            (('欠压', ''), '电压＜15 V\n组件进入待机', 'zzz', L, D, 56)]
    o.append(chip(gx - 6, 8, 202, 24, '实训指导书：电压判定标准', fill=BG, color=D, stroke=C, size=10))
    y = 40
    ticks = ['24 V', '21 V', '15 V']
    for k, (name, desc, icon, fill, col, h) in enumerate(segs):
        o.append(f'<rect x="{gx}" y="{y}" width="{gw}" height="{h}" fill="{fill}" stroke="{C}" stroke-width="1"/>')
        o.append(mtext(gx + gw / 2, y + h / 2, '\n'.join(t for t in name if t), 9, col, 700))
        o.append(img(icon, gx + gw + 8, y + h / 2 - 15, 30))
        o.append(mtext(gx + gw + 44, y + h / 2, desc, 9, '#1F1F1F', 400, 'start', 1.35))
        if k < 3:
            o.append(f'<line x1="{gx - 6}" y1="{y + h}" x2="{gx}" y2="{y + h}" stroke="{D}" stroke-width="1.2"/>' + mtext(gx - 9, y + h, ticks[k], 8.6, D, 700, 'end'))
        y += h
    return svgwrap(W, H, ''.join(o))


figs['f_scene'] = f_scene()


# ================================================================== 图5-2 知识导图
def kmap():
    tasks = [("任务一 判别光伏组件电压条件", ["选择结构示例：单分支、双分支、多分支", "关系运算符与关系表达式", "逻辑运算符与逻辑表达式", "单分支 if 语句及易错点", "任务实施：检测电压是否异常", "边界值测试"]),
             ("任务二 区分组件电压不同状态", ["if…else 语句", "if…else if…else 语句", "switch 语句：break、default、case 穿透", "if…else if…else 与 switch 的比较", "任务实施：区分欠压、正常、过压"]),
             ("任务三 研判光伏组件预告警", ["if 语句的嵌套", "else 的配对：悬空 else 问题", "综合示例：条件运算符、短路求值", "综合示例：switch 与 if 配合、书写规范", "任务实施：过压时再分级"]),
             ("AI升华 用边界值检验 AI", ["设计边界测试数据，逐个检验 AI 的写法", "离开 AI 再做：配对 else、写嵌套版本"])]
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
<text x="68" y="{mid - 4}" fill="#fff" font-size="13" font-weight="700" text-anchor="middle">项目五</text>
<text x="68" y="{mid + 14}" fill="#fff" font-size="10.5" text-anchor="middle">判断场景分支路径</text>
<g font-size="9.6" font-weight="700" text-anchor="middle">{''.join(boxes)}</g>
<g font-size="9.4" fill="#1F1F1F">{''.join(texts)}</g>
<g fill="{C}">{''.join(dots)}</g></svg>'''


figs['f_kmap'] = kmap()


# ================================================================== 图5-3、5-8、5-13 电压数轴（三个任务逐步细分）
def f_zone(stage):
    W = 520
    X0, X1, V0, V1 = 30, 452, 10, 30
    sx = lambda v: X0 + (v - V0) * (X1 - X0) / (V1 - V0)
    ay = 70
    if stage == 1:
        bands = [(V0, 15, '异常', L, D, '输出：电压异常，\n请检查光伏组件！'), (15, 21, '正常', BG, D, '不输出'), (21, V1, '异常', L, D, '输出：电压异常，\n请检查光伏组件！')]
    elif stage == 2:
        bands = [(V0, 15, '欠压', L, D, '欠压，请检查光伏组件！'), (15, 21, '正常', BG, D, '电压正常，组件稳定运行！'), (21, V1, '过压', M, '#fff', '请注意过压！')]
    else:
        bands = [(V0, 15, '欠压', L, D, '欠压，请检查\n光伏组件！'), (15, 21, '正常', BG, D, '电压正常，\n组件稳定运行！'),
                 (21, 24, '过压预警', M, '#fff', '请注意过压！\n及时核查组件\n与线路！'), (24, V1, '紧急过压', D, '#fff', '请注意过压！\n紧急告警，\n立即停机保护！')]
    H = 168 if stage == 3 else 146
    o = []
    for a, z, name, fill, col, out in bands:
        o.append(f'<rect x="{sx(a)}" y="{ay - 34}" width="{sx(z) - sx(a)}" height="28" fill="{fill}" stroke="{C}" stroke-width="0.8"/>')
        o.append(mtext((sx(a) + sx(z)) / 2, ay - 20, name, 10, col, 700))
        o.append(mtext((sx(a) + sx(z)) / 2, ay + 40 + (8 if stage == 3 else 0), out, 8.8, '#1F1F1F' if out != '不输出' else '#7F7F7F', 400, 'middle', 1.3))
    o.append(arrow([(X0 - 6, ay), (X1 + 14, ay)], '#1F1F1F', 1.2))
    o.append(mtext(X1 + 18, ay, '电压（V）', 8.6, '#1F1F1F', 400, 'start'))
    for v in range(V0, V1 + 1):
        big = v in (10, 15, 18, 21, 24, 30)
        o.append(f'<line x1="{sx(v)}" y1="{ay}" x2="{sx(v)}" y2="{ay + (6 if big else 3)}" stroke="#1F1F1F" stroke-width="{1 if big else 0.6}"/>')
        if big:
            o.append(mtext(sx(v), ay + 14, str(v), 8.8, D if v != 18 else '#7F7F7F', 700 if v != 18 else 400))
    # 边界：实心点表示包含该点
    pts = {1: [(15, True), (21, True)], 2: [(15, True), (21, True)], 3: [(15, True), (21, True), (24, True)]}[stage]
    for v, filled in pts:
        o.append(f'<circle cx="{sx(v)}" cy="{ay - 6}" r="3.6" fill="{RED if filled else "#fff"}" stroke="{RED}" stroke-width="1.2"/>')
    if stage == 1:
        for v, lab in ((20, '20 V'), (22, '22 V')):
            o.append(f'<path d="M{sx(v)},{ay - 6} l-5,-9 h10 z" fill="{RED}"/>' + mtext(sx(v), ay - 50, lab, 9, RED, 700))
            o.append(f'<line x1="{sx(v)}" y1="{ay - 44}" x2="{sx(v)}" y2="{ay - 15}" stroke="{RED}" stroke-width="1" stroke-dasharray="2 2"/>')
    o.append(f'<circle cx="{X0 + 2}" cy="{H - 10}" r="3.6" fill="{RED}"/>' + mtext(X0 + 10, H - 10, '红点表示该边界值属于左侧或中间的区间：15 V、21 V 属于正常' + ('，24 V 属于过压预警' if stage == 3 else ''), 8.4, '#4D4D4D', 400, 'start'))
    return svgwrap(W, H, ''.join(o))


figs['f_zone1'] = f_zone(1)
figs['f_zone2'] = f_zone(2)
figs['f_zone3'] = f_zone(3)


# ================================================================== 图5-4 选择结构的三种形式
def f_forms():
    f = FC(520, 262, 9.4)
    # (a) 单分支
    x = 80
    f.dec('a1', x, 56, '条件', 76, 40)
    f.proc('aA', x, 118, 'A', 56, 24)
    f.line([(x, 20), f.p('a1', 't')])
    f.v('a1', 'aA')
    f.line([f.p('aA', 'b'), (x, 172)], False)
    f.line([f.p('a1', 'r'), (x + 56, 56), (x + 56, 162), (x, 162)], False)
    f.line([(x, 162), (x, 196)])
    f.label(x - 10, 90, '是', 'end')
    f.label(x + 50, 48, '否')
    f.note(x, 210, '出口', 'middle')
    # (b) 双分支
    x = 258
    f.dec('b1', x, 56, '条件', 76, 40)
    f.proc('bA', x - 50, 118, 'A', 56, 24)
    f.proc('bB', x + 50, 118, 'B', 56, 24)
    f.line([(x, 20), f.p('b1', 't')])
    f.line([f.p('b1', 'l'), (x - 50, 56), f.p('bA', 't')])
    f.line([f.p('b1', 'r'), (x + 50, 56), f.p('bB', 't')])
    f.line([f.p('bA', 'b'), (x - 50, 162), (x + 50, 162), f.p('bB', 'b')], False)
    f.line([(x, 162), (x, 196)])
    f.label(x - 44, 48, '是')
    f.label(x + 44, 48, '否')
    f.note(x, 210, '出口', 'middle')
    # (c) 多分支：判断框排成一列，分支向右，经右侧总线汇合
    x, bx = 396, 506
    f.dec('c1', x, 50, '条件 1', 80, 38)
    f.dec('c2', x, 112, '条件 2', 80, 38)
    f.proc('cA', x + 74, 50, 'A', 38, 24)
    f.proc('cB', x + 74, 112, 'B', 38, 24)
    f.proc('cC', x, 162, 'C', 56, 24)
    f.line([(x, 14), f.p('c1', 't')])
    f.v('c1', 'c2')
    f.v('c2', 'cC')
    f.line([f.p('c1', 'r'), f.p('cA', 'l')])
    f.line([f.p('c2', 'r'), f.p('cB', 'l')])
    f.line([f.p('cA', 'r'), (bx, 50), (bx, 186), (x, 186)], False)
    f.line([f.p('cB', 'r'), (bx, 112)], False)
    f.line([f.p('cC', 'b'), (x, 186)], False)
    f.line([(x, 186), (x, 200)])
    f.label(x + 46, 41, '是')
    f.label(x + 46, 103, '是')
    f.label(x - 10, 80, '否', 'end')
    f.label(x - 10, 142, '否', 'end')
    f.note(x, 212, '出口', 'middle')
    for cx, t1, t2 in ((80, '（a）单分支', '例：电量提醒'), (258, '（b）双分支', '例：考核是否通过'), (420, '（c）多分支', '例：温度提示')):
        f.el.append(mtext(cx, 234, t1, 10, D, 700) + mtext(cx, 252, t2, 8.8, '#4D4D4D'))
    return f.svg()


figs['f_forms'] = f_forms()


# ================================================================== 图5-5 优先级与条件的解读
def f_prec():
    W, H = 520, 252
    o = [mtext(108, 14, '优先级（从高到低）', 10, D, 700)]
    rows = [('!', '逻辑非'), ('*　/　%', '算术运算符'), ('+　-', '算术运算符'), ('<　<=　>　>=', '关系运算符'), ('==　!=', '关系运算符'),
            ('&&', '逻辑与'), ('||', '逻辑或'), ('? :', '条件运算符'), ('=　+=　-=　…', '赋值运算符')]
    hl = {0: True, 5: True, 6: True}
    for k, (op, name) in enumerate(rows):
        y = 26 + k * 24
        x = 14 + k * 8
        fill = C if (k in hl) else (BG if k in (3, 4) else '#fff')
        col = '#fff' if k in hl else D
        o.append(f'<rect x="{x}" y="{y}" width="112" height="20" rx="3" fill="{fill}" stroke="{C}" stroke-width="0.9"/>')
        o.append(mtext(x + 56, y + 10, op, 9.6, col, 700, mono=True))
        o.append(mtext(x + 120, y + 10, name, 8.8, '#1F1F1F', 400, 'start'))
    o.append(arrow([(6, 30), (6, 238)], C, 1.2))
    o.append(mtext(300, 244, '注：浅蓝底为关系运算符，深蓝底为逻辑运算符', 8.2, '#4D4D4D', 400, 'start'))
    # 右：解读 v < 15 || v > 21（v 为 22）
    bx = 300
    o.append(chip(bx, 20, 210, 22, '解读 v < 15 || v > 21（设 v 为 22）', fill=BG, color=D, stroke=C, size=9.2, rx=3))
    o.append(f'<text x="{bx + 105}" y="{74}" font-size="13" text-anchor="middle" font-family="{MONO}" fill="#1F1F1F" xml:space="preserve">v &lt; 15  ||  v &gt; 21</text>')
    o.append(seg([(bx + 30, 82), (bx + 30, 90), (bx + 88, 90), (bx + 88, 82)], C, 1.2) + seg([(bx + 59, 90), (bx + 59, 104)], C, 1.2))
    o.append(seg([(bx + 122, 82), (bx + 122, 90), (bx + 180, 90), (bx + 180, 82)], C, 1.2) + seg([(bx + 151, 90), (bx + 151, 104)], C, 1.2))
    o.append(chip(bx + 34, 104, 50, 22, '① 0', fill='#fff', color=D, stroke=C, size=10, rx=3))
    o.append(chip(bx + 126, 104, 50, 22, '② 1', fill='#fff', color=D, stroke=C, size=10, rx=3))
    o.append(seg([(bx + 59, 126), (bx + 59, 140), (bx + 151, 140), (bx + 151, 126)], C, 1.2) + arrow([(bx + 105, 140), (bx + 105, 160)], C, 1.2))
    o.append(chip(bx + 66, 160, 78, 24, '③ 0 || 1 → 1', fill=C, size=10, rx=3))
    o.append(mtext(bx + 105, 212, '①② 先算关系运算（优先级高）\n③ 再算逻辑或：一真即真，条件成立', 9, '#1F1F1F', 400, 'middle', 1.4))
    return svgwrap(W, H, ''.join(o))


figs['f_prec'] = f_prec()


# ================================================================== 图5-6 单分支 if 语句
def f_ifsyn():
    W, H = 520, 210
    o = [f'<rect x="14" y="30" width="186" height="96" rx="4" fill="{BG}" stroke="{C}" stroke-width="1"/>']
    o.append(code_lines(30, 56, ['if (表达式)', '{', '    语句组', '}'], 11, 19, D))
    o.append(f'<rect x="44" y="44" width="62" height="17" rx="2" fill="none" stroke="{RED}" stroke-width="1.2"/>')
    o.append(f'<path d="M26,{70} h-6 V{122} h6" fill="none" stroke="{RED}" stroke-width="1.2"/>')
    o.append(mtext(14, 18, '①条件：写在圆括号中，非 0 为真', 9, RED, 700, 'start'))
    o.append(mtext(14, 146, '②执行语句：条件为真时执行；', 9, RED, 700, 'start'))
    o.append(mtext(14, 162, '　多条语句要用花括号括起来', 9, RED, 700, 'start'))
    f = FC(520, 210, 9.4)
    x = 360
    f.dec('d', x, 52, '表达式', 96, 44)
    f.proc('s', x, 118, '语句组', 90, 26)
    f.box('n', x, 182, 'if 语句后面的语句', 140, 24, fill='#fff')
    f.line([(x, 14), f.p('d', 't')])
    f.v('d', 's')
    f.line([f.p('s', 'b'), (x, 156)], False)
    f.line([f.p('d', 'r'), (x + 84, 52), (x + 84, 156), (x, 156)], False)
    f.line([(x, 156), f.p('n', 't')])
    f.label(x - 10, 92, '真（非 0）', 'end')
    f.label(x + 70, 42, '假（0）')
    return svgwrap(W, H, ''.join(o) + ''.join(f.ln) + ''.join(f.el))


figs['f_ifsyn'] = f_ifsyn()


# ================================================================== 图5-7 任务一流程图
def f_flow1():
    f = FC(420, 300, 9.4)
    x = 150
    f.term('s', x, 18, '开始')
    f.io('a', x, 62, '输入电压 v', 140)
    f.dec('d', x, 128, 'v < 15 || v > 21', 170, 58)
    f.io('o', x, 200, '输出“电压异常，请检查光伏组件！”', 230)
    f.term('e', x, 278, '结束')
    f.v('s', 'a')
    f.v('a', 'd')
    f.v('d', 'o')
    f.line([f.p('o', 'b'), (x, 244)], False)
    f.line([f.p('d', 'r'), (x + 150, 128), (x + 150, 244), (x, 244)], False)
    f.line([(x, 244), f.p('e', 't')])
    f.label(x - 10, 168, '是', 'end')
    f.label(x + 120, 118, '否')
    br = ''
    for y1, y2, t in ((48, 76, '输入'), (98, 214, '处理和输出')):
        br += f'<path d="M{x + 170},{y1} h6 V{y2} h-6" fill="none" stroke="{L}" stroke-width="1.2"/>' + mtext(x + 184, (y1 + y2) / 2, t, 9.4, C, 700, 'start')
    return f.svg(br)


figs['f_flow1'] = f_flow1()


# ================================================================== 图5-9 if…else 语句
def f_ifelse():
    W, H = 520, 196
    o = [f'<rect x="14" y="20" width="170" height="160" rx="4" fill="{BG}" stroke="{C}" stroke-width="1"/>']
    o.append(code_lines(30, 42, ['if (表达式)', '{', '    语句组 1', '}', 'else', '{', '    语句组 2', '}'], 10.4, 18.5, D))
    f = FC(520, 196, 9.4)
    x = 370
    f.dec('d', x, 50, '表达式', 96, 44)
    f.proc('a', x - 80, 106, '语句组 1', 84, 26)
    f.proc('b', x + 80, 106, '语句组 2', 84, 26)
    f.box('n', x, 172, 'if 语句后面的语句', 140, 24, fill='#fff')
    f.line([(x, 12), f.p('d', 't')])
    f.line([f.p('d', 'l'), (x - 80, 50), f.p('a', 't')])
    f.line([f.p('d', 'r'), (x + 80, 50), f.p('b', 't')])
    f.line([f.p('a', 'b'), (x - 80, 142), (x + 80, 142), f.p('b', 'b')], False)
    f.line([(x, 142), f.p('n', 't')])
    f.label(x - 66, 40, '真')
    f.label(x + 66, 40, '假')
    return svgwrap(W, H, ''.join(o) + ''.join(f.ln) + ''.join(f.el))


figs['f_ifelse'] = f_ifelse()


# ================================================================== 图5-10 if…else if…else 语句
def f_ladder():
    f = FC(520, 330, 9.2)
    x, px, bus = 150, 320, 410
    ys = [42, 108, 196]
    f.line([(x, 8), (x, ys[0] - 22)])
    for k, (y, t, s) in enumerate(zip(ys, ['表达式 1', '表达式 2', '表达式 n'], ['语句组 1', '语句组 2', '语句组 n'])):
        f.dec(f'd{k}', x, y, t, 104, 44)
        f.proc(f'p{k}', px, y, s, 90, 26)
        f.line([f.p(f'd{k}', 'r'), f.p(f'p{k}', 'l')])
        f.label(x + 66, y - 9, '真')
        f.line([f.p(f'p{k}', 'r'), (bus, y)], False)
    f.line([f.p('d0', 'b'), f.p('d1', 't')])
    f.line([f.p('d1', 'b'), (x, 140)], False)
    f.el.append(mtext(x, 152, '……', 11, D, 700))
    f.line([(x, 160), f.p('d2', 't')])
    for y in (ys[0] + 32, ys[1] + 32, ys[2] + 32):
        f.label(x + 10, y, '假', 'start')
    f.proc('pe', x, 262, '语句组 n+1（else 部分）', 170, 26)
    f.v('d2', 'pe')
    f.line([(bus, ys[0]), (bus, 296)], False)
    f.line([f.p('pe', 'b'), (x, 296), (bus, 296)], False)
    f.line([(280, 296), (280, 318)])
    f.note(286, 318, '整个语句后面的语句', 'start')
    f.el.append(mtext(470, 150, '只执行\n其中一个\n语句组', 9.4, RED, 700, 'middle', 1.3))
    return f.svg()


figs['f_ladder'] = f_ladder()


# ================================================================== 图5-11 switch 语句：有 break 与没有 break
def f_switch():
    W, H = 520, 262
    o = []
    labels = ["case 'A':", "case 'B':", "case 'C':", "case 'D':", 'default:']
    for col, (x0, title, entry, brk) in enumerate(((6, '（a）有 break：只执行一段', 2, True), (266, '（b）没有 break：从入口一直往下执行', 1, False))):
        bx0, bw = x0 + 92, 126            # 语句框的左边和宽度
        cx = bx0 + bw / 2
        o.append(mtext(x0 + 124, 14, title, 9.8, D, 700))
        o.append(chip(bx0 - 40, 26, bw + 50, 22, f"switch (area)　area 为 '{'CB'[col]}'", fill=BG, color=D, stroke=C, size=9, rx=3))
        for k, lab in enumerate(labels):
            y = 64 + k * 36
            run_ = (k == entry) if brk else (k >= entry)
            fill = C if run_ else '#fff'
            o.append(f'<rect x="{bx0}" y="{y}" width="{bw}" height="26" rx="3" fill="{fill}" stroke="{C}" stroke-width="1"/>')
            o.append(mtext(bx0 - 4, y + 13, lab, 9, D, 700, 'end', mono=True))
            txt = '语句组' + ('　break;' if brk and k < 4 else '')
            o.append(mtext(cx, y + 13, txt, 9, '#fff' if run_ else '#7F7F7F', 700 if run_ else 400))
            if not brk and run_ and k < 4:
                o.append(arrow([(cx, y + 26), (cx, y + 36)], RED, 1.4))
        ey = 64 + entry * 36 + 13
        o.append(arrow([(x0, ey), (x0 + 30, ey)], RED, 1.6) + mtext(x0 + 2, ey - 10, '入口', 8.6, RED, 700, 'start'))
        if brk:
            o.append(arrow([(bx0 + bw + 2, ey), (bx0 + bw + 16, ey), (bx0 + bw + 16, 250), (cx + 70, 250)], RED, 1.4)
                     + mtext(bx0 + bw + 20, ey + 14, 'break：\n跳出\nswitch', 8.4, RED, 700, 'start', 1.25))
            o.append(mtext(cx + 66, 250, 'switch 语句后面的语句', 8.8, '#1F1F1F', 400, 'end'))
        else:
            o.append(arrow([(cx, 64 + 4 * 36 + 26), (cx, 240)], RED, 1.4))
            o.append(mtext(cx, 252, 'switch 语句后面的语句', 8.8, '#1F1F1F', 400, 'middle'))
    return svgwrap(W, H, ''.join(o))


figs['f_switch'] = f_switch()


# ================================================================== 图5-12 任务二流程图
def f_flow2():
    f = FC(440, 330, 9.2)
    x, px, bus = 120, 300, 420
    f.term('s', x, 18, '开始')
    f.io('a', x, 60, '输入电压 v', 130)
    f.dec('d1', x, 118, 'v < 15', 110, 46)
    f.dec('d2', x, 190, 'v <= 21', 110, 46)
    f.io('o1', px, 118, '输出“欠压，请检查光伏组件！”', 200, 26)
    f.io('o2', px, 190, '输出“电压正常，组件稳定运行！”', 200, 26)
    f.io('o3', x, 254, '输出“请注意过压！”', 170, 26)
    f.term('e', 260, 314, '结束')
    f.v('s', 'a')
    f.v('a', 'd1')
    f.v('d1', 'd2')
    f.v('d2', 'o3')
    f.line([f.p('d1', 'r'), f.p('o1', 'l')])
    f.line([f.p('d2', 'r'), f.p('o2', 'l')])
    for k in ('o1', 'o2'):
        xx, yy, ww, hh = f.n[k]
        f.line([f.p(k, 'r'), (bus, yy)], False)
    f.line([(bus, 118), (bus, 286), (260, 286)], False)
    f.line([f.p('o3', 'b'), (x, 286), (260, 286)], False)
    f.line([(260, 286), f.p('e', 't')])
    f.label(x + 66, 109, '是')
    f.label(x + 66, 181, '是')
    f.label(x + 10, 152, '否', 'start')
    f.label(x + 10, 224, '否', 'start')
    f.note(x - 58, 160, '走到这里，\n说明 v≥15', 'end', 8.4, RED)
    return f.svg()


figs['f_flow2'] = f_flow2()


# ================================================================== 图5-14 if 嵌套（login2.c）
def f_nest():
    f = FC(470, 352, 9.2)
    x = 150
    f.term('s', x, 16, '开始')
    f.io('a', x, 56, '输入账号 id', 130)
    f.dec('d1', x, 112, '账号正确？', 110, 46)
    f.io('b', x, 170, '输入密码 pwd', 130)
    f.dec('d2', x, 228, '密码正确？', 110, 46)
    f.io('ok', x - 72, 286, '登录成功', 100, 26)
    f.io('no', x + 72, 286, '密码错误', 100, 26)
    f.io('na', 370, 170, '账号不存在', 110, 26)
    f.term('e', 370, 334, '结束')
    f.v('s', 'a')
    f.v('a', 'd1')
    f.v('d1', 'b')
    f.v('b', 'd2')
    f.line([f.p('d2', 'l'), (x - 72, 228), f.p('ok', 't')])
    f.line([f.p('d2', 'r'), (x + 72, 228), f.p('no', 't')])
    f.line([f.p('d1', 'r'), (370, 112), f.p('na', 't')])
    f.line([f.p('ok', 'b'), (x - 72, 334), f.p('e', 'l')])
    f.line([f.p('no', 'b'), (x + 72, 334)], False)
    f.line([f.p('na', 'b'), f.p('e', 't')])
    f.label(x - 10, 144, '是', 'end')
    f.label(x + 70, 102, '否')
    f.label(x - 62, 218, '是')
    f.label(x + 62, 218, '否')
    box = (f'<rect x="{x - 134}" y="{150}" width="268" height="154" rx="6" fill="none" stroke="{RED}" stroke-width="1.2" stroke-dasharray="5 3"/>'
           + mtext(x - 128, 160, '内层 if…else', 9, RED, 700, 'start'))
    box += (f'<rect x="{x - 142}" y="{84}" width="440" height="224" rx="8" fill="none" stroke="{C}" stroke-width="1" stroke-dasharray="2 3"/>'
            + mtext(x + 290, 96, '外层 if…else', 9, C, 700, 'end'))
    return f.svg(box)


figs['f_nest'] = f_nest()


# ================================================================== 图5-15 else 的配对
def f_pair():
    W, H = 520, 250
    o = [mtext(120, 14, '（a）缩进“看起来”的配对', 9.8, D, 700), mtext(390, 14, '（b）加花括号，else 与第一个 if 配对', 9.8, D, 700)]
    left = ['if (v > 21)', '    if (v > 24)', '        printf("紧急…");', 'else', '    printf("没有过压");']
    o.append(f'<rect x="10" y="26" width="236" height="104" rx="4" fill="{BG}" stroke="{C}" stroke-width="1"/>')
    o.append(code_lines(54, 48, left, 10, 19, D))
    # 看起来的配对（灰，打叉）与实际配对（红）
    o.append(seg([(50, 44), (36, 44), (36, 101), (50, 101)], '#9A9A9A', 1.4, True) + mtext(28, 72, '✗', 12, '#9A9A9A', 700))
    o.append(seg([(150, 63), (232, 63), (232, 101), (84, 101)], RED, 1.6))
    o.append(mtext(128, 150, '实际：else 与前面最近的、\n尚未配对的 if（第 2 行）配对', 9.4, RED, 700, 'middle', 1.4))
    o.append(mtext(128, 196, '缩进只是给人看的，\n编译器不看缩进', 9.2, '#4D4D4D', 400, 'middle', 1.4))
    right = ['if (v > 21)', '{', '    if (v > 24)', '    {', '        printf("紧急…");', '    }', '}', 'else', '{', '    printf("没有过压");', '}']
    o.append(f'<rect x="274" y="26" width="236" height="218" rx="4" fill="{BG}" stroke="{C}" stroke-width="1"/>')
    o.append(code_lines(312, 44, right, 9.6, 18.4, D))
    o.append(seg([(308, 40), (294, 40), (294, 173), (308, 173)], C, 1.6) + mtext(286, 106, '✓', 12, C, 700))
    return svgwrap(W, H, ''.join(o))


figs['f_pair'] = f_pair()


# ================================================================== 图5-16 任务三流程图
def f_flow3():
    f = FC(470, 430, 9.2)
    x, px, bus = 110, 300, 440
    f.term('s', x, 18, '开始')
    f.io('a', x, 58, '输入电压 v', 130)
    f.dec('d1', x, 112, 'v < 15', 104, 44)
    f.dec('d2', x, 178, 'v <= 21', 104, 44)
    f.io('o1', px, 112, '输出“欠压，请检查光伏组件！”', 196, 26)
    f.io('o2', px, 178, '输出“电压正常，组件稳定运行！”', 196, 26)
    f.io('o3', x, 238, '输出“请注意过压！”', 160, 26)
    f.dec('d3', x, 298, 'v <= 24', 104, 44)
    f.io('o4', px, 298, '输出“及时核查组件与线路！”', 196, 26)
    f.io('o5', x, 358, '输出“紧急告警，立即停机保护！”', 196, 26)
    f.term('e', 290, 414, '结束')
    for a, b_ in (('s', 'a'), ('a', 'd1'), ('d1', 'd2'), ('d2', 'o3'), ('o3', 'd3'), ('d3', 'o5')):
        f.v(a, b_)
    for d, o_ in (('d1', 'o1'), ('d2', 'o2'), ('d3', 'o4')):
        f.line([f.p(d, 'r'), f.p(o_, 'l')])
        f.label(x + 64, f.n[d][1] - 9, '是')
        f.label(x + 10, f.n[d][1] + 34, '否', 'start')
    for k in ('o1', 'o2', 'o4'):
        f.line([f.p(k, 'r'), (bus, f.n[k][1])], False)
    f.line([(bus, 112), (bus, 388), (290, 388)], False)
    f.line([f.p('o5', 'b'), (x, 388), (290, 388)], False)
    f.line([(290, 388), f.p('e', 't')])
    box = (f'<rect x="8" y="{258}" width="{bus - 14}" height="{118}" rx="6" fill="none" stroke="{RED}" stroke-width="1.2" stroke-dasharray="5 3"/>'
           + mtext(bus - 12, 268, '新增：嵌套在过压分支中', 8.8, RED, 700, 'end'))
    return f.svg(box)


figs['f_flow3'] = f_flow3()


# ================================================================== 图5-17 AI升华：四格漫画
def f_comic():
    W, H = 520, 330
    o = []
    PW, PH = 254, 158
    pos = [(4, 4), (262, 4), (4, 168), (262, 168)]
    for k, (x, y) in enumerate(pos, 1):
        o.append(f'<rect x="{x}" y="{y}" width="{PW}" height="{PH}" rx="8" fill="#fff" stroke="{C}" stroke-width="1.3"/>')
        o.append(f'<circle cx="{x + 14}" cy="{y + 14}" r="9" fill="{C}"/>' + mtext(x + 14, y + 14, str(k), 10, '#fff', 700))
    # 1 请 AI 写三种写法
    x, y = 4, 4
    o.append(av_he(x + 48, y + 120, 24, 'happy'))
    o.append(img('robot', x + 168, y + 92, 52))
    o.append(bubble(x + 26, y + 26, 108, 44, '请给我三种写法\n的判别程序！', (x + 50, y + 94), 8.8))
    o.append(bubble(x + 140, y + 26, 106, 52, '给！三种写法\n运行结果\n完全相同！', (x + 190, y + 90), 8.8))
    # 2 普通数据都对
    x, y = 262, 4
    o.append(f'<rect x="{x + 14}" y="{y + 30}" width="134" height="88" rx="4" fill="#0C0C0C"/>')
    for j, s in enumerate(['输入 22：', '  ①②③ 请注意过压！', '         及时核查……', '输入 18：', '  ①②③ 电压正常……']):
        o.append(f'<text x="{x + 20}" y="{y + 46 + j * 16}" font-size="8" fill="#CCCCCC" font-family="{MONO}" xml:space="preserve">{esc(s)}</text>')
    o.append(av_he(x + 206, y + 124, 22, 'smile'))
    o.append(bubble(x + 158, y + 30, 88, 46, '22 V、18 V\n都对！AI 真厉害', (x + 202, y + 98), 8.6))
    # 3 边界上出错
    x, y = 4, 168
    o.append(f'<rect x="{x + 14}" y="{y + 30}" width="140" height="62" rx="4" fill="#0C0C0C"/>')
    for j, s in enumerate(['写法②，输入 21.5：', '  电压正常，组件稳定', '  运行！']):
        o.append(f'<text x="{x + 20}" y="{y + 46 + j * 16}" font-size="8" fill="#CCCCCC" font-family="{MONO}" xml:space="preserve">{esc(s)}</text>')
    o.append(f'<rect x="{x + 18}" y="{y + 52}" width="132" height="34" fill="none" stroke="{RED}" stroke-width="1.2"/>')
    o.append(av_he(x + 210, y + 124, 22, 'shock'))
    o.append(bubble(x + 160, y + 26, 88, 58, '21.5 V\n明明过压了，\n怎么是正常？', (x + 206, y + 98), 8.6))
    o.append(mtext(x + 84, y + 120, '写法③输入 21，\n也判成了过压！', 8.6, RED, 700, 'middle', 1.3))
    # 4 小智：边界值是试金石
    x, y = 262, 168
    o.append(av_he(x + 40, y + 126, 22, 'think'))
    o.append(av_zhi(x + 206, y + 126, 22, 'happy'))
    o.append(bubble(x + 12, y + 30, 110, 46, '原来“完全相同”\n也要测一测！', (x + 42, y + 102), 8.6))
    o.append(bubble(x + 132, y + 26, 116, 62, '边界最容易出错！\n15、21、24 和它们\n两边的值都要测。', (x + 204, y + 102), 8.4))
    o.append(img('magnifying_glass_tilted_left', x + 104, y + 104, 34))
    return svgwrap(W, H, ''.join(o))


figs['f_comic'] = f_comic()

# ------------------------------------------------------------------ 课堂练习图标（与项目三、四相同）
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
