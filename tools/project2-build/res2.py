# 生成《项目二-配套资源.zip》：程序（4 组）+ 验证记录 + 插图原图 + 运行结果图 + 图片来源与许可。
# 用法：python3 res2.py 已运行过的程序目录（含 .wdiag/.wout/.wret） 图目录(fig) 输出.zip
# 压缩包用 Python zipfile 生成，中文文件名带 UTF-8 标记，Windows 自带解压也不会乱码。
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile

CODE, FIG, OUT = sys.argv[1:4]
N = json.load(open(f'{FIG}/nums.json', encoding='utf8'))
FG, EX = N['fig'], N['ex']
EXP = {'const': 'const_demo', 'var': 'var_demo', 'size': 'size_demo', 'float': 'float_demo', 'char': 'char_code',
       'strlen': 'str_len', 'arith': 'arith', 'group': 'group', 'incdec': 'incdec', 'assign': 'assign_expr',
       'convert': 'convert', 'div': 'div_test', 'prec': 'prec'}
GROUPS = {
    '书中程序': [EXP[k] for k in EX] + ['lab', 'alarm', 'usage', 'digit', 'usage2', 'ai_try4', 'ai_try5', 'ai_try5ok', 'predict'],
    '参考答案': ['room204', 'room204b', 'avg_temp', 'decode', 'zone', 'group_fill', 'group_fill6', 'volt_dev', 'bill',
             'fix_204', 'q18_fix', 'q19', 'q20'],
    '答案核对': ['answers', 'octal', 'define_semi', 'alarm_k'],
    '错误示范': ['bad_usage', 'bad_204', 'bad_204b', 'bad_q18', 'bad_strchar', 'bad_mod', 'bad_lvalue'],
}
GROUP_NOTE = {
    '书中程序': '13 个例题，三个任务的完整程序 lab.c、alarm.c、usage.c，任务二训练 2 的 digit.c，AI 升华中的 usage2.c、ai_try4.c、ai_try5.c、ai_try5ok.c，实训巩固第 17 题的 predict.c',
    '参考答案': '技能训练、离开 AI 再做和实训巩固编程题的参考程序',
    '答案核对': '用来核对课堂练习、“注意”框和实训巩固答案的程序，书中不出现',
    '错误示范': '以 bad_ 开头，是书中提到的错误写法，有意保留错误，只编译不运行',
}
WHERE = {EXP[k]: v for k, v in EX.items()}
WHERE.update({
    'lab': '任务一 完整程序', 'alarm': '任务二 完整程序', 'usage': '任务三 完整程序', 'digit': '任务二 技能训练 2',
    'usage2': 'AI 升华：按编译提示改正后的第二稿', 'ai_try4': 'AI 升华：检验建议④', 'ai_try5': 'AI 升华：检验建议⑤（35 人）',
    'ai_try5ok': 'AI 升华：自己的改法（35 人）', 'predict': '实训巩固第 17 题',
    'room204': '任务一 技能训练 1', 'room204b': '任务一 技能训练 1“再改一项需求”', 'avg_temp': '任务一 技能训练 2',
    'decode': '任务二 技能训练 1', 'zone': '任务二 技能训练 3', 'group_fill': '任务三 技能训练 1',
    'group_fill6': '任务三 技能训练 1“再改一项需求”', 'volt_dev': '任务三 技能训练 2', 'bill': '任务三 技能训练 3',
    'fix_204': 'AI 升华“离开 AI 再做”', 'q18_fix': '实训巩固第 18 题', 'q19': '实训巩固第 19 题', 'q20': '实训巩固第 20 题（挑战题）',
    'answers': '课堂练习和实训巩固中的表达式题', 'octal': '任务一“注意”框第①条：0203 是八进制数',
    'define_semi': '任务一“注意”框第②条：#define 末尾加分号', 'alarm_k': '任务二 课堂验收第 1 项：k 加密后是 L',
    'bad_usage': 'AI 升华：小禾的初稿', 'bad_204': 'AI 升华“离开 AI 再做”', 'bad_204b': 'bad_204.c 补上分号后的样子',
    'bad_q18': '实训巩固第 18 题', 'bad_strchar': '任务二“注意：\'g\' 和 \"g\" 不能混用”', 'bad_mod': '任务三：% 的两边必须是整数',
    'bad_lvalue': '任务三：自增运算和赋值号左边必须是变量',
})
FIGS = sorted(FG, key=lambda k: int(FG[k].split('-')[1]))
RUNS = sorted(set(re.findall(r"F\('(run_\w+)'\)", open('content2.py', encoding='utf8').read())))
FLUENT_USED = sorted({n for n in re.findall(r"['\"]([a-z_0-9]+)['\"]", open('figs2.py', encoding='utf8').read() +
                                             open('content2.py', encoding='utf8').read())
                      if os.path.exists(f'assets/fe/{n}.png')})


def diag_lines(name):
    return [ln for ln in open(f'{CODE}/{name}.wdiag', encoding='utf8').read().split('\n')
            if re.match(r'\S+\.c:\d+:\d+: (error|warning|note|fatal error)', ln)]


tmp = tempfile.mkdtemp()
root = os.path.join(tmp, 'r')
total = sum(len(v) for v in GROUPS.values())
rec = ['项目二程序验证记录（2026-10-19）',
       '环境：Wine 中的小熊猫C++ 3.4 自带 MinGW-w64 GCC 11.5.0；编译选项与小熊猫C++ 默认的 Debug 配置相同：'
       '-finput-charset=UTF-8 -fexec-charset=gbk -g3 -fno-ms-extensions -pipe -Wall -Werror=implicit-int -Werror=return-type -Werror=vla',
       f'程序分 4 组，共 {total} 个：']
for g, names in GROUPS.items():
    rec.append(f'  {g}（{len(names)} 个）：{GROUP_NOTE[g]}。')
rec += ['结果：前三组程序的返回值均为 0，除 define_semi.c 故意演示的 1 条警告外，编译提示均为空；书中的运行结果图由这里的输出生成。错误示范组的编译提示与书中的说法一致。', '']
n_ok = 0
for g, names in GROUPS.items():
    os.makedirs(f'{root}/程序/{g}')
    rec += [f'【{g}】', '']
    for n in names:
        shutil.copy(f'{CODE}/{n}.c', f'{root}/程序/{g}/{n}.c')
        where = f'（{WHERE[n]}）' if n in WHERE else ''
        dl = diag_lines(n)
        if g == '错误示范':
            rec.append(f'=== {n}.c{where}  只编译不运行')
            rec.append('--- 编译提示：' + ('' if dl else '无'))
            rec += dl
            rec.append('')
            continue
        assert not dl or n == 'define_semi', (n, dl)
        rec.append(f'=== {n}.c{where}  编译提示：' + ('无' if not dl else ''))
        rec += dl
        ret = open(f'{CODE}/{n}.wret', encoding='utf8').read().strip()
        assert ret == '0', (n, ret)
        rec.append(f'--- 输出（返回值 {ret}）：')
        rec.append(open(f'{CODE}/{n}.wout', encoding='utf8').read().rstrip('\n'))
        n_ok += 1
        rec.append('')
open(f'{root}/程序/验证记录.txt', 'w', encoding='utf8', newline='\r\n').write('\n'.join(rec) + '\n')

# 插图原图、运行结果图与图片来源
os.makedirs(f'{root}/插图原图/图片来源与许可')
os.makedirs(f'{root}/运行结果图')
for k in FIGS:
    shutil.copy(f'{FIG}/f_{k}.png', f'{root}/插图原图/{FG[k]}_f_{k}.png')
for r in RUNS:
    shutil.copy(f'{FIG}/{r}.png', f'{root}/运行结果图/{r[4:]}.png')
shutil.copy('assets/fe/LICENSE-FluentEmoji-MIT.txt', f'{root}/插图原图/图片来源与许可/')
src = ['项目二 图片来源与许可（2026-10-19）', '',
       '一、彩色图标：Microsoft Fluent Emoji（3D 版）',
       '来源：https://github.com/microsoft/fluentui-emoji （assets/<名称>/3D/ 下的 PNG）',
       '许可：MIT License，Copyright (c) Microsoft Corporation，全文见 LICENSE-FluentEmoji-MIT.txt。可商用，需保留版权与许可声明。',
       '本项目用到的图标文件名：' + '、'.join(FLUENT_USED), '',
       f'二、{FG["charmem"]}、{FG["ascii"]}、{FG["strmem"]} 沿用作者新稿中的插图。', '',
       '三、其余插图、人物头像（小禾、C老师、小智，与前几个项目相同）均为本书自绘；运行结果图由实测输出生成（文件名与程序名相同）。', '',
       '四、插图原图文件名以图号开头，如“图2-3_f_var.png”。']
open(f'{root}/插图原图/图片来源与许可/图片来源与许可.txt', 'w', encoding='utf8', newline='\r\n').write('\n'.join(src) + '\n')
readme = ['项目二 读懂身边多样数据 · 配套资源（2026-10-19）', '',
          '程序/         4 组共 %d 个 C 程序和验证记录.txt（每个程序的编译提示和实测输出）' % total,
          '插图原图/     书中 %d 幅插图的原图（4 倍分辨率，可直接放进课件），以及图片来源与许可' % len(FIGS),
          '运行结果图/   书中 %d 张运行结果图' % len(RUNS), '',
          '程序都在小熊猫C++ 3.4 中实测。源文件为 UTF-8 编码，小熊猫C++ 可直接打开；用其他编辑器时请选择 UTF-8。',
          '“错误示范”中的程序有意保留错误，用于课堂演示编译提示，编译时出现错误或警告是正常的。']
open(f'{root}/说明.txt', 'w', encoding='utf8', newline='\r\n').write('\n'.join(readme) + '\n')

if os.path.exists(OUT):
    os.remove(OUT)
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for dd, dirs, files in sorted(os.walk(root)):
        dirs.sort()
        rel = os.path.relpath(dd, root)
        if rel != '.':
            z.write(dd, rel + '/')
        for f in sorted(files):
            z.write(os.path.join(dd, f), os.path.join(rel, f) if rel != '.' else f)
shutil.rmtree(tmp)
print('programs:', total, 'run ok:', n_ok, 'figs:', len(FIGS), 'runs:', len(RUNS), 'icons:', len(FLUENT_USED))
