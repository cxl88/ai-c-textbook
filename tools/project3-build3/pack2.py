# 清理未用图片、加奇数页页眉（项目名）、更新文档属性、打包为 docx
# 版式沿用项目一 v5：偶数页页眉为书名；本项目另加奇数页页眉“项目三 梳理程序执行逻辑”（作者稿即如此），
# 项目首页不出页眉（首页页脚与其他奇数页相同）。
import os, re, sys, zipfile
D, OUT = sys.argv[1:3]
PROJ = '项目三 梳理程序执行逻辑'
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
# 页眉：header2 奇数页（右对齐项目名），header3 首页（空）
h1 = open(f'{D}/word/header1.xml', encoding='utf8').read()
h2 = h1.replace('<w:jc w:val="left"/>', '<w:jc w:val="right"/>').replace('人工智能助力C语言程序设计', PROJ)
h3 = re.sub(r'<w:p [^>]*>.*</w:p>', '<w:p><w:pPr><w:pStyle w:val="11"/></w:pPr></w:p>', h1, flags=re.S)
open(f'{D}/word/header2.xml', 'w', encoding='utf8').write(h2)
open(f'{D}/word/header3.xml', 'w', encoding='utf8').write(h3)
HT = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/header'
keep += [f'<Relationship Id="rId901" Type="{HT}" Target="header2.xml"/>', f'<Relationship Id="rId902" Type="{HT}" Target="header3.xml"/>']
rels = re.sub(r'<Relationship [^>]*/>', '', rels).replace('</Relationships>', ''.join(keep) + '</Relationships>')
open(rp, 'w', encoding='utf8').write(rels)
ct = open(f'{D}/[Content_Types].xml', encoding='utf8').read()
HCT = 'application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml'
for h in ('header2', 'header3'):
    if f'/word/{h}.xml' not in ct:
        ct = ct.replace('</Types>', f'<Override PartName="/word/{h}.xml" ContentType="{HCT}"/></Types>')
open(f'{D}/[Content_Types].xml', 'w', encoding='utf8').write(ct)
m = re.search(r'<w:sectPr>(.*?)</w:sectPr>\s*</w:body>', doc, re.S)
s = m.group(1)
assert 'w:type="default"' in s and 'rId901' not in s
foot = re.search(r'<w:footerReference r:id="(rId\d+)" w:type="default"/>', s).group(1)
s2 = (f'<w:headerReference r:id="rId901" w:type="default"/><w:headerReference r:id="rId902" w:type="first"/>'
      f'<w:footerReference r:id="{foot}" w:type="first"/>' + s)
s2 = s2.replace('<w:pgSz', '<w:titlePg/><w:pgSz') if '<w:titlePg/>' not in s2 else s2
# titlePg 须排在 pgMar 等之后、cols 等之前？按 CT_SectPr 顺序：…type, pgSz, pgMar, …, cols, …, titlePg, textDirection, …, docGrid
s2 = s2.replace('<w:titlePg/>', '').replace('<w:docGrid', '<w:titlePg/><w:docGrid')
doc = doc[:m.start(1)] + s2 + doc[m.end(1):]
open(f'{D}/word/document.xml', 'w', encoding='utf8').write(doc)
# 模板（WPS 保存）样式的子元素顺序不合 OOXML（如 qFormat 在 uiPriority 前面），按规范顺序重排，Word 校验无误
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
    t = open(cp, encoding='utf8').read()
    t = re.sub(r'<dc:title>.*?</dc:title>', f'<dc:title>人工智能助力C语言程序设计 {PROJ}</dc:title>', t)
    open(cp, 'w', encoding='utf8').write(t)
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
