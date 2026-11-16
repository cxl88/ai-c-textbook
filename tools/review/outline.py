# 提取成品 docx 的大纲与统计（字数、最大图表例题编号、程序清单、栏目个数），审读成品、核对跨项目一致性用。
# 用法：python tools/review/outline.py 输出目录 成品.docx…（每个 docx 写出 .outline.txt 和 .full.txt）
import collections
import os
import re
import sys
import zipfile

sys.stdout.reconfigure(encoding="utf-8")

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
HEAD = re.compile(r'^(项目[一二三四五六七八九十]\s|情境导入$|三维目标$|知识导图$|任务[一二三四五]\s?|任务描述$|任务分析$|相关知识$|任务实施$|技能训练$|'
                  r'项目小结$|AI升华|实训巩固$|附录|\d+\.\s?\S|（\d+）\S|第[一二三四五]步|完整程序|课堂验收|趣味小站|课堂活动|课堂练习|AI 助学|AI助学|小智提示|注意：|训练 \d)')
for f in sys.argv[2:]:
    x = zipfile.ZipFile(f).read('word/document.xml').decode('utf8')
    paras = [''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', p)) for p in re.findall(r'<w:p[ >].*?</w:p>', x, re.S)]
    paras = [p.strip() for p in paras if p.strip()]
    text = '\n'.join(paras)
    name = os.path.basename(f)
    stat = collections.OrderedDict()
    for k, pat in (('图', r'图(\d+)-(\d+)'), ('表', r'表(\d+)-(\d+)'), ('例', r'例(\d+)-(\d+)')):
        nums = {(int(a), int(b)) for a, b in re.findall(pat, text)}
        stat[k] = max((b for a, b in nums), default=0)
    progs = sorted(set(re.findall(r'\b([a-z][a-z0-9_]*\.c)\b', text)))
    boxes = collections.Counter()
    for p in paras:
        for key in ('趣味小站', '课堂活动', '课堂小游戏', '课堂练习', 'AI 助学', '小智提示', '注意：', '课堂验收', '知识拓展', '离开 AI 再做'):
            if p.startswith(key):
                boxes[key] += 1
    with open(os.path.join(OUT, name + '.outline.txt'), 'w', encoding='utf8') as o:
        nchar = len(re.sub(r'\s', '', text))
        o.write(f'{name}\n字数（不含空白）约 {nchar}；段落 {len(paras)}\n')
        o.write('最大编号：' + '，'.join(f'{k}{v}' for k, v in stat.items()) + '\n')
        o.write(f'程序 {len(progs)} 个：' + ' '.join(progs) + '\n')
        o.write('栏目：' + '，'.join(f'{k}{v}' for k, v in boxes.items()) + '\n\n')
        for p in paras:
            if HEAD.match(p) and len(p) < 60:
                o.write(p + '\n')
    with open(os.path.join(OUT, name + '.full.txt'), 'w', encoding='utf8') as o:
        o.write(text)
    print(name, dict(stat), 'progs', len(progs), 'chars', len(text))
