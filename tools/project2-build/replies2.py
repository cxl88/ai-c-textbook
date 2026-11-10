# 带批注回复版：放回作者冯丽娜的 16 条原批注（原文、原时间），逐条加“Claude（项目组）”的处理回复
# 用法：python3 replies2.py 解包目录（已由 content2.py 放好锚点） 作者稿comments.xml
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
    0: '已按全项目的知识点重写：三个任务各学什么（常量与变量、三种基本数据类型、标识符；字符的 ASCII 编码与字符运算；算术、赋值运算符与类型转换），最后是 AI 升华“借助 AI 纠正表达式中的错误”。',
    1: '已在任务三和 AI 升华写完后定稿：知识目标 6 条、能力目标 6 条、素养目标 4 条，每条都能在正文中找到对应的内容和练习。',
    2: '已重画为“任务一、任务二、任务三、AI 升华”四个分支，节点与正文小标题一一对应（图2-2）。',
    3: '已统一：一级 1. 2. 3.，二级（1）（2）（3），三级 ①②③，任务三和 AI 升华也按此排。项目一已按同一体例调整（另交项目一调整版）；项目四本来就是这个体例；项目三待定稿时一并核对。',
    4: '已绘制图2-3：左边是储物柜的类比，右边是内存中的变量 people，变量名 people、值 36、类型 int（占 4 个字节），正文用储物柜作了对应说明。',
    5: '图2-4 已去掉 bool 型。基本类型只保留整型、实型、字符型三类，并标出本项目重点学习的部分。',
    6: '已把“见第×页”改为“见本项目任务三‘相关知识’中的‘3. 类型转换’”，按标题指引，不依赖页码，终稿排版后不用再改。',
    7: '同上，改为“将在任务二中详细介绍”，不再写页码。',
    8: '已根据任务描述写成“已知、处理、输出”三行表格，与任务一、任务二的任务分析格式一致，后面一段说明要用到哪些知识，并引出三格漫画“利用率怎么是 0%？”。',
    9: '已按提纲补齐：1. 算术运算符与表达式（含自增自减）、2. 赋值运算符与表达式（含复合赋值）、3. 类型转换、4. 运算符的优先级与结合性，每部分都有例题、运行结果和课堂练习。',
    10: '已补全例题编号和标题。全项目例题统一为“例2-n＋标题”，共 13 个（例2-1～例2-13），程序都在小熊猫C++ 中实际运行，书中的运行结果就是实际输出。',
    11: '已改写这句话；第一步“程序框架”改为留空的书写框，让学生参照任务一、任务二自己写。',
    12: '已按批注处理：变量名、值从哪里来两列已补齐；类型一列留空让学生填；下面的定义变量语句改为留空的书写框。参考答案见《修改意见与处理说明》第三部分。',
    13: '已补上第三步代码：“输入”环节用赋值语句代替键盘输入，正文说明了原因（键盘输入在项目四学习）。',
    14: '已补充完整程序 usage.c 及运行结果、AI 助学卡、技能训练 3 题、课堂验收，以及其后的项目小结、AI 升华（借助 AI 纠正表达式中的错误）和实训巩固 20 题。',
    15: '已补充附录B：15 级运算符的优先级和结合方向，标★的是本项目学过的运算符；表下注明同一个符号在不同位置的含义不同。',
}
orig = {int(c.get(W + 'id')): c for c in etree.parse(ORIG).getroot().findall(W + 'comment')}
assert sorted(orig) == sorted(REPLIES) == list(range(16))

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
