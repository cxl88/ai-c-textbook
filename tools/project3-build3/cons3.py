# 运行结果截图：由 Wine 实测输出 .wout 加上键盘输入（带下划线）拼成控制台画面
import html, re, sys
CODE = sys.argv[1] if len(sys.argv) > 1 else '/root/cstudy/p3code'
# 程序名, 输出后缀, 输入文件后缀, 等待输入的提示（正则；None 表示没有键盘输入）
RUNS = [('avg', '', '', None), ('card', '', '', r'本次消费：'), ('login', '', '', r'账号：|密码：'),
        ('login', '2', '2', r'账号：|密码：'), ('measure', '', '', r'测量值（Ω）：'), ('resist', '', '', r'阻值（Ω）：')]
out = []
for name, so, si, pat in RUNS:
    w = open(f'{CODE}/{name}.wout{so}', encoding='utf8').read()
    assert open(f'{CODE}/{name}.wret{so}').read().strip() == '0'
    ins = [x for x in open(f'{CODE}/{name}.in{si}').read().split('\n') if x] if pat else []
    parts, k, pos = [], 0, 0
    if pat:
        for m in re.finditer(pat, w):
            parts.append(html.escape(w[pos:m.end()]))
            parts.append('<span class="kin">' + html.escape(ins[k]) + '</span>\n')
            k += 1
            pos = m.end()
        assert k == len(ins), (name, k, len(ins))
    parts.append(html.escape(w[pos:]))
    body = ''.join(parts).rstrip('\n')
    out.append(f'<div class="con" id="run_{name}{so}"><pre>{body}</pre></div>')
css = '''body{margin:0;background:#fff}
.con{display:inline-block;margin:10px;background:#0C0C0C;padding:6px 10px 8px}
pre{margin:0;color:#CCCCCC;font-family:'Noto Sans Mono CJK SC',monospace;font-size:13px;line-height:1.4}
.kin{color:#fff;text-decoration:underline;text-underline-offset:2px}'''
open('fig/cons.html', 'w', encoding='utf8').write(f'<!doctype html><meta charset="utf-8"><style>{css}</style><body>' + '\n'.join(out))
print(' '.join(re.findall(r'id="([^"]+)"', '\n'.join(out))))
