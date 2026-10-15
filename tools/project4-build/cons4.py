# 运行结果截图：由 Wine 实测输出 .wout 加上键盘输入拼成控制台画面
# 每次运行：(程序名, 输出后缀, 输入后缀, [(提示的正则 或 None 表示开头, 这里输入几行), ...])
import html
import re
import sys

CODE = sys.argv[1] if len(sys.argv) > 1 else '/root/cstudy/p4code'
L2 = [(r'用空格隔开）：\n', 1), (r'连续输入）：\n', 1)]
RUNS = [('run', '', '', [(r'距离（千米）：', 1), (r'用时（分钟）：', 1)]),
        ('stmt', '', '', []), ('assign', '', '', []), ('fmt', '', '', []), ('width', '', '', []),
        ('indate', '', '', [(r'2026-10-15）：', 1)]), ('indate', '2', '2', [(r'2026-10-15）：', 1)]),
        ('scanf_nl', '', '', [(r'在室人数：', 3)]),
        ('scanf_msg', '', '', [(None, 1)]),
        ('ledger', '', '', [(r'用空格隔开）：\n', 1)]),
        ('ohm', '', '', [(r'电阻（kΩ）：', 1)]),
        ('ledger_date', '', '', [(r'2026-10-15）：', 1), (r'用空格隔开）：\n', 1)]),
        ('series', '', '', [(r'阻值（kΩ）：', 1)]),
        ('put', '', '', []),
        ('get', '', '', [(r'（Y/N）：', 1)]), ('get', '2', '2', [(r'（Y/N）：', 1)]),
        ('buf', '', '', [(r'阻值（kΩ）：', 1)]),
        ('buf2', '', '', [(r'阻值（kΩ）：', 1), (r'状态（Y/N）：', 1)]),
        ('dog', '', '', [(r'3 个字母：', 1)]),
        ('signin', '', '', [(r'（A～F）：', 1), (r'座位号：', 1), (r'（时:分）：', 1)]),
        ('ledger2', '', '', L2), ('ledger2', '2', '2', L2), ('ledger2', '3', '3', L2),
        ('quiz', '', '', [(r'题号：', 1), (r'（A～D）：', 1)]),
        ('ledger3', '', '', [(r'用空格隔开）：\n', 1)]),
        ('milktea', '', '', [(r'杯数：', 1), (r'大杯）：', 1), (r'单价（元）：', 1)]),
        ('fix_scanf', '3', '3', L2)]


def render(name, so, si, steps):
    w = open(f'{CODE}/{name}.wout{so}', encoding='utf8').read()
    assert open(f'{CODE}/{name}.wret{so}').read().strip() == '0', name
    ins = open(f'{CODE}/{name}.in{si}', encoding='utf8').read().split('\n') if steps else []
    if ins and ins[-1] == '':
        ins.pop()
    parts, k, pos = [], 0, 0
    for pat, n in steps:
        if pat is None:
            end = 0
        else:
            m = re.compile(pat).search(w, pos)
            assert m, (name, so, pat)
            end = m.end()
        parts.append(html.escape(w[pos:end]))
        for j in range(n):
            parts.append('<span class="kin">' + html.escape(ins[k]) + '</span>\n')
            k += 1
        pos = end
    assert k == len(ins), (name, so, k, len(ins))
    parts.append(html.escape(w[pos:]))
    body = ''.join(parts).rstrip('\n')
    return f'<div class="con" id="run_{name}{so}"><pre>{body}</pre></div>'


out = [render(*r) for r in RUNS]
css = '''body{margin:0;background:#fff}
.con{display:inline-block;margin:10px;background:#0C0C0C;padding:6px 10px 8px}
pre{margin:0;color:#CCCCCC;font-family:'Noto Sans Mono CJK SC',monospace;font-size:13px;line-height:1.4;tab-size:8}
.kin{color:#fff;text-decoration:underline;text-underline-offset:2px;white-space:pre}'''
open('fig/cons.html', 'w', encoding='utf8').write(f'<!doctype html><meta charset="utf-8"><style>{css}</style><body>' + '\n'.join(out))
print(' '.join(re.findall(r'id="([^"]+)"', '\n'.join(out))))
