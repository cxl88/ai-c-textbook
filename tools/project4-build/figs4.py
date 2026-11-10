# 项目四插图：生成 fig/figs.html（每张图一个 id），再用 shot.js 截成 PNG
# 版式元素只用主色系：#1D4F91 主色、#153A6B 深、#4A75AE 中、#C5D3E7 浅线、#E8EEF7 浅底，加黑灰
# 彩色只出现在图标（Fluent Emoji，MIT）、插画（unDraw）和电阻色环里（色环颜色是电阻标识本身的颜色）
exec(open('base4.py', encoding='utf8').read())

figs = {}
CJKW = 1.0   # 中文字宽（em）
ASCW = 0.6   # 等宽英文字宽（em）


def tw(s, size, mono=False):
    """估算文字宽度（px）"""
    w = 0
    for ch in s:
        if ord(ch) >= 0x2E80 or ch in '“”‘’（）：，。、；！？':
            w += size * CJKW
        else:
            w += size * (ASCW if mono else 0.56)
    return w


def chip(x, y, w, h, s, fill=C, color='#fff', size=9, weight=700, rx=None, stroke='none', mono=False):
    rx = h / 2 if rx is None else rx
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1"/>'
            + mtext(x + w / 2, y + h / 2, s, size, color, weight, mono=mono))


def arrow(pts, color=M, width=1.4, dash=False):
    d = 'M' + ' L'.join(f'{a:.1f},{b:.1f}' for a, b in pts)
    da = ' stroke-dasharray="4 3"' if dash else ''
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" marker-end="url(#ar)"{da}/>'


# ================================================================== 图4-1 情境导入：生活中的顺序交互
def f_scene():
    W, H = 520, 318
    o = []
    rows = [('mobile-login', '手机解锁', [('input_numbers', '输入密码\n或刷脸'), ('gear', '核对密码'), ('unlocked', '解锁成功\n进入桌面')]),
            ('upload', '线上提交作业', [('file_folder', '选择作业文件'), ('hourglass_not_done', '上传并保存'), ('check_mark_button', '显示\n“提交成功”')]),
            ('order-delivered', '扫码点外卖', [('takeout_box', '扫码，选菜品\n和份数'), ('abacus', '计算总价'), ('receipt', '显示订单\n和应付金额')])]
    heads = ['① 输入', '② 处理', '③ 输出']
    X0, CW, GAP = 150, 100, 22
    o.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="8" fill="#F7F9FC"/>')
    for j, hd in enumerate(heads):
        x = X0 + j * (CW + GAP)
        o.append(chip(x + 22, 8, 60, 20, hd, C, '#fff', 9.6))
        if j < 2:
            o.append(arrow([(x + 86, 18), (x + CW + GAP + 18, 18)], M, 1.3))
    o.append(mtext(80, 18, '生活中的事情', 9.6, D, 700))
    for k, (pic, name, steps) in enumerate(rows):
        y0 = 36 + k * 84
        o.append(f'<rect x="6" y="{y0}" width="{W - 12}" height="76" rx="7" fill="#fff" stroke="{L}" stroke-width="0.9"/>')
        o.append(ud(pic, 14, y0 + 4, 92, 54))
        o.append(mtext(60, y0 + 66, name, 9.6, D, 700))
        for j, (ic, s) in enumerate(steps):
            x = X0 + j * (CW + GAP)
            o.append(f'<rect x="{x}" y="{y0 + 10}" width="{CW}" height="56" rx="6" fill="{BG}" stroke="{L}" stroke-width="0.8"/>')
            o.append(img(ic, x + 6, y0 + 22, 32))
            o.append(mtext(x + 68, y0 + 38, s, 8.8, '#1F1F1F', 400))
            if j < 2:
                o.append(arrow([(x + CW + 3, y0 + 38), (x + CW + GAP - 3, y0 + 38)], M, 1.6))
    o.append(f'<rect x="6" y="{H - 30}" width="{W - 12}" height="24" rx="12" fill="{C}"/>')
    o.append(mtext(W / 2, H - 18, '人机交互程序也一样：先输入数据，再处理数据，最后输出结果，一步接一步', 9.6, '#fff', 700))
    return svgwrap(W, H, ''.join(o))


figs['f_scene'] = f_scene()


# ================================================================== 知识导图
def kmap():
    tasks = [("任务一 电阻阻值台账录入与输出", ["顺序结构：从上到下依次执行", "C 语句：五类语句", "赋值语句与复合赋值", "输入与输出的概念", "printf 函数：按格式输出", "scanf 函数：按格式输入", "任务实施：录入阻值，输出台账"]),
             ("任务二 电阻状态字符读取与显示", ["putchar 函数：输出一个字符", "getchar 函数：输入一个字符", "输入缓冲区与“剩下的回车符”", "字符输入输出与格式化输入输出", "任务实施：读入状态，完善台账"]),
             ("AI升华 让台账程序更“耐用”", ["逐条检验 AI 给出的多种解法", "画缓冲区、预测输出，离开 AI 再做"])]
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
<text x="68" y="{mid - 4}" fill="#fff" font-size="13" font-weight="700" text-anchor="middle">项目四</text>
<text x="68" y="{mid + 14}" fill="#fff" font-size="10.5" text-anchor="middle">开发顺序交互程序</text>
<g font-size="9.6" font-weight="700" text-anchor="middle">{''.join(boxes)}</g>
<g font-size="9.4" fill="#1F1F1F">{''.join(texts)}</g>
<g fill="{C}">{''.join(dots)}</g></svg>'''


figs['f_kmap'] = kmap()


# ================================================================== 电阻（色环）
BAND = {'黑': '#1E1E1E', '棕': '#7B4A23', '红': '#D0312D', '橙': '#F07C1C', '黄': '#F6C915', '绿': '#2E9A47',
        '蓝': '#1F6FD1', '紫': '#7D3CB5', '灰': '#9A9A9A', '白': '#FFFFFF', '金': '#C8A23A'}
RES = [('R1', '0.22 kΩ', '220 Ω', '红红棕金'), ('R2', '1 kΩ', '1000 Ω', '棕黑红金'), ('R3', '4.7 kΩ', '4700 Ω', '黄紫红金'),
       ('R4', '10 kΩ', '10000 Ω', '棕黑橙金'), ('R5', '100 kΩ', '100000 Ω', '棕黑黄金')]


def resistor(x, y, bands, scale=1.0, burnt=False):
    """x, y：左端引线起点（中线）；总长 96*scale"""
    s = scale
    o = [f'<path d="M{x},{y} L{x + 96 * s},{y}" stroke="#A7A9AC" stroke-width="{2.4 * s}" stroke-linecap="round"/>']
    bx, bw, bh = x + 18 * s, 60 * s, 20 * s
    body = '#E6CFA0' if not burnt else '#C9B48C'
    o.append(f'<path d="M{bx},{y - bh / 2 + 3 * s} q0,-{3 * s} {6 * s},-{3 * s} h{bw - 12 * s} q{6 * s},0 {6 * s},{3 * s} v{bh - 6 * s} q0,{3 * s} -{6 * s},{3 * s} h-{bw - 12 * s} q-{6 * s},0 -{6 * s},-{3 * s} z" fill="{body}" stroke="#B4955F" stroke-width="{0.8 * s}"/>')
    pos = [10, 19, 28, 46]
    for p, b in zip(pos, bands):
        stroke = ' stroke="#999" stroke-width="0.5"' if b == '白' else ''
        o.append(f'<rect x="{bx + p * s}" y="{y - bh / 2 + 0.6 * s}" width="{5 * s}" height="{bh - 1.2 * s}" fill="{BAND[b]}"{stroke}/>')
    o.append(f'<rect x="{bx + 3 * s}" y="{y - bh / 2 + 3 * s}" width="{bw - 6 * s}" height="{3 * s}" rx="{1.5 * s}" fill="#fff" opacity="0.35"/>')
    if burnt:
        o.append(f'<ellipse cx="{bx + 36 * s}" cy="{y + 1 * s}" rx="{9 * s}" ry="{6 * s}" fill="#3A2A1A" opacity="0.55"/>')
    return ''.join(o)


def f_res5():
    W, H = 520, 196
    o = [f'<rect x="0" y="0" width="{W}" height="{H}" rx="8" fill="#F7F9FC"/>']
    o.append(mtext(W / 2, 14, '实训课上用过的 5 个电阻（四色环电阻）', 9.6, D, 700))
    for k, (rn, kv, ov, bands) in enumerate(RES):
        x = 8 + k * 102
        o.append(f'<rect x="{x}" y="26" width="96" height="74" rx="6" fill="#fff" stroke="{L}" stroke-width="0.8"/>')
        o.append(resistor(x + 4, 50, bands, 0.92))
        o.append(mtext(x + 48, 74, rn, 9.6, D, 700))
        o.append(mtext(x + 48, 89, f'{kv}（{ov}）', 8, '#333'))
    # 色环读法
    y = 112
    o.append(f'<rect x="8" y="{y}" width="{W - 16}" height="76" rx="6" fill="#fff" stroke="{L}" stroke-width="0.8"/>')
    o.append(mtext(16, y + 13, '色环颜色代表的数字', 8.8, D, 700, 'start'))
    for k, cname in enumerate('黑棕红橙黄绿蓝紫灰白'):
        x = 16 + k * 31
        stroke = '#999' if cname == '白' else BAND[cname]
        o.append(f'<rect x="{x}" y="{y + 22}" width="26" height="14" rx="2" fill="{BAND[cname]}" stroke="{stroke}" stroke-width="0.6"/>')
        o.append(mtext(x + 13, y + 46, f'{cname} {k}', 8.4, '#333'))
    o.append(f'<rect x="{16 + 10 * 31}" y="{y + 22}" width="26" height="14" rx="2" fill="{BAND["金"]}"/>')
    o.append(mtext(16 + 10 * 31 + 13, y + 46, '金 ±5%', 8.4, '#333'))
    o.append(resistor(370, y + 30, '黄紫红金', 0.82))
    o.append(mtext(W - 62, y + 14, '读法示例（R3）', 8.4, D, 700))
    o.append(mtext(W - 62 + 4, y + 50, '黄 4、紫 7、红 ×10²', 8.2, '#333'))
    o.append(mtext(16, y + 64, '第 1、2 环是两位数字，第 3 环表示再乘 10 的几次方，第 4 环是误差。R3：47 × 10² = 4700 Ω = 4.7 kΩ', 8.4, '#333', 400, 'start'))
    return svgwrap(W, H, ''.join(o))


figs['f_res5'] = f_res5()


# ================================================================== 例4-1 的执行过程
def f_runtrace():
    W = 520
    cols = [('步骤', 34), ('执行的语句', 170), ('km', 46), ('minutes', 54), ('pace', 46), ('屏幕上新出现的内容', 160)]
    rows = [('①', 'printf("跑步距离（千米）：");', '?', '?', '?', '跑步距离（千米）：', None),
            ('②', 'scanf("%f", &km);', '3', '?', '?', '3⏎（键盘输入）', 2),
            ('③', 'printf("用时（分钟）：");', '3', '?', '?', '用时（分钟）：', None),
            ('④', 'scanf("%f", &minutes);', '3', '19.5', '?', '19.5⏎（键盘输入）', 3),
            ('⑤', 'pace = minutes / km;', '3', '19.5', '6.5', '（没有显示）', 4),
            ('⑥', 'printf("平均配速：%.2f…", pace);', '3', '19.5', '6.5', '平均配速：6.50 分钟/千米', None)]
    RH, HY = 24, 24
    H = HY + RH * len(rows) + 30
    o = [f'<rect x="0" y="0" width="{W}" height="{H}" rx="6" fill="#fff"/>']
    x = 4
    xs = []
    for name, w in cols:
        xs.append(x)
        o.append(f'<rect x="{x}" y="0" width="{w}" height="{HY}" fill="{C}"/>' + mtext(x + w / 2, HY / 2, name, 9, '#fff', 700, mono=name in ('km', 'minutes', 'pace')))
        x += w
    for r, row in enumerate(rows):
        y = HY + r * RH
        fill = '#fff' if r % 2 == 0 else '#F7F9FC'
        o.append(f'<rect x="4" y="{y}" width="{x - 4}" height="{RH}" fill="{fill}" stroke="{L}" stroke-width="0.5"/>')
        for c, (val, (name, w)) in enumerate(zip(row[:6], cols)):
            cx = xs[c] + w / 2
            if c == 1:
                o.append(mtext(xs[c] + 6, y + RH / 2, val, 8.2, '#1F1F1F', 400, 'start', mono=True))
            elif c in (2, 3, 4):
                hl = row[6] == c
                if hl:
                    o.append(f'<rect x="{xs[c] + 6}" y="{y + 4}" width="{w - 12}" height="{RH - 8}" rx="3" fill="{C}"/>')
                o.append(mtext(cx, y + RH / 2, val, 9, '#fff' if hl else ('#999' if val == '?' else '#1F1F1F'), 700 if hl else 400, mono=True))
            elif c == 5:
                o.append(mtext(xs[c] + 6, y + RH / 2, val, 8.4, '#555' if '（' in val[:1] else '#1F1F1F', 400, 'start'))
            else:
                o.append(mtext(cx, y + RH / 2, val, 10, D, 700))
        if r < len(rows) - 1:
            pass
    yb = HY + RH * len(rows)
    o.append(mtext(8, yb + 16, '说明：深色格是这一步刚刚改变的变量；“?”表示变量还没有得到确定的值。语句按书写的先后顺序执行，每条执行一次。', 8.4, '#4D4D4D', 400, 'start'))
    return svgwrap(W, H, ''.join(o))


figs['f_runtrace'] = f_runtrace()


# ================================================================== C 语句的五种类型（HTML 卡片）
def f_stmt():
    items = [('vertical_traffic_light', '控制语句', '改变语句的执行顺序，共 9 种，如 if、while、return', 'if (x > 0) …\nreturn 0;'),
             ('handshake', '函数调用语句', '函数调用加一个分号，请函数替我们完成一件事', 'printf("Hi");\nscanf("%d", &n);'),
             ('abacus', '表达式语句', '表达式加一个分号，最常见的是赋值语句', 'sum = a + b;\nx = x * 2;'),
             ('zzz', '空语句', '只有一个分号，什么也不做', ';'),
             ('package', '复合语句', '用 { } 把几条语句括起来，当作一条语句使用', '{ t = a;\n  a = b;\n  b = t; }')]
    cards = []
    for k, t, d, ex in items:
        cards.append(f'<div class="sc"><div class="sh"><img src="assets/fe/{k}.png"><b>{t}</b></div><div class="sd">{d}</div><pre class="sx">{esc(ex)}</pre></div>')
    return ('<div class="stmt"><div class="sbar">C 语句：向计算机发出的一条操作指令。分号“;”是语句的组成部分，不能漏写</div>'
            '<div class="sgrid">' + ''.join(cards) + '</div></div>')


figs['f_stmt'] = f_stmt()


# ================================================================== 赋值：把右边的值存入左边的变量
def cell(x, y, name, val, w=56, h=30, hl=False, old=None):
    o = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{C if hl else "#fff"}" stroke="{C}" stroke-width="1.3"/>']
    o.append(mtext(x + w / 2, y + h / 2, val, 12, '#fff' if hl else D, 700, mono=True))
    o.append(mtext(x + w / 2, y - 8, name, 9, '#333', 700, mono=True))
    if old:
        o.append(mtext(x + w + 14, y + h / 2, old, 9.5, '#999', 400, mono=True))
        o.append(f'<path d="M{x + w + 6},{y + h / 2 + 1} l16,0" stroke="#D0312D" stroke-width="1.2"/>')
    return ''.join(o)


def f_assign():
    W, H = 520, 178
    o = [f'<rect x="0" y="0" width="{W}" height="{H}" rx="8" fill="#F7F9FC"/>']
    # (a)
    o.append(f'<rect x="6" y="6" width="300" height="166" rx="7" fill="#fff" stroke="{L}"/>')
    o.append(chip(16, 14, 160, 20, 'score = score + bonus;', BG, D, 9.4, 700, 4, mono=True))
    o.append(cell(26, 64, 'score', '80'))
    o.append(cell(26, 124, 'bonus', '5'))
    o.append(f'<rect x="122" y="88" width="76" height="32" rx="16" fill="{BG}" stroke="{M}"/>' + mtext(160, 104, '80 + 5', 10.5, D, 700, mono=True))
    o.append(arrow([(82, 76), (120, 96)]))
    o.append(arrow([(82, 136), (120, 112)]))
    o.append(mtext(98, 80, '① 取值', 8.4, M, 700, 'start'))
    o.append(cell(232, 89, 'score', '85', 48, 30, True))
    o.append(arrow([(198, 104), (230, 104)]))
    o.append(mtext(206, 128, '② 计算', 8.4, M, 700))
    o.append(mtext(256, 136, '③ 存回 score', 8.4, M, 700))
    o.append(mtext(160, 160, '右边算出结果，再存入左边的变量；原来的 80 被覆盖', 8.4, '#4D4D4D'))
    # (b)
    o.append(f'<rect x="314" y="6" width="200" height="166" rx="7" fill="#fff" stroke="{L}"/>')
    o.append(chip(374, 14, 80, 20, 'a = b;', BG, D, 9.4, 700, 4, mono=True))
    o.append(mtext(340, 56, '执行前', 8.6, '#666', 700))
    o.append(cell(370, 52, 'a', '3', 40, 26))
    o.append(cell(440, 52, 'b', '7', 40, 26))
    o.append(mtext(340, 116, '执行后', 8.6, '#666', 700))
    o.append(cell(370, 112, '', '7', 40, 26, True))
    o.append(cell(440, 112, '', '7', 40, 26))
    o.append(arrow([(460, 80), (460, 92), (392, 92), (392, 108)], M, 1.2))
    o.append(mtext(426, 100, '复制', 8.4, M, 700))
    o.append(mtext(414, 156, '“=”读作“赋值为”，不是“等于”\nb 的值不变', 8.4, '#4D4D4D'))
    return svgwrap(W, H, ''.join(o))


figs['f_assign'] = f_assign()


# ================================================================== 输入与输出（以主机为中心）
def f_io():
    W, H = 520, 214
    o = [f'<rect x="0" y="0" width="{W}" height="{H}" rx="8" fill="#F7F9FC"/>']
    ins = [('keyboard', '键盘'), ('computer_mouse', '鼠标'), ('microphone', '话筒'), ('camera', '摄像头')]
    outs = [('desktop_computer', '显示器'), ('printer', '打印机'), ('speaker_high_volume', '音箱')]
    o.append(mtext(70, 16, '输入设备', 9.6, D, 700))
    for k, (ic, nm) in enumerate(ins):
        x, y = 14 + (k % 2) * 64, 28 + (k // 2) * 64
        o.append(f'<rect x="{x}" y="{y}" width="56" height="56" rx="6" fill="#fff" stroke="{L}"/>' + img(ic, x + 12, y + 5, 32) + mtext(x + 28, y + 46, nm, 8.4, '#333', 700))
    o.append(mtext(450, 16, '输出设备', 9.6, D, 700))
    for k, (ic, nm) in enumerate(outs):
        x, y = 388 + (k % 2) * 64, 28 + (k // 2) * 64
        o.append(f'<rect x="{x}" y="{y}" width="56" height="56" rx="6" fill="#fff" stroke="{L}"/>' + img(ic, x + 12, y + 5, 32) + mtext(x + 28, y + 46, nm, 8.4, '#333', 700))
    # 主机
    o.append(f'<rect x="186" y="26" width="148" height="124" rx="8" fill="{C}"/>')
    o.append(mtext(260, 42, '主机（CPU + 内存）', 9.6, '#fff', 700))
    for k, (nm, v) in enumerate([('r1', '0.22'), ('r2', '1.00'), ('s1', "'Y'")]):
        x = 198 + k * 44
        o.append(f'<rect x="{x}" y="70" width="38" height="24" rx="3" fill="#fff"/>' + mtext(x + 19, 82, v, 8.6, D, 700, mono=True) + mtext(x + 19, 62, nm, 8, L, 700, mono=True))
    o.append(mtext(260, 112, '变量就存放在内存里', 8.4, L))
    o.append(mtext(260, 132, '程序在这里处理数据', 8.4, L))
    o.append(arrow([(142, 88), (182, 88)], C, 2.4))
    o.append(mtext(162, 78, '输入', 9.4, C, 700))
    o.append(arrow([(338, 88), (382, 88)], C, 2.4))
    o.append(mtext(360, 78, '输出', 9.4, C, 700))
    # C 语言中的对应
    y = 162
    o.append(f'<rect x="8" y="{y}" width="{W - 16}" height="44" rx="6" fill="#fff" stroke="{L}"/>')
    o.append(mtext(20, y + 22, 'C 语言中：', 9, D, 700, 'start'))
    o.append(chip(84, y + 11, 54, 22, '键盘', BG, D, 9, 700, 4))
    o.append(arrow([(140, y + 22), (196, y + 22)]))
    o.append(mtext(168, y + 12, 'scanf', 8.4, M, 700, mono=True) + mtext(168, y + 36, 'getchar', 8.4, M, 700, mono=True))
    o.append(chip(200, y + 11, 120, 22, '变量（内存）', C, '#fff', 9, 700, 4))
    o.append(arrow([(322, y + 22), (378, y + 22)]))
    o.append(mtext(350, y + 12, 'printf', 8.4, M, 700, mono=True) + mtext(350, y + 36, 'putchar', 8.4, M, 700, mono=True))
    o.append(chip(382, y + 11, 54, 22, '屏幕', BG, D, 9, 700, 4))
    o.append(mtext(476, y + 22, '都在 stdio.h 中', 8.2, '#666'))
    return svgwrap(W, H, ''.join(o))


figs['f_io'] = f_io()


# ================================================================== printf 的格式控制字符串
def f_printf():
    W, H = 520, 200
    o = [f'<rect x="0" y="0" width="{W}" height="{H}" rx="8" fill="#F7F9FC"/>']
    segs = [('printf("', 'k'), ('实训室', 'n'), ('%d', 'f'), ('，面积', 'n'), ('%.1f', 'f'), ('平方米', 'n'), ('\\n', 'e'), ('", ', 'k'), ('room', 'a1'), (', ', 'k'), ('area', 'a2'), (');', 'k')]
    size = 12
    x = 22
    pos = {}
    y = 58
    o.append(mtext(22, 14, '设 room = 203，area = 86.5', 9, '#4D4D4D', 400, 'start'))
    o.append(mtext(505, 14, '输出表列：与格式说明按顺序一一对应', 8.8, C, 700, 'end'))
    for s_, kind in segs:
        w = tw(s_, size, True) + (6 if kind != 'k' else 0)
        if kind == 'n':
            o.append(f'<rect x="{x}" y="{y - 13}" width="{w}" height="26" rx="3" fill="#fff" stroke="{M}" stroke-width="1"/>')
            o.append(mtext(x + w / 2, y, s_, size, '#1F1F1F', 400))
        elif kind == 'f':
            o.append(f'<rect x="{x}" y="{y - 13}" width="{w}" height="26" rx="3" fill="{C}"/>')
            o.append(mtext(x + w / 2, y, s_, size, '#fff', 700, mono=True))
        elif kind == 'e':
            o.append(f'<rect x="{x}" y="{y - 13}" width="{w}" height="26" rx="3" fill="{BG}" stroke="{C}" stroke-dasharray="3 2"/>')
            o.append(mtext(x + w / 2, y, s_, size, D, 700, mono=True))
        elif kind.startswith('a'):
            o.append(f'<rect x="{x}" y="{y - 13}" width="{w}" height="26" rx="13" fill="{BG}" stroke="{C}"/>')
            o.append(mtext(x + w / 2, y, s_, size, D, 700, mono=True))
        else:
            o.append(mtext(x + w / 2, y, s_, size, '#555', 400, mono=True))
        pos.setdefault(kind, []).append((x, w))
        x += w + (3 if kind != 'k' else 0)
    for a_, f_ in (('a1', 0), ('a2', 1)):
        ax, aw = pos[a_][0]
        fx, fw = pos['f'][f_]
        o.append(f'<path d="M{ax + aw / 2},{y - 14} C{ax + aw / 2},{y - 40} {fx + fw / 2},{y - 40} {fx + fw / 2},{y - 16}" fill="none" stroke="{C}" stroke-width="1.3" stroke-dasharray="4 2" marker-end="url(#ar)"/>')
    # 图例
    ly = 96
    o.append(f'<rect x="22" y="{ly - 7}" width="18" height="14" rx="2" fill="#fff" stroke="{M}"/>' + mtext(46, ly, '普通字符：原样输出', 8.8, '#333', 700, 'start'))
    o.append(f'<rect x="178" y="{ly - 7}" width="18" height="14" rx="2" fill="{C}"/>' + mtext(202, ly, '格式说明：在这里“填入”数据', 8.8, C, 700, 'start'))
    o.append(f'<rect x="362" y="{ly - 7}" width="18" height="14" rx="2" fill="{BG}" stroke="{C}" stroke-dasharray="3 2"/>' + mtext(386, ly, '转义字符：\\n 表示换行', 8.8, D, 700, 'start'))
    # 输出结果
    yo = 124
    o.append(mtext(22, yo, '屏幕上显示：', 9, D, 700, 'start'))
    o.append(f'<rect x="22" y="{yo + 9}" width="300" height="30" rx="3" fill="#0C0C0C"/>')
    o.append(f'<text x="32" y="{yo + 29}" font-size="12" fill="#CCCCCC" font-family="{MONO}">实训室<tspan fill="#fff" text-decoration="underline">203</tspan>，面积<tspan fill="#fff" text-decoration="underline">86.5</tspan>平方米</text>')
    o.append(img('right_arrow_curving_left', 296, yo + 14, 20))
    o.append(mtext(344, yo + 10, '格式说明和输出项：', 8.8, D, 700, 'start'))
    o.append(mtext(344, yo + 25, '个数相等、类型一致、', 8.8, D, 700, 'start'))
    o.append(mtext(344, yo + 40, '顺序一一对应', 8.8, D, 700, 'start'))
    o.append(mtext(22, yo + 62, '下划线部分是由 %d、%.1f 换成的 room、area 的值；最后的 \\n 让光标移到下一行的开头。', 8.6, '#4D4D4D', 400, 'start'))
    return svgwrap(W, H, ''.join(o))


figs['f_printf'] = f_printf()


# ================================================================== 输出宽度与小数位数（方格）
def f_width():
    rows = [('%d', '25', '按实际位数输出'),
            ('%5d', '   25', '占 5 列，右对齐，左边补空格'),
            ('%-5d', '25   ', '占 5 列，左对齐，右边补空格'),
            ('%1d', '25', '宽度不够时按实际位数输出'),
            ('%f', '4.700000', '默认保留 6 位小数'),
            ('%.2f', '4.70', '保留 2 位小数'),
            ('%8.2f', '    4.70', '占 8 列，小数点也算一列'),
            ('%-8.2f', '4.70    ', '占 8 列，左对齐')]
    W, RH = 520, 25
    H = 30 + RH * len(rows) + 8
    o = [f'<rect x="0" y="0" width="{W}" height="{H}" rx="8" fill="#F7F9FC"/>']
    o.append(mtext(64, 16, '格式说明', 9, D, 700) + mtext(214, 16, '输出（每格 1 列，□ 为空格）', 9, D, 700) + mtext(420, 16, '说明', 9, D, 700))
    CW = 17
    for r, (spec, out, note) in enumerate(rows):
        y = 28 + r * RH
        o.append(chip(20, y + 2, 88, 20, spec, '#fff', D, 10.4, 700, 4, C, True))
        for k, ch in enumerate(out):
            x = 132 + k * CW
            if ch == ' ':
                o.append(f'<rect x="{x}" y="{y + 2}" width="{CW - 2}" height="20" fill="#fff" stroke="{L}" stroke-dasharray="2 2"/>')
            else:
                o.append(f'<rect x="{x}" y="{y + 2}" width="{CW - 2}" height="20" fill="{BG}" stroke="{M}" stroke-width="0.8"/>' + mtext(x + (CW - 2) / 2, y + 12, ch, 11, D, 700, mono=True))
        o.append(mtext(340, y + 12, note, 8.8, '#333', 400, 'start'))
    o.append(mtext(214, H - 4, '', 1))
    return svgwrap(W, H, ''.join(o))


figs['f_width'] = f_width()


# ================================================================== scanf：按“地址”把数据送进变量
def f_scanf():
    W, H = 520, 178
    o = [f'<rect x="0" y="0" width="{W}" height="{H}" rx="8" fill="#F7F9FC"/>']
    o.append(f'<rect x="12" y="10" width="270" height="28" rx="4" fill="#fff" stroke="{C}"/>')
    o.append(f'<text x="22" y="29" font-size="12" font-family="{MONO}" fill="#1F1F1F">scanf("<tspan fill="{C}" font-weight="700">%d%f</tspan>", <tspan fill="#D0312D" font-weight="700">&amp;room</tspan>, <tspan fill="#D0312D" font-weight="700">&amp;area</tspan>);</text>')
    o.append(img('keyboard', 12, 56, 36))
    o.append(mtext(30, 100, '键盘输入', 8.4, '#333', 700))
    chars = list('203 86.5') + ['⏎']
    X = 58
    o.append(mtext(X + 3 * 20 + 9, 52, '空格：分隔数据', 7.8, '#666'))
    o.append(mtext(X + 8 * 20 + 9, 52, '⏎：留在缓冲区', 7.8, '#666'))
    for k, ch in enumerate(chars):
        x = X + k * 20
        sp = ch == ' '
        o.append(f'<rect x="{x}" y="60" width="18" height="22" rx="2" fill="{"#fff" if sp else BG}" stroke="{M}" stroke-width="0.8"{" stroke-dasharray=\"2 2\"" if sp else ""}/>' + mtext(x + 9, 71, '' if sp else ch, 11, D, 700, mono=True))
    o.append(f'<path d="M{X},88 h58" stroke="{C}" stroke-width="2"/>' + mtext(X + 29, 98, '%d 读入 203', 8.4, C, 700))
    o.append(f'<path d="M{X + 80},88 h78" stroke="{C}" stroke-width="2"/>' + mtext(X + 119, 98, '%f 读入 86.5', 8.4, C, 700))
    o.append(arrow([(X + 29, 104), (X + 29, 124)], C, 1.4))
    o.append(arrow([(X + 119, 104), (X + 119, 124)], C, 1.4))
    for k, (nm, v, cx) in enumerate([('room', '203', X + 29), ('area', '86.5', X + 119)]):
        o.append(f'<rect x="{cx - 34}" y="126" width="68" height="24" rx="3" fill="{C}"/>' + mtext(cx, 138, v, 11, '#fff', 700, mono=True))
        o.append(mtext(cx, 164, f'变量 {nm}', 8.6, '#333', 700))
    # 右侧：门牌号类比
    o.append(f'<rect x="262" y="48" width="250" height="122" rx="7" fill="#fff" stroke="{L}"/>')
    for k, nm in enumerate(['room', 'area']):
        x = 280 + k * 74
        o.append(img('open_mailbox_with_raised_flag', x + 6, 54, 44))
        o.append(chip(x - 4, 102, 64, 18, f'&{nm}', '#fff', '#D0312D', 9, 700, 9, '#D0312D', True))
    o.append(mtext(476, 70, '& 是', 8.8, D, 700) + mtext(476, 84, '取地址', 8.8, D, 700) + mtext(476, 98, '运算符', 8.8, D, 700))
    o.append(mtext(387, 136, 'scanf 像快递员，要按“门牌号”（地址）', 8.4, '#333'))
    o.append(mtext(387, 152, '把数据送进变量，所以变量名前要加 &', 8.4, '#333'))
    return svgwrap(W, H, ''.join(o))


figs['f_scanf'] = f_scanf()


# ================================================================== 键盘缓冲区
def bufcells(x, y, chars, taken=(), w=20, h=24, size=11, hl=None):
    o = []
    for k, ch in enumerate(chars):
        cx = x + k * w
        sp = ch == ' '
        if k in taken:
            o.append(f'<rect x="{cx}" y="{y}" width="{w - 2}" height="{h}" rx="2" fill="#fff" stroke="{L}" stroke-dasharray="2 2"/>')
            o.append(mtext(cx + (w - 2) / 2, y + h / 2, '␣' if sp else ch, size, '#B8C2D1', 700, mono=True))
        else:
            fill = C if (hl is not None and k in hl) else (BG if not sp else '#fff')
            col = '#fff' if (hl is not None and k in hl) else D
            o.append(f'<rect x="{cx}" y="{y}" width="{w - 2}" height="{h}" rx="2" fill="{fill}" stroke="{M}" stroke-width="0.8"/>')
            o.append(mtext(cx + (w - 2) / 2, y + h / 2, '␣' if sp else ch, size, col, 700, mono=True))
    return ''.join(o)


def f_kbuf():
    W, H = 520, 150
    o = [f'<rect x="0" y="0" width="{W}" height="{H}" rx="8" fill="#F7F9FC"/>']
    o.append(img('keyboard', 14, 34, 44))
    o.append(mtext(36, 90, '敲键盘', 8.6, '#333', 700))
    o.append(arrow([(64, 56), (96, 56)], C, 1.8))
    o.append(f'<rect x="100" y="24" width="150" height="66" rx="8" fill="#fff" stroke="{C}" stroke-width="1.2"/>')
    o.append(mtext(175, 38, '输入缓冲区', 9.4, D, 700))
    o.append(bufcells(124, 48, list('4.7') + ['⏎']))
    o.append(mtext(175, 104, '按 Enter 后，这一行才交给程序', 8.4, '#666'))
    o.append(mtext(175, 118, '（Enter 也变成一个字符 ⏎，即 \\n）', 8.4, '#666'))
    o.append(arrow([(254, 56), (288, 56)], C, 1.8))
    o.append(f'<rect x="292" y="14" width="220" height="96" rx="8" fill="#fff" stroke="{L}"/>')
    o.append(mtext(402, 28, 'scanf("%f", &r); 按需取用', 9, D, 700))
    o.append(bufcells(306, 40, list('4.7') + ['⏎'], taken=(0, 1, 2)))
    o.append(arrow([(330, 68), (330, 78)], C, 1.2))
    o.append(chip(306, 80, 60, 22, 'r = 4.7', C, '#fff', 9.6, 700, 4, mono=True))
    o.append(mtext(452, 52, '⏎ 不是数字的一部分，', 8.4, '#D0312D', 700))
    o.append(mtext(452, 66, '读到这里就停下，', 8.4, '#D0312D', 700))
    o.append(mtext(452, 80, '它还留在缓冲区里', 8.4, '#D0312D', 700))
    o.append(mtext(452, 96, '等下一次输入来取', 8.4, '#666'))
    o.append(mtext(14, 140, '%d、%f 读数据前会自动跳过空格和回车，所以只用 scanf 读数值时，留下的 ⏎ 不会造成影响（任务二会遇到例外）。', 8.4, '#4D4D4D', 400, 'start'))
    return svgwrap(W, H, ''.join(o))


figs['f_kbuf'] = f_kbuf()


# ================================================================== 流程图（任务一、任务二）
def f_flow1():
    f = FC(300, 330, 9.6)
    x = 110
    f.term('s', x, 18, '开始')
    f.io('a', x, 62, '输入 5 个阻值 r1～r5', 168)
    f.proc('p', x, 108, '处理：本任务不需要', 168, blank=True)
    f.io('b', x, 154, '输出台账标题和表头', 168)
    f.io('c', x, 200, '输出 5 行：序号、阻值', 168)
    f.io('d', x, 246, '输出表尾和单位', 168)
    f.term('e', x, 292, '结束')
    for a, b in (('s', 'a'), ('a', 'p'), ('p', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e')):
        f.v(a, b)
    br = ''
    for y1, y2, t in ((48, 76, '第一步'), (94, 122, '第二步'), (140, 260, '第三步')):
        br += f'<path d="M206,{y1} h6 V{y2} h-6" fill="none" stroke="{L}" stroke-width="1.2"/>' + mtext(240, (y1 + y2) / 2, t, 9.4, C, 700)
    return f.svg(br)


figs['f_flow1'] = f_flow1()


def f_flow2():
    f = FC(344, 376, 9.6)
    x = 140
    f.term('s', x, 18, '开始')
    f.io('a', x, 62, '输入 5 个阻值 r1～r5', 180)
    f.proc('g', x, 108, '读走留下的回车符', 180)
    f.io('b', x, 154, '输入 5 个状态字符 s1～s5', 180)
    f.proc('p', x, 200, '处理：本任务不需要', 180, blank=True)
    f.io('c', x, 246, '输出台账标题和表头', 180)
    f.io('d', x, 292, '输出 5 行：序号、阻值、状态', 180)
    f.term('e', x, 338, '结束')
    for a, b in (('s', 'a'), ('a', 'g'), ('g', 'b'), ('b', 'p'), ('p', 'c'), ('c', 'd'), ('d', 'e')):
        f.v(a, b)
    br = ''
    for y1, y2, t in ((48, 168, '第一步'), (186, 214, '第二步'), (232, 306, '第三步')):
        br += f'<path d="M242,{y1} h6 V{y2} h-6" fill="none" stroke="{L}" stroke-width="1.2"/>' + mtext(276, (y1 + y2) / 2, t, 9.4, C, 700)
    br += f'<rect x="44" y="96" width="192" height="24" rx="3" fill="none" stroke="#D0312D" stroke-width="1.2" stroke-dasharray="4 2"/>'
    br += mtext(22, 108, '新增', 8.6, '#D0312D', 700)
    return f.svg(br)


figs['f_flow2'] = f_flow2()


# ================================================================== 任务二：电阻状态
def f_status():
    W, H = 520, 120
    o = [f'<rect x="0" y="0" width="{W}" height="{H}" rx="8" fill="#F7F9FC"/>']
    st = ['Y', 'Y', 'N', 'Y', 'Y']
    for k, ((rn, kv, ov, bands), s) in enumerate(zip(RES, st)):
        x = 8 + k * 102
        bad = s == 'N'
        o.append(f'<rect x="{x}" y="8" width="96" height="104" rx="6" fill="#fff" stroke="{"#D0312D" if bad else L}" stroke-width="{1.2 if bad else 0.8}"/>')
        o.append(resistor(x + 4, 32, bands, 0.92, burnt=bad))
        o.append(mtext(x + 48, 54, f'{rn}  {kv}', 8.8, D, 700))
        o.append(img('check_mark_button' if not bad else 'cross_mark_button', x + 14, 66, 30))
        o.append(f'<rect x="{x + 52}" y="70" width="28" height="24" rx="4" fill="{C if not bad else "#D0312D"}"/>' + mtext(x + 66, 82, s, 13, '#fff', 700, mono=True))
        o.append(mtext(x + 48, 104, '完好' if not bad else '损坏（烧焦）', 8.4, '#333' if not bad else '#D0312D', 700))
    return svgwrap(W, H, ''.join(o))


figs['f_status'] = f_status()


# ================================================================== getchar 与 putchar
def f_getput():
    W, H = 520, 132
    o = [f'<rect x="0" y="0" width="{W}" height="{H}" rx="8" fill="#F7F9FC"/>']
    o.append(mtext(80, 16, '输入缓冲区（输入 Yes 后按 Enter）', 8.8, D, 700))
    o.append(bufcells(14, 26, list('Yes') + ['⏎'], taken=(0,), w=28, h=30, size=13))
    o.append(mtext(78, 70, 'e、s、⏎ 还留在缓冲区里', 8.4, '#666'))
    o.append(arrow([(28, 58), (28, 92), (150, 92)], C, 1.4))
    o.append(chip(154, 80, 112, 24, 'c = getchar();', '#fff', D, 9.6, 700, 4, C, True))
    o.append(mtext(210, 116, '一次只读一个字符', 8.4, C, 700))
    o.append(arrow([(268, 92), (292, 92)], C, 1.4))
    o.append(f'<rect x="296" y="76" width="40" height="32" rx="4" fill="{C}"/>' + mtext(316, 92, "'Y'", 12, '#fff', 700, mono=True) + mtext(316, 68, '变量 c', 8.4, '#333', 700))
    o.append(arrow([(338, 92), (360, 92)], C, 1.4))
    o.append(chip(364, 80, 90, 24, 'putchar(c);', '#fff', D, 9.6, 700, 4, C, True))
    o.append(mtext(410, 116, '一次只输出一个字符', 8.4, C, 700))
    o.append(arrow([(456, 92), (470, 92)], C, 1.4))
    o.append(f'<rect x="474" y="72" width="38" height="40" rx="3" fill="#0C0C0C"/>' + f'<text x="486" y="97" font-size="14" fill="#fff" font-family="{MONO}">Y</text>')
    o.append(img('desktop_computer', 474, 22, 38))
    return svgwrap(W, H, ''.join(o))


figs['f_getput'] = f_getput()


# ================================================================== 剩下的回车符：问题与解决
def f_buf2():
    W, H = 520, 236
    o = [f'<rect x="0" y="0" width="{W}" height="{H}" rx="8" fill="#F7F9FC"/>']
    # 问题
    o.append(f'<rect x="6" y="6" width="{W - 12}" height="106" rx="7" fill="#fff" stroke="#D0312D" stroke-width="1"/>')
    o.append(chip(14, 12, 116, 20, '问题：buf.c', '#D0312D', '#fff', 9, 700, 4))
    o.append(mtext(150, 22, '输入 4.7 后按 Enter', 8.6, '#333', 700, 'start'))
    o.append(bufcells(20, 42, list('4.7') + ['⏎'], taken=(0, 1, 2), w=24, h=26, size=12))
    o.append(mtext(64, 84, '① scanf("%f", &r)', 8.6, C, 700, mono=True))
    o.append(mtext(64, 98, '取走 4.7，留下 ⏎', 8.4, '#666'))
    o.append(arrow([(110, 55), (168, 55)], '#D0312D', 1.4))
    o.append(chip(172, 43, 104, 24, 's = getchar();', '#fff', D, 9.2, 700, 4, C, True))
    o.append(mtext(224, 84, '② 缓冲区里还有 ⏎，', 8.4, '#D0312D', 700))
    o.append(mtext(224, 98, '直接取走，不等你输入', 8.4, '#D0312D', 700))
    o.append(arrow([(278, 55), (300, 55)], '#D0312D', 1.4))
    o.append(f'<rect x="304" y="40" width="64" height="30" rx="4" fill="#D0312D"/>' + mtext(336, 55, "'\\n'", 11, '#fff', 700, mono=True))
    o.append(mtext(336, 84, 's 的值是 10', 8.4, '#D0312D', 700))
    o.append(mtext(336, 98, '（换行符的编码）', 8.4, '#666'))
    o.append(img('face_with_spiral_eyes', 398, 30, 40))
    o.append(mtext(452, 84, '“程序没等我', 8.6, '#333', 700) + mtext(452, 98, '输入就往下走了！”', 8.6, '#333', 700))
    # 解决
    y = 120
    o.append(f'<rect x="6" y="{y}" width="{W - 12}" height="110" rx="7" fill="#fff" stroke="{C}" stroke-width="1"/>')
    o.append(chip(14, y + 6, 116, 20, '解决：buf2.c', C, '#fff', 9, 700, 4))
    o.append(mtext(150, y + 16, '先多写一句 getchar(); 读走 ⏎，再读状态字符', 8.6, '#333', 700, 'start'))
    o.append(bufcells(20, y + 36, list('4.7') + ['⏎'], taken=(0, 1, 2, 3), w=24, h=26, size=12))
    o.append(mtext(64, y + 78, '① scanf 取走 4.7', 8.4, C, 700))
    o.append(mtext(64, y + 92, '② getchar(); 取走 ⏎', 8.4, C, 700))
    o.append(arrow([(110, y + 49), (138, y + 49)], C, 1.4))
    o.append(mtext(186, y + 34, '③ 缓冲区空了，等待输入', 8.4, '#333', 700))
    o.append(bufcells(160, y + 44, ['Y', '⏎'], w=24, h=26, size=12, hl=(0,)))
    o.append(mtext(186, y + 86, '输入 Y 后按 Enter', 8.4, '#666'))
    o.append(arrow([(212, y + 57), (240, y + 57)], C, 1.4))
    o.append(chip(244, y + 45, 104, 24, 's = getchar();', '#fff', D, 9.2, 700, 4, C, True))
    o.append(arrow([(350, y + 57), (372, y + 57)], C, 1.4))
    o.append(f'<rect x="376" y="{y + 42}" width="56" height="30" rx="4" fill="{C}"/>' + mtext(404, y + 57, "'Y'", 12, '#fff', 700, mono=True))
    o.append(mtext(404, y + 86, 's 的值是 89', 8.4, C, 700))
    o.append(img('check_mark_button', 452, y + 36, 40))
    return svgwrap(W, H, ''.join(o))


figs['f_buf2'] = f_buf2()


# ================================================================== AI升华：四格漫画
def f_comic():
    W, H = 520, 330
    o = []
    PW, PH = 254, 158
    pos = [(4, 4), (262, 4), (4, 168), (262, 168)]
    for k, (x, y) in enumerate(pos, 1):
        o.append(f'<rect x="{x}" y="{y}" width="{PW}" height="{PH}" rx="8" fill="#fff" stroke="{C}" stroke-width="1.3"/>')
        o.append(f'<circle cx="{x + 14}" cy="{y + 14}" r="9" fill="{C}"/>' + mtext(x + 14, y + 14, str(k), 10, '#fff', 700))
    # 1 输入时多按了空格
    x, y = 4, 4
    o.append(img('keyboard', x + 120, y + 96, 50))
    o.append(av_he(x + 52, y + 118, 24, 'happy'))
    o.append(bubble(x + 30, y + 28, 196, 44, '0.22 1 4.7 10 100␣，回车！\nYYNYY，回车！', (x + 60, y + 92), 8.8))
    o.append(mtext(x + 192, y + 98, '（100 后面顺手', 8, '#666') + mtext(x + 192, y + 110, '多按了一个空格）', 8, '#666'))
    # 2 台账乱了
    x, y = 262, 4
    o.append(f'<rect x="{x + 14}" y="{y + 26}" width="140" height="112" rx="4" fill="#0C0C0C"/>')
    lines = ['序号   阻值  状态', '  1    0.22', '', '  2    1.00   Y', '  3    4.70   Y', '  4   10.00   N', '  5  100.00   Y']
    for j, s in enumerate(lines):
        o.append(f'<text x="{x + 20}" y="{y + 42 + j * 14}" font-size="8" fill="#CCCCCC" font-family="{MONO}" xml:space="preserve">{esc(s)}</text>')
    o.append(f'<rect x="{x + 82}" y="{y + 92}" width="14" height="13" fill="none" stroke="#D0312D" stroke-width="1.2"/>')
    o.append(av_he(x + 212, y + 124, 22, 'shock'))
    o.append(bubble(x + 162, y + 28, 86, 58, '空了一行？\n第 3 个明明是 N，\n怎么成了 Y！', (x + 206, y + 98), 8.4))
    # 3 小智查缓冲区
    x, y = 4, 168
    o.append(mtext(x + 30, y + 34, '阻值读完后，剩下空格和回车：', 8.4, D, 700, 'start'))
    o.append(bufcells(x + 12, y + 44, [' ', '⏎'], w=18, h=22, size=10, hl=(0,)))
    o.append(bufcells(x + 60, y + 44, list('YYNYY') + ['⏎'], w=18, h=22, size=10))
    o.append(mtext(x + 29, y + 76, '剩下的', 7.8, '#666') + mtext(x + 113, y + 76, '后来输入的状态', 7.8, '#666'))
    o.append(mtext(x + 12, y + 94, 'getchar(); 读走了空格，', 8.2, C, 700, 'start'))
    o.append(mtext(x + 12, y + 108, 's1 读到回车符，', 8.2, '#D0312D', 700, 'start'))
    o.append(mtext(x + 12, y + 122, 's2～s5 读到 Y、Y、N、Y', 8.2, '#D0312D', 700, 'start'))
    o.append(img('magnifying_glass_tilted_left', x + 128, y + 104, 34))
    o.append(av_zhi(x + 212, y + 124, 22, 'think'))
    o.append(bubble(x + 172, y + 30, 76, 46, '找到了！\n多出的空格\n惹的祸', (x + 210, y + 98), 8.4))
    # 4 问 AI，逐个验证
    x, y = 262, 168
    o.append(av_he(x + 40, y + 126, 22, 'think'))
    o.append(bubble(x + 14, y + 30, 112, 48, '那怎么改？\n我去问问 AI！', (x + 42, y + 102), 8.8))
    o.append(av_zhi(x + 206, y + 126, 22, 'happy'))
    o.append(bubble(x + 136, y + 30, 112, 60, 'AI 会给出好几种\n办法，有对有错，\n要一个个验证哦！', (x + 204, y + 102), 8.4))
    o.append(img('clipboard', x + 112, y + 104, 34))
    return svgwrap(W, H, ''.join(o))


figs['f_comic'] = f_comic()


# ================================================================== 挑战题：贴片电阻
def f_smd():
    W, H = 520, 128
    o = [f'<rect x="0" y="0" width="{W}" height="{H}" rx="8" fill="#F7F9FC"/>']
    # 电路板一角
    o.append(f'<rect x="14" y="14" width="160" height="100" rx="6" fill="#2F6B4F"/>')
    for k in range(5):
        o.append(f'<path d="M14,{30 + k * 18} h160" stroke="#3E8763" stroke-width="2"/>')
    o.append(f'<rect x="44" y="46" width="12" height="36" fill="#D8DDE3"/><rect x="132" y="46" width="12" height="36" fill="#D8DDE3"/>')
    o.append(f'<rect x="52" y="42" width="84" height="44" rx="2" fill="#1C1C1C"/>')
    o.append(f'<text x="94" y="72" font-size="22" fill="#fff" font-family="{MONO}" text-anchor="middle" font-weight="700">472</text>')
    o.append(mtext(94, 104, '贴片电阻（放大）', 8.4, '#E8EEF7', 700))
    # 读法
    o.append(mtext(200, 28, '贴片电阻上的 3 位代码怎么读？', 9.6, D, 700, 'start'))
    o.append(chip(204, 44, 28, 26, '4', C, '#fff', 13, 700, 4, mono=True))
    o.append(chip(236, 44, 28, 26, '7', C, '#fff', 13, 700, 4, mono=True))
    o.append(chip(272, 44, 28, 26, '2', '#fff', C, 13, 700, 4, C, True))
    o.append(mtext(234, 82, '前两位：有效数字', 8.4, C, 700))
    o.append(mtext(286, 96, '第三位：再乘 10 的几次方', 8.4, D, 700))
    o.append(mtext(320, 57, '→   47 × 10² = 4700 Ω = 4.7 kΩ', 11, '#1F1F1F', 700, 'start'))
    o.append(mtext(200, 116, '再如：103 → 10 × 10³ = 10000 Ω；221 → 22 × 10¹ = 220 Ω', 8.6, '#4D4D4D', 400, 'start'))
    return svgwrap(W, H, ''.join(o))


figs['f_smd'] = f_smd()


# ------------------------------------------------------------------ 课堂练习图标（与项目三相同）
figs['ico_practice'] = f'''<svg viewBox="0 0 54 54" width="54" height="54"><rect x="1" y="1" width="52" height="52" rx="10" fill="{C}"/>
<path d="M16 38l3-9 15-15 6 6-15 15z" fill="#fff"/><path d="M16 38l3-9 6 6z" fill="{L}"/><path d="M31 17l6 6" stroke="{C}" stroke-width="2"/></svg>'''

CSS = f'''
body {{ margin:0; background:#fff; font-family:{FONT}; }}
.fig {{ display:inline-block; padding:6px; background:#fff; margin:10px; }}
.stmt {{ width:520px; }}
.sbar {{ background:{C}; color:#fff; font-size:10px; font-weight:700; text-align:center; border-radius:12px; padding:4px 8px; margin-bottom:6px; }}
.sgrid {{ display:grid; grid-template-columns:repeat(5,1fr); gap:6px; }}
.sc {{ border:1px solid {L}; border-top:3px solid {C}; border-radius:4px; padding:6px 6px 6px; background:#fff; display:flex; flex-direction:column; }}
.sh {{ display:flex; flex-direction:column; align-items:center; gap:3px; }}
.sh img {{ width:34px; height:34px; }}
.sh b {{ color:{D}; font-size:10px; white-space:nowrap; }}
.sd {{ font-size:8.8px; color:#1F1F1F; margin:5px 0 6px; line-height:1.45; min-height:38px; }}
.sx {{ font-family:{MONO}; font-size:8.6px; color:{D}; background:{BG}; padding:4px 5px; border-radius:3px; margin:0; min-height:40px; line-height:1.45; white-space:pre; }}
'''

if __name__ == '__main__':
    import os
    os.makedirs('fig', exist_ok=True)
    with open('fig/figs.html', 'w', encoding='utf8') as fh:
        fh.write(f'<!doctype html><meta charset="utf-8"><style>{CSS}</style><body>')
        for k, v in figs.items():
            fh.write(f'<div class="fig" id="{k}">{v}</div>\n')
    print(' '.join(figs))
