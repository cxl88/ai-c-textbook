# 生成《项目五-配套资源（初稿）.zip》：程序（分组）+ 待补充练习 + 程序验证记录 + 插图原图 + 图片来源与许可。
# 用法：python3 res5.py 书中程序目录 核对程序目录 图目录(fig) 输出.zip   （两个程序目录都已用 wrun.sh 运行过）
# 压缩包用 Python zipfile 生成，中文文件名带 UTF-8 标记，Windows 自带解压也不会乱码。
import glob
import json
import os
import re
import sys
import zipfile

BOOK, CHECK, FIG, OUT = sys.argv[1:5]
N = json.load(open(f'{FIG}/nums.json', encoding='utf8'))
FG = N['fig']
ROOT = '项目五-配套资源（初稿）'

# 分组：组名 -> (目录, [程序名]) ；学生用的放“学生用”，答案和核对程序放“教师用”
GROUPS = [
    ('学生用/书中示例', BOOK, ['battery', 'exam', 'room_temp', 'rel', 'range_trap', 'logic', 'current', 'semi_if', 'brace_if',
                         'assign_if', 'volt1', 'resok', 'grade', 'grade_bad', 'zone', 'zone_nobreak', 'grade_sw', 'volt2a',
                         'volt2', 'login2', 'dangling', 'vmax', 'avg_guard', 'season', 'volt3', 'ai_a', 'ai_b', 'ai_c']),
    ('学生用/书中示例', CHECK, ['three_if', 'dangling_fix']),          # 正文中写明“见配套资源”
    ('学生用/错误示范（只编译）', BOOK, ['bad_else', 'bad_switch_f']),
    ('学生用/错误示范（只编译）', CHECK, ['bad_div0']),
    ('教师用/参考答案', BOOK, ['charge', 'volt1_const', 'env', 'soc', 'volt2b', 'repair', 'charge_pile', 'volt3b', 'aircon']),
    ('教师用/参考答案', CHECK, ['abs_n', 'leap5', 'kwh', 'grade_sw2', 'nest_ok', 'fix_q14', 'chartype', 'max3', 'ladder_bill']),
    ('教师用/答案核对', CHECK, ['fl_eq', 'cp_rel', 'cp_logic', 'cp_if', 'cp_oddeven', 'cp_grade', 'cp_order', 'cp_zone_c', 'cp_sw105',
                          'cp_login', 'cp_nest', 'cp_dangling25', 'mut_volt1', 'mut_volt2', 'mut_volt3', 'cp_q', 'cp_q13']),
    ('教师用/错误示范（只编译）', CHECK, ['bad_case', 'bad_q14', 'bad_q14b', 'bad_q14c', 'bad_q14d']),
]
# 学生用的待补充练习：与书中技能训练 1 相同的挖空版
FILLS = {'charge': [('&t', '___①___'), ('t < 0 || t > 45', '___②___'), ('printf("检测完毕。\\n");', '___③___;')],
         'soc': [('if (soc >= 80)', 'if (___①___)'), ('else if (soc >= 20)', '___②___ (soc >= 20)'), ('\n    else\n', '\n    ___③___\n')],
         'charge_pile': [("gun == 'Y'", '___①___'), ('scanf("%d", &soc);', '___②___;'), ('soc < 100', '___③___')]}

all_names = [n for _, _, ns in GROUPS for n in ns]
assert len(all_names) == len(set(all_names))
found = {os.path.basename(f)[:-2] for d in (BOOK, CHECK) for f in glob.glob(f'{d}/*.c')}
assert set(all_names) == found, (found - set(all_names), set(all_names) - found)

CMD = ('gcc.exe 程序名.c -o 程序名.exe -finput-charset=UTF-8 -fexec-charset=gbk -g3 -fno-ms-extensions -pipe -Wall '
       '-Werror=implicit-int -Werror=return-type -Werror=vla')


def record(d, n):
    """一个程序的验证记录：编译提示、每次运行的输入、输出和返回值"""
    out = [f'■ {n}.c', '编译提示：' + (open(f'{d}/{n}.wdiag', encoding='utf8').read().strip() or '（无）')]
    if n.startswith('bad_'):
        out.append('（含编译错误或未定义行为，只编译、不运行）')
    for w in sorted(glob.glob(f'{d}/{n}.wout*')):
        s = w.rsplit('.wout', 1)[1]
        inp = f'{d}/{n}.in{s}'
        out.append(f'—— 第 {s or 1} 次运行　键盘输入：' + (open(inp, encoding='utf8').read().strip().replace('\n', ' ⏎ ') + ' ⏎' if os.path.exists(inp) else '（无）'))
        out.append(open(w, encoding='utf8').read().rstrip())
        out.append('返回值：' + open(f'{d}/{n}.wret{s}', encoding='utf8').read().strip())
    return '\n'.join(out)


readme = f'''项目五 判断场景分支路径 —— 配套资源（初稿）

学生用/
  书中示例/            书中的例题、三个任务的完整程序（volt1.c、volt2a.c、volt2.c、volt3.c）、AI 升华中的 ai_a.c～ai_c.c，
                       以及演示易错点的 range_trap.c、semi_if.c、brace_if.c、assign_if.c、grade_bad.c、zone_nobreak.c、dangling.c、three_if.c
                       （这几个程序能运行，但结果是错的，用来观察现象）、dangling.c 加花括号后的 dangling_fix.c；同名的 .txt 是键盘输入数据。
  错误示范（只编译）/  含编译错误的程序，只用来看编译器的提示，不要运行，也不要照抄。
  待补充练习/          三个任务技能训练 1 的挖空程序，①～③处由学生补充。
教师用/（教师另行获取，不发给学生）
  参考答案/            技能训练、课堂练习编程题、离开 AI 再做、实训巩固编程题的参考程序。
  答案核对/            用来核对课堂练习、课堂验收和实训巩固答案的程序，书中不出现。
  错误示范（只编译）/  课堂练习、短路求值和实训巩固找错题中提到的错误写法。
  程序验证记录.txt     每个程序的编译提示、键盘输入、运行输出和返回值（小熊猫C++ 3.4 自带 MinGW-w64 GCC 11.5.0 实测）。
插图原图/              书中 {len(FG)} 幅插图的原图（4 倍分辨率 PNG），可直接用于课件。
图片来源与许可.txt

编译选项与小熊猫C++ 3.4 默认的“MinGW-w64 GCC 11.5.0 64-bit Debug”配置相同：
{CMD}
'''

if os.path.exists(OUT):
    os.remove(OUT)
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr(f'{ROOT}/使用说明.txt', readme)
    rec = ['项目五 程序验证记录', '编译命令：' + CMD, '']
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
            t = t.replace(a, b, 1)
        z.writestr(f'{ROOT}/学生用/待补充练习/{n}_待补充.c', t)
    z.writestr(f'{ROOT}/教师用/程序验证记录.txt', '\n'.join(rec))
    for k in sorted(FG, key=lambda k: int(FG[k].split('-')[1])):
        z.write(f'{FIG}/f_{k}.png', f'{ROOT}/插图原图/{FG[k]}.png')
    have = {f[:-4] for f in os.listdir('assets/fe') if f.endswith('.png')}
    icons = sorted((set(re.findall(r"['\"]([a-z_]+)['\"]", open('figs5.py', encoding='utf8').read()))
                    | set(re.findall(r"ic\('(\w+)'\)", open('content5.py', encoding='utf8').read()))) & have)
    z.writestr(f'{ROOT}/图片来源与许可.txt',
               '彩色 3D 图标：Microsoft Fluent Emoji（github.com/microsoft/fluentui-emoji），MIT 许可，许可全文见下。\n'
               f'本项目用到的图标：{"、".join(icons)}\n'
               '其余流程图、示意图、数轴、漫画中的人物头像为本书自绘。\n\n'
               + open('assets/fe/LICENSE-FluentEmoji-MIT.txt', encoding='utf8').read())
print('res', os.path.getsize(OUT), 'programs', len(all_names))
