# 生成《项目五-编写说明与参考答案》。用法：python3 notes5.py 输出.docx fig/nums.json 书中程序目录 核对程序目录
# 参考答案中的运行结果都从实测输出 .wout 中读取并断言核对（chk），答案与实测不符时脚本报错，不会生成文档。
import json
import os
import sys
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.oxml.ns import qn

OUT = sys.argv[1]
N = json.load(open(sys.argv[2], encoding='utf8'))
BOOK, CHECK = sys.argv[3:5]
FG, TB, EX = N['fig'], N['tab'], N['ex']
PAGES = 0
if os.path.exists('build/p5.pdf'):
    from pypdf import PdfReader
    PAGES = len(PdfReader('build/p5.pdf').pages)


def wo(name, s=''):
    for d in (BOOK, CHECK):
        f = f'{d}/{name}.wout{s}'
        if os.path.exists(f):
            return open(f, encoding='utf8').read()
    raise FileNotFoundError(name + s)


NCHK = [0]


def chk(name, s, *texts):
    """断言实测输出中含有这些文字"""
    w = wo(name, s)
    for t in texts:
        assert t in w, (name, s, t, w)
        NCHK[0] += 1


def diag(name):
    for d in (BOOK, CHECK):
        f = f'{d}/{name}.wdiag'
        if os.path.exists(f):
            return open(f, encoding='utf8').read()
    raise FileNotFoundError(name)


d = Document()
for sec in d.sections:
    sec.page_width, sec.page_height = Cm(21), Cm(29.7)
    sec.left_margin = sec.right_margin = Cm(2.2)
st = d.styles['Normal']
st.font.name = 'Times New Roman'
st.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
st.font.size = Pt(10.5)
for s in ('Heading 1', 'Heading 2', 'Title'):
    d.styles[s].font.color.rgb = RGBColor(0x1D, 0x4F, 0x91)
    d.styles[s].element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')


def h(t, lv=1):
    d.add_heading(t, lv)


def p(t):
    d.add_paragraph(t)


def li(t):
    d.add_paragraph(t, style='List Bullet')


def tbl(rows, widths=None):
    t = d.add_table(rows=len(rows), cols=len(rows[0]))
    t.style = 'Table Grid'
    if widths:
        t.autofit = False
        for j, w in enumerate(widths):
            t.columns[j].width = Cm(w)
    for i, r in enumerate(rows):
        for j, c in enumerate(r):
            cell = t.cell(i, j)
            cell.text = c
            if widths:
                cell.width = Cm(widths[j])
            for para in cell.paragraphs:
                for run in para.runs:
                    run.font.size = Pt(9.5)
                    run.bold = i == 0
    d.add_paragraph()


nf, nt, ne = len(FG), len(TB), len(EX)
d.add_heading('项目五 判断场景分支路径 —— 编写说明与参考答案', 0)
p('供主编、作者和任课教师使用，不随学生用书发放。初稿，2026-11-10。')

h('零、本稿概况')
li('依据：客户框架《5项目五 判断场景分支路径.docx》（8 条批注，另附一张“综合示例要点”参考图）；体例、版式与项目二修订稿、项目三第三稿、项目四初稿一致（人物林小禾、C老师、小智；栏目、编号格式“1. /（1）/①”、程序书写风格相同）。')
li(f'规模：预览 PDF {PAGES} 页；图 {nf} 幅（图5-1～{FG["comic"]}），表 {nt} 个（表5-1～{TB["aitest"]}），例题 {ne} 个（例5-1～{EX["season"]}）；课堂练习 7 组 24 题，课堂活动 2 个，趣味小站 3 个，AI 助学卡 4 张，每个任务有技能训练 3 题和课堂验收 3 项，实训巩固 17 题（第 17 题为挑战题）。')
li('程序：书中程序 39 个、核对与参考程序 34 个，共 73 个，全部在小熊猫C++ 3.4 自带的 MinGW-w64 GCC 11.5.0 中实测（见第三部分）；书中运行结果截图由实测输出生成，书中引用的编译器提示都取自实际编译结果。代码只用 stdio.h。')
li('四色印刷：彩色图标取自 Microsoft Fluent Emoji（MIT 许可），其余插图为本书自绘，版面主色仍为 #1D4F91。')

h('参考课时（建议）')
tbl([['内容', '课时', '课堂组织建议'],
     ['情境导入；任务一 相关知识 1～3（选择结构示例、关系运算符、逻辑运算符）', '2', f'先看{FG["scene"]}，让学生说出 21.5 V 属于哪种状态；三个示例只要求看懂执行流程；“真假站队”放在逻辑运算符之后，约 5 分钟'],
     ['任务一 相关知识 4（单分支 if 语句）、任务实施、技能训练、课堂验收', '2', f'{EX["semi_if"]}～{EX["assign_if"]} 先让学生预测输出再运行；上机写 volt1.c 并按{TB["test1"]} 测 6 组数据，训练 3 可留作课后作业'],
     ['任务二 相关知识 1～2（if…else、if…else if…else 语句）', '2', f'{EX["grade_bad"]} 先让学生预测 95 分的输出；闰年练习可分组完成后用 leap5.c 核对'],
     ['任务二 相关知识 3（switch 语句）、任务实施、技能训练、课堂验收', '2', f'对照{FG["switch"]} 讲 break 和 case 穿透；上机先写 volt2a.c 再写 volt2.c，按{TB["test2"]} 测试'],
     ['任务三 相关知识 1～2（if 嵌套、悬空 else、综合示例）', '2', f'“我是编译器”放在{EX["dangling"]} 之后，约 6 分钟；综合示例（1）（3）可让学生课前自学'],
     ['任务三 任务实施、技能训练、课堂验收', '1', f'上机改出 volt3.c，按{TB["test3"]} 测 7 组数据'],
     ['AI 升华、项目小结、实训巩固', '1', '分组用 7 组边界数据检验 ai_a.c～ai_c.c，填写表5-12；实训巩固作为课后作业'],
     ['合计', '12', '课时紧张时可压缩到 10 课时：综合示例（1）（3）和任务二的 switch 例题只演示不上机，技能训练第 3 题都留作课后作业']], [6.2, 1.2, 9.2])

h('一、编写依据与对客户框架的落实')
tbl([['客户框架 / 批注', '书中落实'],
     ['情境导入（批注：文字多少可以适当调整）', f'原文保留，只把单位写法统一为“15 V”“15～21 V”；配{FG["scene"]}（实训台 + 判定标准标尺）；加小禾、C老师、小智三人对话，与前几个项目一致'],
     ['三维目标（批注：最后根据内容确定）', '按成稿内容写出知识目标 6 条、能力目标 6 条、素养目标 4 条'],
     ['知识导图（批注：最后根据内容手绘）', f'按成稿内容绘制{FG["kmap"]}（与项目四同风格）；作者如需手绘，可按其节点重画'],
     ['任务一 任务描述、任务分析', f'原文保留；配{FG["zone1"]} 电压数轴（标出 20 V、22 V 和边界 15、21）；任务分析用“输入、处理、输出”表格；补趣味小站“额定电压为什么是 18 V”'],
     ['相关知识 1. 选择结构示例（单分支、双分支、多分支各一个，总结三种形式）', f'{EX["battery"]} 电量提醒、{EX["exam"]} 考核是否通过、{EX["room_temp"]} 温度提示；{FG["forms"]} 和{TB["forms3"]} 从“条件判断”“执行流程”两方面总结'],
     ['2. 关系运算符与关系表达式（优先级、结合性、小示例）', f'{TB["relop"]}；{EX["rel"]} 输出关系表达式的值；优先级、结合性分条讲；{EX["range_trap"]} 说明数学写法 15≤v≤21 不能直接写进程序（附编译器的两条警告）；易错点 3 条'],
     ['3. 逻辑运算符与逻辑表达式（优先级、结合性、真值表、组合条件怎样解读）', f'{TB["logop"]}、{TB["truth"]} 真值表、{EX["logic"]} 上机验证真值表；{FG["prec"]} 左边是优先级阶梯，右边按步骤解读 v < 15 || v > 21；补 ! 的圆括号不能省的说明；“真假站队”活动'],
     ['4. 单分支 if 语句（语法、执行过程，从条件和执行语句两个维度说明，易错点）', f'{FG["ifsyn"]}；“①条件 ②执行语句”两个维度；{EX["current"]} 表笔接反提醒；易错点用 3 个能运行但结果错的程序演示：多写分号（{EX["semi_if"]}）、漏写花括号（{EX["brace_if"]}）、= 与 ==（{EX["assign_if"]}），都附实际的编译警告'],
     ['批注（3 处）：相关知识中举题目，供课堂练习', '任务一 3 组 12 题、任务二 3 组 9 题、任务三 1 组 3 题，共 7 组 24 题，答案见第四部分'],
     ['任务一 任务实施：第一步程序框架、第二步定义变量（批注：根据本任务的变量修改）、第三步、完整程序', f'框架中的“第一个电阻阻值 r1、第二个电阻阻值 r2”（沿用自项目四）改为本任务的“测得的电压 v”（{TB["vars1"]}，类型一栏留给学生填）；第三步给出代码片段；完整程序 volt1.c 两次运行；补{TB["test1"]} 边界值测试（实际输出一栏由学生填写）'],
     ['任务一 技能训练', '补充完整（蓄电池充电保护）→ 改一项需求（用符号常量 VMIN、VMAX）→ 独立完成（实训室环境监测）；课堂验收 3 项'],
     ['任务二 任务描述、任务分析（两处不足）', f'原文保留，配{FG["zone2"]}；两处不足各一张“处理、输出”表'],
     ['相关知识 1. if…else 语句', f'格式、{FG["ifelse"]}、{EX["resok"]} 电阻是否合格（4.7 kΩ ±5%）、易错点 3 条（含 bad_else.c 的报错）；课堂练习含项目三的闰年算法'],
     ['2. if…else if…else 语句', f'格式、{FG["ladder"]}、{EX["grade"]} 考核等级（说明“后面的条件隐含前面的条件都不成立”）、{EX["grade_bad"]} 条件顺序写反'],
     ['3. switch 语句（与 if…else if…else 的使用区别）', f'格式、{EX["zone"]} 实训区查询、{EX["zone_nobreak"]} 漏写 break、{FG["switch"]} 有无 break 对比、{EX["grade_sw"]} 用整数除法把成绩归类并共用语句；使用规则 4 条（含 switch 不能判断实型，附 bad_switch_f.c 的报错）；{TB["cmpsw"]} 比较两种语句，并说明电压判断为什么不用 switch；趣味小站“一个 break，让电话网瘫痪 9 小时”'],
     ['任务二 任务实施：第一处不足（if…else）、第二处不足（if…else if…else）、完整程序', f'先改出 volt2a.c 并运行验证，再改出 volt2.c；{FG["flow2"]}；{TB["test2"]} 测试 5 组数据'],
     ['任务二 技能训练', '补充完整（储能电池电量分级）→ 改一项需求（欠压时组件进入待机）→ 独立完成（设备报修菜单，用 switch）；课堂验收 3 项'],
     ['任务三 任务描述、任务分析', f'原文保留，配{FG["zone3"]}'],
     ['相关知识 1. if 嵌套', f'格式、{EX["login2"]}（由项目三的 login.c 改写，先核对账号再核对密码）、{FG["nest"]}；悬空 else 单列一小节：{EX["dangling"]}（附 -Wdangling-else 警告）、{FG["pair"]}、规范 4 条、课堂活动“我是编译器”'],
     ['2. 选择结构综合示例（批注参考图的 5 个要点）', f'①悬空 else：见上；②条件运算符：{EX["vmax"]}；③switch 细节（break、穿透、default、只能匹配整型和字符型、电压为什么不用 switch）：任务二已详讲，综合示例再用{EX["season"]} 演示 switch 与 if 配合、共用语句；④短路求值：{EX["avg_guard"]}（避免除数为 0）；⑤可读性规范：两种写法对比 + {TB["read"]}'],
     ['任务三 任务实施（框架写“在任务一程序的基础上补充”）', f'按任务描述改为在任务二程序 volt2.c 的基础上补充（见第二部分）；分两步：确定嵌套位置、写内层条件；{FG["flow3"]} 标出新增部分；{TB["test3"]} 测 7 组数据'],
     ['任务三 技能训练', '补充完整（充电桩启动判断）→ 改一项需求（紧急过压时输出超出值）→ 独立完成（实训室空调自动控制）；课堂验收 3 项'],
     ['项目小结（框架只给标题）', f'按三个任务小结，{TB["evo"]} 比较三个任务的程序，附 7 条自查清单'],
     ['AI升华（框架只给标题）', f'“用边界值检验 AI 写的程序”：四要素提问 → AI 给出三种写法并声称“结果完全相同” → 设计 7 组边界数据逐个检验（{TB["aitest"]}）→ 写法②（转成整数用 switch、GCC 扩展 case 范围）和写法③（< 与 <= 写错）各错 2 组 → 采用写法① → 四格漫画（{FG["comic"]}）→ AI 使用小结 → 离开 AI 再做']], [6, 10.6])
p('框架之外，按前几个项目的体例补充了：小智提示、注意、趣味小站 3 个、AI 助学卡 4 张、课堂活动 2 个、课堂验收、实训巩固 17 题。')

h('二、需要主编或作者确认的事项')
li('客户原文的技术性修改：① 任务三任务实施框架写“在任务一程序的基础上补充”，与任务三任务描述（在任务二的三种状态上细分过压）不符，书中改为“在任务二程序 volt2.c 的基础上”；② 第二步定义变量的示例表沿用了项目四的“电阻阻值 r1、r2”，按批注改为本任务的电压 v；③ 程序框架写作 #include<stdio.h>、int main()，书中与全书一致写作 #include <stdio.h>、int main(void)。')
li('文字规范：单位统一写作“22 V”“15～21 V”（数字与单位之间加空格，与前几个项目一致）；“第三部”改为“第三步”；任务二任务描述中“一处是……二是……”改为“一是……二是……”；客户原文“输出提示：电压异常，请检查光伏组件！。”去掉多余的句号，程序输出的 6 句提示与原文一字不差。')
li('需要实训指导书或作者核实的教学设定：蓄电池温度 0～45 ℃ 时才能充电（任务一技能训练 1）、组件平均功率低于 80 W 提醒清洁（例5-20）、储能电池电量分级 80%/20%（任务二技能训练 1）、阶梯电价的分档和单价（课堂练习、挑战题，已注明“教学模拟”）。书中都写成“实训规定”或“教学模拟”，不作为行业标准。')
li('趣味小站中的技术数据：晶体硅电池片工作电压约 0.5 V、开路电压约 0.6 V，36 片串联约 18 V / 21.6 V，温度越低电压越高；AT&T 1990 年 1 月 15 日长途电话网瘫痪约 9 小时、起因是一条放错位置的 break。均为公开资料中的常见说法，如嫌后者篇幅大，可删去不影响正文。')
li('术语：“case 穿透”也有教材称为“贯穿”“落空”，可按全书统一；“悬空 else”沿用通行叫法。')
li('与前面项目的衔接（依据项目二修订稿、项目三第三稿、项目四初稿）：项目二——字符按 ASCII 码比较、整数除法只取整数部分、(int) 舍去小数、符号常量 #define、布尔型 _Bool、附录B 运算符优先级表；项目三——选择结构的流程图、login.c、判断闰年的算法；项目四——空语句、复合语句、getchar。前面项目定稿时如有改动，这些地方要同步检查。')
li('非标准写法只作反例：AI 升华中写法② 的 case 15 ... 21 是 GCC 扩展，本书环境编译时没有任何提示，书中明确说明“不是标准 C 语言，不采用”。')
li('学习层级标签：项目二修订稿、项目三第三稿都没有使用“必会/跟着用/选学”标签，本项目保持一致，只在“实数不用 == 比较”一处注明“选学”。')
li('运行结果截图：与项目三、四一致，只显示程序输出（带下划线的是键盘输入）。')
li(f'版式：预览 PDF 由 LibreOffice 渲染（{PAGES} 页），Word 中打开分页会略有不同。数据表格设为表头行跨页重复、8 行以内的短表整表不跨页；程序跨页沿用 v4 规则（20 行以内整段，更长的只在空行处分段）。')

h('三、程序验证')
p('73 个程序分 5 组放在配套资源中（另由参考答案挖空生成“待补充练习”3 个）：学生用的“书中示例”30 个（含正文中提到的 three_if.c、dangling_fix.c）、“错误示范（只编译）”3 个；教师用的“参考答案”18 个、“答案核对”17 个、“错误示范（只编译）”5 个。全部在小熊猫C++ 3.4 自带的 MinGW-w64 GCC 11.5.0（默认 Debug 编译选项，含 -Wall）下编译，能运行的都按配套的键盘输入运行，返回值都是 0。每个程序的编译提示、输入、输出见“程序验证记录.txt”。')
p('编译时有警告或错误的程序都是有意的错误示范，书中引用的提示均取自实际编译结果：')
for n, what in [('range_trap', '15 <= v <= 21'), ('semi_if', 'if 后多写分号'), ('brace_if', '漏写花括号'), ('assign_if', '= 与 =='),
                ('dangling', '悬空 else'), ('bad_else', 'else 前没有配对的 if'), ('bad_switch_f', 'switch 判断实型'),
                ('bad_case', 'case 后写变量条件、实型常量'), ('bad_q14', '实训巩固找错题')]:
    lines = [ln for ln in diag(n).split('\n') if 'error' in ln or 'warning' in ln]
    li(f'{n}.c（{what}）：' + '；'.join(ln.split(': ', 1)[1] for ln in lines[:3]))
p('其余程序（含 ai_b.c 中的 GCC 扩展写法 case 15 ... 21）编译时没有任何提示。说明：在 Wine 中运行的批处理里，以 if_ 开头的程序名会被 cmd 误当作 if 命令，所以三个易错点程序命名为 semi_if、brace_if、assign_if；学生在小熊猫C++ 中使用不受影响。')

h('四、参考答案')
h('任务一 · 课堂练习（关系运算符）', 2)
chk('cp_rel', '', '第1题：0 1 1 1 1', '第2题：0', 'x = 1')
li('1. ① 0　② 1　③ 1　④ 1　⑤ 1（\'a\' 的 ASCII 码 97 大于 \'B\' 的 66）。')
li('2. 值为 0：先算 10 > 5 得 1，再算 1 > 2 得 0（编译时有警告 comparisons like \'X<=Y<=Z\' do not have their mathematical meaning）。')
li('3. ① i != 0　② score >= 60　③ c == \'Y\'')
li('4. x 为 1：关系运算符的优先级高于赋值运算符，先算 3 > 2 得 1，再赋给 x。')
h('任务一 · 课堂练习（逻辑运算符）与课堂活动“真假站队”', 2)
chk('cp_logic', '', '第1题：1 0 1 0', 'v=18 时 0')
li('1. ① 1　② 0　③ 1　④ 0')
li('2. ① t >= 18 && t <= 26　② soc < 20 || soc > 95　③ c != \'Y\' && c != \'N\'')
li('3. v < 15 的值为 0，v > 21 的值为 0，0 || 0 的值为 0。')
li('4. 对（cp_logic.c 用 14、15、21、22、30 五个电压实测，两个表达式的值都相同）。')
li('真假站队：14、22、30 时 v < 15 || v > 21 为 1，15、21 时为 0；v >= 15 && v <= 21 正好相反，因为两个条件互为“反面”。')
h('任务一 · 课堂练习（单分支 if 语句）', 2)
chk('cp_if', '', 'x 为 5 时：AB', 'x 为 1 时：B')
li('1. x 为 5 时输出 AB，x 为 1 时输出 B（if 只控制 printf("A");）。')
li('2. 条件后面多写了分号，if 只控制空语句，不论成绩多少都输出“请参加补考”。去掉分号即可。')
li('3. 改为 if (c == \'Y\') printf("已确认\\n");')
chk('abs_n', '', '绝对值：7')
li('4. 参考程序 abs_n.c：if (n < 0) { n = -n; }，输入 −7 输出 7。')
h('任务一 · 任务实施与技能训练', 2)
for s in ('', '2', '3', '4', '5', '6'):
    wo('volt1', s)
chk('volt1', '', '电压异常')
chk('volt1', '5', '电压异常')
chk('volt1', '6', '电压异常')
for s in ('2', '3', '4'):
    assert '电压异常' not in wo('volt1', s)
li(f'{TB["test1"]} 实测：22、14.9、21.1 输出提示；20、15、21 不输出。')
li('第二步定义变量：float v;（电压可能带小数，不能用 int 型）。')
chk('charge', '', '暂停充电', '检测完毕')
chk('charge', '3', '检测完毕')
assert '暂停' not in wo('charge', '3') and '暂停' not in wo('charge', '4')
li('训练 1：① &t　② t < 0 || t > 45　③ printf("检测完毕。\\n")。再测一测：输入 0 和 45 时都只输出“检测完毕。”（0 和 45 都在允许范围内）。')
chk('volt1_const', '', '（正常区间：15～21 V）')
li('训练 2：参考程序 volt1_const.c：#define VMIN 15、#define VMAX 21，条件改为 v < VMIN || v > VMAX，异常时再输出 printf("（正常区间：%d～%d V）\\n", VMIN, VMAX);')
chk('env', '', '环境异常')
li('训练 3：参考程序 env.c：if (t > 30 || h > 70) 输出提示，最后输出温度和湿度；输入 28 75 时输出提示（湿度超标），输入 26 55 时不输出提示。')
h('任务一 · 课堂验收', 2)
li('1. < <= > >= == !=；! && ||。与：全真才真；或：一真即真；非：真假颠倒。')
li('2. v >= 15 && v <= 21；v < 15 || v > 21（或 !(v >= 15 && v <= 21)）。15 <= v <= 21 先算 15 <= v 得 0 或 1，再与 21 比较，总是成立。')
chk('mut_volt1', '', '电压异常')
li('3. 改成 v >= 21 后，输入 21（上边界，应不输出）时输出了“电压异常……”，只有测试数据 21 能暴露这个错误（mut_volt1.c 实测）。')

h('任务二 · 课堂练习（if…else 语句）', 2)
chk('cp_oddeven', '', '奇数\n偶数')
li('1. x 为 7 时输出“奇数”，x 为 10 时输出“偶数”。')
li('2. 效果相同。② 更好：只判断一次，而且 if…else 保证两条路必走其一、只走其一；① 要判断两次，两个条件写得不互补时还可能都输出或都不输出。')
for s, t in (('', '2024 年是闰年'), ('2', '1900 年不是闰年'), ('3', '2000 年是闰年'), ('4', '2026 年不是闰年')):
    chk('leap5', s, t)
li('3. if ((year % 4 == 0 && year % 100 != 0) || year % 400 == 0) 输出闰年，else 输出不是闰年（参考程序 leap5.c）。实测：2024 是，1900 不是，2000 是，2026 不是。')
h('任务二 · 课堂练习（if…else if…else 语句）', 2)
chk('cp_grade', '', '优秀')
chk('cp_grade', '2', '良好')
chk('cp_grade', '3', '不合格')
li('1. 100 → 优秀，80 → 良好，59 → 不合格。')
chk('cp_order', '', '暖')
li('2. 有问题。输入 35 时输出“暖”：35 满足第一个条件 t > 20，后面被跳过，“热”永远不会被输出。应把 t > 30 写在前面。')
for s, t in (('', '第一档'), ('2', '第二档'), ('3', '第二档'), ('4', '第三档')):
    chk('kwh', s, t)
li('3. if (kwh <= 200) 第一档；else if (kwh <= 400) 第二档；else 第三档（参考程序 kwh.c，200、201、400、401 四个边界实测正确）。')
h('任务二 · 课堂练习（switch 语句）', 2)
chk('cp_zone_c', '', 'C 区', 'D 区', '没有这个实训区')
li('1. 输出三行：C 区：光伏发电实训、D 区：智能控制实训、没有这个实训区，请检查输入。')
li('2. ① switch 后面的表达式 v 是实型，case 后面的 18.0 也是实型常量，都不允许；② case 后面不能写变量和条件。编译实测（bad_case.c）：' + '；'.join(ln.split('error: ', 1)[1] for ln in diag('bad_case').split('\n') if 'error:' in ln))
chk('cp_sw105', '', '优秀')
chk('grade_sw2', '', '成绩输入有误')
li('3. 输出“优秀”：105 / 10 得 10，进入 case 10。改进：先用 if (score < 0 || score > 100) 检查成绩，有效时再用 switch（参考程序 grade_sw2.c，与例5-21 的做法相同）。')
h('任务二 · 任务实施与技能训练', 2)
for s, t in (('', '欠压'), ('2', '电压正常'), ('3', '电压正常'), ('4', '电压正常'), ('5', '请注意过压')):
    chk('volt2', s, t)
li(f'{TB["test2"]} 实测：12 欠压；15、18、21 正常；22 过压。')
chk('three_if', '', '欠压', '电压正常')
li('小智提示中“第二个条件照抄成 v <= 21”的情况，three_if.c 实测输入 12 时同时输出“欠压”和“正常”。')
chk('soc', '3', '电量不足')
li('训练 1：① soc >= 80　② else if　③ else（参考程序 soc.c）。')
chk('volt2b', '', '组件进入待机')
li('训练 2：在 if (v < 15) 的花括号中，“欠压”那一行的后面加 printf("组件进入待机。\\n");，原来已经有花括号，不用再加（参考程序 volt2b.c）。')
chk('repair', '', '8001')
chk('repair', '3', '代码有误')
li('训练 3：参考程序 repair.c：case 1: case 2: 共用“信息中心”的语句，case 3、case 4 各一段，default 提示代码有误。')
h('任务二 · 课堂验收', 2)
li('1. 从上到下依次判断，执行第一个成立的条件对应的分支，其余跳过；都不成立时执行 else。能判断到第 18 行，说明 v < 15 不成立，v 一定不小于 15，所以只写 v <= 21 就表示 15～21 V。')
chk('mut_volt2', '', '欠压')
li('2. 改成 v <= 15 后，输入 15（下边界，应为正常）时输出了“欠压……”，测试数据 15 暴露了错误（mut_volt2.c 实测）。')
li('3. break：跳出 switch 语句；default：表达式的值与所有 case 常量都不相等时执行。电压是实型，又要按范围判断，switch 语句都做不到。')

h('任务三 · 课堂练习（if 嵌套）与课堂活动', 2)
chk('cp_login', '', '密码错误')
li('1. 输出“密码错误，请重新输入。”')
chk('cp_nest', '', '第2题 x=5：2', '第2题 x=-5：0', '第3题 x=5：0', '第3题 x=-5：2', 'x = 0')
li('2. x 为 5 时输出 2，x 为 −5 时输出 0：else 与 if (x > 10) 配对。')
li('3. 加花括号后：x 为 5 时输出 0，x 为 −5 时输出 2。')
li('课堂活动“我是编译器”：else 与 if (b > 0) 配对；a 为 −1 时外层条件不成立，x 不变，仍为 0。')
h('任务三 · 任务实施与技能训练', 2)
for s, t in (('', '欠压'), ('2', '电压正常'), ('3', '电压正常'), ('4', '及时核查'), ('5', '及时核查'), ('6', '紧急告警'), ('7', '紧急告警')):
    chk('volt3', s, t)
li(f'{TB["test3"]} 实测：12 欠压；18、21 正常；21.5、24 过压并核查；24.5、30 过压并紧急告警。')
chk('charge_pile', '', '开始充电')
chk('charge_pile', '2', '请先插好充电枪')
li('训练 1：① gun == \'Y\'　② scanf("%d", &soc)　③ soc < 100（参考程序 charge_pile.c）。')
chk('volt3b', '', '超出 24 V 共 6.0 V')
li('训练 2：在 v > 24 的分支中加 printf("超出 24 V 共 %.1f V。\\n", v - 24);（参考程序 volt3b.c）。')
chk('aircon', '', '制冷')
chk('aircon', '2', '待机')
chk('aircon', '3', '空调关闭')
li('训练 3：参考程序 aircon.c：外层判断 someone == \'Y\'，内层用 if…else if…else 判断温度。')
h('任务三 · 课堂验收', 2)
li('1. else 总是与前面最近的、尚未配对的 if 配对；dangling.c 第 14 行的 else 与第 12 行的 if (v > 24) 配对。')
chk('mut_volt3', '', '紧急告警')
li('2. 改成 v < 24 后，输入 24（预警的上边界）时输出了“紧急告警……”，测试数据 24 暴露了错误（mut_volt3.c 实测）。')
li('3. m = a < b ? a : b;。&& 从左到右计算，n 为 0 时 n != 0 为假，后面的 total / n 不再计算；交换顺序后会先做除数为 0 的整数除法（未定义行为，bad_div0.c 只编译不运行）。')

h('AI 升华 · 表5-12 的依据与离开 AI 再做', 2)
T7 = ['14.9', '15', '21', '21.5', '24', '24.5', '30']
want = ['欠压', '电压正常', '电压正常', '及时核查', '及时核查', '紧急告警', '紧急告警']
ok = {}
for n in ('ai_a', 'ai_b', 'ai_c', 'nest_ok'):
    ok[n] = [want[i] in wo(n, '' if i == 0 else str(i + 1)) for i in range(7)]
assert all(ok['ai_a']) and all(ok['nest_ok'])
assert [T7[i] for i in range(7) if not ok['ai_b'][i]] == ['21.5', '24.5']
assert [T7[i] for i in range(7) if not ok['ai_c'][i]] == ['21', '24']
li('ai_a.c 7 组全部正确；ai_b.c 在 21.5、24.5 出错；ai_c.c 在 21、24 出错（逐组实测，见程序验证记录）。')
chk('cp_dangling25', '', '紧急告警')
li('离开 AI 再做 ①：dangling.c 输入 25 时输出“紧急告警，立即停机保护！”（外层、内层条件都成立）。')
chk('dangling_fix', '', '紧急告警')
chk('dangling_fix', '3', '没有过压')
assert wo('dangling_fix', '2').strip().endswith('：')
li('② 参考程序 dangling_fix.c（花括号见图5-15（b））；测试数据可选 25（紧急告警）、22（不输出）、18（没有过压）。')
li('③ 参考程序 nest_ok.c：把写法③的 v < 21、v < 24 改为 v <= 21、v <= 24，7 组数据全部正确。')

h('实训巩固', 2)
chk('cp_q', '', '第2题：1', '第6题：1', '第8题：3', '第10题：3')
li('1. √　2. ×（3 < 5 得 1，1 < 2 得 1，值为 1）　3. ×　4. ×（与前面最近的、尚未配对的 if 配对）　5. ×（只给出警告，后面紧跟 else 时才会报错）')
li('6. B　7. C　8. C　9. A　10. D')
li('11. 1，0；非 0，0。　12. !，||。')
for s, t in (('', 'C'), ('2', 'B'), ('3', 'A')):
    chk('cp_q13', s, t)
li('13. x 为 5 时输出 C，15 时输出 B，25 时输出 A。')
chk('fix_q14', '', '制冷')
chk('fix_q14', '2', '制热')
chk('fix_q14', '3', '待机')
for _n, _t in (('bad_q14', "expected '(' before 't'"), ('bad_q14b', "expected expression before '<' token"),
               ('bad_q14c', "'elseif' undeclared"), ('bad_q14d', "expected ';' before '}' token")):
    assert _t in diag(_n), (_n, _t)
li('14. 4 处错误：① if t > 26 要写成 if (t > 26)；② =< 要写成 <=；③ elseif 要写成 else；④ printf("空调：待机\\n") 后面漏写分号。改正后的程序 fix_q14.c 输入 28、15、22 分别输出制冷、制热、待机。编译器一次不一定能报出全部错误（bad_q14b.c～bad_q14d.c 逐处改正后实测）：第一次只报第 1 处 expected \'(\' before \'t\'；改正后报出 =< 和 elseif；再改正 =< 后只剩 elseif；改正 elseif 后，才报出第 4 处漏写的分号 expected \';\' before \'}\' token。讲评时可借此说明：改一处、编译一次，直到没有错误。')
for s, t in (('', '大写字母'), ('2', '小写字母'), ('3', '数字字符'), ('4', '其他字符')):
    chk('chartype', s, t)
li('15. 参考程序 chartype.c：依次判断 c >= \'A\' && c <= \'Z\'、c >= \'a\' && c <= \'z\'、c >= \'0\' && c <= \'9\'，其余为其他字符（G、g、7、# 实测正确）。')
chk('max3', '', '最大的数：9')
chk('max3', '2', '最大的数：7')
li('16. 参考程序 max3.c：max = a > b ? a : b; if (c > max) max = c;（3 9 5 → 9，7 2 7 → 7）。')
for s, t in (('', '84.00'), ('2', '173.00'), ('3', '277.00')):
    chk('ladder_bill', s, t)
li('17. 参考程序 ladder_bill.c：if (kwh <= 200) fee = kwh * 0.56; else if (kwh <= 400) fee = 200 * 0.56 + (kwh - 200) * 0.61; else fee = 200 * 0.56 + 200 * 0.61 + (kwh - 400) * 0.86;。实测：150 度 84.00 元，300 度 173.00 元，450 度 277.00 元。')
d.save(OUT)
open('build/asserts.txt', 'w').write(str(NCHK[0]))
print('notes ok', PAGES, 'asserts', NCHK[0])
