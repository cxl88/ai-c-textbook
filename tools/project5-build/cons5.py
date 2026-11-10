# 运行结果截图：由 Wine 实测输出 .wout 加上键盘输入拼成控制台画面（键盘输入加下划线）
# 项目五的程序都是先用 printf 输出以“：”结尾的提示、再读入一行，所以把 .in 中的各行依次插在输出中各个“：”的后面。
# 用法：python3 cons5.py 程序目录，为目录中所有 .wout* 生成画面，id 为 run_程序名[序号]
import glob
import html
import os
import re
import sys

CODE = sys.argv[1] if len(sys.argv) > 1 else '../../code/project05/book'


def render(path):
    name, so = re.match(r'(.+)\.wout(\d*)$', os.path.basename(path)).groups()
    w = open(path, encoding='utf8').read()
    assert open(f'{CODE}/{name}.wret{so}').read().strip() == '0', (name, so)
    inp = f'{CODE}/{name}.in{so}'
    ins = open(inp, encoding='utf8').read().split('\n')[:-1] if os.path.exists(inp) else []
    parts, pos = [], 0
    for line in ins:
        k = w.find('：', pos)
        assert k >= 0, (name, so, line)
        parts.append(html.escape(w[pos:k + 1]) + '<span class="kin">' + html.escape(line) + '</span>\n')
        pos = k + 1
    parts.append(html.escape(w[pos:]))
    return f'<div class="con" id="run_{name}{so}"><pre>{"".join(parts).rstrip()}</pre></div>'


out = [render(p) for p in sorted(glob.glob(f'{CODE}/*.wout*'))]
css = '''body{margin:0;background:#fff}
.con{display:inline-block;margin:10px;background:#0C0C0C;padding:6px 10px 8px}
pre{margin:0;color:#CCCCCC;font-family:'Noto Sans Mono CJK SC',monospace;font-size:13px;line-height:1.4;tab-size:8}
.kin{color:#fff;text-decoration:underline;text-underline-offset:2px;white-space:pre}'''
os.makedirs('fig', exist_ok=True)
open('fig/cons.html', 'w', encoding='utf8').write(f'<!doctype html><meta charset="utf-8"><style>{css}</style><body>' + '\n'.join(out))
print(' '.join(re.findall(r'id="([^"]+)"', '\n'.join(out))))
