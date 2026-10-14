import html
frame = open('frame.txt').read().rstrip('\n')
cant = """====== 一食堂点餐 ======
1. 红烧肉盖饭  15.0 元
2. 番茄炒蛋饭  10.0 元
3. 牛肉拉面    13.0 元
4. 绿豆汤       2.5 元
0. 结账
请输入菜品编号：<span class="kin">1</span>
份数：<span class="kin">1</span>
已点 红烧肉盖饭 × 1，当前合计 15.0 元
请输入菜品编号：<span class="kin">4</span>
份数：<span class="kin">2</span>
已点 绿豆汤 × 2，当前合计 20.0 元
请输入菜品编号：<span class="kin">0</span>
合计：20.0 元，请扫码支付，祝用餐愉快！"""
ico = '<svg class="cw-ico" viewBox="0 0 16 16"><rect x="1" y="2" width="14" height="12" rx="1" fill="#1a1a1a"/><path d="M3.5 6l2.5 2-2.5 2" stroke="#fff" stroke-width="1.2" fill="none"/><path d="M7 10.5h4" stroke="#fff" stroke-width="1.2"/></svg>'
btn = '<svg class="cw-btn" viewBox="0 0 72 12"><path d="M4 6.5h9" stroke="#333" stroke-width="0.9"/><rect x="30" y="2" width="8" height="8" fill="none" stroke="#333" stroke-width="0.9"/><path d="M56 2l8 8M64 2l-8 8" stroke="#333" stroke-width="0.9"/></svg>'


def win(title, body):
    return ('<div class="conwin full"><div class="cw-bar">' + ico + '<span class="cw-t">' + title +
            '</span>' + btn + '</div><pre class="cw-body">' + body + '</pre></div>')


MK = '''<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#4A75AE"/></marker></defs>'''


def kmap():
    tasks = [("任务一 认识C语言程序设计", ["计算机程序、计算机语言与程序设计", "为什么学 C 语言", "C 语言的应用领域", "借助 AI 工具学习，整理学习思路"]),
             ("任务二 第一个C语言程序", ["典型示例：例1-1、例1-2", "基本结构：预处理指令、主函数、注释", "执行流程：编辑→编译→连接→运行", "小熊猫C++ 开发环境", "规则与规范", "任务实施：编写个人专属档案"]),
             ("AI升华 补全档案", ["四要素提问法", "用运行结果检验 AI 的回答"])]
    y = 14
    centers = []
    lines, texts, dots = [], [], []
    for name, leaves in tasks:
        ys = [y + 20 * i for i in range(len(leaves))]
        c = (ys[0] + ys[-1]) / 2
        centers.append(c)
        for ly, t in zip(ys, leaves):
            lines.append(f'<path d="M300 {c} C312 {c} 312 {ly} 326 {ly}"/>')
            texts.append(f'<text x="331" y="{ly + 3.4}">{t}</text>')
            dots.append(f'<circle cx="326" cy="{ly}" r="1.8"/>')
        y = ys[-1] + 30
    H = y - 14
    mid = (centers[0] + centers[-1]) / 2
    for c in centers:
        lines.append(f'<path d="M128 {mid} C150 {mid} 150 {c} 172 {c}"/>')
    boxes = []
    for (name, _), c in zip(tasks, centers):
        boxes.append(f'<rect x="172" y="{c - 15}" width="128" height="30" rx="3" fill="#E8EEF7" stroke="#1D4F91" stroke-width="0.8"/><text x="236" y="{c + 4}" fill="#153A6B">{name}</text>')
    return f'''<svg viewBox="0 0 520 {H}" width="100%" font-family="BSans">
<g stroke="#9DB3D3" stroke-width="1.3" fill="none">{''.join(lines)}</g>
<rect x="8" y="{mid - 25}" width="120" height="50" rx="4" fill="#1D4F91"/>
<text x="68" y="{mid - 4}" fill="#fff" font-size="13" font-weight="700" text-anchor="middle">项目一</text>
<text x="68" y="{mid + 14}" fill="#fff" font-size="10.5" text-anchor="middle">搭建个人专属档案</text>
<g font-size="10.5" font-weight="700" text-anchor="middle">{''.join(boxes)}</g>
<g font-size="9.6" fill="#1F1F1F">{''.join(texts)}</g>
<g fill="#1D4F91">{''.join(dots)}</g></svg>'''


fig13 = '''<div class="cmp2">
<div><div class="cmp-h">操作说明：手机连校园网</div><ol><li>进入 WLAN 页面</li><li>选中 WiFi 名称</li><li>输入密码</li><li>点击登录</li><li>提示登录成功</li></ol></div>
<div class="cmp-mid">好比</div>
<div><div class="cmp-h">程序：新生专属档案</div><ol><li>输出“校园 AI 迎新系统”</li><li>输出姓名、学号</li><li>输出性别、专业</li><li>输出年龄、身高</li><li>输出籍贯、状态，结束</li></ol></div></div>'''


def steps(title, items, foot):
    li = ''.join(f'<li><span class="n">{i + 1}</span><div>{t}</div></li>' for i, t in enumerate(items))
    return f'<div class="fx-s"><div class="fx-h">{title}</div><ol>{li}</ol><div class="fx-f">{foot}</div></div>'


T1 = 'D:\\CStudy\\demo\\canteen.exe'
T2 = 'D:\\CStudy\\demo\\snake.exe'
fun = ('<div class="fx"><div class="fx-row"><div class="fx-c">' + win(T1, cant) + '</div>' +
       steps("点餐小程序：怎么做出来的",
             ["用 <b>printf</b> 输出菜单——本项目就能学会",
              "用 <b>scanf</b> 读入菜品编号和份数，用算术运算累计金额",
              "用<b>数组</b>存放菜名和价格，用<b>循环</b>反复点餐，用<b>选择</b>判断编号是否有效"],
             "手机点餐 App 的界面用其他技术制作，但“点菜—算钱—结账”的逻辑和这个程序一样。") +
       '</div><div class="fx-row"><div class="fx-c">' + win(T2, html.escape(frame)) + '</div>' +
       steps("贪吃蛇小游戏：怎么做出来的",
             ["把场地看成坐标格子，用字符画出围墙 #、蛇头 @、蛇身 o 和食物 *",
              "用<b>数组</b>记下蛇身每一节的坐标，每走一步，每一节都移到前一节位置",
              "用<b>循环</b>让游戏一直进行，用<b>选择</b>判断按键、撞墙和吃到食物"],
             "按 W/A/S/D 控制方向。程序用到 Windows 专用的 conio.h、windows.h，只能在 Windows 下运行。") +
       '</div></div>')

pre = '''<svg viewBox="0 0 524 200" width="100%" font-family="BSans">''' + MK + '''
<g font-size="9.4" font-weight="700" fill="#153A6B" text-anchor="middle"><text x="80" y="13">① 预处理前：hello.c</text><text x="262" y="13">② 预处理后：完整的源程序</text><text x="444" y="13">③ 编译后：目标程序 hello.o</text></g>
<rect x="4" y="20" width="152" height="150" fill="#F5F7FA" stroke="#C5D3E7"/>
<rect x="8" y="27" width="112" height="15" fill="#FFE9A8"/>
<g font-family="BMono" font-size="8.2" fill="#1F1F1F"><text x="11" y="38">#include &lt;stdio.h&gt;</text><text x="11" y="66">int main()</text><text x="11" y="80">{</text><text x="19" y="94">printf("hi\\n");</text><text x="19" y="108">return 0;</text><text x="11" y="122">}</text></g>
<rect x="186" y="20" width="152" height="150" fill="#F5F7FA" stroke="#C5D3E7"/>
<rect x="190" y="25" width="144" height="58" fill="#FFF4D1" stroke="#E5B94A" stroke-dasharray="3 2"/>
<g font-family="BMono" font-size="7.4" fill="#5A4A1A"><text x="194" y="37">/* stdio.h 的内容（节选）*/</text><text x="194" y="50">int printf(const char *,</text><text x="216" y="61">...);</text><text x="194" y="74">……（共几百行）</text></g>
<g font-family="BMono" font-size="8.2" fill="#1F1F1F"><text x="193" y="100">int main()</text><text x="193" y="113">{</text><text x="201" y="126">printf("hi\\n");</text><text x="201" y="139">return 0;</text><text x="193" y="152">}</text></g>
<rect x="368" y="20" width="152" height="150" fill="#F5F7FA" stroke="#C5D3E7"/>
<g font-family="BMono" font-size="8.2" fill="#4A75AE"><text x="378" y="40">01001000 10001011</text><text x="378" y="56">00000101 11101000</text><text x="378" y="72">00110000 00000000</text><text x="378" y="88">11001001 11000011</text><text x="378" y="104">……</text></g>
<text x="444" y="132" font-size="8.4" fill="#4D4D4D" text-anchor="middle">二进制形式的目标代码，</text><text x="444" y="145" font-size="8.4" fill="#4D4D4D" text-anchor="middle">还要连接后才能运行</text>
<g stroke="#4A75AE" stroke-width="1.6"><path d="M158 95 H183" marker-end="url(#arr)"/><path d="M340 95 H365" marker-end="url(#arr)"/></g>
<g font-size="8.4" fill="#153A6B" text-anchor="middle" font-weight="700"><text x="171" y="86">预处理</text><text x="353" y="86">编译</text></g>
<text x="262" y="190" font-size="8.6" fill="#4D4D4D" text-anchor="middle">#include 这一行被换成 stdio.h 的内容，其中有 printf 的声明，编译器因此“认识”printf</text>
</svg>'''


def rect(x, y, w, h, t):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="#1D4F91"/><text x="{x + w / 2}" y="{y + h / 2 + 4}" fill="#fff" font-size="11" font-weight="700" text-anchor="middle">{t}</text>'


def term(cx, y, t):
    return f'<rect x="{cx - 36}" y="{y}" width="72" height="24" rx="12" fill="#fff" stroke="#1D4F91" stroke-width="1.2"/><text x="{cx}" y="{y + 16}" fill="#153A6B" font-size="10.5" font-weight="700" text-anchor="middle">{t}</text>'


def dia(cx, cy, t):
    return f'<path d="M{cx} {cy - 22} L{cx + 52} {cy} L{cx} {cy + 22} L{cx - 52} {cy} Z" fill="#E8EEF7" stroke="#1D4F91" stroke-width="1.1"/><text x="{cx}" y="{cy + 4}" fill="#153A6B" font-size="10" font-weight="700" text-anchor="middle">{t}</text>'


def note(x, y, a, b):
    return f'<text x="{x}" y="{y}" font-size="8.6" fill="#4D4D4D">{a}</text><text x="{x}" y="{y + 12}" font-family="BMono" font-size="8.6" fill="#153A6B">{b}</text>'


cx = 150
flow = f'''<svg viewBox="0 0 330 434" width="100%" font-family="BSans">{MK}
{term(cx, 6, "开始")}
{rect(cx - 46, 48, 92, 28, "编辑")}{note(214, 58, "源程序", "f.c")}
{rect(cx - 46, 100, 92, 28, "编译")}{note(214, 110, "目标程序", "f.obj")}
{dia(cx, 172, "有错？")}
{rect(cx - 46, 222, 92, 28, "连接")}
<rect x="214" y="222" width="104" height="28" fill="#fff" stroke="#858585" stroke-dasharray="3 2"/><text x="266" y="233" font-size="8.4" fill="#4D4D4D" text-anchor="middle">库函数和</text><text x="266" y="245" font-size="8.4" fill="#4D4D4D" text-anchor="middle">其他目标程序</text>
{rect(cx - 46, 274, 92, 28, "执行")}{note(214, 284, "可执行目标程序", "f.exe")}
{dia(cx, 346, "结果正确？")}
{term(cx, 404, "结束")}
<g stroke="#4A75AE" stroke-width="1.4" fill="none">
<path d="M{cx} 30 V46" marker-end="url(#arr)"/><path d="M{cx} 76 V98" marker-end="url(#arr)"/><path d="M{cx} 128 V148" marker-end="url(#arr)"/>
<path d="M{cx} 194 V220" marker-end="url(#arr)"/><path d="M{cx} 250 V272" marker-end="url(#arr)"/><path d="M{cx} 302 V322" marker-end="url(#arr)"/><path d="M{cx} 368 V402" marker-end="url(#arr)"/>
<path d="M214 236 H198" marker-end="url(#arr)"/>
<path d="M{cx - 52} 172 H58 V56 H{cx - 48}" marker-end="url(#arr)"/>
<path d="M{cx - 52} 346 H34 V68 H{cx - 48}" marker-end="url(#arr)"/>
</g>
<g font-size="9" fill="#153A6B" font-weight="700"><text x="80" y="167">有</text><text x="{cx + 6}" y="212">无</text><text x="50" y="341">不正确</text><text x="{cx + 6}" y="390">正确</text></g>
</svg>'''

CSS = '''html,body{margin:0;background:#fff} body{width:148mm;padding:0;font-family:BSerif;font-size:10.8pt}
.f{background:#fff;padding:3pt 2pt;margin:0 0 20pt}
.fx{display:flex;flex-direction:column;gap:8pt}
.fx-row{display:grid;grid-template-columns:57% 1fr;gap:9pt;align-items:stretch}
.fx .cw-body{font-size:8.2pt;line-height:1.32}
.fx .conwin{margin:0;flex:1;display:flex;flex-direction:column}
.fx-c{display:flex;flex-direction:column}
.fx .cw-body{flex:1;margin:0}
.fx-s{text-align:left;border:0.6pt solid var(--c-lt);background:var(--c-bg2);padding:5pt 8pt 6pt;font-size:8.8pt;line-height:1.55;display:flex;flex-direction:column}
.fx-h{font-family:BSans;font-weight:700;color:var(--c-dk);border-bottom:0.5pt solid var(--c-lt);padding-bottom:2.5pt;margin-bottom:4pt}
.fx-s ol{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:4pt}
.fx-s li{display:flex;gap:5pt}
.fx-s .n{flex:none;width:12pt;height:12pt;border-radius:50%;background:var(--c);color:#fff;font:700 7.6pt/12pt BSans;text-align:center;margin-top:1.5pt}
.fx-s b{font-family:BSans;color:var(--c-dk)}
.fx-f{margin-top:auto;padding-top:5pt;font-size:8pt;color:#555;border-top:0.5pt dashed var(--c-lt)}
#flow{width:92mm}
'''

page = ('<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="../../book4/style.css"><style>' + CSS +
        '</style></head><body>' +
        '<div class="f" id="kmap">' + kmap() + '</div>' +
        '<div class="f" id="fig13">' + fig13 + '</div>' +
        '<div class="f" id="fun">' + fun + '</div>' +
        '<div class="f" id="pre">' + pre + '</div>' +
        '<div class="f" id="flow">' + flow + '</div></body></html>')
open('figs.html', 'w').write(page)
