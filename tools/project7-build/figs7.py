# 项目七插图：生成 fig/figs.html（每张图一个 id），再用 shot.js 截成 PNG
# 版式元素只用主色系：#1D4F91 主色、#153A6B 深、#4A75AE 中、#C5D3E7 浅线、#E8EEF7 浅底，加黑灰；
# 强调用红色 #D0312D（与项目四～六相同）；彩色只出现在图标（Fluent Emoji，MIT）中
# 图中的电压、状态与书中程序的实测输入相同（第 1～3 轮的数据）
exec(open('base4.py', encoding='utf8').read())

figs = {}
RED = '#D0312D'
GRY = '#7F7F7F'
K1, K2, K3 = C, '#2F8F5B', '#B86E00'          # 定义各部分的标注色
V1 = ['4.02', '3.98', '12.00', '4.05', '3.42', '0.00', '3.96', '4.01']
V2 = ['4.01', '3.99', '12.00', '4.03', '3.67', '0.00', '3.97', '4.02']
V3 = ['4.03', '3.97', '12.00', '4.04', '3.15', '0.00', '3.95', '4.00']
ST = ['正常', '正常', '开路', '正常', '接触不良', '短路', '正常', '正常']
BADK = (2, 4, 5)                               # 第 1 轮异常的测点：V3、V5、V6


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


def cell(x, y, w, h, s, fill='#fff', stroke=C, color='#1F1F1F', size=9.6, mono=False, weight=400, sw=1, dash=False):
    da = ' stroke-dasharray="3 2"' if dash else ''
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{da}/>'
            + (mtext(x + w / 2, y + h / 2, s, size, color, weight, mono=mono) if s else ''))


def res_v(x, y, h=28, w=11, broken=False):
    """竖直放置的电阻（矩形符号），y 为上端"""
    if broken:
        return (f'<rect x="{x - w / 2}" y="{y}" width="{w}" height="{h * 0.42}" fill="#fff" stroke="{D}" stroke-width="1.2"/>'
                f'<rect x="{x - w / 2}" y="{y + h * 0.58}" width="{w}" height="{h * 0.42}" fill="#fff" stroke="{D}" stroke-width="1.2"/>')
    return f'<rect x="{x - w / 2}" y="{y}" width="{w}" height="{h}" fill="#fff" stroke="{D}" stroke-width="1.2"/>'


def wire(pts, color=D, width=1.2):
    return seg(pts, color, width)


def ground(x, y):
    return (f'<line x1="{x - 9}" y1="{y}" x2="{x + 9}" y2="{y}" stroke="{D}" stroke-width="1.4"/>'
            f'<line x1="{x - 6}" y1="{y + 3.5}" x2="{x + 6}" y2="{y + 3.5}" stroke="{D}" stroke-width="1.2"/>'
            f'<line x1="{x - 3}" y1="{y + 7}" x2="{x + 3}" y2="{y + 7}" stroke="{D}" stroke-width="1"/>')


# ================================================================== 图7-1 情境：多路直流分压负载测试实训台
def f_scene():
    W, H = 520, 316
    o = [chip(10, 6, 226, 24, '多路直流分压负载测试实训台', size=10.5),
         chip(246, 6, 264, 24, '每组支路：上电阻 2 kΩ、下电阻 1 kΩ', fill=BG, color=D, stroke=C, size=9.6)]
    top, bot, tp = 50, 178, 113
    xs = [96 + k * 55 for k in range(8)]
    # 电源
    sx = 38
    o.append(f'<line x1="{sx - 13}" y1="104" x2="{sx + 13}" y2="104" stroke="{D}" stroke-width="1.8"/>'
             f'<line x1="{sx - 7}" y1="112" x2="{sx + 7}" y2="112" stroke="{D}" stroke-width="3"/>')
    o.append(mtext(sx + 16, 98, '+', 10, D, 700) + mtext(sx - 18, 108, '12 V', 9.6, D, 700, 'end'))
    o.append(wire([(sx, 104), (sx, top), (xs[-1], top)]) + wire([(sx, 112), (sx, bot), (xs[-1], bot)]))
    o.append(mtext(sx + 4, top - 8, '+12 V', 8.4, GRY, 400, 'start') + mtext(sx + 4, bot + 11, '0 V', 8.4, GRY, 400, 'start'))
    for k, x in enumerate(xs):
        o.append(f'<circle cx="{x}" cy="{top}" r="2" fill="{D}"/><circle cx="{x}" cy="{bot}" r="2" fill="{D}"/>')
        o.append(wire([(x, top), (x, 62)]) + res_v(x, 62, 30) + wire([(x, 92), (x, 136)]) + res_v(x, 136, 30) + wire([(x, 166), (x, bot)]))
        o.append(f'<circle cx="{x}" cy="{tp}" r="3.6" fill="{RED}"/>')
        o.append(mtext(x + 7, tp, f'V{k + 1}', 9, RED, 700, 'start'))
    o.append(mtext(xs[0] - 9, 77, '2 kΩ', 8.4, D, 400, 'end') + mtext(xs[0] - 9, 151, '1 kΩ', 8.4, D, 400, 'end'))
    # 第 1 轮测量记录
    y0 = 200
    o.append(img('memo', 10, y0 - 6, 22) + mtext(36, y0 + 5, '第 1 轮测量记录', 10, D, 700, 'start'))
    o.append(mtext(510, y0 + 5, '两人一组：一人用万用表依次测量，一人记录', 8.6, GRY, 400, 'end'))
    cx0, cw, rh = 10, 55, 24
    rows = [('测点', [f'V{k + 1}' for k in range(8)]), ('电压（V）', V1), ('状态', ST)]
    for r, (lab, vals) in enumerate(rows):
        y = y0 + 18 + r * rh
        o.append(cell(cx0, y, 60, rh, lab, BG if r else C, C, '#fff' if r == 0 else D, 9.2, weight=700))
        for k, s in enumerate(vals):
            bad = r > 0 and k in BADK
            o.append(cell(cx0 + 60 + k * cw, y, cw, rh, s, C if r == 0 else '#fff', C, '#fff' if r == 0 else (RED if bad else '#1F1F1F'),
                          9.2, mono=(r == 1), weight=700 if (r == 0 or bad) else 400))
    o.append(mtext(260, H - 8, '按分压公式，各测点的电压都应为 4 V；红色为偏离 4 V 的测点', 8.6, GRY))
    return svgwrap(W, H, ''.join(o))


figs['f_scene'] = f_scene()


# ================================================================== 图7-2 知识导图
def kmap():
    tasks = [("任务一 存储多支路采样电压", ["一维数组示例：高于平均分的成绩", "数组的基本特点：同类型、下标从 0 开始", "一维数组的定义、初始化和引用", "典型应用：求最值、冒泡排序", "任务实施：录入并显示 8 路电压"]),
             ("任务二 搭建多批次电压矩阵", ["二维数组的定义：按行存放", "二维数组的初始化", "二维数组的引用：两层循环", "典型应用：矩阵转置、杨辉三角", "任务实施：3 轮 × 8 路电压数据表"]),
             ("任务三 记录支路电压状态码", ["字符数组的定义和初始化", "字符数组的引用：用 \" %c\" 读入", "典型应用：统计选票、字母加密", "任务实施：状态码与状态对照输出"]),
             ("任务四 录入状态文本字符串", ["字符串：以 '\\0' 结尾，汉字占 2 字节", "字符串的输入输出：%s、puts", "strlen、strcpy、strcat、strcmp", "典型示例：密码强度、回文", "任务实施：状态文本、检修清单"]),
             ("AI升华 让排序结果对得上号", ["用含相同数据的测试检验 AI 的办法", "离开 AI 再做：状态文本一起排序"])]
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
    return f'''<svg viewBox="0 0 560 {H}" width="560" height="{H}" font-family="{FONT}">
<g stroke="#9DB3D3" stroke-width="1.3" fill="none">{''.join(lines)}</g>
<rect x="8" y="{mid - 25}" width="120" height="50" rx="4" fill="{C}"/>
<text x="68" y="{mid - 4}" fill="#fff" font-size="13" font-weight="700" text-anchor="middle">项目七</text>
<text x="68" y="{mid + 14}" fill="#fff" font-size="10.5" text-anchor="middle">构建批量信息数组</text>
<g font-size="9.6" font-weight="700" text-anchor="middle">{''.join(boxes)}</g>
<g font-size="9.4" fill="#1F1F1F">{''.join(texts)}</g>
<g fill="{C}">{''.join(dots)}</g></svg>'''


figs['f_kmap'] = kmap()


# ================================================================== 图7-3 为什么需要数组
def f_why():
    W, H = 520, 236
    o = []
    o.append(chip(10, 6, 236, 24, '不用数组：6 个变量', fill=BG, color=D, stroke=C, size=10, rx=4))
    o.append(f'<rect x="10" y="38" width="236" height="152" rx="4" fill="#fff" stroke="{L}" stroke-width="1"/>')
    o.append(code_lines(22, 60, ['int s1, s2, s3, s4, s5, s6;', 'scanf("%d", &s1);', 'scanf("%d", &s2);'], 9.8, 17))
    o.append(mtext(128, 112, '…… 还要 4 条 scanf ……', 9, GRY))
    o.append(code_lines(22, 138, ['if (s1 > avg) printf(…);'], 9.8, 17))
    o.append(mtext(128, 164, '…… 还要 5 条 if ……', 9, GRY))
    o.append(mtext(128, 206, '输入、比较的语句都要写 6 遍', 10, RED, 700))
    o.append(mtext(128, 224, '45 位同学：45 个变量、90 条语句', 9, '#4D4D4D'))
    x0 = 274
    o.append(chip(x0, 6, 236, 24, '用数组：一个名字，一批数据', fill=C, size=10, rx=4))
    o.append(f'<rect x="{x0}" y="38" width="236" height="152" rx="4" fill="{BG}" stroke="{C}" stroke-width="1"/>')
    o.append(code_lines(x0 + 14, 60, ['int score[6];', 'for (i = 0; i < 6; i++)', '    scanf("%d", &score[i]);', 'for (i = 0; i < 6; i++)',
                                      '    if (score[i] > avg)', '        printf(…);'], 9.8, 20))
    o.append(mtext(x0 + 118, 206, '下标 i 一变，处理的元素就变', 10, C, 700))
    o.append(mtext(x0 + 118, 224, '45 位同学：只要把 6 改成 45', 9, '#4D4D4D'))
    o.append(arrow([(250, 114), (270, 114)], M, 1.6))
    return svgwrap(W, H, ''.join(o), REDMK)


figs['f_why'] = f_why()


# ================================================================== 图7-4 数组的基本特点
def f_mem():
    W, H = 520, 206
    o = [chip(60, 6, 250, 24, '数组 v：8 个 float 型元素', fill=C, size=10, rx=4)]
    x0, w, y = 64, 49, 58
    o.append(mtext(32, y + 10, 'v', 16, D, 700, mono=True) + mtext(32, y + 28, '数组名', 8.6, D, 700))
    o.append(arrow([(42, y + 10), (x0 - 2, y + 10)], M, 1.4))
    o.append(mtext(36, y - 10, '测点', 8.6, GRY) + mtext(36, y + 52, '元素', 8.6, D, 700) + mtext(36, y + 70, '字节', 8.6, GRY))
    for k in range(8):
        x = x0 + k * w
        o.append(mtext(x + w / 2, y - 10, f'V{k + 1}', 9, GRY, 700))
        o.append(cell(x, y, w, 34, V1[k], BG, C, '#1F1F1F', 10, mono=True))
        o.append(mtext(x + w / 2, y + 52, f'v[{k}]', 9.6, D, 700, mono=True))
        o.append(mtext(x + w / 2, y + 70, f'{4 * k}～{4 * k + 3}', 8, GRY))
    xe = x0 + 8 * w + 4
    o.append(cell(xe, y, 46, 34, '', '#fff', RED, dash=True) + mtext(xe + 23, y + 17, '?', 13, RED, 700))
    o.append(mtext(xe + 23, y + 52, 'v[8]', 9.6, RED, 700, mono=True) + mtext(xe + 23, y + 70, '不存在', 8.6, RED, 700))
    items = [('类型相同', '8 个元素都是 float 型'), ('下标从 0 开始', 'v[0]～v[7]，测点编号 = 下标 + 1'), ('连续存放', '每个元素 4 个字节，共 32 个字节')]
    for k, (t1, t2) in enumerate(items):
        bx = 10 + k * 170
        o.append(f'<rect x="{bx}" y="148" width="162" height="48" rx="4" fill="#fff" stroke="{L}" stroke-width="1"/>')
        o.append(num(bx + 14, 164, k + 1, C))
        o.append(mtext(bx + 26, 164, t1, 9.6, D, 700, 'start') + mtext(bx + 10, 183, t2, 8.4, '#1F1F1F', 400, 'start'))
    o.append(mtext(510, 22, '字节编号为示意（本书环境）', 8, GRY, 400, 'end'))
    return svgwrap(W, H, ''.join(o))


figs['f_mem'] = f_mem()


# ================================================================== 图7-5 一维数组的定义
def f_defn():
    W, H = 520, 150
    size, cw = 24, 0.602 * 24
    s = 'float v[8];'
    x0 = 260 - len(s) * cw / 2
    o = [f'<rect x="{x0 - 16}" y="16" width="{len(s) * cw + 32}" height="46" rx="5" fill="{BG}" stroke="{C}" stroke-width="1"/>',
         f'<text x="{x0}" y="48" font-size="{size}" font-weight="700" fill="{D}" font-family="{MONO}" xml:space="preserve">{s}</text>']
    parts = [(0, 5, K1, '类型名', '每个元素的类型', 120), (6, 7, K2, '数组名', '命名规则与变量名相同', 260), (8, 9, K3, '长度：元素的个数', '必须是大于 0 的常量表达式', 400)]
    for c0, c1, col, t1, t2, lx in parts:
        a, b_ = x0 + c0 * cw, x0 + c1 * cw
        o.append(f'<path d="M{a + 1},{66} v6 H{b_ - 1} v-6" fill="none" stroke="{col}" stroke-width="1.6"/>')
        o.append(seg([((a + b_) / 2, 72), (lx, 96)], col, 1.2, True))
        o.append(mtext(lx, 106, t1, 10, col, 700) + mtext(lx, 124, t2, 8.8, '#1F1F1F'))
    o.append(mtext(260, 143, '定义后得到 8 个元素 v[0]～v[7]，每个都是 float 型', 8.8, GRY))
    return svgwrap(W, H, ''.join(o))


figs['f_defn'] = f_defn()


# ================================================================== 图7-6 冒泡排序的第 1 轮
def f_bubble():
    v = [float(s) for s in V1]
    W, rh = 520, 27
    o = [mtext(10, 14, '第 1 轮（i = 0）：j 从 0 到 6，相邻的两个数比较 7 次，前大后小就交换', 9.6, D, 700, 'start')]
    x0, w, y0 = 54, 40, 30
    for j in range(7):
        y = y0 + j * rh
        o.append(mtext(14, y + 11, f'j={j}', 9, D, 700, 'start', mono=True))
        for k in range(8):
            hi = k in (j, j + 1)
            o.append(cell(x0 + k * w, y, w - 3, 22, f'{v[k]:.2f}', BG if hi else '#fff', RED if hi else L, '#1F1F1F', 9, mono=True, sw=1.4 if hi else 1))
        a, b_ = v[j], v[j + 1]
        sw = a > b_
        txt = f'{a:.2f} > {b_:.2f}，交换' if sw else f'{a:.2f} < {b_:.2f}，不交换'
        o.append(mtext(x0 + 8 * w + 8, y + 11, txt, 9, RED if sw else GRY, 700 if sw else 400, 'start'))
        if sw:
            v[j], v[j + 1] = b_, a
    y = y0 + 7 * rh + 6
    o.append(mtext(14, y + 11, '结果', 9, C, 700, 'start'))
    for k in range(8):
        last = k == 7
        o.append(cell(x0 + k * w, y, w - 3, 22, f'{v[k]:.2f}', C if last else '#fff', C, '#fff' if last else '#1F1F1F', 9, mono=True, weight=700 if last else 400))
    o.append(mtext(x0 + 8 * w + 8, y + 11, '最大的 12.00 到了最后', 9, C, 700, 'start'))
    H = y + 50
    o.append(mtext(260, H - 10, '第 2 轮对前 7 个数再做一遍（比较 6 次）……共 7 轮', 8.6, GRY))
    return svgwrap(W, H, ''.join(o))


figs['f_bubble'] = f_bubble()


# ================================================================== 图7-7 任务一流程图
def f_flow1():
    f = FC(540, 418, 9.4)
    xl, xr = 130, 350
    f.term('s', xl, 20, '开始')
    f.proc('a', xl, 64, 'i = 0', 90, 26)
    f.dec('d1', xl, 122, 'i < 8', 110, 46)
    f.io('b', xl, 194, '输出提示“请输入V(i+1)\n的电压”，输入 v[i]', 196, 42)
    f.proc('c', xl, 254, 'i++', 90, 26)
    f.io('e', xr, 122, '输出表头“测点 电压（V）”', 196, 28)
    f.proc('g', xr, 176, 'i = 0', 90, 26)
    f.dec('d2', xr, 234, 'i < 8', 110, 46)
    f.io('h', xr, 304, '输出 V(i+1) 和 v[i]', 170, 28)
    f.proc('k', xr, 354, 'i++', 90, 26)
    f.term('t', xr, 400, '结束')
    for a_, b_ in (('s', 'a'), ('a', 'd1'), ('d1', 'b'), ('b', 'c'), ('e', 'g'), ('g', 'd2'), ('d2', 'h'), ('h', 'k')):
        f.v(a_, b_)
    f.line([f.p('c', 'l'), (24, 254), (24, 122), f.p('d1', 'l')])
    f.line([f.p('d1', 'r'), f.p('e', 'l')])
    f.line([f.p('k', 'l'), (246, 354), (246, 234), f.p('d2', 'l')])
    f.line([f.p('d2', 'r'), (466, 234), (466, 400), f.p('t', 'r')])
    f.label(xl + 8, 158, '是', 'start')
    f.label(206, 112, '否', 'middle')
    f.label(xr + 8, 270, '是', 'start')
    f.label(474, 300, '否', 'start')
    br = (chip(xl - 50, 274, 100, 20, '录入：循环 8 次', fill=BG, color=D, stroke=C, size=8.8)
          + chip(xr + 62, 166, 100, 20, '显示：循环 8 次', fill=BG, color=D, stroke=C, size=8.8))
    return f.svg(br)


figs['f_flow1'] = f_flow1()


# ================================================================== 图7-8 二维数组的逻辑结构和存放顺序
def f_arr2d():
    W, H = 520, 244
    o = [mtext(10, 14, '（a）逻辑结构：3 行 8 列', 10, D, 700, 'start')]
    x0, y0, w, h = 76, 40, 54, 26
    for j in range(8):
        o.append(mtext(x0 + j * w + w / 2, y0 - 8, f'V{j + 1}  [{j}]', 8.4, GRY, 700))
    shade = [BG, '#D6E1F1', '#C2D3EA']
    for i in range(3):
        o.append(mtext(x0 - 6, y0 + i * h + h / 2, f'第{i + 1}轮  [{i}]', 8.6, GRY, 700, 'end'))
        for j in range(8):
            o.append(cell(x0 + j * w, y0 + i * h, w, h, f'v[{i}][{j}]', shade[i], C, '#1F1F1F', 8.6, mono=True))
    o.append(mtext(x0 + 4 * w, y0 + 3 * h + 16, '行下标表示第几轮（0～2），列下标表示第几路（0～7）', 8.8, '#4D4D4D'))
    yb = 170
    o.append(mtext(10, yb - 13, '（b）在内存中按行存放：先第 0 行，再第 1 行，最后第 2 行', 10, D, 700, 'start'))
    cw = 20
    for k in range(24):
        i = k // 8
        o.append(cell(20 + k * cw, yb, cw, 22, '', shade[i], C))
    for i in range(3):
        xa, xb = 20 + i * 8 * cw, 20 + (i + 1) * 8 * cw
        o.append(f'<path d="M{xa + 2},{yb + 28} v5 H{xb - 2} v-5" fill="none" stroke="{M}" stroke-width="1.2"/>')
        o.append(mtext((xa + xb) / 2, yb + 44, f'第 {i} 行：v[{i}][0]～v[{i}][7]', 8.6, D, 700))
    o.append(rarrow([(26, yb + 11), (20 + 24 * cw - 6, yb + 11)], 1.2, True))
    o.append(mtext(260, H - 10, '共 24 个元素，一个挨着一个存放', 8.8, GRY))
    return svgwrap(W, H, ''.join(o), REDMK)


figs['f_arr2d'] = f_arr2d()


# ================================================================== 图7-9 杨辉三角
def f_yanghui():
    W, H = 520, 214
    rows = [[1]]
    for r in range(1, 6):
        p = rows[-1]
        rows.append([1] + [p[k - 1] + p[k] for k in range(1, r)] + [1])
    o = []
    dx, dy, cx = 46, 30, 168
    pos = {}
    for r, row in enumerate(rows):
        for k, n in enumerate(row):
            x = cx + (k - r / 2) * dx
            y = 24 + r * dy
            pos[(r, k)] = (x, y)
            hi = (r, k) in ((3, 1), (3, 2), (4, 2))
            col = RED if (r, k) == (4, 2) else (C if hi else L)
            o.append(f'<circle cx="{x}" cy="{y}" r="12" fill="{BG if not hi else "#fff"}" stroke="{col}" stroke-width="{1.6 if hi else 1}"/>'
                     + mtext(x, y, str(n), 10, RED if (r, k) == (4, 2) else D, 700))
    for a in ((3, 1), (3, 2)):
        (x1, y1), (x2, y2) = pos[a], pos[(4, 2)]
        o.append(rarrow([(x1 + (x2 - x1) * 0.3, y1 + 10), (x2 - (x2 - x1) * 0.25, y2 - 10)], 1.4))
    o.append(mtext(330, 60, '两条斜边上都是 1', 9.6, D, 700, 'start'))
    o.append(mtext(330, 84, '中间的数 = “肩上”两数之和', 9.6, RED, 700, 'start'))
    o.append(mtext(330, 108, '如 6 = 3 + 3', 9.6, RED, 700, 'start'))
    o.append(mtext(330, 140, '用数组 a 存放：', 9.2, D, 700, 'start'))
    o.append(mtext(330, 160, 'a[4][2] = a[3][1] + a[3][2]', 9.2, '#1F1F1F', 400, 'start', mono=True))
    o.append(mtext(330, 180, 'a[i][j] = a[i-1][j-1] + a[i-1][j]', 9.2, '#1F1F1F', 400, 'start', mono=True))
    return svgwrap(W, H, ''.join(o), REDMK)


figs['f_yanghui'] = f_yanghui()


# ================================================================== 图7-10 纸质记录表与二维数组的对应
def f_map38():
    W, H = 520, 252
    o = [img('memo', 8, 4, 22) + mtext(34, 15, '纸质记录表（3 轮 × 8 路，单位：V）', 10, D, 700, 'start')]
    x0, y0, w, h = 64, 30, 55, 24
    for j in range(8):
        o.append(cell(x0 + j * w, y0, w, h, f'V{j + 1}', C, C, '#fff', 9.2, weight=700))
    o.append(cell(x0 - 54, y0, 54, h, '轮次', C, C, '#fff', 9.2, weight=700))
    marks = {(0, 0): C, (1, 4): RED, (2, 7): C}
    for i, vals in enumerate((V1, V2, V3)):
        y = y0 + (i + 1) * h
        o.append(cell(x0 - 54, y, 54, h, f'第{i + 1}轮', BG, C, D, 9.2, weight=700))
        for j, s in enumerate(vals):
            m = marks.get((i, j))
            o.append(cell(x0 + j * w, y, w, h, s, '#fff', m or L, m or '#1F1F1F', 9.2, mono=True, weight=700 if m else 400, sw=2 if m else 1))
    yb = 168
    targets = [((0, 0), 'v[0][0]', '第 1 轮 V1', 100), ((1, 4), 'v[1][4]', '第 2 轮 V5', 260), ((2, 7), 'v[2][7]', '第 3 轮 V8', 420)]
    for (i, j), name, t, bx in targets:
        cx, cy = x0 + j * w + w / 2, y0 + 4 * h          # 箭头从表格底边（同一列）引出，不压住其他数据
        col = marks[(i, j)]
        o.append(arrow([(cx, cy + 3), (bx, yb - 4)], col, 1.3, True) if col != RED else rarrow([(cx, cy + 3), (bx, yb - 4)], 1.3, True))
        o.append(chip(bx - 62, yb, 124, 26, f'{t} → {name}', fill=BG if col != RED else '#fff', color=col, stroke=col, size=9.4, rx=4))
    o.append(f'<rect x="90" y="{yb + 40}" width="340" height="30" rx="4" fill="{C}"/>' + mtext(260, yb + 55, '第 r 轮测点 Vc 的电压  →  v[r-1][c-1]', 10, '#fff', 700))
    return svgwrap(W, H, ''.join(o), REDMK)


figs['f_map38'] = f_map38()


# ================================================================== 图7-11 分压支路的 4 种状态
def f_branch():
    W, H = 520, 252
    o = []
    panels = [('（a）支路正常', 'A', '4 V', 'normal'), ('（b）支路开路', 'B', '约 12 V', 'open'),
              ('（c）支路短路', 'C', '约 0 V', 'short'), ('（d）接触不良', 'D', '偏离 4 V\n且不稳定', 'loose')]
    for k, (title, code, volt, kind) in enumerate(panels):
        x0 = 4 + k * 129
        o.append(f'<rect x="{x0}" y="4" width="124" height="242" rx="6" fill="#fff" stroke="{L}" stroke-width="1"/>')
        o.append(mtext(x0 + 62, 20, title, 9.8, D, 700))
        x = x0 + 42
        o.append(mtext(x, 38, '+12 V', 8.4, GRY))
        o.append(f'<circle cx="{x}" cy="46" r="2" fill="{D}"/>')
        if kind == 'loose':
            o.append(wire([(x, 46), (x, 54)]) + f'<path d="M{x},54 l-5,4 l10,4 l-10,4 l10,4 l-5,4" fill="none" stroke="{RED}" stroke-width="1.4"/>'
                     + wire([(x, 74), (x, 80)]) + mtext(x - 9, 64, '接触\n电阻', 7.8, RED, 700, 'end', 1.15))
        else:
            o.append(wire([(x, 46), (x, 80)]))
        o.append(res_v(x, 80, 32) + mtext(x + 10, 96, '2 kΩ', 8, D, 400, 'start'))
        o.append(wire([(x, 112), (x, 150)]))
        o.append(res_v(x, 150, 32, broken=(kind == 'open')) + mtext(x + 10, 166, '1 kΩ', 8, D, 400, 'start'))
        if kind == 'open':
            o.append(mtext(x - 10, 166, '×', 14, RED, 700, 'end') + mtext(x - 10, 184, '断开', 8, RED, 700, 'end'))
        o.append(wire([(x, 182), (x, 196)]) + ground(x, 196))
        o.append(f'<circle cx="{x}" cy="131" r="3.6" fill="{RED}"/>')
        if kind == 'short':
            o.append(seg([(x, 131), (x - 18, 131), (x - 18, 190), (x, 190)], RED, 1.8) + mtext(x - 22, 160, '短接', 8, RED, 700, 'end'))
        # 万用表读数
        mx = x0 + 70
        o.append(seg([(x + 4, 131), (mx, 131)], GRY, 1, True))
        o.append(f'<rect x="{mx}" y="{116 if kind != "loose" else 110}" width="48" height="{30 if kind != "loose" else 42}" rx="4" fill="{BG}" stroke="{C}" stroke-width="1"/>')
        o.append(mtext(mx + 24, 131, volt, 9, RED if kind != 'normal' else D, 700, lh=1.2))
        o.append(chip(x0 + 34, 214, 56, 22, f'状态码 {code}', fill=C, size=9, rx=4))
    return svgwrap(W, H, ''.join(o))


figs['f_branch'] = f_branch()


# ================================================================== 图7-12 字符数组的初始化
def f_chararr():
    W, H = 520, 196
    o = [mtext(10, 14, "（a）char code[8] = {'A', 'A', 'B', 'A', 'D', 'C', 'A', 'A'};", 9.6, D, 700, 'start', mono=True)]
    x0, w, y = 70, 46, 46
    for k, ch in enumerate(['A', 'A', 'B', 'A', 'D', 'C', 'A', 'A']):
        x = x0 + k * w
        o.append(mtext(x + w / 2, y - 8, f'V{k + 1}', 8.6, GRY, 700))
        o.append(cell(x, y, w - 2, 28, ch, BG, C, RED if ch != 'A' else D, 12, mono=True, weight=700))
        o.append(mtext(x + w / 2, y + 42, f'code[{k}]', 8.4, D, 400, mono=True))
    o.append(mtext(40, y + 14, '状态码', 8.6, D, 700))
    y = 132
    o.append(mtext(10, y - 22, "（b）char b[5] = {'O', 'K'};", 9.6, D, 700, 'start', mono=True))
    for k, (ch, asc) in enumerate([('O', '79'), ('K', '75'), ('\\0', '0'), ('\\0', '0'), ('\\0', '0')]):
        x = x0 + k * w
        z = ch == '\\0'
        o.append(cell(x, y, w - 2, 28, ch, '#EFEFEF' if z else BG, C, GRY if z else D, 11, mono=True, weight=700))
        o.append(mtext(x + w / 2, y + 42, f'ASCII {asc}', 8.2, GRY))
    o.append(mtext(x0 + 5 * w + 14, y + 14, '没有赋初值的元素自动为空字符 \'\\0\'（ASCII 码为 0）', 8.8, '#1F1F1F', 400, 'start'))
    return svgwrap(W, H, ''.join(o))


figs['f_chararr'] = f_chararr()


# ================================================================== 图7-13 字符串在字符数组中的存放
def f_strmem():
    W, H = 520, 230
    o = []
    bw, x0 = 28, 142

    def bytes_row(y, cells, label, note):
        out = [mtext(10, y + 14, label, 9.2, D, 700, 'start', mono=True)]
        x = x0
        k = 0
        for s, n in cells:                      # n：占几个字节
            z = s == '\\0'
            fill = '#EFEFEF' if z else BG
            out.append(cell(x, y, bw * n - 2, 28, s, fill, C, GRY if z else D, 11 if n == 1 else 12, mono=(n == 1), weight=700))
            if n == 2:                          # 一个汉字 2 个字节：上下边各画一个短刻度，不压住汉字
                out.append(seg([(x + bw - 1, y), (x + bw - 1, y + 5)], C, 1.2) + seg([(x + bw - 1, y + 23), (x + bw - 1, y + 28)], C, 1.2))
            for t in range(n):
                out.append(mtext(x + t * bw + bw / 2 - 1, y - 7, str(k), 7.6, GRY))
                k += 1
            x += bw * n
        out.append(mtext(x + 10, y + 14, note, 8.8, RED, 700, 'start'))
        return ''.join(out)
    o.append(mtext(x0 - 2, 14, '字节编号', 8.2, GRY, 400, 'end'))
    o.append(bytes_row(26, [('O', 1), ('K', 1), ('\\0', 1)], 'char s1[] = "OK";', '3 个字节，长度为 2'))
    o.append(bytes_row(88, [('支', 2), ('路', 2), ('正', 2), ('常', 2), ('\\0', 1)], 'char s2[] = "支路正常";', '9 个字节，长度为 8'))
    o.append(bytes_row(150, [('H', 1), ('i', 1)] + [('\\0', 1)] * 8, 'char s3[10] = "Hi";', '10 个字节，长度为 2'))
    o.append(mtext(260, 206, '本书环境（GBK 编码）中一个汉字占 2 个字节；字符串的长度不含结束标志 \'\\0\'', 8.8, GRY))
    o.append(mtext(260, 222, '灰色的 \'\\0\' 是字符串结束标志', 8.6, GRY))
    return svgwrap(W, H, ''.join(o))


figs['f_strmem'] = f_strmem()


# ================================================================== 图7-14 用二维字符数组存放 8 条状态文本
def f_state2d():
    W, H = 520, 288
    TX = ['支路正常', '支路正常', '支路开路', '支路正常', '接触不良', '支路短路', '支路正常', '支路正常']
    o = [mtext(10, 14, 'char state[8][10];　每行存放一条状态文本（字符串）', 9.6, D, 700, 'start')]
    x0, y0, w, h = 116, 44, 24, 26
    for c in range(10):
        o.append(mtext(x0 + c * w + w / 2, y0 - 8, str(c), 8, GRY))
    o.append(mtext(x0 - 6, y0 - 8, '列下标', 8, GRY, 400, 'end'))
    for r, t in enumerate(TX):
        y = y0 + r * h
        bad = r in BADK
        o.append(mtext(x0 - 36, y + h / 2, f'state[{r}]', 8.6, RED if bad else D, 700, 'end', mono=True))
        o.append(mtext(x0 - 6, y + h / 2, f'V{r + 1}', 8.4, GRY, 700, 'end'))
        for k, ch in enumerate(t):
            xa = x0 + 2 * k * w
            o.append(cell(xa, y, 2 * w, h, ch, BG, C, RED if bad else D, 10.5, weight=700))
            o.append(seg([(xa + w, y), (xa + w, y + 4)], C, 1) + seg([(xa + w, y + h - 4), (xa + w, y + h)], C, 1))
        o.append(cell(x0 + 8 * w, y, w, h, '\\0', '#EFEFEF', C, GRY, 9, mono=True, weight=700))
        o.append(cell(x0 + 9 * w, y, w, h, '', '#fff', L))
    xn = x0 + 10 * w + 18
    o.append(mtext(xn, 70, '每行 10 个元素：', 9, D, 700, 'start'))
    o.append(mtext(xn, 88, '4 个汉字占 8 个字节，', 8.8, '#1F1F1F', 400, 'start'))
    o.append(mtext(xn, 104, '加上 \'\\0\' 共 9 个字节', 8.8, '#1F1F1F', 400, 'start'))
    o.append(mtext(xn, 140, 'state[2] 是第 3 行这个', 8.8, '#1F1F1F', 400, 'start'))
    o.append(mtext(xn, 156, '一维字符数组的名字：', 8.8, '#1F1F1F', 400, 'start'))
    o.append(mtext(xn, 174, 'scanf("%s", state[2]);', 8.6, D, 700, 'start', mono=True))
    o.append(mtext(xn, 192, 'printf("%s", state[2]);', 8.6, D, 700, 'start', mono=True))
    o.append(arrow([(xn - 4, 150), (x0 + 10 * w + 4, y0 + 2 * h + h / 2)], M, 1.2, True))
    o.append(mtext(260, H - 10, '红色为需要检修的支路；最后一列没有用到', 8.6, GRY))
    return svgwrap(W, H, ''.join(o))


figs['f_state2d'] = f_state2d()


# ================================================================== 图7-15 AI 升华：四格漫画
def f_comic():
    W, H = 520, 330
    o = []
    PW, PH = 254, 158
    pos = [(4, 4), (262, 4), (4, 168), (262, 168)]
    for k, (x, y) in enumerate(pos, 1):
        o.append(f'<rect x="{x}" y="{y}" width="{PW}" height="{PH}" rx="8" fill="#fff" stroke="{C}" stroke-width="1.3"/>')
        o.append(f'<circle cx="{x + 14}" cy="{y + 14}" r="9" fill="{C}"/>' + mtext(x + 14, y + 14, str(k), 10, '#fff', 700))
    # 1 排好了
    x, y = 4, 4
    o.append(f'<rect x="{x + 12}" y="{y + 28}" width="128" height="120" rx="4" fill="#0C0C0C"/>')
    for j, s in enumerate(['从低到高：', 'V1   0.00', 'V2   3.42', 'V3   3.96', '……', 'V8  12.00']):
        o.append(f'<text x="{x + 20}" y="{y + 46 + j * 18}" font-size="9" fill="#CCCCCC" font-family="{MONO}" xml:space="preserve">{esc(s)}</text>')
    o.append(av_he(x + 206, y + 124, 22, 'happy'))
    o.append(bubble(x + 160, y + 30, 86, 46, '排好了！\n一目了然', (x + 200, y + 100), 9))
    # 2 对不上
    x, y = 262, 4
    o.append(img('memo', x + 16, y + 26, 26) + mtext(x + 46, y + 40, '第 1 轮记录', 9, D, 700, 'start'))
    for j, (a, b_) in enumerate([('V1', '4.02'), ('V3', '12.00'), ('V6', '0.00')]):
        o.append(cell(x + 18, y + 54 + j * 24, 40, 22, a, BG, C, D, 9, weight=700) + cell(x + 58, y + 54 + j * 24, 52, 22, b_, '#fff', RED if j else C, RED if j else '#1F1F1F', 9, mono=True, weight=700))
    o.append(av_he(x + 212, y + 126, 22, 'shock'))
    o.append(bubble(x + 126, y + 28, 120, 54, 'V1 明明是 4.02，\n0.00 是 V6 的，\n怎么对不上了？', (x + 200, y + 102), 8.6))
    # 3 原因
    x, y = 4, 168
    o.append(mtext(x + 28, y + 36, '排序前', 8.6, GRY, 700, 'start') + mtext(x + 28, y + 84, '排序后', 8.6, GRY, 700, 'start'))
    for k, (a, b_) in enumerate([('4.02', '0.00'), ('3.98', '3.42'), ('12.00', '3.96')]):
        xx = x + 70 + k * 44
        o.append(cell(xx, y + 24, 40, 22, a, BG, C, '#1F1F1F', 8.6, mono=True))
        o.append(cell(xx, y + 72, 40, 22, b_, BG, C, '#1F1F1F', 8.6, mono=True))
        o.append(mtext(xx + 20, y + 106, f'V{k + 1}', 8.6, RED, 700))
    o.append(mtext(x + 16, y + 126, '电压搬了家，编号 i+1 却没跟着走！', 8.6, RED, 700, 'start'))
    o.append(av_zhi(x + 222, y + 46, 18, 'think'))
    o.append(rarrow([(x + 92, y + 48), (x + 92, y + 70)], 1.2))
    # 4 问 AI
    x, y = 262, 168
    o.append(av_he(x + 40, y + 126, 22, 'think'))
    o.append(bubble(x + 12, y + 28, 112, 54, '怎样让编号\n跟着电压走？\n问问 AI！', (x + 42, y + 102), 8.8))
    o.append(av_zhi(x + 206, y + 126, 22, 'happy'))
    o.append(bubble(x + 132, y + 28, 116, 54, 'AI 的办法，\n要多用几组数据\n试一试哦！', (x + 204, y + 102), 8.6))
    o.append(img('magnifying_glass_tilted_left', x + 104, y + 106, 34))
    return svgwrap(W, H, ''.join(o), REDMK)


figs['f_comic'] = f_comic()


# ================================================================== 图7-16 办法①：编号跟着电压一起交换
def f_swap():
    W, H = 520, 246
    o = [mtext(10, 14, '（a）一次交换（j = 0）：4.02 > 3.98，电压交换，编号也交换', 9.6, D, 700, 'start')]

    def pair(x, y, n, v, hi=False):
        st = RED if hi else C
        return (cell(x, y, 46, 22, f'no={n}', '#fff', st, D, 8.6, mono=True, weight=700, sw=1.4 if hi else 1)
                + cell(x, y + 22, 46, 22, v, BG, st, '#1F1F1F', 9, mono=True, sw=1.4 if hi else 1))
    o.append(mtext(30, 54, '交换前', 8.8, GRY, 700))
    o.append(pair(60, 32, 1, '4.02', True) + pair(108, 32, 2, '3.98', True) + pair(156, 32, 3, '12.00'))
    o.append(arrow([(214, 54), (270, 54)], RED, 1.6) if False else rarrow([(214, 54), (270, 54)], 1.6))
    o.append(mtext(242, 44, '交换', 8.6, RED, 700))
    o.append(mtext(300, 54, '交换后', 8.8, GRY, 700))
    o.append(pair(330, 32, 2, '3.98', True) + pair(378, 32, 1, '4.02', True) + pair(426, 32, 3, '12.00'))
    o.append(mtext(260, 96, '每一列的编号和电压是“一对”，交换时一起交换，对应关系就不会乱', 8.8, '#1F1F1F'))
    y0 = 128
    o.append(mtext(10, y0 - 8, '（b）排序前后的两个数组', 9.6, D, 700, 'start'))
    before_no = [str(k + 1) for k in range(8)]
    order = sorted(range(8), key=lambda k: (float(V1[k]), k))
    after_no = [str(k + 1) for k in order]
    after_v = [V1[k] for k in order]
    rows = [('排序前 no', before_no), ('排序前 v', V1), ('排序后 no', after_no), ('排序后 v', after_v)]
    for r, (lab, vals) in enumerate(rows):
        y = y0 + r * 26 + (8 if r >= 2 else 0)
        o.append(mtext(80, y + 11, lab, 8.8, D, 700, 'end'))
        for k, s in enumerate(vals):
            is_no = r % 2 == 0
            o.append(cell(90 + k * 50, y, 48, 22, s, '#fff' if is_no else BG, C if r < 2 else RED if is_no else C, D if is_no else '#1F1F1F', 9, mono=True, weight=700 if is_no else 400))
    return svgwrap(W, H, ''.join(o), REDMK)


figs['f_swap'] = f_swap()

# ------------------------------------------------------------------ 课堂练习图标（与项目三～六相同）
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
