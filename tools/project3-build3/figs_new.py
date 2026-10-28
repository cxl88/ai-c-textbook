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
def f_scene2():
    W, H = 520, 262
    o = []
    road = f'M14,70 H452 A57,57 0 0 1 452,184 H70'
    o.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="8" fill="#F7F9FC"/>')
    o.append(f'<path d="{road}" fill="none" stroke="#DCE4F0" stroke-width="30" stroke-linecap="round"/>')
    o.append(f'<path d="{road}" fill="none" stroke="#fff" stroke-width="2" stroke-dasharray="8 7"/>')
    st = [('magnifying_glass_tilted_left', '核验录取信息', '报到大厅'), ('card_index_dividers', '核对专业班级', '学院迎新点'),
          ('credit_card', '领一卡通和物资', '物资发放点'), ('memo', '办理入住登记', '宿舍楼值班室'),
          ('key', '领取宿舍钥匙', '宿舍楼值班室'), ('bed', '确认床位信息', '宿舍房间'), ('laptop', '录入学籍信息', '学籍登记处')]
    pos = [(108, 70), (218, 70), (328, 70), (438, 70), (402, 184), (292, 184), (182, 184)]
    for k, ((ic, t, wh), (x, y)) in enumerate(zip(st, pos), 1):
        o.append(f'<circle cx="{x}" cy="{y}" r="23" fill="#fff" stroke="{C}" stroke-width="1.6"/>')
        o.append(img(ic, x - 15, y - 15, 30))
        o.append(f'<circle cx="{x - 18}" cy="{y - 18}" r="8.5" fill="{C}"/>' + mtext(x - 18, y - 18, str(k), 9.5, '#fff', 700))
        o.append(mtext(x, y + 36, t, 9.6, D, 700))
        o.append(mtext(x, y + 49, wh, 8.2, '#666'))
    # 起点、终点
    o.append(img('school', 6, 18, 40))
    o.append(mtext(26, 11, '起点：校门', 8.6, D, 700))
    o.append(img('party_popper', 48, 160, 46))
    o.append(mtext(71, 218, '报到完成！', 9.8, D, 700))
    o.append(mtext(71, 231, '开启大学生活', 8.2, '#666'))
    # 回头路：核验不通过
    o.append(f'<path d="M100,44 C100,22 122,18 124,40" fill="none" stroke="{M}" stroke-width="1.1" stroke-dasharray="3 2" marker-end="url(#ar)"/>')
    o.append(mtext(150, 23, '信息有误？更正后重来', 8, M, 400))
    return svgwrap(W, H, ''.join(o))


figs['f_scene'] = f_scene2()


# ------------------------------------------------------------------ 图：程序 = 算法 + 数据结构（做菜类比，重画）
def f_prog2():
    W, H = 520, 232
    o = []

    def card(x, y, w, h, title, dark=False):
        f, tc = (C, '#fff') if dark else ('#fff', D)
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{f}" stroke="{C}" stroke-width="1.1"/>')
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="20" rx="6" fill="{D if dark else BG}"/>')
        o.append(f'<rect x="{x}" y="{y + 14}" width="{w}" height="6" fill="{D if dark else BG}"/>')
        o.append(mtext(x + w / 2, y + 10.5, title, 9.6, '#fff' if dark else D, 700))

    def sym(x, y, s):
        o.append(mtext(x, y, s, 22, C, 700))

    for row, y0 in ((0, 10), (1, 122)):
        o.append(f'<rect x="4" y="{y0}" width="512" height="102" rx="8" fill="{"#F7F9FC" if row == 0 else "#F3F6FB"}"/>')
    # 第一行：做菜
    o.append(img('man_cook', 12, 26, 46))
    o.append(mtext(35, 84, '做菜', 10, D, 700))
    card(70, 20, 120, 84, '食材（数据）')
    o.append(img('tomato', 82, 46, 30) + img('egg', 116, 46, 28) + img('leafy_green', 148, 46, 30))
    o.append(mtext(130, 90, '番茄 2 个、鸡蛋 3 个', 8.4, '#333'))
    sym(203, 64, '+')
    card(216, 20, 150, 84, '菜谱（算法）')
    o.append(img('memo', 224, 40, 30))
    o.append(mtext(304, 55, '① 打蛋　② 炒蛋盛出', 8.6, '#1F1F1F'))
    o.append(mtext(304, 72, '③ 炒番茄　④ 倒回鸡蛋', 8.6, '#1F1F1F'))
    o.append(mtext(291, 92, '步骤清楚，顺序不能乱', 8.2, M))
    sym(379, 64, '=')
    card(392, 20, 116, 84, '一道菜', True)
    o.append(img('shallow_pan_of_food', 430, 42, 40))
    o.append(mtext(450, 92, '番茄炒蛋', 9.4, '#fff', 700))
    # 第二行：编程
    o.append(img('technologist', 12, 138, 46))
    o.append(mtext(35, 196, '编程', 10, D, 700))
    card(70, 132, 120, 84, '数据（数据结构）')
    for k, n in enumerate(['86', '92', '78']):
        o.append(f'<rect x="{80 + k * 36}" y="{160}" width="30" height="22" rx="4" fill="{BG}" stroke="{L}"/>' + mtext(95 + k * 36, 171, n, 10, D, 700, mono=True))
    o.append(mtext(130, 202, '三门成绩、总分、平均分', 8.4, '#333'))
    sym(203, 176, '+')
    card(216, 132, 150, 84, '算法（解题步骤）')
    o.append(img('card_index_dividers', 224, 152, 30))
    o.append(mtext(304, 167, '① 输入成绩　② 求总分', 8.6, '#1F1F1F'))
    o.append(mtext(304, 184, '③ 求平均分　④ 输出', 8.6, '#1F1F1F'))
    o.append(mtext(291, 204, '本项目重点学习', 8.2, M))
    sym(379, 176, '=')
    card(392, 132, 116, 84, '程序', True)
    o.append(img('laptop', 430, 154, 40))
    o.append(mtext(450, 204, 'avg.c（例3-1）', 9, '#fff', 700))
    return svgwrap(W, H, ''.join(o))


figs['f_prog'] = f_prog2()


# ------------------------------------------------------------------ 图：交换两杯饮料（饮料上色）
def f_swap2():
    W, H = 520, 162
    o = []
    COLA, JUICE = '#5A3825', '#F3A43B'

    def cup(x, y, name, liq):
        o.append(f'<path d="M{x},{y} L{x + 34},{y} L{x + 30},{y + 50} Q{x + 17},{y + 54} {x + 4},{y + 50} Z" fill="#FDFEFF" stroke="#8A97AA" stroke-width="1.1"/>')
        if liq:
            col = COLA if liq == '可乐' else JUICE
            o.append(f'<path d="M{x + 1.4},{y + 14} L{x + 32.6},{y + 14} L{x + 29.2},{y + 49} Q{x + 17},{y + 52.5} {x + 4.8},{y + 49} Z" fill="{col}"/>')
            o.append(f'<ellipse cx="{x + 17}" cy="{y + 14}" rx="15.6" ry="2.2" fill="{"#7A5238" if liq == "可乐" else "#F8C276"}"/>')
            if liq == '可乐':
                o.append(''.join(f'<circle cx="{x + cx}" cy="{y + cy}" r="1.3" fill="#fff" opacity=".55"/>' for cx, cy in ((10, 24), (20, 32), (14, 40), (24, 22))))
        o.append(f'<path d="M{x + 5},{y + 4} L{x + 8},{y + 44}" stroke="#fff" stroke-width="2.2" opacity=".7"/>')
        o.append(mtext(x + 17, y + 64, name, 9, D, 700))
        o.append(mtext(x + 17, y + 77, liq or '空', 8.2, '#555'))

    titles = ['开始', '第 1 步：A 倒入 C', '第 2 步：B 倒入 A', '第 3 步：C 倒入 B']
    states = [('可乐', '果汁', None), (None, '果汁', '可乐'), ('果汁', None, '可乐'), ('果汁', '可乐', None)]
    for i, (t, (a, b, c)) in enumerate(zip(titles, states)):
        x0 = 6 + i * 130
        o.append(f'<rect x="{x0}" y="6" width="120" height="146" rx="6" fill="#F7F9FC" stroke="{L}" stroke-width="0.9"/>')
        o.append(mtext(x0 + 60, 22, t, 9.6, D, 700))
        cup(x0 + 3, 46, 'A 杯', a)
        cup(x0 + 43, 46, 'B 杯', b)
        cup(x0 + 83, 46, 'C 杯', c)
    for i in range(3):
        x = 6 + i * 130 + 120
        o.append(f'<path d="M{x + 1},80 L{x + 9},80" stroke="{M}" stroke-width="1.5" marker-end="url(#ar)"/>')
    return svgwrap(W, H, ''.join(o))


figs['f_swap'] = f_swap2()


# ------------------------------------------------------------------ 新图：高斯的配对算法
def f_gauss():
    W, H = 520, 150
    o = [f'<rect x="0" y="0" width="{W}" height="{H}" rx="8" fill="#F7F9FC"/>']
    top = ['1', '2', '3', '4', '…', '49', '50']
    bot = ['100', '99', '98', '97', '…', '52', '51']
    for k, (a, b) in enumerate(zip(top, bot)):
        x = 18 + k * 46
        if a == '…':
            o.append(mtext(x + 17, 38, '…', 14, M, 700) + mtext(x + 17, 108, '…', 14, M, 700))
            continue
        o.append(f'<rect x="{x}" y="24" width="34" height="26" rx="5" fill="#fff" stroke="{C}" stroke-width="1.1"/>' + mtext(x + 17, 37, a, 11, D, 700))
        o.append(f'<rect x="{x}" y="94" width="34" height="26" rx="5" fill="{C}"/>' + mtext(x + 17, 107, b, 11, '#fff', 700))
        o.append(f'<line x1="{x + 17}" y1="52" x2="{x + 17}" y2="92" stroke="{L}" stroke-width="1.4"/>')
        o.append(f'<rect x="{x + 1}" y="63" width="32" height="18" rx="9" fill="{BG}" stroke="{L}"/>' + mtext(x + 17, 72, '101', 9.2, C, 700))
    o.append(mtext(160, 12, '正着写 1～50', 8.6, '#555'))
    o.append(mtext(160, 136, '倒着写 100～51', 8.6, '#555'))
    o.append(f'<rect x="352" y="22" width="156" height="100" rx="8" fill="#fff" stroke="{C}" stroke-width="1.2"/>')
    o.append(img('light_bulb', 362, 32, 30))
    o.append(mtext(452, 40, '上下每一对', 9.4, D, 700) + mtext(452, 54, '的和都是 101', 9.4, D, 700))
    o.append(f'<line x1="364" y1="70" x2="496" y2="70" stroke="{L}"/>')
    o.append(mtext(430, 86, '共 50 对', 9.4, '#1F1F1F'))
    o.append(mtext(430, 106, '101 × 50 = 5050', 11, C, 700))
    return svgwrap(W, H, ''.join(o))


figs['f_gauss'] = f_gauss()


# ------------------------------------------------------------------ 新图：两种猜数字算法（代替原表3-2）
def f_guess():
    W, H = 520, 292
    o = [f'<rect x="0" y="0" width="{W}" height="{H}" rx="8" fill="#F7F9FC"/>']
    X0, X1 = 140, 446

    def sx(v):
        return X0 + (v - 1) * (X1 - X0) / 99

    # 顺序猜
    o.append(img('snail', 12, 10, 30))
    o.append(mtext(48, 18, '顺序猜', 10.4, D, 700, 'start') + mtext(48, 33, '1、2、3……逐个猜', 8.4, '#555', 400, 'start'))
    for v in range(1, 101):
        x = sx(v) - 1.5
        f = C if v < 70 else ('#E4572E' if v == 70 else '#fff')
        o.append(f'<rect x="{x:.1f}" y="16" width="3" height="14" fill="{f}" stroke="{L}" stroke-width="0.4"/>')
    o.append(mtext(sx(35), 42, '猜了 70 次才猜中', 8.6, D, 700))
    o.append(mtext(486, 17, '最多', 8, '#666') + mtext(486, 30, '100 次', 9.6, D, 700))
    o.append(f'<line x1="10" y1="56" x2="510" y2="56" stroke="{L}" stroke-dasharray="3 3"/>')
    # 折半猜
    o.append(img('rabbit_face', 12, 64, 30))
    o.append(mtext(48, 72, '折半猜', 10.4, D, 700, 'start') + mtext(48, 87, '每次猜中间数', 8.4, '#555', 400, 'start'))
    rows = [(1, 100, 50, '小了'), (51, 100, 75, '大了'), (51, 74, 62, '小了'), (63, 74, 68, '小了'),
            (69, 74, 71, '大了'), (69, 70, 69, '小了'), (70, 70, 70, '猜对了！')]
    y = 104
    for k, (lo, hi, g, r) in enumerate(rows, 1):
        o.append(mtext(112, y, f'第{k}次', 8.6, '#555'))
        o.append(f'<rect x="{X0}" y="{y - 4}" width="{X1 - X0}" height="8" rx="4" fill="#E9EDF3"/>')
        o.append(f'<rect x="{sx(lo) - 2:.1f}" y="{y - 4}" width="{sx(hi) - sx(lo) + 4:.1f}" height="8" rx="4" fill="{L}"/>')
        o.append(mtext(sx(lo) - 5, y, str(lo), 7.6, '#666', 400, 'end') if hi - lo > 3 else '')
        if hi != lo and hi - lo > 3:
            o.append(mtext(sx(hi) + 5, y, str(hi), 7.6, '#666', 400, 'start'))
        hit = g == 70
        o.append(f'<circle cx="{sx(g):.1f}" cy="{y}" r="8" fill="{"#E4572E" if hit else C}"/>' + mtext(sx(g), y, str(g), 7.8, '#fff', 700))
        o.append(mtext(486, y, r, 8.6, '#E4572E' if hit else D, 700))
        y += 25
    o.append(img('party_popper', sx(70) + 12, y - 52, 24))
    o.append(mtext(486, 72, '最多', 8, '#666') + mtext(486, 85, '7 次', 9.6, D, 700))
    o.append(mtext(293, y - 2, '浅蓝色是“答案可能在的范围”：每猜一次，范围缩小一半', 8.4, '#555'))
    return svgwrap(W, H, ''.join(o))


figs['f_guess'] = f_guess()


# ------------------------------------------------------------------ 图：算法的五个特征（换 3D 图标）
def f_feat2():
    items = [('chequered_flag', '有穷性', '步骤有限，能在有限时间内结束', '导航只说“一直往前开”，却不说开到哪里停'),
             ('bullseye', '确定性', '每一步含义明确，不会有两种理解', '“加盐适量”：多少算适量？不同的人做法不同'),
             ('check_mark_button', '可行性', '每一步都能实际做到', '“用 10 除以 0”“1 秒内从宿舍跑到图书馆”都做不到'),
             ('inbox_tray', '有零个或多个输入', '从外界获得要处理的数据', '求平均分要先输入成绩；打印“欢迎新生”则不需要输入'),
             ('outbox_tray', '有一个或多个输出', '至少给出一个结果', '算了半天却不显示平均分，这个算法就没有意义')]
    cards = []
    for k, t, d, ex in items:
        cards.append(f'<div class="fc"><div class="fh"><img src="assets/fe/{k}.png"><b>{t}</b></div><div class="fd">{d}</div><div class="fx"><span>反例</span>{ex}</div></div>')
    return '<div class="feat">' + ''.join(cards) + '</div>'


figs['f_feat'] = f_feat2()


# ------------------------------------------------------------------ 新图：跟踪 i 和 sum 的变化
def f_trace():
    W, H = 520, 150
    o = [f'<rect x="0" y="0" width="{W}" height="{H}" rx="8" fill="#F7F9FC"/>']
    cards = [('开始', None, 'sum=0', 'i = 1'), ('第 1 轮', '1<=100 ✓', 'sum=0+1=1', 'i = 2'),
             ('第 2 轮', '2<=100 ✓', 'sum=1+2=3', 'i = 3'), ('第 3 轮', '3<=100 ✓', 'sum=3+3=6', 'i = 4'),
             None, ('第 100 轮', '100<=100 ✓', 'sum=5050', 'i = 101'), ('结束', '101<=100 ✗', '输出 5050', '')]
    x = 14
    for c in cards:
        if c is None:
            o.append(mtext(x + 16, 70, '……', 12, M, 700))
            x += 38
            continue
        t, cond, s, i = c
        w = 72
        end = t == '结束'
        o.append(f'<rect x="{x}" y="22" width="{w}" height="100" rx="6" fill="{C if end else "#fff"}" stroke="{C}" stroke-width="1.1"/>')
        o.append(mtext(x + w / 2, 36, t, 9.4, '#fff' if end else D, 700))
        o.append(f'<line x1="{x + 6}" y1="46" x2="{x + w - 6}" y2="46" stroke="{L if not end else "#fff"}" stroke-width="0.8"/>')
        tc = '#fff' if end else '#1F1F1F'
        if cond:
            o.append(mtext(x + w / 2, 60, cond, 8.4, tc if end else M, 700, mono=True))
        o.append(mtext(x + w / 2, 80, s, 8.6, tc, 700 if end else 400, mono=not end))
        if i:
            o.append(f'<rect x="{x + w / 2 - 22}" y="{92}" width="44" height="18" rx="9" fill="{BG}"/>' + mtext(x + w / 2, 101, i, 8.6, C, 700, mono=True))
        x += w + 6
    o.append(mtext(260, 12, '每一轮：先判断条件，再累加，最后让 i 增加 1', 8.8, D, 700))
    o.append(mtext(260, 138, '判断条件 ✓ 表示成立，✗ 表示不成立；i 的值在每轮最后加 1', 8.2, '#666'))
    return svgwrap(W, H, ''.join(o))


figs['f_trace'] = f_trace()


# ------------------------------------------------------------------ 新图：三种结构一图看懂
def f_threestr():
    W, H = 520, 262
    o = []
    cols = [('wait-in-line', '顺序结构', '一步接一步，每步做一次', '排队打饭：取餐盘→打菜→刷卡'),
            ('road-sign', '选择结构', '遇到岔路口，按条件选一条', '下雨就坐校车，不下雨就骑车'),
            ('jogging', '循环结构', '条件满足就再来一遍', '绕操场跑圈，跑够 3 圈才停')]
    for k, (pic, t, d, ex) in enumerate(cols):
        x0 = 4 + k * 172
        o.append(f'<rect x="{x0}" y="2" width="164" height="256" rx="8" fill="#F7F9FC" stroke="{L}" stroke-width="0.9"/>')
        o.append(ud(pic, x0 + 10, 8, 144, 86))
        o.append(f'<rect x="{x0 + 32}" y="100" width="100" height="22" rx="11" fill="{C}"/>' + mtext(x0 + 82, 111, t, 10.4, '#fff', 700))
        o.append(mtext(x0 + 82, 136, d, 9, D, 700))
        # 迷你流程图
        cx, y = x0 + 82, 150
        if k == 0:
            for j, s in enumerate(['A', 'B', 'C']):
                o.append(f'<rect x="{cx - 22}" y="{y + j * 26}" width="44" height="16" rx="2" fill="{C}"/>' + mtext(cx, y + j * 26 + 8, s, 8.6, '#fff', 700))
                if j < 2:
                    o.append(f'<path d="M{cx},{y + j * 26 + 16} L{cx},{y + j * 26 + 25}" stroke="{M}" stroke-width="1.2" marker-end="url(#ar)"/>')
        elif k == 1:
            o.append(f'<polygon points="{cx},{y} {cx + 26},{y + 13} {cx},{y + 26} {cx - 26},{y + 13}" fill="{BG}" stroke="{C}" stroke-width="1.1"/>' + mtext(cx, y + 13, '条件', 7.8, D, 700))
            o.append(f'<path d="M{cx - 26},{y + 13} L{cx - 46},{y + 13} L{cx - 46},{y + 34}" fill="none" stroke="{M}" stroke-width="1.2" marker-end="url(#ar)"/>')
            o.append(f'<path d="M{cx + 26},{y + 13} L{cx + 46},{y + 13} L{cx + 46},{y + 34}" fill="none" stroke="{M}" stroke-width="1.2" marker-end="url(#ar)"/>')
            o.append(f'<rect x="{cx - 62}" y="{y + 36}" width="32" height="16" rx="2" fill="{C}"/>' + mtext(cx - 46, y + 44, 'A', 8.6, '#fff', 700))
            o.append(f'<rect x="{cx + 30}" y="{y + 36}" width="32" height="16" rx="2" fill="{C}"/>' + mtext(cx + 46, y + 44, 'B', 8.6, '#fff', 700))
            o.append(f'<path d="M{cx - 46},{y + 52} L{cx - 46},{y + 64} L{cx + 46},{y + 64} L{cx + 46},{y + 52}" fill="none" stroke="{M}" stroke-width="1.2"/>')
            o.append(mtext(cx - 38, y + 6, '是', 7.8, D, 700) + mtext(cx + 38, y + 6, '否', 7.8, D, 700))
        else:
            o.append(f'<polygon points="{cx},{y} {cx + 26},{y + 13} {cx},{y + 26} {cx - 26},{y + 13}" fill="{BG}" stroke="{C}" stroke-width="1.1"/>' + mtext(cx, y + 13, '条件', 7.8, D, 700))
            o.append(f'<path d="M{cx},{y + 26} L{cx},{y + 35}" stroke="{M}" stroke-width="1.2" marker-end="url(#ar)"/>')
            o.append(f'<rect x="{cx - 24}" y="{y + 36}" width="48" height="16" rx="2" fill="{C}"/>' + mtext(cx, y + 44, '循环体', 8, '#fff', 700))
            o.append(f'<path d="M{cx - 24},{y + 44} L{cx - 40},{y + 44} L{cx - 40},{y + 13} L{cx - 27},{y + 13}" fill="none" stroke="{M}" stroke-width="1.2" marker-end="url(#ar)"/>')
            o.append(f'<path d="M{cx + 26},{y + 13} L{cx + 44},{y + 13} L{cx + 44},{y + 64}" fill="none" stroke="{M}" stroke-width="1.2" marker-end="url(#ar)"/>')
            o.append(mtext(cx + 8, y + 31, '是', 7.8, D, 700, 'start') + mtext(cx + 36, y + 6, '否', 7.8, D, 700))
        o.append(f'<rect x="{x0 + 8}" y="226" width="148" height="24" rx="5" fill="#fff" stroke="{L}"/>' + mtext(x0 + 82, 238, ex, 8.4, '#333'))
    return svgwrap(W, H, ''.join(o))


figs['f_threestr'] = f_threestr()


# ------------------------------------------------------------------ 新图：结构化程序设计四个要点
def f_sp4():
    W, H = 520, 132
    o = []
    items = [('world_map', '自顶向下', '先看全局：要做哪几件大事', '写作文：先列提纲'),
             ('magnifying_glass_tilted_left', '逐步细化', '一层层拆小，直到每步都会写', '把提纲扩成段落'),
             ('puzzle_piece', '模块化设计', '独立的功能做成模块，分头完成', '分工写不同章节'),
             ('laptop', '结构化编码', '只用三种基本结构写成程序', '逐字逐句写出来')]
    for k, (ic, t, d, an) in enumerate(items):
        x0 = 4 + k * 129
        o.append(f'<rect x="{x0}" y="4" width="122" height="124" rx="8" fill="#F7F9FC" stroke="{L}" stroke-width="0.9"/>')
        o.append(img(ic, x0 + 43, 10, 36))
        o.append(f'<circle cx="{x0 + 16}" cy="18" r="8" fill="{C}"/>' + mtext(x0 + 16, 18, str(k + 1), 9, '#fff', 700))
        o.append(mtext(x0 + 61, 60, t, 10.4, D, 700))
        o.append(mtext(x0 + 61, 82, d if len(d) <= 12 else d[:len(d) // 2 + 1] + '\n' + d[len(d) // 2 + 1:], 8.4, '#333', lh=1.35))
        o.append(f'<rect x="{x0 + 10}" y="102" width="102" height="18" rx="9" fill="{BG}"/>' + mtext(x0 + 61, 111, an, 8.2, C, 700))
        if k < 3:
            o.append(f'<path d="M{x0 + 123},66 L{x0 + 129},66" stroke="{M}" stroke-width="1.4" marker-end="url(#ar)"/>')
    return svgwrap(W, H, ''.join(o))


figs['f_sp4'] = f_sp4()


# ------------------------------------------------------------------ 新图：四格漫画“AI 也会翻车”
def f_comic():
    W, H = 520, 330
    o = []
    PW, PH = 254, 158
    pos = [(4, 4), (262, 4), (4, 168), (262, 168)]
    for k, (x, y) in enumerate(pos, 1):
        o.append(f'<rect x="{x}" y="{y}" width="{PW}" height="{PH}" rx="8" fill="#fff" stroke="{C}" stroke-width="1.3"/>')
        o.append(f'<circle cx="{x + 14}" cy="{y + 14}" r="9" fill="{C}"/>' + mtext(x + 14, y + 14, str(k), 10, '#fff', 700))
    # 第 1 格：提问
    x, y = 4, 4
    o.append(av_he(x + 40, y + 120, 22, 'happy'))
    o.append(bubble(x + 14, y + 30, 124, 52, '小智，帮我写个程序：\n同一个电阻测 5 次，\n求平均值！', (x + 44, y + 96), 8.8))
    o.append(av_zhi(x + 206, y + 118, 22, 'happy'))
    o.append(bubble(x + 150, y + 30, 96, 36, '小意思，\n3 秒搞定！', (x + 200, y + 88), 9.2))
    o.append(img('sparkles', x + 224, y + 72, 22))
    # 第 2 格：编译通过
    x, y = 262, 4
    o.append(f'<rect x="{x + 16}" y="{y + 28}" width="150" height="80" rx="5" fill="#fff" stroke="#8A97AA"/>')
    o.append(f'<rect x="{x + 16}" y="{y + 28}" width="150" height="14" rx="5" fill="#E9EDF3"/><rect x="{x + 16}" y="{y + 36}" width="150" height="6" fill="#E9EDF3"/>')
    o.append(''.join(f'<circle cx="{x + 25 + j * 8}" cy="{y + 35}" r="2.4" fill="#B8C2D1"/>' for j in range(3)))
    o.append(mtext(x + 100, y + 35, 'bad_loop.c', 7.6, '#555', 400, mono=True))
    for j, w in enumerate([90, 120, 70, 104]):
        o.append(f'<rect x="{x + 26}" y="{y + 50 + j * 9}" width="{w}" height="4" rx="2" fill="{L}"/>')
    o.append(f'<rect x="{x + 16}" y="{y + 88}" width="150" height="20" fill="{BG}"/>' + mtext(x + 91, y + 98, '编译：0 个错误，0 个警告', 8.2, C, 700))
    o.append(av_he(x + 210, y + 120, 22, 'happy'))
    o.append(bubble(x + 172, y + 30, 76, 50, '编译通过，\n稳了！', (x + 208, y + 96), 9.2))
    o.append(img('thumbs_up', x + 170, y + 104, 22))
    # 第 3 格：停不下来
    x, y = 4, 168
    o.append(f'<rect x="{x + 16}" y="{y + 26}" width="134" height="118" rx="4" fill="#0C0C0C"/>')
    for j in range(7):
        o.append(f'<text x="{x + 22}" y="{y + 42 + j * 14}" font-size="8.2" fill="#CCCCCC" font-family="{MONO}">{"第1次测量值（Ω）：" if j < 6 else "……"}</text>')
    o.append(av_he(x + 208, y + 122, 22, 'dizzy'))
    o.append(img('sweat_droplets', x + 222, y + 92, 18))
    o.append(bubble(x + 158, y + 26, 90, 62, '怎么一直是\n“第1次”？\n停不下来了！', (x + 202, y + 98), 9))
    # 第 4 格：手动跟踪
    x, y = 262, 168
    o.append(f'<rect x="{x + 16}" y="{y + 28}" width="110" height="76" rx="4" fill="{BG}" stroke="{L}"/>')
    o.append(mtext(x + 71, y + 40, '手动跟踪', 8.6, D, 700))
    for j, s in enumerate(['第1轮  i = 1', '第2轮  i = 1', '第3轮  i = 1']):
        o.append(mtext(x + 71, y + 56 + j * 14, s, 8.2, '#1F1F1F', 400, mono=True))
    o.append(img('magnifying_glass_tilted_left', x + 104, y + 74, 30))
    o.append(av_he(x + 40, y + 130, 20, 'shock'))
    o.append(mtext(x + 96, y + 124, 'i 一直是 1！', 9, '#E4572E', 700, 'start'))
    o.append(av_zhi(x + 214, y + 128, 20, 'think'))
    o.append(bubble(x + 140, y + 26, 108, 66, '我漏写了\ni = i + 1，\n成了死循环。\n谢谢你抓到 bug！', (x + 210, y + 102), 8.6))
    return svgwrap(W, H, ''.join(o))


figs['f_comic'] = f_comic()


# ------------------------------------------------------------------ 新图：农夫过河（挑战题）
def f_river():
    W, H = 520, 150
    o = []
    o.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="8" fill="#F7F9FC"/>')
    o.append(f'<path d="M150,0 C170,40 140,100 165,{H} L355,{H} C330,100 370,40 350,0 Z" fill="{BG}"/>')
    for j in range(5):
        yy = 22 + j * 26
        o.append(f'<path d="M{190 + (j % 2) * 30},{yy} q8,-5 16,0 t16,0" fill="none" stroke="{L}" stroke-width="1.4"/>')
        o.append(f'<path d="M{270 + (j % 2) * 24},{yy + 12} q8,-5 16,0 t16,0" fill="none" stroke="{L}" stroke-width="1.4"/>')
    o.append(img('canoe', 196, 74, 56))
    o.append(mtext(224, 136, '小船：每次只能载农夫和一样东西', 8.4, D, 700))
    for k, (ic, nm) in enumerate([('man_farmer', '农夫'), ('wolf', '狼'), ('ewe', '羊'), ('leafy_green', '白菜')]):
        x = 14 + (k % 2) * 64
        yy = 8 + (k // 2) * 60
        o.append(img(ic, x, yy, 40) + mtext(x + 20, yy + 50, nm, 8.8, '#333', 700))
    o.append(mtext(78, 141, '左岸', 8.4, '#666'))
    o.append(img('chequered_flag', 420, 38, 40))
    o.append(mtext(440, 96, '目标：全部安全到右岸', 9, D, 700))
    o.append(mtext(440, 114, '农夫不在时，狼会吃羊，', 8.2, '#555') + mtext(440, 127, '羊会吃白菜', 8.2, '#555'))
    return svgwrap(W, H, ''.join(o))


figs['f_river'] = f_river()

CSS2 = f'''
.fh img {{ width:34px; height:34px; }}
'''


# ================================================================== 第三稿（按作者 2026-10 批注）新画与重画
def meter(x, y):
    """简笔万用表测电阻：表体、显示屏、旋钮、两根表笔夹住一个色环电阻"""
    o = [f'<rect x="{x}" y="{y}" width="58" height="84" rx="7" fill="#3A3F47"/>',
         f'<rect x="{x + 6}" y="{y + 7}" width="46" height="20" rx="2" fill="#CFE3C8"/>',
         f'<text x="{x + 29}" y="{y + 21.5}" font-size="9.6" font-weight="700" fill="#1F1F1F" text-anchor="middle" font-family="{MONO}">100.2Ω</text>',
         f'<circle cx="{x + 29}" cy="{y + 50}" r="13" fill="#5B616B" stroke="#8A9099"/>',
         f'<path d="M{x + 29},{y + 50} L{x + 29},{y + 39}" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/>',
         f'<circle cx="{x + 17}" cy="{y + 74}" r="3.2" fill="#E04A3F"/><circle cx="{x + 41}" cy="{y + 74}" r="3.2" fill="#222"/>',
         f'<path d="M{x + 17},{y + 76} C{x + 22},{y + 100} {x + 60},{y + 96} {x + 72},{y + 72}" fill="none" stroke="#E04A3F" stroke-width="2"/>',
         f'<path d="M{x + 41},{y + 76} C{x + 50},{y + 106} {x + 110},{y + 98} {x + 110},{y + 72}" fill="none" stroke="#222" stroke-width="2"/>',
         f'<path d="M{x + 66},{y + 70} L{x + 116},{y + 70}" stroke="#9AA0A6" stroke-width="1.6"/>',
         f'<rect x="{x + 78}" y="{y + 63}" width="26" height="14" rx="6" fill="#E8D3A8" stroke="#B89B66" stroke-width="0.8"/>']
    for j, col in enumerate(['#8B5A2B', '#222', '#8B5A2B', '#D4A017']):
        o.append(f'<rect x="{x + 83 + j * 5}" y="{y + 63.5}" width="2.4" height="13" fill="{col}"/>')
    return ''.join(o)


# ------------------------------------------------------------------ 重画：三种基本结构一图看懂（批注 7：上面场景图片，下面结构流程图，做成上下对照的表格）
def f_threestr3():
    W, H = 524, 360
    o = []
    lx, cw, x1 = 4, 156, 50          # 左侧行名列宽 46，三列各宽 156
    rows = [(4, 30), (34, 170), (174, 318), (322, 356)]
    # 表格底色与框线
    o.append(f'<rect x="{lx}" y="4" width="{W - 8}" height="352" rx="6" fill="#fff" stroke="{L}" stroke-width="1"/>')
    o.append(f'<rect x="{lx}" y="4" width="{W - 8}" height="26" rx="6" fill="{C}"/><rect x="{lx}" y="20" width="{W - 8}" height="10" fill="{C}"/>')
    for y in (170, 318):
        o.append(f'<line x1="{lx}" y1="{y + 2}" x2="{W - 4}" y2="{y + 2}" stroke="{L}" stroke-width="1"/>')
    o.append(f'<rect x="{lx}" y="30" width="{x1 - lx}" height="326" fill="{BG}"/>')
    o.append(f'<line x1="{x1}" y1="4" x2="{x1}" y2="356" stroke="{L}"/>')
    for k in range(1, 3):
        o.append(f'<line x1="{x1 + k * cw}" y1="4" x2="{x1 + k * cw}" y2="356" stroke="{L}"/>')
    o.append(mtext((lx + x1) / 2, 102, '生活\n场景', 9.4, D, 700))
    o.append(mtext((lx + x1) / 2, 246, '结构\n流程图', 9.4, D, 700))
    o.append(mtext((lx + x1) / 2, 339, '特点', 9.4, D, 700))
    names = ['顺序结构', '选择结构', '循环结构']
    caps = ['① 上课前依次取出物品，\n打开实训计算机', '② 账号、密码都正确\n才能登录教学平台', '③ 同一个电阻\n反复测量 5 次']
    feats = ['一步接一步，每步只做一次', '按条件二选一，只走一条路', '条件成立就重复，不成立就停']
    for k in range(3):
        cx = x1 + k * cw + cw / 2
        o.append(mtext(cx, 17, names[k], 10.6, '#fff', 700))
        o.append(mtext(cx, 150, caps[k], 8.6, '#333', lh=1.35))
        o.append(mtext(cx, 339, feats[k], 8.6, D, 700))
    # 场景 1：依次取出的物品（带序号）
    cx0 = x1 + cw / 2
    items = ['books', 'pencil', 'notebook', 'cup_with_straw', 'laptop']
    xs = [cx0 - 56, cx0 - 20, cx0 + 16, cx0 - 38, cx0 + 0]
    ys = [44, 44, 44, 90, 90]
    o.append(img('backpack', cx0 + 38, 84, 36))
    for j, (it, x, y) in enumerate(zip(items, xs, ys)):
        o.append(img(it, x, y, 30))
        o.append(f'<circle cx="{x + 4}" cy="{y + 3}" r="6" fill="{C}"/>' + mtext(x + 4, y + 3, str(j + 1), 7.4, '#fff', 700))
    # 场景 2：手机登录 + 对错
    cx1 = x1 + cw + cw / 2
    o.append(ud('mobile-login', cx1 - 62, 38, 92, 86))
    o.append(img('check_mark_button', cx1 + 36, 46, 26) + img('cross_mark_button', cx1 + 36, 88, 26))
    # 场景 3：测电阻 + 重复 5 次
    cx2 = x1 + 2 * cw + cw / 2
    o.append(meter(cx2 - 62, 40))
    o.append(img('repeat_button', cx2 + 38, 50, 28))
    o.append(f'<rect x="{cx2 + 36}" y="86" width="32" height="18" rx="9" fill="{C}"/>' + mtext(cx2 + 52, 95, '×5', 9, '#fff', 700))
    # 下排：一般形式的流程图
    def pbox(x, y, s, w=56, h=20):
        return f'<rect x="{x - w / 2}" y="{y}" width="{w}" height="{h}" rx="2" fill="{C}"/>' + mtext(x, y + h / 2, s, 8.8, '#fff', 700)

    def arr(pts, mk=True):
        d = 'M' + ' L'.join(f'{a},{b}' for a, b in pts)
        return f'<path d="{d}" fill="none" stroke="{M}" stroke-width="1.3"{" marker-end=" + chr(34) + "url(#ar)" + chr(34) if mk else ""}/>'

    def dia(x, y, s, w=64, h=34):
        return f'<polygon points="{x},{y} {x + w / 2},{y + h / 2} {x},{y + h} {x - w / 2},{y + h / 2}" fill="{BG}" stroke="{C}" stroke-width="1.2"/>' + mtext(x, y + h / 2, s, 8.6, D, 700)
    c = cx0
    o.append(arr([(c, 184), (c, 200)]) + pbox(c, 202, 'A') + arr([(c, 222), (c, 238)]) + pbox(c, 240, 'B') + arr([(c, 260), (c, 276)]) + pbox(c, 278, 'C') + arr([(c, 298), (c, 312)]))
    c = cx1
    o.append(arr([(c, 180), (c, 192)]) + dia(c, 194, '条件'))
    o.append(arr([(c - 32, 211), (c - 50, 211), (c - 50, 240)]) + arr([(c + 32, 211), (c + 50, 211), (c + 50, 240)]))
    o.append(pbox(c - 50, 242, 'A', 40) + pbox(c + 50, 242, 'B', 40))
    o.append(arr([(c - 50, 262), (c - 50, 280), (c + 50, 280), (c + 50, 262)], False) + arr([(c, 280), (c, 312)]))
    o.append(mtext(c - 44, 202, '成立', 8, D, 700) + mtext(c + 46, 202, '不成立', 8, D, 700))
    c = cx2
    o.append(arr([(c, 176), (c, 192)]) + dia(c, 194, '条件'))
    o.append(arr([(c, 228), (c, 242)]) + pbox(c, 244, '循环体', 56))
    o.append(arr([(c - 28, 254), (c - 46, 254), (c - 46, 186), (c - 3, 186)]))
    o.append(arr([(c + 32, 211), (c + 54, 211), (c + 54, 312)]))
    o.append(mtext(c + 14, 236, '成立', 8, D, 700, 'start') + mtext(c + 50, 202, '不成立', 8, D, 700))
    return svgwrap(W, H, ''.join(o))


figs['f_threestr'] = f_threestr3()


# ------------------------------------------------------------------ 重画：结构化程序设计四个要点（批注 11、12：类比改为盖宿舍楼，并与电阻检测逐条对应）
def f_sp4b():
    W, H = 524, 268
    o = []
    x1, cw = 62, 115
    items = [('world_map', '自顶向下', '先看全局，\n分出几件大事'),
             ('magnifying_glass_tilted_left', '逐步细化', '大事拆成小事，\n直到每步都会做'),
             ('puzzle_piece', '模块化设计', '独立的功能做成\n模块，分别完成'),
             ('laptop', '结构化编码', '只用三种基本\n结构写成程序')]
    house = ['先定总体方案：\n建几层、每层\n做什么用', '再画施工图：\n细到每个房间、\n每扇门窗', '门窗、楼梯做成\n标准构件，分别\n预制、分别验收', '按图纸施工，\n只用标准构件\n逐层搭建']
    resist = ['分成三件大事：\n准备、逐个检测、\n输出结果', '“逐个检测”拆成\n读入、判断、计数、\n换下一个', '“检测一个电阻”\n可单独编写、测试\n（后续用函数）', '用顺序、选择、\n循环写出\nresist.c']
    o.append(f'<rect x="4" y="4" width="{W - 8}" height="{H - 8}" rx="6" fill="#fff" stroke="{L}"/>')
    o.append(f'<rect x="4" y="4" width="{x1 - 4}" height="{H - 8}" rx="6" fill="{BG}"/>')
    for y in (104, 184):
        o.append(f'<line x1="4" y1="{y}" x2="{W - 4}" y2="{y}" stroke="{L}"/>')
    for k in range(4):
        o.append(f'<line x1="{x1 + k * cw}" y1="4" x2="{x1 + k * cw}" y2="{H - 4}" stroke="{L}"/>')
    o.append(mtext(x1 / 2 + 2, 54, '要点', 9.4, D, 700))
    o.append(mtext(x1 / 2 + 2, 144, '类比：\n盖一栋\n宿舍楼', 9, D, 700))
    o.append(mtext(x1 / 2 + 2, 224, '本例：\n电阻检测', 9, D, 700))
    for k, (ic, t, d) in enumerate(items):
        cx = x1 + k * cw + cw / 2
        o.append(img(ic, cx - 15, 10, 30))
        o.append(f'<circle cx="{x1 + k * cw + 14}" cy="18" r="8" fill="{C}"/>' + mtext(x1 + k * cw + 14, 18, str(k + 1), 9, '#fff', 700))
        o.append(mtext(cx, 52, t, 10.2, D, 700))
        o.append(mtext(cx, 80, d, 8.4, '#333', lh=1.35))
        o.append(mtext(cx, 144, house[k], 8.4, '#333', lh=1.4))
        o.append(f'<rect x="{x1 + k * cw + 5}" y="190" width="{cw - 10}" height="68" rx="4" fill="#F7F9FC"/>')
        o.append(mtext(cx, 224, resist[k], 8.4, C, 700, lh=1.4))
        if k < 3:
            o.append(f'<path d="M{x1 + (k + 1) * cw - 5},52 L{x1 + (k + 1) * cw + 5},52" stroke="{M}" stroke-width="1.4" marker-end="url(#ar)"/>')
    return svgwrap(W, H, ''.join(o))


figs['f_sp4'] = f_sp4b()


# ------------------------------------------------------------------ 新图：求 1+2+3+4+5 的两种写法（批注 3）
def f_sum5():
    W, H = 524, 214
    o = []
    # 左：原始方法
    o.append(f'<rect x="4" y="4" width="212" height="206" rx="8" fill="#F7F9FC" stroke="{L}"/>')
    o.append(f'<rect x="4" y="4" width="212" height="26" rx="8" fill="{M}"/><rect x="4" y="20" width="212" height="10" fill="{M}"/>' + mtext(110, 17, '原始方法：一步写一个算式', 10, '#fff', 700))
    steps = ['步骤 1：1 + 2 = 3', '步骤 2：3 + 3 = 6', '步骤 3：6 + 4 = 10', '步骤 4：10 + 5 = 15']
    for j, s in enumerate(steps):
        o.append(f'<rect x="20" y="{40 + j * 30}" width="140" height="24" rx="3" fill="#fff" stroke="{L}"/>' + mtext(30, 52 + j * 30, s, 9.4, '#1F1F1F', 400, 'start'))
    o.append(img('face_with_spiral_eyes', 168, 92, 40))
    o.append(mtext(110, 172, '加到 1000：要写 999 步！\n加到 1 万：要写 9999 步！', 9, D, 700, lh=1.4))
    # 中间箭头
    o.append(f'<path d="M222,107 L250,107" stroke="{C}" stroke-width="2.4" marker-end="url(#ar)"/>' + mtext(236, 92, '改进', 8.6, C, 700))
    # 右：改进方法
    x0 = 256
    o.append(f'<rect x="{x0}" y="4" width="264" height="206" rx="8" fill="#F7F9FC" stroke="{L}"/>')
    o.append(f'<rect x="{x0}" y="4" width="264" height="26" rx="8" fill="{C}"/><rect x="{x0}" y="20" width="264" height="10" fill="{C}"/>' + mtext(x0 + 132, 17, '改进方法：两个变量 + 反复执行', 10, '#fff', 700))
    # 两个变量“盒子”
    for j, (nm, note) in enumerate([('sum', '存放累加的和'), ('i', '存放要加的数')]):
        bx = x0 + 14 + j * 64
        o.append(f'<rect x="{bx}" y="42" width="52" height="34" rx="4" fill="#fff" stroke="{C}" stroke-width="1.4"/>' + mtext(bx + 26, 59, nm, 12, C, 700, mono=True))
        o.append(mtext(bx + 26, 86, note, 7.8, '#444'))
    o.append(img('light_bulb', x0 + 214, 40, 36))
    rows = [('S1', '0 ⇒ sum', '和先清零'), ('S2', '1 ⇒ i', '从 1 开始'), ('S3', 'sum + i ⇒ sum', '把 i 加进和里'), ('S4', 'i + 1 ⇒ i', '换下一个数'), ('S5', 'i ≤ 5 就回到 S3', '否则执行 S6'), ('S6', '输出 sum', '结束')]
    for j, (a, b, c) in enumerate(rows):
        y = 100 + j * 17
        hl = j in (2, 3, 4)
        o.append(f'<rect x="{x0 + 12}" y="{y - 7}" width="190" height="15" rx="2" fill="{BG if hl else "#fff"}"/>')
        o.append(mtext(x0 + 16, y + 0.5, a, 8.6, C, 700, 'start') + mtext(x0 + 36, y + 0.5, b, 8.6, '#1F1F1F', 400, 'start') + mtext(x0 + 132, y + 0.5, c, 8, '#555', 400, 'start'))
    o.append(f'<path d="M{x0 + 206},{y - 7} C{x0 + 230},{y - 14} {x0 + 230},{134 - 8} {x0 + 206},{134 - 1}" fill="none" stroke="{M}" stroke-width="1.4" marker-end="url(#ar)"/>')
    o.append(mtext(x0 + 236, 150, '重复', 8.4, M, 700, 'start'))
    o.append(mtext(x0 + 132, 202, '加到 1000：只要把 S5 中的 5 改成 1000', 8.8, C, 700))
    return svgwrap(W, H, ''.join(o))


figs['f_sum5'] = f_sum5()
