# 清理未用图片、更新文档属性、打包为 docx
import os, re, sys, zipfile
D, OUT = sys.argv[1:3]
doc = open(f'{D}/word/document.xml', encoding='utf8').read()
used = set(re.findall(r'r:(?:embed|id)="(rId\d+)"', doc))
rp = f'{D}/word/_rels/document.xml.rels'
rels = open(rp, encoding='utf8').read()
keep = []
for m in re.finditer(r'<Relationship [^>]*/>', rels):
    r = m.group(0)
    rid = re.search(r'Id="([^"]+)"', r).group(1)
    tgt = re.search(r'Target="([^"]+)"', r).group(1)
    if '/image' in r and rid not in used:
        p = f'{D}/word/{tgt}'
        if os.path.exists(p):
            os.remove(p)
        continue
    keep.append(r)
rels = re.sub(r'<Relationship [^>]*/>', '', rels).replace('</Relationships>', ''.join(keep) + '</Relationships>')
open(rp, 'w', encoding='utf8').write(rels)
# 模板（WPS 保存）样式的子元素顺序不合 OOXML（如 qFormat 在 uiPriority 前面），按规范顺序重排（与项目二修订稿起的 pack 脚本相同）
from lxml import etree
ORDER = 'name aliases basedOn next link autoRedefine hidden uiPriority semiHidden unhideWhenUsed qFormat locked personal personalCompose personalReply rsid pPr rPr tblPr trPr tcPr tblStylePr'.split()
WNS = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
sp = f'{D}/word/styles.xml'
stree = etree.parse(sp)
for style in stree.getroot().iter(WNS + 'style'):
    kids = list(style)
    kids.sort(key=lambda e: ORDER.index(e.tag[len(WNS):]) if e.tag.startswith(WNS) and e.tag[len(WNS):] in ORDER else len(ORDER))
    for k in kids:
        style.append(k)
stree.write(sp, xml_declaration=True, encoding='UTF-8', standalone=True)
cp = f'{D}/docProps/core.xml'
if os.path.exists(cp):
    s = open(cp, encoding='utf8').read()
    s = re.sub(r'<dc:title>.*?</dc:title>', '<dc:title>人工智能助力C语言程序设计 项目四 开发顺序交互程序</dc:title>', s)
    open(cp, 'w', encoding='utf8').write(s)
if os.path.exists(OUT):
    os.remove(OUT)
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    z.write(f'{D}/[Content_Types].xml', '[Content_Types].xml')
    for root, _, files in os.walk(D):
        for f in files:
            full = os.path.join(root, f)
            arc = os.path.relpath(full, D)
            if arc != '[Content_Types].xml':
                z.write(full, arc)
print('ok', os.path.getsize(OUT))
