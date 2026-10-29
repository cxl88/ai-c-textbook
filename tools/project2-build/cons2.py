# 运行结果截图：由 Wine 实测输出 .wout 拼成控制台画面（项目二的程序都不需要键盘输入）
import html
import re
import sys

CODE = sys.argv[1] if len(sys.argv) > 1 else '../../code/project02'
RUNS = ['const_demo', 'octal', 'var_demo', 'size_demo', 'float_demo', 'lab', 'room204', 'avg_temp', 'char_code',
        'str_len', 'alarm', 'decode', 'zone', 'arith', 'group', 'incdec', 'assign_expr', 'convert', 'div_test', 'prec',
        'usage', 'group_fill', 'volt_dev', 'bill', 'usage2', 'ai_try4', 'ai_try5', 'ai_try5ok', 'define_semi', 'fix_204']


def render(name):
    w = open(f'{CODE}/{name}.wout', encoding='utf8').read()
    assert open(f'{CODE}/{name}.wret').read().strip() == '0', name
    body = html.escape(w).rstrip('\n')
    return f'<div class="con" id="run_{name}"><pre>{body}</pre></div>'


out = [render(r) for r in RUNS]
css = '''body{margin:0;background:#fff}
.con{display:inline-block;margin:10px;background:#0C0C0C;padding:6px 10px 8px}
pre{margin:0;color:#CCCCCC;font-family:'Noto Sans Mono CJK SC',monospace;font-size:13px;line-height:1.4;tab-size:8}'''
open('fig/cons.html', 'w', encoding='utf8').write(f'<!doctype html><meta charset="utf-8"><style>{css}</style><body>' + '\n'.join(out))
print(' '.join(re.findall(r'id="([^"]+)"', '\n'.join(out))))
