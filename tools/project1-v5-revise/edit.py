# 在作者批注稿（WPS 另存的 docx）上直接改 XML，保留作者的版式
# 用法：python3 -I edit.py 解包目录 图目录
import copy
import re
import sys
from lxml import etree
from PIL import Image

D, FIG = sys.argv[1], sys.argv[2]
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
      'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
W = '{%s}' % NS['w']
R = '{%s}' % NS['r']
doc = etree.parse(f'{D}/word/document.xml')
body = doc.getroot().find(W + 'body')
rels = etree.parse(f'{D}/word/_rels/document.xml.rels')
log = []


def blocks():
    return [k for k in body if k.tag in (W + 'p', W + 'tbl')]


def text(el):
    return ''.join(t.text or '' for t in el.iter(W + 't'))


def paras(el):
    return [el] if el.tag == W + 'p' else list(el.iter(W + 'p'))


def find(s, nth=None):
    hits = [k for k in blocks() if s in text(k)]
    if nth is None:
        assert len(hits) == 1, (s, len(hits))
        return hits[0]
    return hits[nth]


def replace_range(p, start, end, new):
    """把段落 p 的拼接文字中 [start, end) 换成 new，新文字沿用第一个被触及的 run 的格式"""
    pos = 0
    first = True
    if start == end:  # 纯插入
        for t in p.iter(W + 't'):
            s = t.text or ''
            if pos <= start <= pos + len(s) and s:
                k = start - pos
                t.text = s[:k] + new + s[k:]
                t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
                return
            pos += len(s)
        raise AssertionError(('insert point not found', start, new))
    for t in list(p.iter(W + 't')):
        s = t.text or ''
        a, b = pos, pos + len(s)
        pos = b
        if b <= start or a >= end:
            if a == b == start and first and start == end:
                pass
            continue
        lo, hi = max(start, a) - a, min(end, b) - a
        if first:
            t.text = s[:lo] + new + s[hi:]
            first = False
        else:
            t.text = s[:lo] + s[hi:]
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    assert not first, ('range not found', start, end, new)


def rep(el, old, new, count=0, must=True):
    """在 el 的各段落中把 old 换成 new（可跨 run）；count=0 表示全部"""
    n = 0
    for p in paras(el):
        while True:
            s = text(p)
            i = s.find(old)
            if i < 0:
                break
            replace_range(p, i, i + len(old), new)
            n += 1
            if count and n >= count:
                return n
            if old in new:
                # 防止死循环：只替换一次每段
                break
    if must:
        assert n, ('not found', old)
    return n


def set_text(p, new):
    ts = list(p.iter(W + 't'))
    ts[0].text = new
    ts[0].set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    for t in ts[1:]:
        t.text = ''


# ---------------------------------------------------------------- 图片
def add_image(png, rid_hint):
    import shutil
    ext = png.rsplit('.', 1)[-1].lower()
    name = f'v5_{rid_hint}.{ext}'
    shutil.copy(png, f'{D}/word/media/{name}')
    root = rels.getroot()
    ids = [int(x.get('Id')[3:]) for x in root if x.get('Id', '').startswith('rId')]
    rid = f'rId{max(ids) + 1}'
    el = etree.SubElement(root, '{http://schemas.openxmlformats.org/package/2006/relationships}Relationship')
    el.set('Id', rid)
    el.set('Type', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image')
    el.set('Target', f'media/{name}')
    return rid


def set_drawing(p, png, cx=None, rid_hint='x'):
    """把段落 p 中唯一的图片换成 png，宽度 cx（EMU，默认保持原宽），高度按比例"""
    dr = p.find('.//' + W + 'drawing')
    ext = dr.find('.//{%s}extent' % NS['wp'])
    w0 = int(ext.get('cx'))
    cx = cx or w0
    iw, ih = Image.open(png).size
    cy = int(cx * ih / iw)
    ext.set('cx', str(cx))
    ext.set('cy', str(cy))
    aext = dr.find('.//{%s}xfrm/{%s}ext' % (NS['a'], NS['a']))
    aext.set('cx', str(cx))
    aext.set('cy', str(cy))
    blip = dr.find('.//{%s}blip' % NS['a'])
    blip.set(R + 'embed', add_image(png, rid_hint))


docpr_id = [5000]


def new_image_para(template_p, png, cx, rid_hint):
    p = copy.deepcopy(template_p)
    for tag in ('commentRangeStart', 'commentRangeEnd'):
        for e in p.findall('.//' + W + tag):
            e.getparent().remove(e)
    for r in p.findall(W + 'r'):
        if r.find(W + 'commentReference') is not None:
            p.remove(r)
    set_drawing(p, png, cx, rid_hint)
    for e in p.iter('{%s}docPr' % NS['wp'], '{%s}cNvPr' % NS['pic']):
        docpr_id[0] += 1
        e.set('id', str(docpr_id[0]))
        e.set('name', f'图片 {docpr_id[0]}')
    return p


def move_comment_markers(src_p, dst_first, dst_last):
    """把 src_p 中的批注锚点移到 dst_first 段首、dst_last 段尾"""
    for e in src_p.findall('.//' + W + 'commentRangeStart'):
        e.getparent().remove(e)
        ppr = dst_first.find(W + 'pPr')
        (ppr.addnext(e) if ppr is not None else dst_first.insert(0, e))
    for e in src_p.findall('.//' + W + 'commentRangeEnd'):
        e.getparent().remove(e)
        dst_last.append(e)
    for r in src_p.findall('.//' + W + 'r'):
        if r.find(W + 'commentReference') is not None:
            r.getparent().remove(r)
            dst_last.append(r)


def prevb(el):
    e = el.getprevious()
    while e is not None and e.tag not in (W + 'p', W + 'tbl'):
        e = e.getprevious()
    return e


TEXTW = 5324475  # 版心宽（EMU）

# ================================================================ 0. 清理零宽字符
for t in body.iter(W + 't'):
    if t.text and '‌' in t.text:
        t.text = t.text.replace('‌', '')
log.append('删去零宽字符 U+200C')

# ================================================================ 1. 图、表重新编号（先做，后插入的新图不受影响）
FIGMAP = {6: 7, 7: 8, 8: 10, 9: 11, 10: 12, 11: 13}
for k in blocks():
    for p in paras(k):
        s = text(p)
        ms = list(re.finditer(r'图1-(\d+)', s))
        for m in reversed(ms):
            n = int(m.group(1))
            if n in FIGMAP:
                replace_range(p, m.start(1), m.end(1), str(FIGMAP[n]))
rep(find('例1-1 程序解读'), '表1-4', '表1-3')
rep(find('例1-2 程序解读'), '表1-5', '表1-4')
rep(find('安装和配置中的常见问题'), '表1-6', '表1-5')
log.append('图、表重新编号')

# ================================================================ 2. 三维目标（批注 0）
goals = find('知识目标')
cells = goals.findall('.//' + W + 'tc')
kn = [c for c in cells if text(c).startswith('知识目标')][0]
ab = [c for c in cells if text(c).startswith('能力目标')][0]


def set_list(cell, items):
    ps = cell.findall(W + 'p')
    head, body_ps = ps[0], ps[1:]
    tmpl = [p for p in body_ps if 'printf' not in text(p)][0]
    for i, it in enumerate(items):
        if i < len(body_ps):
            p = body_ps[i]
        else:
            p = copy.deepcopy(tmpl)
            body_ps[-1].addnext(p)
            body_ps.append(p)
        if isinstance(it, tuple):  # (旧文字片段, 新文字) 用于保留 printf 的代码字体
            for o, n in it:
                rep(p, o, n)
        else:
            set_text(p, it)
    for p in body_ps[len(items):]:
        cell.remove(p)


kps_all = kn.findall(W + 'p')
khead, kbody = kps_all[0], kps_all[1:]
pf = [p for p in kbody if 'printf' in text(p)][0]
others = [p for p in kbody if p is not pf]
for o, n in (('掌握 ', '会用 '), ('函数输出各类数据的方法', '函数输出文字和整数')):
    rep(pf, o, n)
newk = ['理解计算机程序、计算机语言和程序设计的含义', '了解 C 语言的特点及其在工科领域中的应用',
        '掌握 C 语言程序的基本结构：预处理指令、主函数和注释', '掌握 C 语言程序的书写规则与规范', None,
        '理解编辑、编译、连接、运行的执行流程']
order = []
for t in newk:
    if t is None:
        order.append(pf)
        continue
    p = others.pop(0) if others else copy.deepcopy(order[0])
    set_text(p, t)
    order.append(p)
for p in kbody:
    kn.remove(p)
for p in order:
    kn.append(p)
kps = [text(p) for p in kn.findall(W + 'p')]
assert kps[5].startswith('会用 printf'), kps
set_list(ab, ['能借助 AI 工具检索、整理学习资料，并核对 AI 的回答',
              '能读懂简单的 C 语言程序并仿写',
              '能安装、配置并使用小熊猫C++',
              '能根据编译器提示修改简单的语法错误',
              '能独立编写并运行个人专属档案程序',
              '能用四要素提问法向 AI 提问'])
log.append('三维目标按两个任务重写')

# ================================================================ 3. 知识导图、图1-3、执行流程图（批注 1、2、5）
kmap_p = [k for k in blocks() if k.find('.//' + W + 'drawing') is not None and k.getnext() is not None and '项目一知识导图' in text(k.getnext())][0]
set_drawing(kmap_p, f'{FIG}/kmap.png', TEXTW, 'kmap')
f13 = [k for k in blocks() if k.find('.//' + W + 'drawing') is not None and '程序和操作说明' in text(k.getnext())][0]
set_drawing(f13, f'{FIG}/fig13.png', TEXTW, 'fig13')
flow_cap = find('C 程序的执行流程')
flow_p = prevb(flow_cap)
set_drawing(flow_p, f'{FIG}/flow.png', 3200400, 'flow')
log.append('知识导图、图1-3、图1-10 换新图')

# ================================================================ 4. 图1-5 改为照片版式（批注 3）
cap15 = find('C 语言在工科领域中的应用')
img15 = prevb(cap15)
assert img15.find('.//' + W + 'drawing') is not None
cards = [('auto', '自动控制', '图为 STM32 开发板通过驱动板控制无刷电机。电机驱动器、智能温控器等设备中的单片机程序常用 C 语言编写，负责采集信号、计算并输出控制量。'),
         ('pv', '光伏发电', '图为开源 MPPT 光伏控制器。光伏控制器、逆变器中的最大功率点跟踪（MPPT）算法运行在 STM32、DSP 等控制芯片上，多用 C 语言实现。'),
         ('robot', '机器人', '图为开源六轴机械臂 Thor。工业机器人、服务机器人的关节电机驱动、传感器数据采集等底层程序，常用 C 语言编写。'),
         ('uav', '无人机', '图为装有开源飞控的四旋翼无人机。开源飞控固件 Betaflight 主要用 C 语言编写，负责读取陀螺仪数据、计算飞行姿态并控制电机转速。'),
         ('cnc', '装备制造', '图为开源数控雕刻机 LowRider。数控系统（如开源的 LinuxCNC）的运动控制核心用 C 语言编写，控制机床各轴按程序精确运动。'),
         ('sys', '系统软件', '图为 Linux 终端。Linux 内核、SQLite 数据库、Python 官方解释器 CPython 主要都用 C 语言编写；最后一行用 gcc 编译运行了一个 C 程序。')]
PHOTO = sys.argv[3] if len(sys.argv) > 3 else None
COLW = 2795
PHW = 1691640  # 约 4.7 cm
tbl = etree.SubElement(body, W + 'tbl')
body.remove(tbl)
tbl_xml = f'''<w:tbl xmlns:w="{NS['w']}"><w:tblPr><w:tblW w:w="{COLW * 3}" w:type="dxa"/><w:jc w:val="center"/>
<w:tblBorders><w:top w:val="nil"/><w:left w:val="nil"/><w:bottom w:val="nil"/><w:right w:val="nil"/><w:insideH w:val="nil"/><w:insideV w:val="nil"/></w:tblBorders>
<w:tblLayout w:type="fixed"/><w:tblCellMar><w:top w:w="40" w:type="dxa"/><w:left w:w="57" w:type="dxa"/><w:bottom w:w="80" w:type="dxa"/><w:right w:w="57" w:type="dxa"/></w:tblCellMar></w:tblPr>
<w:tblGrid><w:gridCol w:w="{COLW}"/><w:gridCol w:w="{COLW}"/><w:gridCol w:w="{COLW}"/></w:tblGrid></w:tbl>'''
tbl = etree.fromstring(tbl_xml)
RPR_T = f'<w:rPr xmlns:w="{NS["w"]}"><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:eastAsia="微软雅黑" w:cs="Arial" w:hint="eastAsia"/><w:b/><w:bCs/><w:color w:val="153A6B"/><w:sz w:val="19"/><w:szCs w:val="19"/></w:rPr>'
RPR_B = f'<w:rPr xmlns:w="{NS["w"]}"><w:rFonts w:hint="eastAsia"/><w:color w:val="333333"/><w:sz w:val="16"/><w:szCs w:val="16"/></w:rPr>'


def mkp(txt, rpr, jc='left', before=0, after=0, line=260):
    p = etree.fromstring(f'<w:p xmlns:w="{NS["w"]}"><w:pPr><w:keepNext/><w:spacing w:before="{before}" w:after="{after}" w:line="{line}" w:lineRule="exact"/><w:ind w:firstLine="0" w:firstLineChars="0"/><w:jc w:val="{jc}"/></w:pPr><w:r>{rpr}<w:t xml:space="preserve">{txt}</w:t></w:r></w:p>')
    return p


for row in range(2):
    tr = etree.SubElement(tbl, W + 'tr')
    etree.SubElement(etree.SubElement(tr, W + 'trPr'), W + 'cantSplit')
    for col in range(3):
        key, title, desc = cards[row * 3 + col]
        tc = etree.SubElement(tr, W + 'tc')
        tcpr = etree.SubElement(tc, W + 'tcPr')
        tw = etree.SubElement(tcpr, W + 'tcW')
        tw.set(W + 'w', str(COLW))
        tw.set(W + 'type', 'dxa')
        ip = new_image_para(img15, f'{PHOTO}/p_{key}.jpg' if PHOTO else f'{FIG}/ph_{key}.png', PHW, 'ph_' + key)
        ppr = ip.find(W + 'pPr')
        ppr.find(W + 'spacing').set(W + 'before', '0')
        tc.append(ip)
        tc.append(mkp(title, RPR_T, 'center', 40, 0, 280))
        tc.append(mkp(desc, RPR_B, 'left', 0, 0, 240))
cap15.addprevious(tbl)
move_comment_markers(img15, cap15, cap15)
if PHOTO:
    src_note = copy.deepcopy(find('说明：图1-1 是情境示意图'))
    set_text(src_note, '图片来源：自动控制，SimpleFOC 项目文档（MIT 许可）；光伏发电，Libre Solar 项目 MPPT 2420 HC（CERN-OHL-W-2.0）；机器人，Thor 开源机械臂项目（CC BY-SA 4.0）；无人机，PX4 自动驾驶仪文档（CC BY 4.0）；装备制造，V1 Engineering LowRider 文档（CC BY-SA 4.0）；系统软件，编者截图。部分图片经裁剪。')
    cap15.addnext(src_note)
body.remove(img15)
log.append('图1-5 改为 6 张照片位的表格')

# 新图1-6：趣味示例
lead_tmpl = find('C 语言的应用范围非常广泛')
lead = copy.deepcopy(lead_tmpl)
set_text(lead, 'C 语言不只用在工厂设备里，同学们喜欢的小游戏、点餐小程序也能用它写出来。图1-6 是用 C 语言编写的两个控制台小程序，右侧说明了它们是怎样做出来的。源程序在本书资源包中，学完后面项目中的输入、选择、循环和数组后，你也能读懂、改写它们。')
cap16 = copy.deepcopy(cap15)
for e in cap16.findall('.//' + W + 'commentRangeStart') + cap16.findall('.//' + W + 'commentRangeEnd'):
    e.getparent().remove(e)
for r in cap16.findall(W + 'r'):
    if r.find(W + 'commentReference') is not None:
        cap16.remove(r)
s = text(cap16)
m = re.search(r'图1-5', s)
replace_range(cap16, m.start(), m.end(), '图1-6')
s = text(cap16)
i = s.find('C 语言在工科领域中的应用')
replace_range(cap16, i, len(s), '用 C 语言编写的点餐小程序和贪吃蛇小游戏')
fun_p = new_image_para(f13, f'{FIG}/fun.png', TEXTW, 'fun')
(src_note if PHOTO else cap15).addnext(lead)
lead.addnext(fun_p)
fun_p.addnext(cap16)
log.append('新增图1-6 趣味示例')

# ================================================================ 5. 预处理示意图（批注 4）
pre_par = find('①预处理指令')
rep(pre_par, '才得到目标程序。', '才得到目标程序（见图1-9）。本书资源包中的动画“预处理在做什么”演示了这一过程。')
pre_img = new_image_para(f13, f'{FIG}/pre.png', TEXTW, 'pre')
pre_cap = copy.deepcopy(cap16)
s = text(pre_cap)
replace_range(pre_cap, 0, len(s), '图1-9  预处理示意：#include 把头文件的内容“抄”进源程序')
# 题注第一个 run 是加粗的“图1-”，保持“图1-9”加粗、其余正常：重新拆分
ts = list(pre_cap.iter(W + 't'))
runs = [t.getparent() for t in ts]
r0 = runs[0]
r_rest = copy.deepcopy(runs[-1] if len(runs) > 1 else r0)
for r in runs[1:]:
    pre_cap.remove(r)
r0.find(W + 't').text = '图1-9'
r_rest.find(W + 't').text = '  预处理示意：#include 把头文件的内容“抄”进源程序'
r0.addnext(r_rest)
pre_par.addnext(pre_img)
pre_img.addnext(pre_cap)
log.append('新增图1-9 预处理示意')

# 图1-6 题注同样处理加粗
ts = list(cap16.iter(W + 't'))
runs = [t.getparent() for t in ts if (t.text or '')]
r0, rl = runs[0], runs[-1]
for r in runs[1:]:
    cap16.remove(r)
r0.find(W + 't').text = '图1-6'
rl = copy.deepcopy(rl)
rl.find(W + 't').text = '  用 C 语言编写的点餐小程序和贪吃蛇小游戏'
r0.addnext(rl)

# ================================================================ 6. 项目小结（批注 6）
summ = find('主要内容归纳如表1-14')
set_text(summ, '本项目以校园 AI 迎新系统中的新生专属档案为线索，分两个任务展开。任务一“认识C语言程序设计”借助 AI 检索和追问，弄清了计算机程序、计算机语言和程序设计的含义，了解了 C 语言的特点、为什么要学以及它在工科领域的应用，并整理出自己的学习思路。任务二“第一个C语言程序”通过例1-1、例1-2 归纳出 C 程序的基本结构（预处理指令、main 主函数、注释），理解了编辑、编译、连接、运行的执行流程，学会了在小熊猫C++ 中编写、运行程序，掌握了英文分号、英文标点、区分大小写、括号成对、只有一个 main 函数等书写规则和规范，最后用 printf 输出了个人专属档案。AI 升华中，又用四要素提问法请 AI 补全档案，并用运行结果检验了 AI 的回答。')
chk = find('能用 printf 输出文字')
rep(chk, '能用 printf 输出文字', '能用 printf 输出文字和整数')
last_chk = find('能在小熊猫C++ 中独立完成')
nc = copy.deepcopy(last_chk)
set_text(nc, '能用四要素提问法向 AI 提问，并用运行结果检验 AI 的回答')
last_chk.addnext(nc)
log.append('项目小结改为一段总结；自查清单补两处')

# ================================================================ 7. 标题层级、病句、遗留问题
for s in ('4. 小熊猫', '5. 规则与规范'):
    p = find(s)
    ppr = p.find(W + 'pPr')
    ppr.find(W + 'pStyle').set(W + 'val', '5')
    ppr.find(W + 'spacing').set(W + 'before', '209')
rep(find('这个过程将在任务三中详细介绍'), '这个过程将在任务三中详细介绍', '这个过程将在任务二的“C语言程序的执行流程”中详细介绍')
rep(find('编辑好的指令代码'), '编辑好的指令代码', '编写好的指令')
rep(find('欢迎语'), '欢迎使用校园AI迎新系统！。', '欢迎使用校园AI迎新系统！')
rep(find('不论main主函数在整个程序中的位置如何'), '不论main主函数在整个程序中的位置如何（不论main函数放在程序的最前边，还是最后边）', '不论main主函数放在程序的什么位置（最前边、中间还是最后边）')
rep(find('PLC 外围控制器'), 'PLC 外围控制器', 'PLC（可编程控制器）')
rep(find('它由国内开发者'), '它由国内开发者', '它是由国内开发者')
rep(find('第7页的表1-2'), '翻到本书第7页的表1-2', '翻到本任务后面的表1-2')
rep(find('第6页的四条搜索话术'), '依次使用第6页的四条搜索话术提问', '依次使用前面“AI 助学 · 搜索话术”中的四条话术提问')
p = find('（1）编辑')
rep(p, 'text.c', 'f.c')
p = find('再由编译系统')
rep(p, 'text.o或text.obj，默认存放在用户当前目录下。', 'f.o 或 f.obj。用小熊猫C++ 编译单个源文件时，编译和连接是一次完成的，目标程序只是临时文件，所以文件夹中通常只看到 .c 和 .exe 两个文件。')
rep(find('（3）连接'), 'text.exe', 'f.exe')
log.append('标题层级、病句、遗留的“任务三”、页码引用、目标程序存放位置')

# ================================================================ 8. 例1-2 按本书书写规范加空格，并对齐注释
ex12 = [k for k in blocks() if k.tag == W + 'tbl' and 'int a,b,sum' in text(k) and 'printf' in text(k) and '今日合计' in text(k) and '// ' in text(k)][0]
for o, n in (('int a,b,sum;', 'int a, b, sum;'), ('a=1268;', 'a = 1268;'), ('b=532;', 'b = 532;'), ('sum=a+b;', 'sum = a + b;'),
             ('本行是程序的声明部分，定义a,b,sum为整型变量', '定义整型变量 a、b、sum'),
             ('计算合计报到人数a+b，并把运算结果存储在变量sum中', '求和，结果存入变量 sum'),
             ('输出今日合计报到人数，%d处对应sum的值', '%d 处输出 sum 的值'),
             ('预处理指令：包含标准输入输出头文件', '预处理：包含头文件 stdio.h')):
    rep(ex12, o, n)


def dw(s):
    return sum(2 if ord(c) > 0x2E80 else 1 for c in s)


def align(tbl_el, col):
    for p in paras(tbl_el):
        s = text(p)
        i = s.find('// ')
        if i < 0:
            continue
        left = s[:i].rstrip()
        j = len(left)
        replace_range(p, j, i, ' ' * max(1, col - dw(left)))


align(ex12, 38)
ex11 = [k for k in blocks() if k.tag == W + 'tbl' and '欢迎使用校园AI迎新系统' in text(k) and '// ' in text(k)][0]
rep(ex11, '预处理指令：包含标准输入输出头文件', '预处理：包含头文件 stdio.h')
align(ex11, 38)
t14 = find('例1-2 程序解读').getnext()
for o, n in (('int a,b,sum;', 'int a, b, sum;'), ('a=1268;', 'a = 1268;'), ('b=532;', 'b = 532;'), ('sum=a+b;', 'sum = a + b;'),
             ('定义a,b,sum为整型变量', '定义 a、b、sum 为整型变量')):
    rep(t14, o, n, must=False)
log.append('例1-2 代码加空格')

# ================================================================ 9. 规范示例不用 %s；规则⑤示例
spec = find('规范：一行')
rep(spec, 'printf("姓名：%s\\n","林小禾");', 'printf("姓名：林小禾\\n");')
rep(spec, 'printf("姓名：%s\\n", "林小禾");', 'printf("姓名：林小禾\\n");')
rules = find('必须遵守的规则').getnext()
rep(rules, '（main 写成了 mian）', '（main 写成了 mian；或者写了两个 main 函数）')
log.append('规范示例去掉 %s；规则⑤补“两个 main”的示例')

# ================================================================ 10. slip.c 行号、图号
slip = find('slip.c（待补充）')
for p in paras(slip):
    s = text(p)
    m = re.match(r'(\s*)(1[1-8])(\s)', s)
    if m:
        n = int(m.group(2)) - 5
        replace_range(p, m.start(2), m.end(2), f'{n:2d}' if len(m.group(1)) == 0 else str(n))
rep(find('如下图所示'), '如下图所示', '如图1-12所示')
log.append('slip.c 行号连续；“如下图所示”改为图号')

# ================================================================ 11. profile8.c 与 profile.c 一致
p8 = find('profile8.c')
lines = {7: ('学号：202605022001', '性别：女'), 8: ('性别：女', '年龄：18'), 9: ('专业：智能控制技术', '学号：202605022001'),
         10: ('年龄：18 岁', '专业：智能控制技术'), 13: ('状态： 已报到', '状态：已报到')}
for p in paras(p8):
    s = text(p)
    m = re.match(r'\s*(\d+)\s', s)
    if m and int(m.group(1)) in lines:
        o, n = lines[int(m.group(1))]
        rep(p, o, n)
log.append('profile8.c 与 profile.c 的顺序和写法一致')

# ================================================================ 12. 实训巩固第 8 题
rep(find('下面的程序有 3 处错误'), '下面的程序有 3 处错误，', '下面的程序有 3 处错误（其中 1 处编译器只给出[警告]），')

# ================================================================ 13. 用空段落凑分页的地方
def empty(k):
    return k.tag == W + 'p' and not text(k).strip() and k.find('.//' + W + 'drawing') is None and k.find('.//' + W + 'sectPr') is None \
        and k.find('.//' + W + 'bookmarkStart') is None


ks = blocks()
i = 0
removed = 0
while i < len(ks):
    j = i
    while j < len(ks) and empty(ks[j]):
        j += 1
    if j - i >= 2:
        for k in ks[i:j]:
            body.remove(k)
            removed += 1
    i = max(j, i + 1)
t2 = [k for k in blocks() if text(k).strip().startswith('任务二') and '第一个C语言程序' in text(k)][0]
ppr = t2.find(W + 'pPr')
pb = ppr.find(W + 'pageBreakBefore')
if pb is None:
    pb = etree.SubElement(ppr, W + 'pageBreakBefore')
    ppr.remove(pb)
    ppr.find(W + 'pStyle').addnext(pb)
pb.set(W + 'val', '1')
log.append(f'删去连续空段落 {removed} 个，任务二改为段前分页')

ctp = f'{D}/[Content_Types].xml'
ct = open(ctp, encoding='utf-8').read()
if 'Extension="jpg"' not in ct:
    ct = ct.replace('<Default Extension="png"', '<Default Extension="jpg" ContentType="image/jpeg"/><Default Extension="png"', 1)
    open(ctp, 'w', encoding='utf-8').write(ct)
doc.write(f'{D}/word/document.xml', xml_declaration=True, encoding='UTF-8', standalone=True)
rels.write(f'{D}/word/_rels/document.xml.rels', xml_declaration=True, encoding='UTF-8', standalone=True)
print('\n'.join(log))
