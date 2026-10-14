#!/usr/bin/env python3
"""Post-process the docx written by build_docx.js.

- settings: mirror margins (inside/outside), Chinese default tab stop, no punctuation compression
- styles: document defaults (fonts, zh-CN language, no automatic CJK/Latin spacing), Normal as the
  default paragraph style, dot-leader tab for the TOC styles
- document: page references become PAGEREF fields, TOC tab stops sit at the text-block edge
usage: post.py in.docx out.docx text_width_twips
"""
import re
import sys
import zipfile

src, dst, text_w = sys.argv[1], sys.argv[2], int(sys.argv[3])

DEFAULTS = (
    '<w:docDefaults><w:rPrDefault><w:rPr>'
    '<w:rFonts w:ascii="Times New Roman" w:eastAsia="宋体" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
    '<w:sz w:val="21"/><w:szCs w:val="21"/><w:lang w:val="en-US" w:eastAsia="zh-CN" w:bidi="ar-SA"/>'
    '</w:rPr></w:rPrDefault><w:pPrDefault><w:pPr>'
    '<w:autoSpaceDE w:val="0"/><w:autoSpaceDN w:val="0"/><w:spacing w:after="0" w:line="240" w:lineRule="auto"/>'
    '</w:pPr></w:pPrDefault></w:docDefaults>'
)
TOC_TAB = f'<w:tabs><w:tab w:val="right" w:leader="dot" w:pos="{text_w}"/></w:tabs>'


def fix_settings(s):
    assert '<w:evenAndOddHeaders/>' in s
    s = s.replace('<w:evenAndOddHeaders/>',
                  '<w:mirrorMargins/><w:defaultTabStop w:val="420"/><w:evenAndOddHeaders/>'
                  '<w:characterSpacingControl w:val="doNotCompress"/>', 1)
    return s


def fix_styles(s):
    s, n = re.subn(r'<w:docDefaults>.*?</w:docDefaults>', DEFAULTS, s, count=1, flags=re.S)
    assert n == 1
    s, n = re.subn(r'<w:style w:type="paragraph" w:styleId="Normal">', '<w:style w:type="paragraph" w:default="1" w:styleId="Normal">', s)
    assert n == 1, n
    for sid in ('TOC1', 'TOC2'):
        m = re.search(r'<w:style w:type="paragraph" w:styleId="%s">.*?</w:style>' % sid, s, re.S)
        assert m, sid
        st = m.group(0)
        st2 = st.replace('<w:spacing', TOC_TAB + '<w:spacing', 1)
        assert st2 != st
        s = s.replace(st, st2)
    return s


PAGEREF = re.compile(r'<w:r>(<w:rPr>(?:(?!</w:rPr>).)*</w:rPr>)?<w:t xml:space="preserve">⟦PAGEREF:([A-Za-z0-9_]+):([^⟧]*)⟧</w:t></w:r>')


def pageref(m):
    rpr = m.group(1) or ''
    name, num = m.group(2), m.group(3)
    return (f'<w:r>{rpr}<w:fldChar w:fldCharType="begin"/></w:r>'
            f'<w:r>{rpr}<w:instrText xml:space="preserve"> PAGEREF {name} \\h </w:instrText></w:r>'
            f'<w:r>{rpr}<w:fldChar w:fldCharType="separate"/></w:r>'
            f'<w:r>{rpr}<w:t>{num}</w:t></w:r>'
            f'<w:r>{rpr}<w:fldChar w:fldCharType="end"/></w:r>')


def fix_document(s):
    n_ph = s.count('⟦PAGEREF:')
    s, n = PAGEREF.subn(pageref, s)
    assert n == n_ph and n > 0, (n, n_ph)
    assert '⟦' not in s
    s, n = re.subn(r'<w:tabs>(?:<w:tab w:val="clear" w:pos="\d+"/>)?<w:tab w:val="right" w:pos="\d+" w:leader="dot"/></w:tabs>', TOC_TAB, s)
    assert n >= 19, n
    s = s.replace('<w:rPr><w:rStyle w:val="IndexLink"/></w:rPr>', '')
    return s


BDR_ORDER = ['top', 'left', 'start', 'bottom', 'right', 'end', 'between', 'bar']


def fix_pbdr(s):
    # docx-js writes paragraph borders as top, bottom, left, right; the schema wants top, left, bottom, right
    def one(m):
        kids = re.findall(r'<w:(\w+) [^>]*/>', m.group(1))
        parts = re.findall(r'(<w:(\w+) [^>]*/>)', m.group(1))
        assert ''.join(p for p, _ in parts) == m.group(1), m.group(1)
        parts.sort(key=lambda p: BDR_ORDER.index(p[1]))
        return '<w:pBdr>' + ''.join(p for p, _ in parts) + '</w:pBdr>'
    return re.sub(r'<w:pBdr>(.*?)</w:pBdr>', one, s)


zin = zipfile.ZipFile(src)
zout = zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED)
for item in zin.infolist():
    data = zin.read(item.filename)
    if item.filename in ('word/settings.xml', 'word/styles.xml', 'word/document.xml'):
        s = data.decode('utf-8')
        s = {'word/settings.xml': fix_settings, 'word/styles.xml': fix_styles, 'word/document.xml': fix_document}[item.filename](s)
        data = s.encode('utf-8')
    if item.filename.startswith('word/') and item.filename.endswith('.xml'):
        t = data.decode('utf-8')
        if '<w:pBdr>' in t:
            data = fix_pbdr(t).encode('utf-8')
    zout.writestr(item, data)
zout.close()
print('post ok', dst)
