# 给作者的 7 条批注逐条加“已处理”回复，并在正文放好锚点
# 用法：python3 -I replies.py 解包目录 comment.py路径
import re
import subprocess
import sys
from lxml import etree

D, CPY = sys.argv[1], sys.argv[2]
REPLIES = {
    0: '已按调整后的两个任务重写三维目标：知识目标 6 条、能力目标 6 条，素养目标不变。原“掌握 printf 输出各类数据”超出本项目所学，改为“会用 printf 输出文字和整数”。',
    1: '知识导图已按“任务一、任务二、AI升华”重画，节点与正文小标题一一对应。',
    2: '图1-3 已按批注重画：左侧“操作说明：手机连校园网”五步，右侧“程序：新生专属档案”五步。',
    3: '保留六个领域的版式，每格改为“实物照片＋标题＋一句说明”的表格，文字可直接改。照片取自开源项目公开发布的实拍图（授权允许出版使用，来源和许可证列在图下），系统软件一格是编者在 Linux 上的实拍截图。其后新增图1-6：点餐小程序和贪吃蛇小游戏，各用三步说明是怎么做出来的；两个程序已上机编译，源程序放入资源包。',
    4: '已做动画“预处理在做什么”（MP4 和 GIF 各一份，约 18 秒），放入资源包；书中新增静态分镜图1-9，本段末尾加“见图1-9”和动画说明。资源平台地址确定后，可在这里加二维码。',
    5: '已按所附常用图重画为竖向流程图：开始—编辑—编译—有错？—连接—执行—结果正确？—结束，文件名用 f.c、f.obj、f.exe；正文（1）～（3）中的示例文件名同步改为 f.c、f.o 或 f.obj、f.exe。',
    6: '已改为一段话，概括两个任务各自做了什么、学了哪些知识点，以及 AI 升华；删去了不存在的“表1-14”。自查清单补了“输出整数”和“四要素提问法”两项。',
}
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
pairs = {}
for pid, txt in REPLIES.items():
    out = subprocess.run(['python3', CPY, D, txt, '--parent', str(pid), '--author', 'Claude（项目组）', '--initials', 'CL'],
                         capture_output=True, text=True, cwd=CPY.rsplit('/', 1)[0])
    assert out.returncode == 0, out.stderr
    pairs[pid] = max(int(x) for x in re.findall(r'w:id="(\d+)"', out.stdout))
doc = etree.parse(f'{D}/word/document.xml')
for pid, cid in pairs.items():
    st = doc.find(f'.//{W}commentRangeStart[@{W}id="{pid}"]')
    en = doc.find(f'.//{W}commentRangeEnd[@{W}id="{pid}"]')
    ref = [r for r in doc.iter(W + 'r') if r.find(f'{W}commentReference[@{W}id="{pid}"]') is not None][0]
    s2 = etree.Element(W + 'commentRangeStart')
    s2.set(W + 'id', str(cid))
    st.addnext(s2)
    e2 = etree.Element(W + 'commentRangeEnd')
    e2.set(W + 'id', str(cid))
    en.addnext(e2)
    r2 = etree.fromstring(f'<w:r xmlns:w="{W[1:-1]}"><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="{cid}"/></w:r>')
    ref.addnext(r2)
doc.write(f'{D}/word/document.xml', xml_declaration=True, encoding='UTF-8', standalone=True)
print(pairs)
