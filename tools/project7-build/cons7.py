# 运行结果截图：由实测输出 .wout 加上键盘输入拼成控制台画面（键盘输入加下划线）。
# 程序先用 printf 输出提示、再读入一行；把 .in 中的各行依次插在输出中各个“提示”的后面。
# 提示默认按全角冒号“：”识别；输出本身在输入之前就含“：”的程序，要在 PROMPT 中给出正则。
# 限时运行（死循环）的程序用 .wcap（开头的输出）和 .cin（键盘输入），只取开头 CAP_LINES 行，id 为 cap_程序名。
# 用法：python3 cons7.py 书中程序目录
import glob
import html
import os
import re
import sys

CODE = sys.argv[1] if len(sys.argv) > 1 else '../../code/project07/book'
PROMPT = {}                  # 项目七各程序的提示都以全角冒号“：”结尾，用默认的正则即可
CAPS = {}                    # 项目七没有限时运行（死循环）的程序
EARLY = {}                   # 程序提前结束、测试输入中后面几行不会被读入的运行


def build(name, w, ins, cap=False, prompt=None):
    pat = re.compile(PROMPT.get(prompt or name, '：'))
    parts, pos, k = [], 0, 0
    for m in pat.finditer(w):
        if k == len(ins):
            break
        parts.append(html.escape(w[pos:m.end()]) + '<span class="kin">' + html.escape(ins[k]) + '</span>\n')
        pos = m.end()
        k += 1
    assert k == len(ins) or (cap and k == len(ins)) or EARLY.get(name) == k, (name, k, len(ins))
    parts.append(html.escape(w[pos:]))
    return ''.join(parts).rstrip()


def lines_of(path):
    return open(path, encoding='utf8').read().split('\n')[:-1] if os.path.exists(path) else []


out = []
for p in sorted(glob.glob(f'{CODE}/*.wout*')):
    name, so = re.match(r'(.+)\.wout(\d*)$', os.path.basename(p)).groups()
    assert open(f'{CODE}/{name}.wret{so}').read().strip() == '0', (name, so)
    body = build(name + so, open(p, encoding='utf8').read(), lines_of(f'{CODE}/{name}.in{so}'), prompt=name)
    out.append(f'<div class="con" id="run_{name}{so}"><pre>{body}</pre></div>')
for name, k in CAPS.items():
    assert open(f'{CODE}/{name}.wcapret').read().startswith('timeout'), name
    w = '\n'.join(open(f'{CODE}/{name}.wcap', encoding='utf8').read().split('\n')[:k]) + '\n'
    body = build(name, w, lines_of(f'{CODE}/{name}.cin'), cap=True)
    out.append(f'<div class="con" id="cap_{name}"><pre>{body}</pre></div>')
css = '''body{margin:0;background:#fff}
.con{display:inline-block;margin:10px;background:#0C0C0C;padding:6px 10px 8px}
pre{margin:0;color:#CCCCCC;font-family:'Noto Sans Mono CJK SC',monospace;font-size:13px;line-height:1.4;tab-size:8}
.kin{color:#fff;text-decoration:underline;text-underline-offset:2px;white-space:pre}'''
os.makedirs('fig', exist_ok=True)
open('fig/cons.html', 'w', encoding='utf8').write(f'<!doctype html><meta charset="utf-8"><style>{css}</style><body>' + '\n'.join(out))
print(' '.join(re.findall(r'id="([^"]+)"', '\n'.join(out))))
