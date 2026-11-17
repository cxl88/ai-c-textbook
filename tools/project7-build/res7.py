# 生成《项目七-配套资源（初稿）.zip》：程序（分组）+ 待补充练习 + 程序验证记录 + 插图原图 + 图片来源与许可。
# 用法：python3 res7.py 书中程序目录 核对程序目录 图目录(fig) 输出.zip   （两个程序目录都已用 wrun.sh 运行过）
# 压缩包用 Python zipfile 生成，中文文件名带 UTF-8 标记，Windows 自带解压也不会乱码。
import glob
import json
import os
import re
import sys
import zipfile
from p3lib import _vw

BOOK, CHECK, FIG, OUT = sys.argv[1:5]
N = json.load(open(f'{FIG}/nums.json', encoding='utf8'))
FG = N['fig']
ROOT = '项目七-配套资源（初稿）'

# 分组：组名 -> (目录, [程序名]) ；学生用的放“学生用”，答案和核对程序放“教师用”
GROUPS = [
    ('学生用/书中示例', BOOK, ['above_avg', 'init1', 'fib_arr', 'maxv', 'bubble', 'volt8', 'init2', 'lamp_arr', 'transpose',
                         'yanghui', 'volt38', 'char_init', 'upper5', 'vote', 'caesar', 'state8', 'hz', 'name_in', 'str_func',
                         'eq_str', 'pwd_chk', 'palin', 'state_text', 'repair_list', 'rank_try', 'ai_a', 'ai_b', 'ai_c']),
    ('学生用/错误示范（只编译）', BOOK, ['bad_bound']),
    ('学生用/错误示范（只编译）', CHECK, ['bad_vla', 'bad_paren', 'bad_nolen', 'bad_excess', 'bad_assign', 'bad_fidx', 'bad_nocol',
                                 'bad_hz', 'bad_strset', 'bad_amp']),
    ('教师用/参考答案', BOOK, ['abn8', 'query8', 'temp7', 'avg38', 'volt83', 'max34', 'cnt4', 'abn_code', 'quiz10', 'login',
                         'find_state', 'longest']),
    ('教师用/参考答案', CHECK, ['cp_rev', 'cp_minv', 'cp_desc', 'cp_trans3', 'cp_round2', 'cp_more', 'fix_q14', 'cp_q15',
                          'cp_q16', 'cp_q17']),
    ('教师用/答案核对', CHECK, ['cp_def', 'cp_init', 'cp_ref', 'cp_volt8', 'mut_volt8', 'cp_init2', 'cp_ref2', 'cp_volt38',
                          'mut_volt38', 'cp_cinit', 'cp_cref', 'cp_caesar', 'cp_vote', 'cp_state8', 'mut_state8', 'cp_str',
                          'cp_io', 'cp_func', 'cp_pal', 'cp_digit', 'cp_repair', 'mut_repair', 'cp_q', 'cp_q13']),
    ('教师用/错误示范（只编译）', CHECK, ['bad_q14', 'bad_q14b']),
]
# 学生用的待补充练习：与书中技能训练 1 相同的挖空版（替换后行尾注释仍对齐在原来的列）
FILLS = {'abn8': [('i < 8', '___①___'), ('v[i] < 3.8 || v[i] > 4.2', '___②___'), ('count++', '___③___')],
         'avg38': [('j < 8', '___①___'), ('sum = 0;', '___②___;'), ('v[i][j]', '___③___')],
         'cnt4': [('{0}', '___①___'), ("code[i] - 'A'", '___②___'), ('cnt[3]', '___③___')],
         'login': [('scanf("%s", user);', 'scanf("%s", ___①___);'), ('strcmp(user, "linxh") == 0', '___②___'), (' && ', ' ___③___ ')]}

all_names = [n for _, _, ns in GROUPS for n in ns]
assert len(all_names) == len(set(all_names))
found = {os.path.basename(f)[:-2] for d in (BOOK, CHECK) for f in glob.glob(f'{d}/*.c')}
assert set(all_names) == found, (found - set(all_names), set(all_names) - found)

CMD = ('gcc.exe 程序名.c -o 程序名.exe -finput-charset=UTF-8 -fexec-charset=gbk -g3 -fno-ms-extensions -pipe -Wall '
       '-Werror=implicit-int -Werror=return-type -Werror=vla')


def fill(text, old, new):
    """与 content7.py 的 fill 相同：把 old 换成 new，行尾注释仍对齐在原来的列（汉字占 2 列）"""
    out = []
    for ln in text.split('\n'):
        i = ln.find(old)
        if i >= 0:
            k = ln.find('//', i + len(old))
            if k >= 0:
                head = ln[:i] + new + ln[i + len(old):k].rstrip()
                ln = head + ' ' * max(1, _vw(ln[:k], 2) - _vw(head, 2)) + ln[k:]
            else:
                ln = ln[:i] + new + ln[i + len(old):]
        out.append(ln)
    return '\n'.join(out)


def keys(f):
    return open(f, encoding='utf8').read().strip().replace('\n', ' ⏎ ') + ' ⏎' if os.path.exists(f) else '（无）'


def record(d, n):
    """一个程序的验证记录：编译提示、每次运行的输入、输出和返回值"""
    out = [f'■ {n}.c', '编译提示：' + (open(f'{d}/{n}.wdiag', encoding='utf8').read().strip() or '（无）')]
    if n.startswith('bad_'):
        out.append('（错误示范：只编译、不运行）')
    for w in sorted(glob.glob(f'{d}/{n}.wout*')):
        s = w.rsplit('.wout', 1)[1]
        out.append(f'—— 第 {s or 1} 次运行　键盘输入：' + keys(f'{d}/{n}.in{s}'))
        out.append(open(w, encoding='utf8').read().rstrip())
        out.append('返回值：' + open(f'{d}/{n}.wret{s}', encoding='utf8').read().strip())
    return '\n'.join(out)


readme = f'''项目七 构建批量信息数组 —— 配套资源（初稿）

学生用/
  书中示例/            书中的例题、四个任务的完整程序（volt8.c、volt38.c、state8.c、state_text.c、repair_list.c）、
                       AI 升华中的 rank_try.c 和 ai_a.c～ai_c.c；eq_str.c、rank_try.c、ai_b.c 能运行，但结果是错的，
                       用来观察现象；同名的 _输入N.txt 是键盘输入数据（含汉字的，在运行窗口中要用中文输入法输入）。
  错误示范（只编译）/  含错误的程序，只用来看编译器的提示，不要照抄。bad_bound.c 是下标越界，编译没有任何提示，
                       但运行的结果不可预料，不要运行。
  待补充练习/          四个任务技能训练 1 的挖空程序，①～③处由学生补充。
教师用/（教师另行获取，不发给学生）
  参考答案/            技能训练、课堂练习编程题、离开 AI 再做、实训巩固编程题的参考程序。
  答案核对/            用来核对课堂练习、测试表、课堂验收和实训巩固答案的程序，书中不出现（mut_ 开头的是课堂验收中“同伴改错”的程序）。
  错误示范（只编译）/  实训巩固找错题（bad_q14.c）和改掉前两处错误后的程序（bad_q14b.c，编译没有任何提示，但仍有两处错误）。
  程序验证记录.txt     每个程序的编译提示、键盘输入、运行输出和返回值（小熊猫C++ 3.4 自带 MinGW-w64 GCC 11.5.0 实测）。
插图原图/              书中 {len(FG)} 幅插图的原图（4 倍分辨率 PNG），可直接用于课件。
图片来源与许可.txt

编译选项与小熊猫C++ 3.4 默认的“MinGW-w64 GCC 11.5.0 64-bit Debug”配置相同（程序中的汉字按 GBK 编码，一个汉字占 2 个字节）：
{CMD}
'''

if os.path.exists(OUT):
    os.remove(OUT)
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr(f'{ROOT}/使用说明.txt', readme)
    rec = ['项目七 程序验证记录', '编译命令：' + CMD, '键盘输入数据以 UTF-8 存放，运行时转换为 GBK 编码送给程序（与在运行窗口中输入汉字相同）。', '']
    for g, d, names in GROUPS:
        rec.append(f'========== {g} ==========')
        for n in names:
            z.write(f'{d}/{n}.c', f'{ROOT}/{g}/{n}.c')
            for i in sorted(glob.glob(f'{d}/{n}.in*')):
                s = i.rsplit('.in', 1)[1]
                z.write(i, f'{ROOT}/{g}/{n}_输入{s or 1}.txt')
            rec.append(record(d, n))
            rec.append('')
    for n, reps in FILLS.items():
        t = open(f'{BOOK}/{n}.c', encoding='utf8').read()
        for a, b in reps:
            assert a in t, (n, a)
            t = fill(t, a, b)
        t, k = re.subn(r'（任务[一二三四] 技能训练 1）', '（待补充）', t, count=1)
        assert k == 1, n
        z.writestr(f'{ROOT}/学生用/待补充练习/{n}_待补充.c', t)
    z.writestr(f'{ROOT}/教师用/程序验证记录.txt', '\n'.join(rec))
    for k in sorted(FG, key=lambda k: int(FG[k].split('-')[1])):
        z.write(f'{FIG}/f_{k}.png', f'{ROOT}/插图原图/{FG[k]}.png')
    have = {f[:-4] for f in os.listdir('assets/fe') if f.endswith('.png')}
    icons = sorted((set(re.findall(r"['\"]([a-z_]+)['\"]", open('figs7.py', encoding='utf8').read()))
                    | set(re.findall(r"ic\('(\w+)'\)", open('content7.py', encoding='utf8').read()))) & have)
    z.writestr(f'{ROOT}/图片来源与许可.txt',
               '彩色 3D 图标：Microsoft Fluent Emoji（github.com/microsoft/fluentui-emoji），MIT 许可，许可全文见下。\n'
               f'本项目用到的图标：{"、".join(icons)}\n'
               '其余电路图、示意图、流程图、漫画中的人物头像为本书自绘。\n\n'
               + open('assets/fe/LICENSE-FluentEmoji-MIT.txt', encoding='utf8').read())
print('res', os.path.getsize(OUT), 'programs', len(all_names))
