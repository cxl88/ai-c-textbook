# 把项目四要随配套资源发放的程序整理到一个目录（统一命名、补上说明注释），供 wrun.sh 统一编译运行。
# 用法：python3 prep_pack.py 书中程序目录(p4code) 核对程序目录(p4check) 输出目录
import os
import re
import shutil
import sys

CODE, CHECK, OUT = sys.argv[1:4]
os.makedirs(OUT, exist_ok=True)

# 分组：(组名, [(发放的文件名, 来源目录, 来源名, 新的说明注释或 None 表示原样复制)])
BOOK = ['run', 'stmt', 'assign', 'fmt', 'width', 'indate', 'scanf_msg', 'scanf_nl', 'put', 'get', 'dog',
        'buf', 'buf2', 'signin', 'ledger', 'ledger2', 'fix_scanf']
GROUPS = {
    '书中示例': [(n, CODE, n, None) for n in BOOK],
    '错误示范': [
        ('bad_semi', CODE, 'bad_semi', '漏写分号（任务一 相关知识 2，“注意：别漏写分号”）'),
        ('bad_expr', CHECK, 'bad_expr', '没有作用的表达式语句、字符常量漏写单引号（任务一 相关知识 2；任务二 相关知识 1 “注意”②）'),
        ('bad_order', CHECK, 'bad_order', '语句顺序写反，变量还没有得到值就参加运算（例4-1 之后）'),
        ('bad_lvalue', CODE, 'bad_lvalue', '赋值号左边不是变量（赋值语句的易错点①）'),
        ('bad_init', CODE, 'bad_init', '定义变量时连续赋初值（赋值语句的易错点③）'),
        ('bad_studio', CHECK, 'bad_studio', '把 stdio.h 写成 studio.h（趣味小站“函数名里的秘密”）'),
        ('bad_args', CODE, 'bad_args', 'printf 的格式说明与输出项个数不一致（printf 的常见错误①）'),
        ('bad_type', CODE, 'bad_type', 'printf 的格式说明与数据类型不一致（printf 的常见错误②）'),
        ('bad_upper', CHECK, 'bad_upper', '格式字符写成大写字母（printf 的常见错误③）'),
        ('bad_amp', CODE, 'bad_amp', 'scanf 中变量名前漏写 &（表4-5 第 1 行）'),
        ('bad_lf', CODE, 'bad_lf', 'double 型变量用 %f 输入（表4-5 第 2 行）'),
        ('bad_prec', CODE, 'bad_prec', 'scanf 中规定小数位数（表4-5 第 3 行）'),
        ('bad_multi', CHECK, 'bad_multi', 'putchar 一次输出多个字符（任务二 相关知识 1 “注意”①）'),
        ('bad_ledger_amp', CHECK, 'bad_ledger_amp', 'ledger.c 的 scanf 中删掉一个 &（任务一 课堂验收第 3 项）'),
        ('bad_fflush', CODE, 'bad_fflush', '用 fflush(stdin) 清空输入缓冲区（AI 升华 办法③，C 标准没有规定其行为）'),
        ('bad_q12', CODE, 'bad_q12', None)],
    '参考答案': [
        ('ohm', CODE, 'ohm', None), ('ledger_date', CODE, 'ledger_date', None), ('series', CODE, 'series', None),
        ('quiz', CODE, 'quiz', None), ('ledger3', CODE, 'ledger3', None), ('milktea', CODE, 'milktea', None),
        ('elec', CODE, 'elec', None), ('smd', CODE, 'smd', None),
        ('fix_line', CODE, 'fix_line', None),
        ('fix_twice', CHECK, 'fix_twice', 'AI 升华 办法④：在读走回车符的 getchar(); 后面再加一个 getchar();（用于检验，不采用）')],
    '答案核对': [
        ('hd_assign', CHECK, 'cp1', '任务一 课堂练习（赋值语句）第 1～3 题'),
        ('hd_ops', CHECK, 'cp_ops', '表4-1 复合赋值运算符的结果，以及正文中 %.2f 输出 2.675、-12.8 赋给 int 型变量等结果'),
        ('hd_efmt', CHECK, 'efmt2', '表4-2 中 %e 等格式字符的输出，以及宽度不够时按实际位数输出'),
        ('hd_printf', CHECK, 'cp2', '任务一 课堂练习（printf）第 1～4 题（第 4 题为改正后的写法）'),
        ('hd_scanf_ret', CHECK, 'cp3', '任务一 课堂练习（scanf）第 1 题，输入 12 abc'),
        ('hd_scanf_comma', CHECK, 'cp3b', '任务一 课堂练习（scanf）第 2 题，依次输入 3,5、3 5、3, 5、3 ,5'),
        ('hd_ledger_lines', CODE, 'ledger', '任务一 任务实施“试一试”：5 个阻值分 5 行输入（程序与 ledger.c 相同，只换了输入）'),
        ('hd_getchar', CHECK, 'cp4', '任务二 课堂练习（字符输入输出）第 1、2 题，输入 abc'),
        ('hd_getchar2', CHECK, 'q8', '任务二 课堂练习第 3 题、实训巩固第 8 题，输入 a 后按 Enter'),
        ('hd_scanf_getchar', CHECK, 'cp5', '任务二 课堂练习（字符输入输出）第 4 题，输入 5 后按 Enter'),
        ('hd_age_a', CHECK, 'cp6a', '任务二 课堂练习（两类函数比较）第 2 题写法 A'),
        ('hd_age_b', CHECK, 'cp6b', '任务二 课堂练习（两类函数比较）第 2 题写法 B'),
        ('hd_signin2', CHECK, 'signin2', '任务二 课堂练习（两类函数比较）第 3 题：先输入座位号、再输入组别'),
        ('hd_gg5_6', CHECK, 'q5', '实训巩固第 5、6 题'),
        ('hd_gg12', CHECK, 'q11', '实训巩固第 12 题'),
        ('hd_gg13', CHECK, 'q12', '实训巩固第 13 题改正后的程序')],
}
INPUTS = {'hd_ledger_lines': (CHECK, 'ledger_nl')}  # 输入文件另取


def header(name, text, grp):
    kind = {'错误示范': '（错误示范，只编译不运行）', '答案核对': '（核对答案用）'}.get(grp, '')
    return f'/* 程序名：{name}.c{kind}\n   {"说明" if kind else "功能"}：{text} */\n'


for grp, items in GROUPS.items():
    for new, src_dir, old, note in items:
        s = open(f'{src_dir}/{old}.c', encoding='utf8').read()
        if note:
            s = re.sub(r'\A/\*.*?\*/\n', '', s, flags=re.S)  # 去掉原有的说明注释
            s = header(new, note, grp) + s
        open(f'{OUT}/{new}.c', 'w', encoding='utf8').write(s)
        idir, iname = INPUTS.get(new, (src_dir, old))
        for f in os.listdir(idir):
            m = re.fullmatch(re.escape(iname) + r'\.in(\d?)', f)
            if m:
                shutil.copy(f'{idir}/{f}', f'{OUT}/{new}.in{m.group(1)}')
open(f'{OUT}/groups.txt', 'w', encoding='utf8').write(
    '\n'.join(f'{g}\t' + ' '.join(n for n, *_ in items) for g, items in GROUPS.items()) + '\n')
print(' '.join(n for items in GROUPS.values() for n, *_ in items))
