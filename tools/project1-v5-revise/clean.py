import re,os,sys
from lxml import etree
D=sys.argv[1]
W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
t=etree.parse(f'{D}/word/document.xml')
for tag in ('commentRangeStart','commentRangeEnd'):
    for e in list(t.iter(W+tag)): e.getparent().remove(e)
for r in list(t.iter(W+'r')):
    if r.find(W+'commentReference') is not None: r.getparent().remove(r)
t.write(f'{D}/word/document.xml',xml_declaration=True,encoding='UTF-8',standalone=True)
p=f'{D}/word/_rels/document.xml.rels'; s=open(p).read(); open(p,'w').write(re.sub(r'<Relationship [^>]*Target="comments[^"]*\.xml"/>','',s))
p=f'{D}/[Content_Types].xml'; s=open(p).read(); open(p,'w').write(re.sub(r'<Override PartName="/word/comments[^"]*\.xml"[^>]*/>','',s))
for f in os.listdir(f'{D}/word'):
    if f.startswith('comments'): os.remove(f'{D}/word/{f}')
