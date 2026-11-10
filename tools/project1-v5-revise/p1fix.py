# 项目一 v5 → v5.1：按作者冯丽娜在项目二批注 3 中的要求统一知识点层级序号
#   一级 1. 2. 3.；二级（1）（2）（3）；三级 ①②③。只改序号，正文其余内容不动。
# 用法：python3 p1fix.py 解包目录（清洁版、带批注回复版各运行一次）
import sys
from lxml import etree

D = sys.argv[1]
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
FIX = [  # (段首原文, 改为)
    ('1）计算机程序', '（1）计算机程序'), ('2）计算机语言', '（2）计算机语言'), ('3）程序设计', '（3）程序设计'),
    ('①预处理指令。', '（1）预处理指令。'), ('②main主函数。', '（2）main主函数。'),
    ('函数头。函数的第1行', '①函数头。函数的第1行'), ('函数体。函数头下面', '②函数体。函数头下面'),
    ('③注释。', '（3）注释。'),
    ('①下载安装包。', '（1）下载安装包。'), ('②安装。', '（2）安装。'), ('③基本配置。', '（3）基本配置。'),
]
doc = etree.parse(f'{D}/word/document.xml')
done = []
for p in doc.getroot().iter(W + 'p'):
    ts = [t for t in p.iter(W + 't')]
    full = ''.join(t.text or '' for t in ts)
    lead = len(full) - len(full.lstrip())
    for old, new in FIX:
        if full[lead:].startswith(old):
            # 从段首（跳过前导空白）起删去 old 的字符，再把 new 写进第一个被改动的文字块
            k, need, first = 0, len(old), None
            pos = 0
            for t in ts:
                s = t.text or ''
                a, z = max(lead - pos, 0), len(s)
                if pos + z <= lead or need == 0:
                    pos += z
                    continue
                take = min(need, z - a)
                if first is None:
                    first = t
                    t.text = s[:a] + new + s[a + take:]
                else:
                    t.text = s[:a] + s[a + take:]
                need -= take
                pos += z
            assert need == 0
            done.append(old)
            break
doc.write(f'{D}/word/document.xml', xml_declaration=True, encoding='UTF-8', standalone=True)
missing = [o for o, _ in FIX if o not in done]
print('改了', len(done), '处', '未找到：' + '、'.join(missing) if missing else '')
assert not missing and len(done) == len(FIX)
