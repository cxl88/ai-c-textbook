# 生成《项目四-配套资源（初稿）.zip》：程序（4 组）+ 验证记录 + 插图原图 + 图片来源与许可。
# 用法：python3 res4.py 已运行过的程序目录(prep_pack.py 的输出，含 .wdiag/.wout/.wret) 图目录(fig) 输出.zip
# 压缩包用 Python zipfile 生成，中文文件名带 UTF-8 标记，Windows 自带解压也不会乱码。
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile

PACK, FIG, OUT = sys.argv[1:4]
N = json.load(open(f'{FIG}/nums.json', encoding='utf8'))
FG, EX = N['fig'], N['ex']
GROUP_ORDER = ['书中示例', '参考答案', '答案核对', '错误示范']
GROUP_NOTE = {
    '书中示例': '14 个例题、两个任务的完整程序 ledger.c 和 ledger2.c、AI 升华最终采用的 fix_scanf.c',
    '参考答案': '技能训练和实训巩固编程题的参考程序 8 个，AI 升华中检验办法②④用的 fix_line.c、fix_twice.c',
    '答案核对': '以 hd_ 开头，用来核对课堂练习、表格和实训巩固的答案，书中不出现',
    '错误示范': '以 bad_ 开头，是书中提到的错误写法，有意保留错误，只编译不运行',
}
WHERE = {k: v for k, v in EX.items()}
WHERE.update({'ledger': '任务一 任务实施', 'ledger2': '任务二 任务实施', 'fix_scanf': 'AI 升华 办法①',
              'ohm': '任务一 技能训练 1', 'ledger_date': '任务一 技能训练 2', 'series': '任务一 技能训练 3',
              'quiz': '任务二 技能训练 1', 'ledger3': '任务二 技能训练 2', 'milktea': '任务二 技能训练 3',
              'elec': '实训巩固第 14 题', 'smd': '实训巩固第 15 题（挑战题）',
              'fix_line': 'AI 升华 办法②', 'fix_twice': 'AI 升华 办法④', 'bad_q12': '实训巩固第 13 题'})
FIGS = sorted(FG, key=lambda k: int(FG[k].split('-')[1]))
FLUENT_USED = sorted(set(re.findall(r"['\"]([a-z_]+)['\"]", open('figs4.py', encoding='utf8').read()))
                     & {f[:-4] for f in os.listdir('assets/fe') if f.endswith('.png')}
                     | set(re.findall(r"ic\('(\w+)'\)", open('content4.py', encoding='utf8').read())))
UNDRAW_USED = ['mobile-login', 'upload', 'order-delivered']

groups = {}
for ln in open(f'{PACK}/groups.txt', encoding='utf8'):
    g, names = ln.rstrip('\n').split('\t')
    groups[g] = names.split()
assert sorted(groups) == sorted(GROUP_ORDER), groups.keys()


def desc(name):
    """程序开头说明注释中“功能：”或“说明：”后面的文字"""
    s = open(f'{PACK}/{name}.c', encoding='utf8').read()
    m = re.search(r'(?:功能|说明)：(.*?)\s*\*/', s, re.S)
    return re.sub(r'\s+', ' ', m.group(1)) if m else ''


def inputs(name):
    out = []
    for f in sorted(os.listdir(PACK)):
        m = re.fullmatch(re.escape(name) + r'\.in(\d?)', f)
        if m:
            out.append((m.group(1), f))
    return sorted(out, key=lambda t: int(t[0] or 1))


def show_input(path):
    """行尾空格看不见，记作 ␣"""
    lines = open(path, encoding='utf8').read().split('\n')
    if lines and lines[-1] == '':
        lines.pop()
    return '\n'.join(re.sub(r' +$', lambda m: '␣' * len(m.group(0)), ln) for ln in lines)


def diag_lines(name):
    return [ln for ln in open(f'{PACK}/{name}.wdiag', encoding='utf8').read().split('\n')
            if re.match(r'\S+\.c:\d+:\d+: (error|warning|note|fatal error)', ln)]


tmp = tempfile.mkdtemp()
root = os.path.join(tmp, 'r')
rec = ['项目四程序验证记录（2026-10-15）',
       '环境：Wine 中的小熊猫C++ 3.4 自带 MinGW-w64 GCC 11.5.0；编译选项与小熊猫C++ 默认的 Debug 配置相同：'
       '-finput-charset=UTF-8 -fexec-charset=gbk -g3 -fno-ms-extensions -pipe -Wall -Werror=implicit-int -Werror=return-type -Werror=vla',
       f'程序分 4 组，共 {sum(len(v) for v in groups.values())} 个：']
for g in GROUP_ORDER:
    rec.append(f'  {g}（{len(groups[g])} 个）：{GROUP_NOTE[g]}。')
rec += ['.in 文件是运行时的键盘输入，.in2、.in3 …… 是第 2、3 …… 次运行的输入。运行时用文件代替键盘输入，输入的内容不会显示出来，所以提示文字和输出连在一行。输入中行尾的 ␣ 表示一个空格。',
        '结果：前三组程序的编译提示均为空、返回值均为 0；书中的运行结果截图由这里的输出生成。错误示范组的编译提示与书中的说法一致。', '']
n_ok = 0
for g in GROUP_ORDER:
    os.makedirs(f'{root}/程序/{g}')
    rec += [f'【{g}】', '']
    for n in groups[g]:
        shutil.copy(f'{PACK}/{n}.c', f'{root}/程序/{g}/{n}.c')
        ins = inputs(n)
        for _, f in ins:
            shutil.copy(f'{PACK}/{f}', f'{root}/程序/{g}/{f}')
        where = f'（{WHERE[n]}）' if n in WHERE else ''
        if g == '错误示范':
            dl = diag_lines(n)
            rec.append(f'=== {n}.c{where}  只编译不运行')
            rec.append(f'说明：{desc(n)}')
            rec.append('--- 编译提示：' + ('' if dl else '无（C 标准没有规定这种写法的行为，编译器发现不了）'))
            rec += dl
            rec.append('')
            continue
        dg = open(f'{PACK}/{n}.wdiag', encoding='utf8').read()
        assert dg == '', (n, dg)
        rec.append(f'=== {n}.c{where}  编译提示：无')
        if g == '答案核对':
            rec.append(f'说明：{desc(n)}')
        runs = [(s, f) for s, f in ins] or [('', None)]
        for s, f in runs:
            ret = open(f'{PACK}/{n}.wret{s}', encoding='utf8').read().strip()
            assert ret == '0', (n, s, ret)
            if f:
                rec.append(f'--- 输入（{f}）：')
                rec.append(show_input(f'{PACK}/{f}'))
            rec.append(f'--- 输出（返回值 {ret}）：')
            rec.append(open(f'{PACK}/{n}.wout{s}', encoding='utf8').read().rstrip('\n'))
        n_ok += 1
        rec.append('')
open(f'{root}/程序/验证记录.txt', 'w', encoding='utf8', newline='\r\n').write('\n'.join(rec) + '\n')

# 插图原图与图片来源
os.makedirs(f'{root}/插图原图/图片来源与许可')
for k in FIGS:
    shutil.copy(f'{FIG}/f_{k}.png', f'{root}/插图原图/f_{k}.png')
shutil.copy('assets/fe/LICENSE-FluentEmoji-MIT.txt', f'{root}/插图原图/图片来源与许可/')
shutil.copy('assets/ud/LICENSE-collection-MIT.txt', f'{root}/插图原图/图片来源与许可/')
src = ['项目四初稿 图片来源与许可（2026-10-15）', '',
       '一、彩色图标：Microsoft Fluent Emoji（3D 版）',
       '来源：https://github.com/microsoft/fluentui-emoji （assets/<名称>/3D/ 下的 PNG）',
       '许可：MIT License，Copyright (c) Microsoft Corporation，全文见 LICENSE-FluentEmoji-MIT.txt。可商用，需保留版权与许可声明。',
       '本项目用到的图标文件名：' + '、'.join(FLUENT_USED),
       f'用在：{FG["scene"]}、{FG["stmt"]}、{FG["io"]}、{FG["printf"]}、{FG["scanf"]}、{FG["kbuf"]}、{FG["status"]}、{FG["getput"]}、{FG["buf2"]}、{FG["comic"]}，以及趣味小站、课堂小游戏、课堂活动的图标。', '',
       '二、人物插画：unDraw（https://undraw.co）',
       '取自 https://github.com/balazser/undraw-svg-collection 收录的 SVG，主色由 #6c63ff 改为本书主色 #1D4F91。',
       'unDraw 许可要点：可免费用于商业和非商业用途，无需署名；不得把插画汇编成图库再分发或用于与 unDraw 竞争的服务。收录仓库自身以 MIT 许可发布，见 LICENSE-collection-MIT.txt。',
       '本环境无法直接打开 undraw.co 核对许可原文，出版前请再核一次。',
       f'用到的插画：{"、".join(UNDRAW_USED)}（均在 {FG["scene"]}）。', '',
       '三、其余插图、流程图、色环电阻和贴片电阻示意图、人物头像（小禾、小智，与书中头像同款）均为本书自绘。', '',
       '四、插图原图文件与图号对照：']
src += [f'{FG[k]}  f_{k}.png' for k in FIGS]
open(f'{root}/插图原图/图片来源与许可/图片来源与许可.txt', 'w', encoding='utf8', newline='\r\n').write('\n'.join(src) + '\n')

# 打包（目录项在前，按路径排序）
if os.path.exists(OUT):
    os.remove(OUT)
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for d, dirs, files in sorted(os.walk(root)):
        dirs.sort()
        rel = os.path.relpath(d, root)
        if rel != '.':
            z.write(d, rel + '/')
        for f in sorted(files):
            z.write(os.path.join(d, f), os.path.join(rel, f) if rel != '.' else f)
shutil.rmtree(tmp)
print('programs:', sum(len(v) for v in groups.values()), 'run ok:', n_ok, 'figs:', len(FIGS), 'icons:', len(FLUENT_USED))
