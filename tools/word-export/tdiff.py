#!/usr/bin/env python3
"""Character-level diff of two texts after removing all whitespace; prints each difference with context."""
import re, subprocess, sys, tempfile, os
def norm(s):
    return re.sub(r'[\s 　​‌‍⁠﻿­]+', '', s)
a = norm(open(sys.argv[1], encoding='utf-8').read())
b = norm(open(sys.argv[2], encoding='utf-8').read())
print('chars', len(a), len(b))
d = tempfile.mkdtemp()
fa, fb = os.path.join(d, 'a'), os.path.join(d, 'b')
open(fa, 'w', encoding='utf-8').write('\n'.join(a) + '\n')
open(fb, 'w', encoding='utf-8').write('\n'.join(b) + '\n')
r = subprocess.run(['diff', fa, fb], capture_output=True, text=True).stdout
hunks = re.findall(r'^(\d+)(?:,(\d+))?([acd])(\d+)(?:,(\d+))?$', r, re.M)
print('hunks', len(hunks))
for a1, a2, op, b1, b2 in hunks:
    a1 = int(a1); a2 = int(a2 or a1); b1 = int(b1); b2 = int(b2 or b1)
    if op == 'a': left = ''; ctx = a[max(0, a1 - 12):a1]; after = a[a1:a1 + 8]; right = b[b1 - 1:b2]
    elif op == 'd': left = a[a1 - 1:a2]; right = ''; ctx = a[max(0, a1 - 13):a1 - 1]; after = a[a2:a2 + 8]
    else: left = a[a1 - 1:a2]; right = b[b1 - 1:b2]; ctx = a[max(0, a1 - 13):a1 - 1]; after = a[a2:a2 + 8]
    print(f'{ctx}[-{left[:80]}{"…" if len(left) > 80 else ""}-][+{right[:80]}{"…" if len(right) > 80 else ""}+]{after}')
