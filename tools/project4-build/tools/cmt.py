# 检查/对齐行尾注释：IDE 中汉字和全角符号占 2 列
import sys, glob, os, unicodedata
def vw(s, r=2.0):
    return sum(r if unicodedata.east_asian_width(ch) in 'WF' else 1 for ch in s)
def split_comment(line):
    """返回 (代码部分去尾空格, 注释) 或 None；跳过字符串和字符常量里的 //"""
    q = None; i = 0
    while i < len(line):
        c = line[i]
        if q:
            if c == '\\': i += 2; continue
            if c == q: q = None
        elif c in '"\'': q = c
        elif line.startswith('//', i):
            code = line[:i].rstrip()
            return (code, line[i:]) if code.strip() else None
        i += 1
    return None
def groups(lines):
    out, cur = [], []
    for k, ln in enumerate(lines):
        if not ln.strip():
            if cur: out.append(cur); cur = []
            continue
        sc = split_comment(ln)
        if sc: cur.append(k)
    if cur: out.append(cur)
    return out
if __name__ == '__main__':
    fix = '--fix' in sys.argv
    for f in sorted(glob.glob(sys.argv[1] + '/*.c')):
        L = open(f, encoding='utf8').read().split('\n')
        changed = False
        for g in groups(L):
            cols = [vw(L[k][:L[k].index(split_comment(L[k])[1], len(split_comment(L[k])[0]))]) for k in g]
            need = max(vw(split_comment(L[k])[0]) for k in g) + 2
            if len(set(cols)) == 1 and cols[0] >= need:
                continue
            tgt = max(need, min(cols))
            if True:
                print(os.path.basename(f), [k + 1 for k in g], cols, '->', tgt,
                      'maxlen', max(tgt + vw(split_comment(L[k])[1]) for k in g))
                if fix:
                    for k in g:
                        code, cm = split_comment(L[k])
                        L[k] = code + ' ' * int(tgt - vw(code)) + cm
                    changed = True
        if changed:
            open(f, 'w', encoding='utf8').write('\n'.join(L))
