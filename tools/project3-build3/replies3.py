# 项目三第三稿带批注回复版：放回作者冯丽娜的 16 条原批注（原文、原时间），逐条加“Claude（项目组）”的处理回复
# 用法：python3 replies3.py 解包目录（已由 content2.py 放好锚点） 作者稿comments.xml
import copy
import re
import sys
from pathlib import Path
from lxml import etree

sys.path.insert(0, '/mnt/skills/public/docx/scripts')
from comment import add_comment  # noqa: E402

D, ORIG = sys.argv[1], sys.argv[2]
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
REPLIES = {
    0: '已按定稿内容调整：知识目标 5 条、能力目标 6 条、素养目标 4 条。新增“理解算法的概念”和“能用变量和判断、重复的思路写出典型算法的步骤”，与新写的“2. 算法的概念”“3. 算法举例”对应；每条都能在正文中找到对应内容和练习。',
    1: '已重画知识导图（图3-2）：任务一的节点改为“程序 = 算法 + 数据结构、算法的概念、算法举例（累加求和、判断闰年、辗转相除）、算法的五个特征、算法的表示、任务实施”，与正文小标题一一对应；AI 升华的名称与正文一致。',
    2: '已补写“2. 算法的概念”：广义定义（解决问题的方法和步骤）→ 计算机算法 → 数值运算算法与非数值运算算法两类（各举 3 例）→ 算法与程序的关系（算法与语言无关，程序是用语言写出的算法）。保留您原有的“算法并不神秘……”一段作结。',
    3: '已按您的思路写成“原始方法 → 改进方法”：先用步骤 1～4 逐步求 1+2+3+4+5，指出加到 1000、1 万要写 999、9999 步；再引入 sum、i 两个变量写出 S1～S6（反复执行 S3～S5，判断 i 是否超过 5）。配图3-3 对比两种方法，表3-1 跟踪每一轮变量的变化，最后点明“加到 1000 只改 S5 中的 5”，这就是编程的思路，并说明任务二会把它写成 while 循环。下面的自然语言表示法也用同一套 S1、S2 写法。',
    4: '已重写两个案例：（2）判断闰年，典型的选择问题，每一步先判断再选路，表3-2 用 2000、1900、2024、2026 四个年份验证，并提醒判断次序不能乱；（3）辗转相除法求最大公约数，典型的循环问题，情境是 84 个电阻、60 个电容最多分几组，表3-3 跟踪三轮，说明余数越来越小所以一定能结束。两例都用 S1、S2……和变量 ⇒ 的写法分析。对应的 C 程序 leap.c、gcd.c 放在配套资源中（已实测），正文不出现代码。',
    5: '已改为表格（表3-4）：五个特征各一行，列出“含义”和“在本节例子中的体现”，例子取自前面的求和、闰年、辗转相除三个算法，不再用图；表后保留一句话强调有穷性与死循环。',
    6: '已改：连接点画成空心圆圈，去掉了字母 A；说明改为“把画在不同位置的流程线连接起来”。',
    7: '已按您的建议重画成上下对照的表格（图3-8）：上面一行是林小禾的三个场景图片（依次取出物品、手机登录对错、万用表测电阻 ×5），下面一行是对应结构的流程图，最后一行用一句话写各自特点。三个场景与任务描述的①②③一致。',
    8: '已按调整后的任务描述重写：依次从书包中取出课本、签字笔、笔记本、水杯，摆放在课桌上，再打开实训计算机等候上课。原来“背书包去教室”“取出物品一定在到达教室之后”的说法随之删去；改为说明生活中先取哪样可以灵活，但写成算法后计算机严格按写好的顺序执行。',
    9: '图3-9（b）已按任务内容重画：开始 → 取出课本 → 取出签字笔 → 取出笔记本 → 取出水杯 → 摆放在课桌上 → 打开实训计算机 → 等候上课 → 结束；标题改为“上课前的准备”。',
    10: '已互换：（a）单分支、（b）双分支，正文中单分支、双分支两段的顺序和图号引用同步调整。',
    11: '图3-12 已重画，见下一条的回复。',
    12: '同意，写作文的比喻与四句话对应不严。已改为“盖一栋宿舍楼”：总体方案（自顶向下）→ 施工图细到每个房间（逐步细化）→ 门窗、楼梯做成标准构件分别预制验收（模块化设计）→ 按图纸用标准构件搭建（结构化编码），四句一一对应。图3-12 做成三行表：要点、盖楼类比、本例电阻检测的具体做法，上下逐列对等。',
    13: '您指出的三点都已改，图3-13 重画：第 1 层写全问题“逐个检测 5 个标称 100 Ω 的电阻（95～105 Ω 为合格），统计合格个数和不合格个数”；第 2 层①改为“合格数 ok、不合格数 bad 都清零，从第 1 个电阻开始”，③输出两个数；第 3 层把“逐个检测”细化为读入、判断、合格 ok 加 1/不合格 bad 加 1、i 加 1 共 4 小步。图3-14 流程图、resist.c（增加变量 bad）和正文的行号对应同步修改，已上机实测。',
    14: '这一行原意是填任务描述中的①②③分别属于哪种结构，名称确实不清楚。已改为“对应的办事过程（填①②③）”，表前加一句说明填法；为便于学生照着填，顺序结构一列各行都给了示例。',
    15: '已按前面补写的内容重写任务一的小结：算法的概念，三个算法举例体现的“用变量记录数据、按条件选择、反复执行”的思路，五个特征，两种表示方法和报到流程；任务二一段的“整理书包”同步改为“上课前的准备”。',
}
orig = {int(c.get(W + 'id')): c for c in etree.parse(ORIG).getroot().findall(W + 'comment')}
assert sorted(orig) == sorted(REPLIES) == list(range(16)), sorted(orig)

# 1. 作者原批注：编号、作者、时间不变；多段原文用换行保留
for cid in range(16):
    c = orig[cid]
    lines = [''.join(p.itertext()) for p in c.findall('.//' + W + 'p')]
    while lines and not lines[-1].strip():
        lines.pop()
    add_comment(D, ' '.join(lines), comment_id=cid, author=c.get(W + 'author'), initials=c.get(W + 'initials') or '冯')
cp = Path(D) / 'word' / 'comments.xml'
tree = etree.parse(str(cp))
for c in tree.getroot().findall(W + 'comment'):
    cid = int(c.get(W + 'id'))
    c.set(W + 'date', orig[cid].get(W + 'date'))
    for t in c.iter(W + 't'):
        if ' ' in (t.text or ''):
            r = t.getparent()
            parts = t.text.split(' ')
            t.text = parts[0]
            prev = r
            for s in parts[1:]:
                nr = copy.deepcopy(r)
                for k in list(nr):
                    if k.tag != W + 'rPr':
                        nr.remove(k)
                etree.SubElement(nr, W + 'br')
                nt = etree.SubElement(nr, W + 't')
                nt.text = s
                nt.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
                prev.addnext(nr)
                prev = nr
tree.write(str(cp), xml_declaration=True, encoding='UTF-8', standalone=True)

# 2. 回复：放在原批注之后（编号 16～31），锚点套在原批注的锚点里
doc = etree.parse(f'{D}/word/document.xml')
for pid, txt in REPLIES.items():
    cid, _, _ = add_comment(D, txt, author='Claude（项目组）', initials='CL', parent_id=pid)
    st = doc.find(f'.//{W}commentRangeStart[@{W}id="{pid}"]')
    en = doc.find(f'.//{W}commentRangeEnd[@{W}id="{pid}"]')
    ref = [r for r in doc.iter(W + 'r') if r.find(f'{W}commentReference[@{W}id="{pid}"]') is not None][0]
    s2 = etree.Element(W + 'commentRangeStart')
    s2.set(W + 'id', str(cid))
    st.addnext(s2)
    e2 = etree.Element(W + 'commentRangeEnd')
    e2.set(W + 'id', str(cid))
    en.addprevious(e2)
    r2 = etree.fromstring(f'<w:r xmlns:w="{W[1:-1]}"><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="{cid}"/></w:r>')
    ref.addnext(r2)
doc.write(f'{D}/word/document.xml', xml_declaration=True, encoding='UTF-8', standalone=True)
print('comments:', len(etree.parse(str(cp)).getroot()))
