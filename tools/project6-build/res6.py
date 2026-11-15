# 生成《项目六-配套资源（初稿）.zip》：程序（分组）+ 待补充练习 + 程序验证记录 + 插图原图 + 图片来源与许可。
# 用法：python3 res6.py 书中程序目录 核对程序目录 图目录(fig) 输出.zip   （两个程序目录都已用 wrun.sh 运行过，死循环另用 wcap.sh）
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
ROOT = '项目六-配套资源（初稿）'

# 分组：组名 -> (目录, [程序名]) ；学生用的放“学生用”，答案和核对程序放“教师用”
GROUPS = [
    ('学生用/书中示例', BOOK, ['sum_while', 'sum_do', 'sum_n', 'fold', 'digits', 'lamp1', 'sum_for', 'fact', 'semi_for', 'grid',
                         'mul9', 'row1', 'lamp2', 'prime', 'switch_loop', 'skip3', 'bc', 'fib', 'chicken', 'lamp3_try',
                         'lamp3', 'ai_a', 'ai_b', 'ai_c']),
    ('学生用/书中示例', CHECK, ['digits_w', 'lamp1_while', 'cp_chick', 'ai_a2']),     # 正文中写明“见配套资源”
    ('学生用/错误示范（只编译）', BOOK, ['bad_wsemi']),
    ('学生用/错误示范（只编译）', CHECK, ['bad_nosum', 'bad_dosemi', 'bad_comma', 'bad_brk', 'bad_cont', 'bad_wcont']),
    ('教师用/参考答案', BOOK, ['odd_sum', 'lamp1_cnt', 'res_avg', 'res_sum', 'lamp2_rc', 'triangle', 'pwd3', 'lamp3_cnt', 'avg_valid']),
    ('教师用/参考答案', CHECK, ['even_sum', 'cp_sum3', 'mul99', 'ai_a_code', 'fix_q14', 'harmonic', 'narc', 'hail']),
    ('教师用/答案核对', CHECK, ['cp_while', 'cp_moon', 'cp_dowhile', 'mut_lamp1', 'cp_for', 'cp_nest', 'mut_lamp2', 'cp_brk',
                          'cp_prime', 'cp_t3', 'cp_nz3', 'mut_lamp3', 'cp_l3', 'cp_q', 'cp_q13', 'harm_int']),
    ('教师用/错误示范（只编译）', CHECK, ['bad_nobrace', 'bad_q14', 'bad_q14b', 'bad_q14c', 'bad_q14d']),
]
# 学生用的待补充练习：与书中技能训练 1 相同的挖空版（替换后行尾注释仍对齐在原来的列）
FILLS = {'odd_sum': [('i = 1;', 'i = ___①___;'), ('i <= 99', '___②___'), ('i = i + 2;', '___③___;')],
         'res_sum': [('i = 1; i <= 5; i++', '___①___; ___②___; i++'), ('total = total + r;', '___③___;')],
         'pwd3': [('i <= 3; i++', '___①___; i++'), ('break;', '___②___;'), ('if (i > 3)', 'if (___③___)')]}

all_names = [n for _, _, ns in GROUPS for n in ns]
assert len(all_names) == len(set(all_names))
found = {os.path.basename(f)[:-2] for d in (BOOK, CHECK) for f in glob.glob(f'{d}/*.c')}
assert set(all_names) == found, (found - set(all_names), set(all_names) - found)

CMD = ('gcc.exe 程序名.c -o 程序名.exe -finput-charset=UTF-8 -fexec-charset=gbk -g3 -fno-ms-extensions -pipe -Wall '
       '-Werror=implicit-int -Werror=return-type -Werror=vla')


def fill(text, old, new):
    """与 content6.py 的 fill 相同：把 old 换成 new，行尾注释仍对齐在原来的列（汉字占 2 列）"""
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
    """一个程序的验证记录：编译提示、每次运行的输入、输出和返回值；死循环附限时运行记录"""
    out = [f'■ {n}.c', '编译提示：' + (open(f'{d}/{n}.wdiag', encoding='utf8').read().strip() or '（无）')]
    if n.startswith('bad_'):
        out.append('（错误示范：只编译、不按普通程序运行）')
    for w in sorted(glob.glob(f'{d}/{n}.wout*')):
        s = w.rsplit('.wout', 1)[1]
        out.append(f'—— 第 {s or 1} 次运行　键盘输入：' + keys(f'{d}/{n}.in{s}'))
        out.append(open(w, encoding='utf8').read().rstrip())
        out.append('返回值：' + open(f'{d}/{n}.wret{s}', encoding='utf8').read().strip())
    if os.path.exists(f'{d}/{n}.wcapret'):
        st = open(f'{d}/{n}.wcapret', encoding='utf8').read().split()
        assert st[0] == 'timeout', (n, st)
        out.append(f'—— 限时运行　键盘输入：{keys(f"{d}/{n}.cin")}')
        out.append(f'运行 {st[1][:-1]} 秒仍未结束，被强制结束（停不下来）；此前共输出 {st[-2][6:]} 行、{st[-1][6:]} 字节。开头的输出：')
        out.append(open(f'{d}/{n}.wcap', encoding='utf8').read().rstrip() or '（没有输出）')
    return '\n'.join(out)


readme = f'''项目六 编写重复操作流程 —— 配套资源（初稿）

学生用/
  书中示例/            书中的例题、三个任务的完整程序（lamp1.c、row1.c、lamp2.c、lamp3.c）、任务三的“先试一试”lamp3_try.c、
                       AI 升华中的 ai_a.c～ai_c.c 和 ai_a2.c，以及正文中提到的 digits_w.c、lamp1_while.c、cp_chick.c；
                       semi_for.c、switch_loop.c、digits_w.c、lamp3_try.c 能运行，但结果是错的，用来观察现象；同名的 .txt 是键盘输入数据。
  错误示范（只编译）/  含错误的程序，只用来看编译器的提示，不要照抄。其中 bad_wsemi.c、bad_wcont.c 是死循环，
                       运行后停不下来，要按 Ctrl+C 或关闭运行窗口结束。
  待补充练习/          三个任务技能训练 1 的挖空程序，①～③处由学生补充。
教师用/（教师另行获取，不发给学生）
  参考答案/            技能训练、课堂练习编程题、离开 AI 再做、实训巩固编程题的参考程序。
  答案核对/            用来核对课堂练习、课堂验收和实训巩固答案的程序，书中不出现（mut_ 开头的是课堂验收中“同伴改错”的程序）。
  错误示范（只编译）/  课堂练习和实训巩固找错题中的错误写法（bad_nobrace.c 是死循环）。
  程序验证记录.txt     每个程序的编译提示、键盘输入、运行输出和返回值（小熊猫C++ 3.4 自带 MinGW-w64 GCC 11.5.0 实测）；
                       停不下来的程序附限时运行 5 秒的记录。
插图原图/              书中 {len(FG)} 幅插图的原图（4 倍分辨率 PNG），可直接用于课件。
图片来源与许可.txt

编译选项与小熊猫C++ 3.4 默认的“MinGW-w64 GCC 11.5.0 64-bit Debug”配置相同：
{CMD}
'''

if os.path.exists(OUT):
    os.remove(OUT)
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr(f'{ROOT}/使用说明.txt', readme)
    rec = ['项目六 程序验证记录', '编译命令：' + CMD, '']
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
        t = re.sub(r'（任务[一二三] 技能训练 1）', '（待补充）', t, count=1)
        z.writestr(f'{ROOT}/学生用/待补充练习/{n}_待补充.c', t)
    z.writestr(f'{ROOT}/教师用/程序验证记录.txt', '\n'.join(rec))
    for k in sorted(FG, key=lambda k: int(FG[k].split('-')[1])):
        z.write(f'{FIG}/f_{k}.png', f'{ROOT}/插图原图/{FG[k]}.png')
    have = {f[:-4] for f in os.listdir('assets/fe') if f.endswith('.png')}
    icons = sorted((set(re.findall(r"['\"]([a-z_]+)['\"]", open('figs6.py', encoding='utf8').read()))
                    | set(re.findall(r"ic\('(\w+)'\)", open('content6.py', encoding='utf8').read()))) & have)
    z.writestr(f'{ROOT}/图片来源与许可.txt',
               '彩色 3D 图标：Microsoft Fluent Emoji（github.com/microsoft/fluentui-emoji），MIT 许可，许可全文见下。\n'
               f'本项目用到的图标：{"、".join(icons)}\n'
               '其余流程图、示意图、漫画中的人物头像为本书自绘。\n\n'
               + open('assets/fe/LICENSE-FluentEmoji-MIT.txt', encoding='utf8').read())
print('res', os.path.getsize(OUT), 'programs', len(all_names))
