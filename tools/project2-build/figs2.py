# 项目二插图：生成 fig/figs.html（每张图一个 id），再用 shot.js 截成 PNG
# 版式元素只用主色系：#1D4F91 主色、#153A6B 深、#4A75AE 中、#C5D3E7 浅线、#E8EEF7 浅底，加黑灰
# 彩色只出现在图标（Fluent Emoji 3D，MIT 许可）里
exec(open('base4.py', encoding='utf8').read())

figs = {}
RED = '#C0392B'


def chip(x, y, w, h, s, fill=C, color='#fff', size=9, weight=700, rx=None, stroke='none', mono=False):
    rx = h / 2 if rx is None else rx
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1"/>'
            + mtext(x + w / 2, y + h / 2, s, size, color, weight, mono=mono))


def arrow(pts, color=M, width=1.4, dash=False):
    d = 'M' + ' L'.join(f'{a:.1f},{b:.1f}' for a, b in pts)
    da = ' stroke-dasharray="4 3"' if dash else ''
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" marker-end="url(#ar)"{da}/>'


def t(x, y, s, size=9, fill='#1F1F1F', weight=400, anchor='middle', mono=False):
    return mtext(x, y, s, size, fill, weight, anchor, mono=mono)


# ================================================================== 图2-1 情境导入：AI 智能数据看板
def f_scene():
    W, H = 520, 300
    o = [f'<defs><linearGradient id="bgd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#16325C"/><stop offset="1" stop-color="#0F2445"/></linearGradient></defs>']
    o.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="10" fill="url(#bgd)"/>')
    o.append(img('robot', 12, 8, 26))
    o.append(t(44, 21, '6 号实训楼 0203 实训室 · AI 智能数据看板', 11, '#fff', 700, 'start'))
    o.append(t(W - 14, 21, '10:30  数据为课堂模拟', 8, '#9FB6D8', 400, 'end'))
    rows = [('固定不变', '#7FA6DB', [('school', '实训室类型', 'C', ''), ('round_pushpin', '实训室编号', '0203', ''),
                                    ('chair', '总座位数', '48', '个'), ('electric_plug', '额定电压', '220', 'V')]),
            ('实时变化', '#F2C14E', [('student', '在室人数', '36', '人'), ('thermometer', '环境温度', '24.5', '℃'),
                                    ('high_voltage', '工作电压', '218.6', 'V'), ('battery', '工作电流', '1.25', 'A')]),
            ('计算得出', '#7ED3A6', [('chair', '空座位数', '12', '个'), ('bar_chart', '座位利用率', '75.0', '%'),
                                    ('light_bulb', '计算机功率', '273.25', 'W'), ('locked_with_key', '告警报文', 'H', '（已加密）')])]
    y0 = 36
    for k, (tag, tc, cards) in enumerate(rows):
        y = y0 + k * 86
        o.append(f'<rect x="10" y="{y}" width="22" height="78" rx="5" fill="{tc}" opacity="0.95"/>')
        for j, ch in enumerate(tag):
            o.append(t(21, y + 16 + j * 15, ch, 9.4, '#10223F', 700))
        for j, (ic, lab, val, unit) in enumerate(cards):
            x = 40 + j * 119
            o.append(f'<rect x="{x}" y="{y}" width="112" height="78" rx="7" fill="#1E4378" stroke="#2F5B97" stroke-width="1"/>')
            o.append(f'<rect x="{x}" y="{y}" width="112" height="3" rx="1.5" fill="{tc}"/>')
            o.append(img(ic, x + 8, y + 12, 26))
            o.append(t(x + 40, y + 25, lab, 9, '#C9D8EE', 400, 'start'))
            vs = 19 if len(val) <= 5 else 17
            o.append(t(x + 10, y + 56, val, vs, '#FFFFFF', 700, 'start', mono=True))
            vw = len(val) * vs * 0.6
            o.append(t(x + 14 + vw, y + 58, unit, 9, '#C9D8EE', 400, 'start'))
            o.append(t(x + 102, y + 71, '●', 6, tc, 400, 'end'))
    return svgwrap(W, H, ''.join(o))


figs['f_scene'] = f_scene()


# ================================================================== 图2-2 知识导图
def kmap():
    tasks = [("任务一 建立实训室数据档案", ["常量：直接常量、符号常量 #define", "变量：定义、赋值、初始化", "数据类型：整型、实型、字符型", "字节数、取值范围与精度（sizeof）", "标识符：关键字、预定义、用户标识符", "任务实施：显示 0203 实训室档案"]),
             ("任务二 加密实训室告警信息", ["字符与 ASCII 码", "字符集：五类字符", "字符常量、转义字符、字符串常量", "字符变量与字符运算", "任务实施：告警字母 g → G → H"]),
             ("任务三 解析运算符与表达式", ["运算符、表达式的概念", "算术运算符：+ - * / %，++ --", "赋值、复合赋值运算符与赋值表达式", "类型转换：自动转换、强制转换", "运算符的优先级与结合性", "任务实施：座位利用率与功率"]),
             ("AI升华 借助 AI 纠正表达式", ["四要素提问：程序 + 提示 + 结果 + 期望", "逐条验证 AI 的建议，离开 AI 再做"])]
    y = 14
    centers, lines, texts, dots = [], [], [], []
    for name, leaves in tasks:
        ys = [y + 19 * i for i in range(len(leaves))]
        c = (ys[0] + ys[-1]) / 2
        centers.append(c)
        for ly, s in zip(ys, leaves):
            lines.append(f'<path d="M318 {c} C330 {c} 330 {ly} 344 {ly}"/>')
            texts.append(f'<text x="349" y="{ly + 3.4}">{esc(s)}</text>')
            dots.append(f'<circle cx="344" cy="{ly}" r="1.8"/>')
        y = ys[-1] + 28
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
<text x="68" y="{mid - 4}" fill="#fff" font-size="13" font-weight="700" text-anchor="middle">项目二</text>
<text x="68" y="{mid + 14}" fill="#fff" font-size="10.5" text-anchor="middle">读懂身边多样数据</text>
<g font-size="9.6" font-weight="700" text-anchor="middle">{''.join(boxes)}</g>
<g font-size="9.2" fill="#1F1F1F">{''.join(texts)}</g>
<g fill="{C}">{''.join(dots)}</g></svg>'''


figs['f_kmap'] = kmap()


# ================================================================== 图2-3 变量的存储结构（people = 36）
def f_var():
    W, H = 520, 212
    o = [f'<rect x="0" y="0" width="{W}" height="{H}" rx="8" fill="#F7F9FC"/>']
    # 左：储物柜类比
    o.append(f'<rect x="8" y="8" width="196" height="196" rx="7" fill="#fff" stroke="{L}"/>')
    o.append(t(106, 24, '生活中：实训室储物柜', 9.6, D, 700))
    for r in range(3):
        for c in range(3):
            x, y = 30 + c * 52, 38 + r * 46
            hl = (r, c) == (1, 1)
            o.append(f'<rect x="{x}" y="{y}" width="48" height="42" rx="3" fill="{"#fff" if hl else BG}" stroke="{C if hl else L}" stroke-width="{1.6 if hl else 1}"/>')
            if not hl:
                o.append(f'<circle cx="{x + 40}" cy="{y + 21}" r="2" fill="{L}"/>')
    x, y = 82, 84
    o.append(f'<rect x="{x + 6}" y="{y + 4}" width="36" height="12" rx="2" fill="{C}"/>' + t(x + 24, y + 10, 'people', 7.6, '#fff', 700, mono=True))
    o.append(t(x + 24, y + 30, '36', 12, D, 700, mono=True))
    o.append(t(106, 186, '标签找格子，格子有规格，\n格子里的东西可以更换', 8.4, '#4D4D4D'))
    # 右：内存中
    o.append(f'<rect x="212" y="8" width="300" height="196" rx="7" fill="#fff" stroke="{L}"/>')
    o.append(t(362, 24, '程序中：int people = 36;', 9.6, D, 700))
    bx, by, cw, ch = 248, 92, 36, 38
    o.append(t(232, by + ch / 2, '内存', 8.4, '#666', 700))
    for i in (0, 5):
        x = bx + i * cw
        o.append(f'<rect x="{x}" y="{by}" width="{cw}" height="{ch}" fill="#F2F2F2" stroke="#C8C8C8" stroke-width="1"/>' + t(x + cw / 2, by + ch / 2, '…', 10, '#999', 700))
    o.append(f'<rect x="{bx + cw}" y="{by}" width="{cw * 4}" height="{ch}" fill="{BG}" stroke="{C}" stroke-width="2.2"/>')
    for i in range(1, 4):
        x = bx + cw + i * cw
        o.append(f'<line x1="{x}" y1="{by + ch - 6}" x2="{x}" y2="{by + ch}" stroke="{C}" stroke-width="1"/>')
    o.append(t(bx + cw + 8, by + 10, '变量值', 7.6, M, 700, 'start'))
    o.append(t(bx + cw * 3, by + ch / 2 + 2, '36', 16, D, 700, mono=True))
    o.append(f'<path d="M{bx + cw},{by - 8} l0,-6 l{cw * 4},0 l0,6" fill="none" stroke="{M}" stroke-width="1.1"/>')
    o.append(chip(bx + cw * 3 - 46, by - 40, 92, 20, '变量名 people', C, '#fff', 9))
    o.append(f'<path d="M{bx + cw},{by + ch + 8} l0,6 l{cw * 4},0 l0,-6" fill="none" stroke="{M}" stroke-width="1.1"/>')
    o.append(t(bx + cw * 3, by + ch + 26, '变量类型 int：占 4 个字节（每个小刻度 1 个字节）', 8.8, D, 700))
    o.append(t(362, 178, '格子里存放的是 36 的二进制形式：\n00000000 00000000 00000000 00100100', 8.2, '#4D4D4D'))
    return svgwrap(W, H, ''.join(o))


figs['f_var'] = f_var()


# ================================================================== 图2-4 C 语言的数据类型（去掉布尔型）
def f_types():
    W, H = 520, 208
    o = []
    root = (8, 92, 104, 34)
    o.append(f'<rect x="{root[0]}" y="{root[1]}" width="{root[2]}" height="{root[3]}" rx="4" fill="{C}"/>' + t(60, 109, 'C 语言数据类型', 10.5, '#fff', 700))
    mids = [('基本类型', 48, True), ('构造类型', 128, False), ('指针类型', 160, False), ('空类型', 192, False)]
    for name, y, main in mids:
        o.append(f'<path d="M112 109 C128 109 128 {y} 144 {y}" fill="none" stroke="#9DB3D3" stroke-width="1.3"/>')
        if main:
            o.append(f'<rect x="144" y="{y - 13}" width="78" height="26" rx="4" fill="{C}"/>' + t(183, y, name, 10, '#fff', 700))
        else:
            o.append(f'<rect x="144" y="{y - 12}" width="78" height="24" rx="4" fill="#F2F2F2" stroke="#BDBDBD"/>' + t(183, y, name, 9.6, '#4D4D4D', 700))
    descs = {128: '数组、结构体、共用体、枚举（后续学习）', 160: '用来存放数据的地址（后续学习）', 192: 'void，表示“没有”，如 int main(void) 中的 void'}
    for y, s in descs.items():
        o.append(t(232, y, s, 8.8, '#333', 400, 'start'))
    o.append(f'<rect x="236" y="6" width="278" height="98" rx="6" fill="none" stroke="{M}" stroke-width="1" stroke-dasharray="4 3"/>')
    o.append(t(508, 96, '本项目重点学习', 8, M, 700, 'end'))
    subs = [('整型', 'short  int  long  long long', 22), ('实型（浮点型）', 'float  double', 50), ('字符型', 'char', 78)]
    for name, kw, y in subs:
        o.append(f'<path d="M222 48 C232 48 232 {y} 244 {y}" fill="none" stroke="#9DB3D3" stroke-width="1.2"/>')
        o.append(f'<rect x="244" y="{y - 11}" width="86" height="22" rx="4" fill="{BG}" stroke="{C}"/>' + t(287, y, name, 9.2, D, 700))
        o.append(t(338, y, kw, 9, D, 400, 'start', mono=True))
    return svgwrap(W, H, ''.join(o))


figs['f_types'] = f_types()


# ================================================================== 任务三 图：C 语言的运算符一览
def f_ops():
    W, H = 520, 196
    o = [f'<rect x="0" y="0" width="{W}" height="{H}" rx="8" fill="#F7F9FC"/>']
    items = [('abacus', '算术运算符', '+  -  *  /  %\n++  --', True), ('pencil', '赋值运算符', '=  +=  -=\n*=  /=  %=', True),
             ('straight_ruler', '求字节数运算符', 'sizeof', True), ('counterclockwise_arrows_button', '强制类型转换', '(类型名)', True),
             ('balance_scale', '关系运算符', '>  <  >=  <=\n==  !=', False), ('puzzle_piece', '逻辑运算符', '&&  ||  !', False),
             ('red_question_mark', '条件运算符', '? :', False), ('gear', '其他', '逗号  ,\n位运算  &  |  等', False)]
    for k, (ic, name, ops, now) in enumerate(items):
        x, y = 8 + (k % 4) * 128, 8 + (k // 4) * 92
        o.append(f'<rect x="{x}" y="{y}" width="120" height="84" rx="7" fill="#fff" stroke="{C if now else "#C8C8C8"}" stroke-width="{1.4 if now else 1}"/>')
        o.append(img(ic, x + 7, y + 7, 24))
        o.append(t(x + 36, y + 19, name, 9.4, D if now else '#555', 700, 'start'))
        o.append(t(x + 60, y + 50, ops, 10.5 if len(ops) < 14 else 9.6, D if now else '#666', 700, mono=True))
        o.append(chip(x + 30, y + 66, 60, 14, '本项目学习' if now else '后续学习', C if now else '#E3E3E3', '#fff' if now else '#666', 7.6))
    return svgwrap(W, H, ''.join(o))


figs['f_ops'] = f_ops()


# ================================================================== 整除与求余：36 人每组 5 人
def f_divmod():
    W, H = 520, 172
    o = [f'<rect x="0" y="0" width="{W}" height="{H}" rx="8" fill="#F7F9FC"/>']
    o.append(t(W / 2, 16, '36 名同学做实训，每组 5 人，能分几组？还剩几人？', 9.8, D, 700))
    for g in range(7):
        x = 10 + g * 72
        o.append(f'<rect x="{x}" y="28" width="66" height="74" rx="6" fill="#fff" stroke="{C}" stroke-width="1.2"/>')
        o.append(t(x + 33, 40, f'第 {g + 1} 组', 8, D, 700))
        for p in range(5):
            px = x + 4 + (p % 3) * 20 + (10 if p >= 3 else 0)
            py = 48 + (p // 3) * 26
            o.append(img('student', px, py, 20))
    o.append(f'<rect x="10" y="108" width="66" height="30" rx="6" fill="#FFF7E6" stroke="#E0A030" stroke-width="1.2" stroke-dasharray="3 2"/>')
    o.append(img('person_raising_hand', 16, 111, 24) + t(56, 123, '剩 1 人', 8, '#8A5A00', 700))
    o.append(chip(98, 112, 190, 24, '36 / 5 = 7　→　能分成 7 组', C, '#fff', 9.6, 700, 5, mono=False))
    o.append(chip(298, 112, 212, 24, '36 % 5 = 1　→　还剩 1 人', '#fff', D, 9.6, 700, 5, C))
    o.append(t(W / 2, 156, '“/”求商：两个整数相除，只取整数部分；“%”求余数：两边都必须是整数', 8.6, '#4D4D4D'))
    return svgwrap(W, H, ''.join(o))


figs['f_divmod'] = f_divmod()


# ================================================================== 自增：前置与后置
def box(x, y, name, val, w=46, h=26, hl=False):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{C if hl else "#fff"}" stroke="{C}" stroke-width="1.3"/>'
            + t(x + w / 2, y + h / 2, val, 12, '#fff' if hl else D, 700, mono=True) + t(x + w / 2, y - 8, name, 8.6, '#333', 700, mono=True))


def f_incdec():
    W, H = 520, 176
    o = [f'<rect x="0" y="0" width="{W}" height="{H}" rx="8" fill="#F7F9FC"/>']
    for k, (code, tag, s1, s2, nv, pv, before) in enumerate([
            ('n = people++;', '后置：先用后加', '① 先把 36 赋给 n', '② people 再加 1', '36', '37', '36'),
            ('n = ++people;', '前置：先加后用', '① people 先加 1', '② 再把 38 赋给 n', '38', '38', '37')]):
        x0 = 8 + k * 258
        o.append(f'<rect x="{x0}" y="6" width="250" height="164" rx="7" fill="#fff" stroke="{L}"/>')
        o.append(chip(x0 + 12, 14, 112, 22, code, BG, D, 10, 700, 4, mono=True))
        o.append(chip(x0 + 132, 15, 106, 20, tag, C, '#fff', 9.2))
        o.append(t(x0 + 34, 62, '执行前', 8.4, '#666', 700))
        o.append(box(x0 + 66, 58, 'people', before, 50))
        o.append(t(x0 + 160, 62, 'n 的值不确定', 8.2, '#888', 400, 'start') if k == 0 else t(x0 + 160, 62, '(n 原来是 36)', 8.2, '#888', 400, 'start'))
        o.append(t(x0 + 125, 100, s1 + '　' + s2, 8.8, M, 700))
        o.append(t(x0 + 34, 138, '执行后', 8.4, '#666', 700))
        o.append(box(x0 + 66, 134, 'people', pv, 50, hl=True))
        o.append(box(x0 + 150, 134, 'n', nv, 50, hl=True))
    return svgwrap(W, H, ''.join(o))


figs['f_incdec'] = f_incdec()


# ================================================================== 类型转换示意
def f_conv():
    W, H = 520, 176
    o = [f'<rect x="0" y="0" width="{W}" height="{H}" rx="8" fill="#F7F9FC"/>']
    o.append(f'<rect x="8" y="8" width="296" height="160" rx="7" fill="#fff" stroke="{L}"/>')
    o.append(t(156, 24, '运算时：自动向“高级别”类型转换', 9.6, D, 700))
    steps = ['char\nshort', 'int', 'long', 'long long', 'float', 'double']
    for i, s in enumerate(steps):
        x = 16 + i * 48
        h = 22 + i * 10
        y = 132 - h
        o.append(f'<rect x="{x}" y="{y}" width="42" height="{h}" rx="3" fill="{C if i == 5 else BG}" stroke="{C}" stroke-width="1"/>')
        o.append(t(x + 21, y + h / 2, s.replace(' long', '\nlong'), 8 if len(s) > 5 else 8.8, '#fff' if i == 5 else D, 700, mono=True))
    o.append(arrow([(20, 146), (292, 146)], M, 1.3))
    o.append(t(24, 158, '低', 8.4, '#666', 700) + t(286, 158, '高', 8.4, '#666', 700))
    o.append(t(156, 158, '例：36 / 48.0 → 36.0 / 48.0 = 0.75', 8.2, D, 400))
    o.append(f'<rect x="312" y="8" width="200" height="160" rx="7" fill="#fff" stroke="{L}"/>')
    o.append(t(412, 24, '赋值时：转换成左边变量的类型', 9.6, D, 700))
    o.append(chip(334, 40, 156, 22, 'int a = 24.9;', BG, D, 10, 700, 4, mono=True))
    o.append(t(370, 84, '24.9', 14, '#888', 700, mono=True))
    o.append(arrow([(396, 80), (432, 80)], M, 1.3))
    o.append(box(440, 68, '', '24', 44, 26, hl=True))
    o.append(t(412, 112, '小数部分被直接舍去\n（不是四舍五入）', 8.6, RED, 700))
    o.append(t(412, 148, '强制转换：(double)people\n只得到一个新值，people 不变', 8.2, '#4D4D4D'))
    return svgwrap(W, H, ''.join(o))


figs['f_conv'] = f_conv()


# ================================================================== 表达式的计算顺序：座位利用率
def f_eval():
    W, H = 520, 196
    o = [f'<rect x="0" y="0" width="{W}" height="{H}" rx="8" fill="#F7F9FC"/>']
    cols = [('people / seats * 100', ['① people / seats → 36 / 48 → 0', '　（两个整数相除，只取整数部分）', '② 0 * 100 → 0'], '0', False),
            ('(double)people / seats * 100', ['① (double)people → 36.0', '② 36.0 / seats → 36.0 / 48.0 → 0.75', '③ 0.75 * 100 → 75.0'], '75.0', True)]
    for k, (expr, steps, res, ok) in enumerate(cols):
        x0 = 8 + k * 258
        o.append(f'<rect x="{x0}" y="6" width="250" height="184" rx="7" fill="#fff" stroke="{C if ok else "#E3B3AD"}" stroke-width="1.2"/>')
        o.append(chip(x0 + 10, 14, 230, 24, expr, BG if ok else '#FBEDEB', D if ok else RED, 9.6, 700, 4, mono=True))
        for j, s in enumerate(steps):
            o.append(t(x0 + 16, 58 + j * 22, s, 8.8, '#1F1F1F', 400, 'start', mono=False))
        o.append(t(x0 + 16, 136, '座位利用率：', 9.2, D, 700, 'start'))
        o.append(t(x0 + 80, 136, res + ' %', 15, RED if not ok else C, 700, 'start', mono=True))
        o.append(img('cross_mark' if not ok else 'check_mark_button', x0 + 206, 118, 30))
        o.append(t(x0 + 125, 172, '运算顺序：同一级别从左往右' if ok else '先算的整数除法已经把 0.75 变成了 0', 8.4, '#4D4D4D'))
    return svgwrap(W, H, ''.join(o))


figs['f_eval'] = f_eval()


# ================================================================== 优先级阶梯（本项目学过的运算符）
def f_prec():
    W, H = 520, 196
    o = [f'<rect x="0" y="0" width="{W}" height="{H}" rx="8" fill="#F7F9FC"/>']
    rows = [('()   后置 ++ --', '圆括号、后置自增', '自左向右'), ('+ -（正负号） 前置 ++ -- (类型名) sizeof', '单目运算符', '自右向左'),
            ('*  /  %', '乘、除、求余', '自左向右'), ('+  -', '加、减', '自左向右'), ('=  +=  -=  *=  /=  %=', '赋值类', '自右向左')]
    o.append(t(24, 16, '高', 9, D, 700) + t(24, 182, '低', 9, D, 700))
    o.append(f'<path d="M24 24 L24 170" stroke="{M}" stroke-width="1.6" marker-end="url(#ar)"/>')
    for i, (ops, name, assoc) in enumerate(rows):
        y = 10 + i * 36
        x = 40 + i * 14
        w = 300 - i * 14
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="30" rx="5" fill="{C if i == 0 else BG}" stroke="{C}"/>')
        o.append(t(x + 12, y + 15, ops, 10, '#fff' if i == 0 else D, 700, 'start', mono=True))
        o.append(t(348, y + 15, name, 9.2, D, 700, 'start'))
        o.append(chip(436, y + 6, 74, 18, assoc, '#fff', M, 8.6, 700, 9, M))
    return svgwrap(W, H, ''.join(o))


figs['f_prec'] = f_prec()


# ================================================================== 三格漫画：利用率为什么是 0？
def f_comic():
    W, H = 520, 176
    o = []
    PW, PH = 168, 168
    for k in range(3):
        x = 4 + k * 172
        o.append(f'<rect x="{x}" y="4" width="{PW}" height="{PH}" rx="8" fill="#fff" stroke="{C}" stroke-width="1.3"/>')
        o.append(f'<circle cx="{x + 14}" cy="18" r="9" fill="{C}"/>' + t(x + 14, 18, str(k + 1), 10, '#fff', 700))
    # 1
    x = 4
    o.append(f'<rect x="{x + 30}" y="14" width="128" height="50" rx="4" fill="#0C0C0C"/>')
    o.append(f'<text x="{x + 36}" y="32" font-size="8" fill="#CCCCCC" font-family="{MONO}">座位利用率：0%</text>')
    o.append(f'<text x="{x + 36}" y="48" font-size="8" fill="#CCCCCC" font-family="{MONO}">计算机功率：273.25 W</text>')
    o.append(av_he(x + 40, 136, 22, 'shock'))
    o.append(bubble(x + 70, 84, 92, 46, '36 个人在上课，\n利用率怎么\n是 0%？！', (x + 62, 124), 8.4))
    # 2
    x = 176
    o.append(f'<rect x="{x + 26}" y="30" width="136" height="22" rx="4" fill="{BG}"/>')
    o.append(f'<text x="{x + 31}" y="45" font-size="7.6" fill="{D}" font-family="{MONO}">rate = people / seats * 100</text>')
    o.append(img('magnifying_glass_tilted_left', x + 22, 62, 30))
    o.append(av_zhi(x + 132, 140, 22, 'think'))
    o.append(bubble(x + 10, 98, 96, 54, '36 / 48，两个整数\n相除，商只取整数\n部分，得 0！', (x + 108, 132), 8.2))
    # 3
    x = 348
    o.append(img('teacher', x + 10, 108, 52))
    o.append(bubble(x + 18, 28, 140, 66, '让一个数先变成实数：\n(double)people / seats\n再乘 100，就是 75.0%。\n这就是本任务要学的！', (x + 40, 106), 8.2))
    o.append(img('light_bulb', x + 120, 112, 34))
    return svgwrap(W, H, ''.join(o))


figs['f_comic'] = f_comic()


# ================================================================== 课堂练习图标（与项目三、四相同）
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
