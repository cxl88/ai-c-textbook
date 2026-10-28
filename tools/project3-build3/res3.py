# 生成《项目三-配套资源（第三稿）.zip》：程序（4 组）+ 验证记录 + 插图原图 + 运行结果图 + 图片来源与许可。
# 用法：python3 res3.py 已运行过的程序目录（含 .in*/.wdiag/.wout*/.wret*） 图目录(fig) 输出.zip
# 压缩包用 Python zipfile 生成，中文文件名带 UTF-8 标记，Windows 自带解压也不会乱码。
import glob
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
GROUPS = {
    '书中程序': ['avg', 'card', 'login', 'measure', 'resist', 'bad_loop'],
    '算法举例（选看）': ['sum5', 'sum1000', 'sum10000', 'leap', 'gcd'],
    '参考答案': ['sort3', 'door', 'fact10', 'oddeven'],
    '答案核对': ['frag10'],
}
GROUP_NOTE = {
    '书中程序': '4 个例题，任务二任务实施的 resist.c，AI 升华中有意保留死循环的 bad_loop.c（只编译不运行）',
    '算法举例（选看）': '任务一“算法举例”中三个算法的 C 程序，书中只写步骤不写代码，学完任务二后可以对照阅读',
    '参考答案': '技能训练和实训巩固编程题的参考程序',
    '答案核对': '用来核对实训巩固答案的程序，书中不出现',
}
WHERE = {k: v for k, v in EX.items()}
WHERE.update({
    'resist': '任务二 任务实施', 'bad_loop': 'AI 升华：AI 写的程序（漏写 i = i + 1，死循环）',
    'sum5': '算法举例（1）：求 1+2+3+4+5', 'sum1000': '算法举例（1）：加到 1000，只改 N',
    'sum10000': '算法举例（1）：加到 1 万，只改 N', 'leap': '算法举例（2）：判断闰年', 'gcd': '算法举例（3）：辗转相除法求最大公约数',
    'sort3': '任务二 技能训练 2', 'door': '任务二 技能训练 3（密码 203203 为虚构）',
    'fact10': '实训巩固第 9 题', 'oddeven': '实训巩固第 8 题', 'frag10': '实训巩固第 10 题：i 从 0 开始时循环执行几次',
})
FIGS = sorted(FG, key=lambda k: int(FG[k].split('-')[1]))
RUNS = sorted(set(re.findall(r"F\('(run_\w+)'\)", open('content3.py', encoding='utf8').read())))
html = open(f'{FIG}/figs.html', encoding='utf8').read()
FLUENT, UNDRAW = set(), {}
for m in re.finditer(r'<div class="fig" id="f_(\w+)">(.*?)</div>\n', html, re.S):
    if m.group(1) in FG:
        FLUENT.update(re.findall(r'assets/fe/(\w+)\.png', m.group(2)))
        for u in re.findall(r'assets/ud/([\w-]+)\.svg', m.group(2)):
            UNDRAW.setdefault(u, set()).add(FG[m.group(1)])
FLUENT.update(re.findall(r"ic\('(\w+)'\)", open('content3.py', encoding='utf8').read()))
FLUENT = sorted(n for n in FLUENT if os.path.exists(f'assets/fe/{n}.png'))


def diag_lines(name):
    return [ln for ln in open(f'{CODE}/{name}.wdiag', encoding='utf8').read().split('\n')
            if re.match(r'\S+\.c:\d+:\d+: (error|warning|note|fatal error)', ln)]


def runs_of(name):
    """每次运行：(输入文件名或 None, 输出, 返回值)。第 1 次是 .in/.wout/.wret，第 k 次是 .ink/.woutk/.wretk。"""
    out = []
    for k in [''] + [str(i) for i in range(2, 10)]:
        if not os.path.exists(f'{CODE}/{name}.wout{k}'):
            break
        inp = f'{CODE}/{name}.in{k}'
        out.append((inp if os.path.exists(inp) else None,
                    open(f'{CODE}/{name}.wout{k}', encoding='utf8').read().rstrip('\n'),
                    open(f'{CODE}/{name}.wret{k}', encoding='utf8').read().strip()))
    return out


tmp = tempfile.mkdtemp()
root = os.path.join(tmp, 'r')
total = sum(len(v) for v in GROUPS.values())
rec = ['项目三程序验证记录（第三稿，2026-10-28）',
       '环境：Wine 中的小熊猫C++ 3.4 自带 MinGW-w64 GCC 11.5.0；编译选项与小熊猫C++ 默认的 Debug 配置相同：'
       '-finput-charset=UTF-8 -fexec-charset=gbk -g3 -fno-ms-extensions -pipe -Wall -Werror=implicit-int -Werror=return-type -Werror=vla',
       f'程序分 4 组，共 {total} 个：']
for g, names in GROUPS.items():
    rec.append(f'  {g}（{len(names)} 个）：{GROUP_NOTE[g]}。')
rec += ['结果：16 个程序的编译提示均为空。除 bad_loop.c（死循环，只编译不运行）外，15 个程序共运行 25 次，返回值都是 0；'
        '书中的运行结果图由这里的输出生成，键盘输入在图中用下划线标出。有键盘输入的程序，同名的 .in、.in2 等文件就是每次运行用的输入。', '']
n_run = 0
for g, names in GROUPS.items():
    os.makedirs(f'{root}/程序/{g}')
    rec += [f'【{g}】', '']
    for n in names:
        shutil.copy(f'{CODE}/{n}.c', f'{root}/程序/{g}/{n}.c')
        where = f'（{WHERE[n]}）' if n in WHERE else ''
        dl = diag_lines(n)
        assert not dl, (n, dl)
        if n.startswith('bad_'):
            rec += [f'=== {n}.c{where}  编译提示：无', '--- 只编译不运行：循环条件 i <= 5 永远成立，运行后会一直要求输入，要按 Ctrl+C 结束。', '']
            continue
        rec.append(f'=== {n}.c{where}  编译提示：无')
        rs = runs_of(n)
        assert rs, n
        for j, (inp, out, ret) in enumerate(rs, 1):
            assert ret == '0', (n, j, ret)
            if inp:
                shutil.copy(inp, f'{root}/程序/{g}/{os.path.basename(inp)}')
                data = open(inp, encoding='utf8').read().split()
                rec.append(f'--- 第 {j} 次运行，键盘输入：{" ".join(data)}（返回值 {ret}）')
            else:
                rec.append(f'--- 运行（无输入，返回值 {ret}）：')
            rec.append(out)
            n_run += 1
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
shutil.copy('assets/ud/LICENSE-collection-MIT.txt', f'{root}/插图原图/图片来源与许可/')
src = ['项目三第三稿 图片来源与许可（2026-10-28）', '',
       '一、彩色图标：Microsoft Fluent Emoji（3D 版）',
       '来源：https://github.com/microsoft/fluentui-emoji （assets/<名称>/3D/ 下的 PNG）',
       '许可：MIT License，Copyright (c) Microsoft Corporation，全文见 LICENSE-FluentEmoji-MIT.txt。可商用，需保留版权与许可声明。',
       '本项目用到的图标文件名：' + '、'.join(FLUENT), '',
       '二、人物插画：unDraw（https://undraw.co）',
       '取自 https://github.com/balazser/undraw-svg-collection 收录的 SVG，主色由 #6c63ff 改为本书主色 #1D4F91。',
       'unDraw 许可要点：可免费用于商业和非商业用途，无需署名；不得把插画汇编成图库再分发或用于与 unDraw 竞争的服务。收录仓库自身以 MIT 许可发布，见 LICENSE-collection-MIT.txt。',
       '本环境无法直接打开 undraw.co 核对许可原文，出版前请再核一次。',
       '用到的插画：' + '、'.join(f'{u}（{"、".join(sorted(v))}）' for u, v in sorted(UNDRAW.items())) + '。', '',
       f'三、其余插图、流程图、人物头像（小禾、小智，与前几个项目相同）均为本书自绘；{FG["threestr"]} 中的万用表和色环电阻是自绘简笔画。'
       '运行结果图由实测输出生成（文件名与程序名相同）。', '',
       '四、插图原图文件名以图号开头，如“图3-8_f_threestr.png”。']
open(f'{root}/插图原图/图片来源与许可/图片来源与许可.txt', 'w', encoding='utf8', newline='\r\n').write('\n'.join(src) + '\n')
readme = ['项目三 梳理程序执行逻辑 · 配套资源（第三稿，2026-10-28）', '',
          '程序/         4 组共 %d 个 C 程序、键盘输入文件和验证记录.txt（每个程序的编译提示和实测输出）' % total,
          '插图原图/     书中 %d 幅插图的原图（4 倍分辨率，可直接放进课件），以及图片来源与许可' % len(FIGS),
          '运行结果图/   书中 %d 张运行结果图' % len(RUNS), '',
          '程序都在小熊猫C++ 3.4 中实测。源文件为 UTF-8 编码，小熊猫C++ 可直接打开；用其他编辑器时请选择 UTF-8。',
          '“算法举例（选看）”中的程序用到任务二才学的 if、while，学完任务二后再看。',
          'bad_loop.c 有意保留错误（漏写 i = i + 1;），编译没有任何提示，运行后停不下来，用于课堂演示“编译通过不等于程序正确”。']
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
print('programs:', total, 'runs:', n_run, 'figs:', len(FIGS), 'run images:', len(RUNS), 'icons:', len(FLUENT), 'undraw:', sorted(UNDRAW))
