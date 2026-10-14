#!/usr/bin/env python3
"""生成教师用《参考答案与评分说明》（A4，PDF）。

用法：python3 teacher_doc.py [补充验证目录]（一般由 pack.py 调用）
  页码取自 out/body.pdf（印刷版正文页码），图表编号取自 out/body.html；
  程序的编译提示和运行结果取自 code/ 和补充验证目录（check/ 中的程序重新运行后的结果），不手写。
输出：out/teacher.html、out/teacher.pdf
"""
import html, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent
CODE, CHECK, OUT = ROOT / "code", ROOT / "check", ROOT / "out"
BOOK = "人工智能助力C语言程序设计（项目一～项目二）"
esc = html.escape

# check/ 中的程序：用于核对参考答案的改动版本（只改了说明中的一处，其余与书中程序相同）
CHECK_INFO = {
    "bad_ex125": ("项目一任务二", "课堂练习第 5 题的程序（原样）"),
    "bad_ex125b": ("项目一任务二", "课堂练习第 5 题：只改正第 4 行后再编译"),
    "profile19": ("项目一任务二", "课堂验收：profile.c 第 7 行年龄改为 19"),
    "bad_profile14": ("项目一任务三", "课堂验收：删去 profile.c 第 14 行末尾的分号"),
    "lab48": ("项目二任务一", "课堂验收：lab.c 第 10 行在室人数改为 48"),
    "alarm_k": ("项目二任务二", "课堂验收：alarm.c 输入告警字母 k（输入1）和 Z（输入2）"),
    "scanf_eof": ("项目二任务三", "例2-7 scanf_types.c 遇到输入结束：输入1 为空，输入2 为 Ctrl+Z 回车，输入3 为 36 回车后 Ctrl+Z 回车"),
    "lab210_40": ("项目二任务三", "训练 3：lab210.c 在室人数改为 40"),
    "lab210_0": ("项目二任务三", "训练 3：lab210.c 在室人数改为 0"),
    "labfull48": ("项目二任务三", "课堂验收：lab_full.c 在室人数改为 48"),
    "labfull0": ("项目二任务三", "课堂验收：lab_full.c 在室人数改为 0"),
}


def squash(s):
    return re.sub(r"[\s\u2060]+", "", s)


class Book:
    """正文页码与图表编号"""
    def __init__(self):
        t = subprocess.run(["pdftotext", "-layout", str(OUT / "body.pdf"), "-"], capture_output=True, text=True, check=True).stdout
        self.sq = [squash(p) for p in t.split("\f")]
        h = (OUT / "body.html").read_text(encoding="utf-8").replace("\u2060", "")
        self.caps = [(n, re.sub(r"<[^>]+>", "", t).strip()) for n, t in
                     re.findall(r'<(?:p class="tcap"|figcaption)><b>([表图]\d+-\d+)</b>(.*?)</(?:p|figcaption)>', h)]

    def pg(self, text, after=1):
        p = squash(text)
        for i in range(after - 1, len(self.sq)):
            if p in self.sq[i]:
                return i + 1
        raise SystemExit(f"正文中找不到：{text}")

    def all(self, text):
        p = squash(text)
        return [i + 1 for i, s in enumerate(self.sq) if p in s]

    def cap(self, title, k=0):
        hit = [n for n, t in self.caps if t == title]
        if len(hit) <= k:
            raise SystemExit(f"找不到图表：{title}")
        return hit[k]


def rd(d, name, ext):
    return (d / f"{name}.{ext}").read_text(encoding="utf-8")


def out(name, s="", d=CODE, prompt=None):
    o = rd(d, name, f"wout{s}")
    if prompt:
        assert o.startswith(prompt), (name, o[:40])
        o = o[len(prompt):]
    return o.rstrip("\n")


def run(text, label=None):
    return f'<div class="run">{f"<div class=rl>{esc(label)}</div>" if label else ""}<pre>{esc(text)}</pre></div>'


def listing(name, d=CODE):
    lines = rd(d, name, "c").rstrip("\n").split("\n")
    return '<pre class="src">' + "\n".join(f'<span class="ln">{i:>2}</span>  {esc(l)}' for i, l in enumerate(lines, 1)) + "</pre>"


def table(head, rows, widths=None, cls=""):
    w = widths or [None] * len(head)
    th = "".join(f'<th{f" style=width:{x}" if x else ""}>{h}</th>' for h, x in zip(head, w))
    return f'<table class="{cls}"><thead><tr>{th}</tr></thead><tbody>' + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table>"


def c(s):
    return f"<code>{esc(s)}</code>"


def keep(*parts):
    return '<div class="keep">' + "".join(parts) + "</div>"


def score_sheet(items):
    head = ["序号", "学号", "姓名"] + [f"{n}<br>（{v}）" for n, v in items] + ["总分", "达标"]
    rows = [[str(i)] + [""] * (len(head) - 1) for i in range(1, 16)]
    return table(head, rows, cls="sheet long")


def build(check_dir=CHECK):
    b = Book()
    K = pathlib.Path(check_dir)
    p2 = b.pg("项目二读懂身边多样数据")
    ex, acc = b.all("课堂练习"), b.all("课堂验收（任务")
    assert len(ex) == 6 and len(acc) == 6, (ex, acc)
    P = {   # 正文页码
        "e11": ex[0], "e12": ex[1], "e13": ex[2], "e21": ex[3], "e22": ex[4], "e23": ex[5],
        "a11": acc[0], "a12": acc[1], "a13": acc[2], "a21": acc[3], "a22": acc[4], "a23": acc[5],
        "slip": b.pg("补充完整：新生报到凭条"),
        "slip2": b.pg("改一项需求。完成训练1后"), "club": b.pg("独立完成：社团活动通知"),
        "run": b.pg("上机运行报到凭条程序"), "ev1": b.pg("项目一评价表"), "solo1": b.pg("新建profile8.c"),
        "seat": b.pg("204实训室空座位统计", p2), "avg": b.pg("浮点型数据：计算平均温度", p2),
        "dec": b.pg("字符型数据：后台还原告警字母", p2), "digit": b.pg("数字字符与整数。阅读下面的程序", p2),
        "zone": b.pg("独立完成：楼层区号换码", p2), "fix": b.pg("205实训室数据诊断。", p2),
        "pv": b.pg("为光伏电站的数据选择类型", p2), "l210": b.pg("独立完成：210实训室数据档案", p2),
        "ev2": b.pg("项目二评价表", p2), "solo2": b.pg("独立诊断下面的程序bad_204.c", p2),
    }
    F = {   # 图表编号
        "slip": b.cap("报到凭条的预期运行结果"), "club": b.cap("社团活动通知的预期运行结果"),
        "card": b.cap("个人专属档案卡片的运行结果"), "rec1": b.cap("个人专属档案程序运行记录"),
        "rec_slip": b.cap("报到凭条程序运行记录"), "ev1": b.cap("项目一评价表"), "card7": b.cap("七项信息的个人专属档案卡片"),
        "seat": b.cap("训练 1 的预期运行结果", 0), "avg": b.cap("训练 2 的预期运行结果"), "dec": b.cap("训练 1 的预期运行结果", 1),
        "alarm": b.cap("告警字母与故障类型"), "zone": b.cap("训练 3 的预期运行结果（输入 c）"),
        "range": b.cap("常用数据类型的取值范围（本书环境）"), "l210": b.cap("训练 3 的预期运行结果"),
        "dict": b.cap("修改后的数据字典"), "kind": b.cap("三类问题的发现和处理方法"), "diag": b.cap("异常诊断记录"),
        "labin": b.cap("lab_input.c 测试记录"), "ev2": b.cap("项目二评价表"),
    }
    order = ["e11", "a11", "e12", "slip", "slip2", "club", "a12", "e13", "run", "a13", "ev1", "solo1",
             "e21", "seat", "avg", "a21", "e22", "dec", "digit", "zone", "a22", "e23", "fix", "pv", "l210", "a23", "ev2", "solo2"]
    assert all(P[x] <= P[y] for x, y in zip(order, order[1:])), [(k, P[k]) for k in order]
    pg = lambda k: f'<span class="pg">第 {P[k]} 页</span>'

    def diag_lines(name, d=CODE):
        return [l for l in rd(d, name, "wdiag").split("\n") if re.match(r"^\S+:\d+:\d+: (error|warning): ", l)]

    # ---- 需要从程序结果中取出的数值，全部核对一遍再用
    o_alarm_k = out("alarm_k", d=K, prompt="请输入告警字母（g～n）：")
    o_alarm_z = out("alarm_k", "2", d=K, prompt="请输入告警字母（g～n）：")
    assert "加密报文：L" in o_alarm_k and o_alarm_z == "输入的不是 g～n 中的告警字母，程序结束。"
    assert "空座位数：0" in out("lab48", d=K)
    assert "座位使用率：100.0%" in out("labfull48", d=K) and "座位使用率：0.0%" in out("labfull0", d=K)
    assert "座位使用率：100.0%" in out("lab210_40", d=K) and "座位使用率：0.0%" in out("lab210_0", d=K)
    assert "年龄：19 岁" in out("profile19", d=K)
    assert "平均温度：38.2 ℃" in out("lab206_mid") and "平均温度：25.6 ℃" in out("lab206_ok")
    assert "座位使用率：0.0%" in out("lab204_mid") and "座位使用率：75.0%" in out("lab204_ok")
    assert rd(CODE, "lab204_mid", "wdiag").strip() == "" and rd(CODE, "lab206_mid", "wdiag").strip() == ""
    eof = [out("scanf_eof", s, d=K, prompt="请输入人数、温度和故障编码：").split("\n")[0] for s in ("", "2", "3")]
    assert eof == ["scanf 返回值：-1", "scanf 返回值：-1", "scanf 返回值：1"], eof
    assert all(out("scanf_eof", s, d=K).endswith("输入格式不对，程序结束。") for s in ("", "2", "3"))
    d125, d125b, dp14 = diag_lines("bad_ex125", K), diag_lines("bad_ex125b", K), diag_lines("bad_profile14", K)
    d204, d206 = diag_lines("bad_204"), diag_lines("bad_206")
    assert len(d125) == 2 and len(d125b) == 2 and len(dp14) == 1 and len(d204) == 3 and len(d206) == 2
    sizeof_g = [l for l in out("str_len").split("\n") if "sizeof('g')" in l][0]
    digit = out("digit").split("\n")
    dec = out("decode", prompt="请输入收到的加密报文（H～O）："), out("decode", "2", prompt="请输入收到的加密报文（H～O）：")
    zp = "请输入楼层区字母（a～f）："
    zone = [out("zone", s, prompt=zp) for s in ("", "2", "3", "4")]
    zin = [rd(CODE, "zone", f"in{s}").strip() for s in ("", "2", "3", "4")]

    H = []
    H.append(f"""<div class="title">
<div class="t0">{esc(BOOK)}</div>
<h1>参考答案与评分说明</h1>
<div class="t1">教师用　·　配套资源 VER_PLACEHOLDER　·　页码为印刷版 v4 正文页码</div>
</div>

<h2>使用说明</h2>
<ol class="use">
<li>本说明供任课教师使用，不随学生用资源发放。内容包括：课堂练习的参考答案；技能训练的填空答案、预期结果和评分要点；课堂验收的检查要点和通过标准；“离开 AI 再做”的参考结果；两个项目评价表的评分细则和评分记录表；项目二任务三课堂验收用的待诊断程序。</li>
<li>文中凡是程序的编译提示和运行结果，都是在本书环境（小熊猫C++ 3.4 自带的 MinGW-w64 GCC 11.5.0，默认编译选项）中实际编译、运行得到的，原始记录见“程序验证记录”。为核对答案而改动过的程序（如“年龄改为 19”）也一并验证，见验证记录中的“补充验证”。</li>
<li>简答题、独立完成题的写法不唯一：输出与预期结果一致，学生能说清每一处写法的理由，即可判为正确。</li>
<li>课堂验收和项目评价都要求学生从 .c 源文件当场重新编译、运行，不以截图或以前生成的 .exe 代替。</li>
<li>评分细则中的分值和达标条件以书中的评价表为准；表中“评分细则（建议）”一栏是把分值拆到具体证据上的参考做法，可按班级情况调整。</li>
</ol>
""")

    # ================================================================ 项目一
    H.append('<h2 class="proj">项目一　搭建个人专属档案</h2>')
    H.append("<h3>一、课堂练习参考答案</h3>")
    H.append(f"<h4>任务一　认识C语言程序设计 {pg('e11')}</h4>")
    H.append(table(["题号", "答案", "说明"], [
        ["1", "×", "计算机只能直接执行机器语言。C 源程序要经过编译、连接，生成可执行程序后才能运行"],
        ["2", "×", "程序设计包括分析任务、设计步骤、编写程序、运行测试和修改，写程序只是其中一环"],
        ["3", "A", ""],
        ["4", "C", "A、D 的说法错误；C 语言不只用来编写电脑软件，B 错误"],
        ["5", "开放题", "结合专业、言之有理即可，例如单片机、PLC 外围控制器、变频器、光伏逆变器、机器人、无人机等设备中的程序"],
    ], ["8%", "12%", None], "ans"))
    H.append(f"<h4>任务二　第一个C语言程序 {pg('e12')}</h4>")
    H.append(table(["题号", "答案", "说明"], [
        ["1", "B", "一个 C 程序有且只有一个 main 函数"],
        ["2", "C", "A 漏写分号；B 用了中文分号；D 把 printf 写成了 Printf（C 语言区分大小写）"],
        ["3", c("3+5=8"), ""],
        ["4", c("%.2f"), ""],
        ["5", "3 处", f"① 第 1 行 {c('#include <stdio.h>;')} 末尾多了分号，应删去；② 第 4 行 printf 语句末尾漏写分号；③ 第 5 行 {c('return 0')} 末尾漏写分号。"
              f"<br><span class='k'>实测：第一次编译只报第 1 行的警告和第 4 行的错误（{c(d125[1].split(': ', 2)[2])}）；改正第 4 行后再编译，才报第 5 行的错误（{c(d125b[1].split(': ', 2)[2])}）。可借此说明“改一处、编译一次”。</span>"],
    ], ["8%", "12%", None], "ans"))
    H.append(f"<h4>任务三　开发环境搭建与程序执行流程 {pg('e13')}</h4>")
    H.append(table(["题号", "答案", "说明"], [
        ["1", "编辑→编译→连接→运行", ""],
        ["2", "A；C", "源程序扩展名 .c，Windows 中可执行程序扩展名 .exe"],
        ["3", "×", "编译只能检查语法等问题，结果是否正确要运行后与预期结果核对"],
        ["4", "F9；F11", "源程序修改后还没编译就按 F11 时，小熊猫C++ 会自动保存并重新编译"],
    ], ["8%", "26%", None], "ans"))

    H.append("<h3>二、技能训练答案与评分要点</h3>")
    H.append(f"<h4>任务二　训练 1　新生报到凭条（slip.c）{pg('slip')}</h4>")
    H.append(f"<p>填空：① {c(chr(34) + '林小禾' + chr(34))}　② {c('room, bed')}　③ {c('%.2f')}　④ {c('return 0;')}</p>")
    H.append(run(out("slip"), f"运行结果（与{F['slip']} 一致）"))
    H.append("<p class='pt'>评分要点：① 要带英文双引号；② 两个变量的顺序要与两个 <code>%d</code> 的顺序对应；④ 不要漏写分号。四处都对、运行结果与书中一致即为正确。</p>")
    H.append(f"<h4>任务二　训练 2　改一项需求（slip2.c）{pg('slip2')}</h4>")
    H.append(f"<p>改 5 处：room 改为 415，bed 改为 3，money 改为 86.5；宿舍一行的“6 号楼”改为“7 号楼”；余额的格式说明符改为 {c('%.1f')}。</p>")
    H.append(run(out("slip2"), "运行结果"))
    H.append("<p class='pt'>评分要点：先写预测、再上机核对；预测与运行结果不一致时，能说出原因。</p>")
    H.append(f"<h4>任务二　训练 3　社团活动通知（club.c）{pg('club')}</h4>")
    H.append(f"<p>参考程序见“参考答案\\project01\\club.c”。输出与{F['club']} 一致即可；名额 30 必须用 {c('%d')} 输出，例如 {c('printf(' + chr(34) + '名额：%d 人' + chr(92) + 'n' + chr(34) + ', 30);')}。换成另一项校园活动时，资料自拟，格式正确即可。</p>")
    H.append(run(out("club"), "参考程序的运行结果"))
    H.append(f"<h4>任务三　训练　上机运行报到凭条程序 {pg('run')}</h4>")
    H.append(f"<p>{F['rec_slip']} 的填写要点：文件保存位置为 <code>D:\\CStudy\\project01\\slip.c</code>；错误数、警告数和提示原文按学生实际情况填写，要抄原文；最后一栏写明运行结果与{F['slip']} 是否一致。拓展中故意制造的错误，提示原文可对照“程序验证记录”中 bad_semi.c、bad_case.c 等程序的记录。</p>")

    H.append("<h3>三、课堂验收检查要点</h3>")
    H.append(table(["任务", "检查要点", "通过标准与参考结果"], [
        [f"任务一<br>{pg('a11')}", "合上书说出什么是程序、什么是程序设计",
         "意思对即可：程序是为完成任务而编写的、按顺序排列的指令集合；程序设计是分析任务、设计步骤、编写程序、运行测试和修改的完整过程。不要求逐字背诵"],
        ["", "从自己的 AI 对话中找出一处需要核实的说法",
         "能指出具体是哪一句，说明用什么核实（教材、老师、上机运行等）以及结论"],
        [f"任务二<br>{pg('a12')}", "把专业改成另一个专业名称，说出改的是哪一行",
         "改 profile.c 第 16 行 printf 中的字符串，重新编译运行后专业一行随之改变"],
        ["", "把年龄改为 19，先说出结果怎样变化，再运行核对",
         "预测：只有“年龄”一行变为“年龄：19 岁”，其余不变。实测一致（补充验证 profile19.c）"],
        ["", "同伴删去一个分号或写错一个字母，找出错误并说明原因",
         "能按提示的行号找到错误，说出原因（漏写分号 / C 语言区分大小写）"],
        [f"任务三<br>{pg('a13')}", "从自己保存的 .c 文件重新编译、运行",
         "当场完成，错误数为 0，运行结果正确；不接受截图或以前生成的 .exe"],
        ["", "删去 profile.c 中一条 printf 末尾的分号，读出提示中的行号，说明提示为什么出现在下一行之前",
         f"例如删去第 14 行末尾的分号，提示为 {c(dp14[0].split(': ', 2)[2])}，位置在第 14 行末尾（补充验证 bad_profile14.c）。原因：编译器读到下一行开头的 printf 时，才发现上一条语句没有结束，所以提示“在 printf 之前缺少分号”"],
        ["", f"改正后重新编译运行，在{F['rec1']} 中记录",
         "首次提示原文、修改方法、复测结果三项齐全"],
    ], ["13%", "33%", None], "long"))

    H.append(f"<h3>四、离开 AI 再做：参考结果（profile8.c）{pg('solo1')}</h3>")
    H.append(run(out("profile8"), "参考程序的运行结果（参考答案\\project01\\profile8.c）"))
    H.append(f"<p class='pt'>检查要点：“爱好”一行在“籍贯”之后；身高显示为“1.70 米”。年龄用 {c('%d')}（整数），身高用 {c('%.2f')}（保留 2 位小数），姓名、籍贯、爱好等文字用 {c('%s')}；学生能说出这样选的理由。运行前写了预测，运行后逐字核对。</p>")

    H.append(f"<h3>五、项目一评价表评分细则（{F['ev1']}）{pg('ev1')}</h3>")
    H.append(table(["评价项", "分值", "书中的验收证据", "评分细则（建议）"], [
        ["成功编译并运行", "25", "从提交的 .c 文件当场重新编译、运行，不以截图代替",
         "当场编译没有错误并运行出结果，得 25 分；要老师提示才能改正编译错误的，得 15 分；不能运行的，得 0 分。只交截图或 .exe 的，本项不得分"],
        ["档案内容、顺序和换行正确", "25", "姓名、性别、年龄、学号、专业五项，每项正确得 5 分",
         f"对照{F['card']} 的格式逐项核对：内容、位置和换行都正确，得 5 分；内容错、顺序错或缺少换行，该项不得分"],
        ["独立修改与解释", "20", "当场改一项内容得 10 分，说清对应的语句得 10 分",
         "按老师指定的一项（如专业、年龄）当场修改，运行正确得 10 分；能指出对应语句的行号，说清其中字符串或格式说明符的作用，得 10 分"],
        ["纠错记录与复测", "20", "首次提示原文 5 分，修改理由 5 分，复测结果 10 分",
         f"以{F['rec1']} 为依据。编程中没有遇到错误的学生，用任务三课堂验收中“删去一个分号”的记录评分"],
        ["隐私与规范", "10", "使用虚构资料 5 分，命名、缩进和注释清楚 5 分",
         "档案中出现真实的身份证号、手机号、家庭住址等，“使用虚构资料”不得分；缩进 4 格、花括号对齐、有必要的注释，得 5 分"],
    ], ["18%", "7%", "30%", None], "long"))
    H.append("<p class='pt'>达标：总分 60 分及以上，同时必须能从源程序当场重新编译运行，并能独立修改一项内容。选学内容（如自己编写函数）不作为达标门槛。</p>")
    H.append(keep("<h4>项目一评分记录表</h4>", score_sheet([("编译运行", 25), ("档案内容", 25), ("修改解释", 20), ("纠错复测", 20), ("隐私规范", 10)])))

    # ================================================================ 项目二
    H.append('<h2 class="proj p2">项目二　读懂身边多样数据</h2>')
    H.append("<h3>一、课堂练习参考答案</h3>")
    H.append(f"<h4>任务一　建立实训室数据档案 {pg('e21')}</h4>")
    H.append(table(["题号", "答案", "说明"], [
        ["1", "B", f"A 是字符串常量；C 不加引号，是标识符；D 的 67 虽然是 {c(chr(39) + 'C' + chr(39))} 的 ASCII 码，但它是整型常量"],
        ["2", "A", "B 末尾多了分号（分号会一起被替换进程序）；C 多了等号；D 少了 #"],
        ["3", "×", f"const 定义的只读变量不能再赋值，编译出错（{c('assignment of read-only variable')}，见验证记录 bad_const.c）"],
        ["4", "score、max_num、Float、_count、seat2", "3d 以数字开头；a b 含空格；float 是关键字；room-1 含减号；#num 含 #"],
        ["5", "参考写法", f"{c('int fans = 12;')}　{c('double volt = 219.8;')}<br>{c('char level = ' + chr(39) + 'B' + chr(39) + ';')}　{c('_Bool fan_on = 1;')}<br>变量名不唯一，见名知意即可；电压有小数，按本书约定用 double"],
        ["6", "8", ""],
    ], ["8%", "22%", None], "ans"))
    H.append(f"<h4>任务二　实训室设备告警字符加密传输 {pg('e22')}</h4>")
    H.append(table(["题号", "答案", "说明"], [
        ["1", "68；100", "大小写字母的 ASCII 码相差 32"],
        ["2", "B", f"{c(chr(39) + 'b' + chr(39))} 的 ASCII 码 98，减 32 得 66，即 {c(chr(39) + 'B' + chr(39))}"],
        ["3", "C", f"{c(chr(34) + 'a' + chr(34))} 是字符串常量"],
        ["4", "4；3", f"字符串末尾还有一个 {c(chr(39) + chr(92) + '0' + chr(39))}，所以占 4 个字节；strlen 不计 {c(chr(39) + chr(92) + '0' + chr(39))}"],
        ["5", "B", "double 型用 %lf 读入，变量名前要加 &amp;"],
        ["6", c("b 98"), f"{c(chr(39) + 'a' + chr(39) + ' + 1')} 的值是 98，用 %c 输出是 b，用 %d 输出是 98"],
    ], ["8%", "14%", None], "ans"))
    H.append(f"<h4>任务三　实训室数据字典适配与异常诊断 {pg('e23')}</h4>")
    H.append(table(["题号", "答案", "说明"], [
        ["1", "−128；127", f"见{F['range']}"],
        ["2", "7", "小数部分直接舍去，不是四舍五入"],
        ["3", "2；2.5", "两个整数相除，结果是整数"],
        ["4", "C", "B 先做整数除法得 0，再转换为 0.0；D 仍是整数除法"],
        ["5", "×", "警告往往说明有类型或格式不匹配，要先改正、再运行"],
        ["6", "×", "逻辑错误编译器发现不了，要用测试数据核对运行结果"],
    ], ["8%", "14%", None], "ans"))

    H.append("<h3>二、技能训练答案与评分要点</h3>")
    H.append(f"<h4>任务一　训练 1　204 实训室空座位统计（seat204.c）{pg('seat')}</h4>")
    H.append(f"<p>填空：① {c('int')}　② {c('seats - people')}　③ {c('ROOM')}　④ {c('empty')}</p>")
    H.append(run(out("seat204"), f"运行结果（与{F['seat']} 一致）"))
    H.append(f"<p>再改一项需求：新增定义 {c('double temp = 23.6;')}，在最后一条 printf 之后新增 {c('printf(' + chr(34) + '当前环境温度：%.1f ℃' + chr(92) + 'n' + chr(34) + ', temp);')}（参考答案 seat204b.c）。</p>")
    H.append(run(out("seat204b"), "改后的运行结果"))
    H.append(f"<h4>任务一　训练 2　计算平均温度（temp_avg.c）{pg('avg')}</h4>")
    H.append(f"<p>参考程序见“参考答案\\project02\\temp_avg.c”。(24.5 + 25.1 + 23.9) / 3 = 24.5，输出与{F['avg']} 一致。</p>")
    H.append(run(out("temp_avg"), "参考程序的运行结果"))
    H.append(f"<p class='pt'>评分要点：温度用 double 型；求平均值时加括号 {c('(t1 + t2 + t3) / 3')}，漏加括号会先算 t3 / 3；用 {c('%.1f')} 输出。</p>")
    H.append(f"<h4>任务二　训练 1　后台还原告警字母（decode.c）{pg('dec')}</h4>")
    H.append(f"<p>填空：① {c('getchar()')}　② {c('secret - 1 + 32')}　③ {c('code')}　故障类型：网络中断（查{F['alarm']}，j 表示网络中断）</p>")
    H.append(table(["输入", "运行结果"], [[c(rd(CODE, "decode", "in").strip()), esc(dec[0])], [c(rd(CODE, "decode", "in2").strip()), esc(dec[1])]], ["14%", None]))
    H.append(f"<h4>任务二　训练 2　数字字符与整数（digit.c）{pg('digit')}</h4>")
    H.append(table(["程序行", "实际的输出"], [["第 8 行", esc(digit[0])], ["第 9 行", esc(digit[1])], ["第 10 行", esc(digit[2])]], ["14%", None]))
    H.append(f"<p class='pt'>评分要点：先写预测、再运行核对。能说出 {c(chr(39) + '7' + chr(39))} 的 ASCII 码是 55、{c(chr(39) + '0' + chr(39))} 是 48，所以 {c('ch - ' + chr(39) + '0' + chr(39))} 得到整数 7。学生用资源不附本题的运行结果，参考答案中的 digit-运行结果.txt 供核对。</p>")
    H.append(f"<h4>任务二　训练 3　楼层区号换码（zone.c）{pg('zone')}</h4>")
    H.append(keep(f"<p>参考程序见“参考答案\\project02\\zone.c”，区号的算法是 {c('zone - ' + chr(39) + 'a' + chr(39) + ' + 1')}。四组测试的结果：</p>",
                  table(["输入", "运行结果"], [[c(i), esc(o).replace("\n", "<br>")] for i, o in zip(zin, zone)], ["14%", None])))
    H.append(f"<p class='pt'>评分要点：照任务二做两项检查（是否读到字符、是否在 a～f 之中），输入 g 时给出提示并结束；输入 c 的结果与{F['zone']} 一致。</p>")

    H.append(f"<h4>任务三　训练 1　205 实训室数据诊断（fix205.c）{pg('fix')}</h4>")
    H.append(table(["行号", "问题", "修改方法"], [
        ["9、13", "int 型不能保存小数，25.6 存成了 25（第 13 行用 %d 输出）", f"第 9 行改为 {c('double temp = 25.6;')}，第 13 行改用 {c('%.1f')}"],
        ["14", "故障编码用 %d 输出，显示的是 n 的 ASCII 码 110", f"改用 {c('%c')}"],
        ["11", "整数除法：35 / 48 的结果是 0，使用率显示 0.0%", f"改为 {c('(double)people / seats * 100')}"],
    ], ["10%", "45%", None]))
    H.append(run(out("fix205_ok"), "改正后的运行结果（参考答案 fix205_ok.c）"))
    H.append("<p class='pt'>说明：本程序用默认编译选项编译没有任何提示（实测）；加 -Wconversion 后的提示见程序验证记录的补充验证。第 9 行和第 13 行是同一个问题，表中合为一行；分成两行写也算对。</p>")
    H.append(f"<h4>任务三　训练 2　为光伏电站的数据选择类型 {pg('pv')}</h4>")
    H.append(table(["数据", "示例值", "类型", "理由"], [
        ["光伏板温度", "45.3 ℃", c("double"), "有小数"],
        ["逆变器编号", "B", c("char"), "一个字符"],
        ["今日发电量", "1250 度", c("int"), "整数，int 足够存放（需要保留小数时用 double 也对）"],
        ["电站累计发电量", "3200000000 度", c("long long"), f"超过 int 的最大值 2147483647（约 21 亿），int 存不下；见{F['range']}"],
        ["是否已并网", "是", c("_Bool"), "只有“是”“否”两种状态，用 1 表示已并网"],
    ], ["22%", "18%", "14%", None]))
    H.append(f"<h4>任务三　训练 3　210 实训室数据档案（lab210.c）{pg('l210')}</h4>")
    H.append(keep(f"<p>参考数据字典（格式同{F['dict']}）：</p>", table(["变量名", "含义", "范围/精度", "类型", "选择理由"], [
        [c("BUILDING"), "楼栋号", "6", "符号常量", "固定的配置值"],
        [c("room"), "实训室编号", "201～210", c("const int"), "整数，运行中不变"],
        [c("seats"), "总座位数", "40", c("const int"), "整数，运行中不变"],
        [c("type"), "实训室类型", "'A'～'Z'", c("char"), "一个字母"],
        [c("people"), "实时在室人数", "0～40", c("int"), "整数"],
        [c("times"), "今日实训场次", "0 及以上", c("int"), "整数"],
        [c("faults"), "设备故障次数", "0 及以上", c("int"), "整数"],
        [c("temp"), "室内环境温度", "1 位小数", c("double"), "有小数"],
        [c("wet"), "空气湿度", "1 位小数（%）", c("double"), "有小数"],
        [c("volt"), "实际供电电压", "0～380 V", c("double"), "380 超出 char 的范围，电压也可能有小数"],
        [c("power"), "设备开关机状态", "1 开机，0 关机", c("_Bool"), "只有两种状态"],
        [c("code"), "故障编码", "'g'～'n'", c("char"), "一个字母，用单引号"],
        [c("empty"), "空座位数", "0～40", c("int"), "计算得出的整数"],
        [c("rate"), "座位使用率", "1 位小数（%）", c("double"), "有小数，计算时要避免整数除法"],
        [c("secret"), "加密报文", "'H'～'O'", c("char"), "计算得出的一个字母"],
    ], ["15%", "18%", "17%", "15%", None])))
    H.append(run(out("lab210"), f"参考程序的运行结果（与{F['l210']} 一致）"))
    H.append(f"<p>在室人数改为 40：座位使用率 40 / 40 × 100 = 100.0%；改为 0：座位使用率 0.0%。两项都已实测（补充验证 lab210_40.c、lab210_0.c）。</p>")

    H.append("<h3>三、课堂验收检查要点</h3>")
    H.append(table(["任务", "检查要点", "通过标准与参考结果"], [
        [f"任务一<br>{pg('a21')}", "为“投影仪亮度 3200 流明”选择类型、起名，写出定义语句",
         f"参考：{c('int brightness = 3200;')}。整数，int 足够；名字见名知意，不用中文，不以数字开头"],
        ["", "把 lab.c 中的在室人数改为 48，先说出空座位数，再运行核对", "48 − 48 = 0，运行显示“空座位数：0”（补充验证 lab48.c）"],
        ["", "说出哪些数据用了符号常量、哪些用了只读变量，为什么",
         "TYPE、ROOM 用 #define 定义为符号常量，是程序中固定的配置值；seats 用 const 定义为只读变量，是需要明确类型（int）的固定数据（见书中“#define 与 const 的区别”表）"],
        [f"任务二<br>{pg('a22')}", "不看程序说出 k 加密后是什么，再输入 k 核对",
         f"k 转为大写 K，取下一个字母，加密报文是 L。实测：{esc(o_alarm_k.split(chr(10))[-1])}（补充验证 alarm_k.c）"],
        ["", "输入 5 或 Z，说明为什么给出提示并结束，是哪一项检查起了作用",
         "检查 2（是否是 g～n 中的字母）起作用：'5' 的 ASCII 码是 53，'Z' 是 90，都小于 'g' 的 103，程序提示“输入的不是 g～n 中的告警字母”并结束。检查 1 只在没有读到字符时起作用。实测：输入 5 见验证记录 alarm.c 第 5 次运行，输入 Z 见补充验证 alarm_k.c 第 2 次运行"],
        ["", "说出 'g' 和 \"g\" 的区别，以及 sizeof('g') 为什么等于 4",
         f"'g' 是字符常量，表示一个字符；\"g\" 是字符串，由 g 和 '\\0' 组成，占 2 个字节。C 语言中字符常量的类型是 int，本书环境中 int 占 4 个字节，所以 sizeof('g') 是 4（str_len.c 实测：{esc(sizeof_g)}）"],
        [f"任务三<br>{pg('a23')}", "对老师给出的新的待诊断程序，把每条编译提示归类，并说明能不能运行",
         "可以使用下面“四”中的 bad_206.c（只在教师用资源中）。两条提示都归类正确，并说出“有错误不能运行；有格式不匹配的警告也先改正、不运行”，即为通过"],
        ["", "把 lab_full.c 中的在室人数改为 48 和 0，先算出座位使用率，再运行核对",
         "48 / 48 × 100 = 100.0%；0 / 48 × 100 = 0.0%。实测一致（补充验证 labfull48.c、labfull0.c）"],
        ["", "从自己的源程序重新编译、运行，并解释一处修改为什么有效", "当场完成，解释能落到具体的行号和规则上"],
    ], ["13%", "33%", None], "long"))

    H.append(f"<h3>四、任务三课堂验收用的待诊断程序（bad_206.c）</h3>")
    H.append("<p>本程序只在教师用资源中（“课堂验收程序\\project02\\bad_206.c”），验收时当场发给学生。它含有三类问题各一处，与书中的例子不同。</p>")
    H.append(listing("bad_206"))
    H.append(table(["行号", "编译提示（实测，节选）", "类别", "处理"], [
        ["13", c(d206[0].split(": ", 2)[2]), "语法错误", "不能运行。要改座位数，就修改第 7 行的初值为 52，并删去第 13 行"],
        ["17", c(d206[1].split(": ", 2)[2]), "类型或格式不匹配", f"不运行，先改正：改用 {c('%.1f')}"],
        ["14", "（没有提示）", "逻辑错误", f"改正上面两处后编译没有提示，运行显示“平均温度：38.2 ℃”，与手算的 (25.2 + 26.0) / 2 = 25.6 ℃ 不符：计算顺序不对，先算了 t2 / 2。改为 {c('avg = (t1 + t2) / 2;')}"],
    ], ["8%", "38%", "14%", None]))
    H.append('<div class="two">' + run(out("lab206_mid"), "只改正编译提示指出的两处后（lab206_mid.c）") + run(out("lab206_ok"), "全部改正后（lab206_ok.c）") + "</div>")

    H.append(f"<h3>五、离开 AI 再做：bad_204.c 参考诊断 {pg('solo2')}</h3>")
    H.append(f"<p><b>（1）编译。</b>1 个错误、2 个警告，按{F['kind']} 归类：</p>")
    H.append(table(["行号", "编译提示（实测，节选）", "类别"], [
        [re.match(r"^\S+?:(\d+):", l).group(1), c(l.split(": ", 2)[2]), "语法错误" if ": error: " in l else "类型或格式不匹配"] for l in sorted(d204, key=lambda l: (": error: " not in l, int(re.match(r"^\S+?:(\d+):", l).group(1))))
    ], ["8%", None, "18%"]))
    H.append("<p>这时不能运行：有错误，不会生成可执行程序；有类型或格式不匹配的警告，也要先改正。</p>")
    H.append("<p><b>（2）改正三处后再编译，</b>没有任何提示（实测，lab204_mid.c）。</p>")
    H.append(f"<p><b>（3）运行核对。</b>座位使用率显示 0.0%，与预期的 75.0% 不符，是第 13 行的整数除法：30 / 40 的结果是 0。</p>")
    H.append(run(out("lab204_mid"), "改正三处后的运行结果（lab204_mid.c）"))
    H.append(keep(f"<p><b>（4）诊断记录</b>（格式同{F['diag']}）：</p>", table(["行号", "原来的写法", "发现方式", "问题与原因", "修改方法"], [
        ["16", c('printf("座位使用率：%.1f%%\\n", rate)'), "编译错误", "漏写分号", "末尾加分号"],
        ["10", c('char type = "B";'), "编译警告", f"字符与字符串混用：{c(chr(34) + 'B' + chr(34))} 是字符串", f"改为 {c(chr(39) + 'B' + chr(39))}"],
        ["15", f"{c('temp')} 用 {c('%d')} 输出", "编译警告", f"格式不匹配：{c('%d')} 要求 int 型数据", f"改用 {c('%.1f')}"],
        ["13", c("people / seats * 100"), "运行核对", "整数除法：30 / 40 的结果是 0", c("(double)people / seats * 100")],
    ], ["7%", "27%", "11%", "28%", None])))
    H.append(run(out("lab204_ok"), "全部改正后的运行结果（参考答案 lab204_ok.c）"))

    H.append("<h3>六、补充说明：例2-7 中 scanf 返回 EOF 的实测</h3>")
    H.append(f"<p>书中说明：一个数据都还没读到，输入就结束时，scanf 返回 EOF（本书环境中是 −1），它不是读入的数据个数。用 scanf_types.c 在本书环境中实测（补充验证 scanf_eof.c）：没有任何输入时，{esc(eof[0])}；只输入 Ctrl+Z 再按回车时，{esc(eof[1])}；输入 36 回车后再按 Ctrl+Z 回车时，已读入 1 个数据，{esc(eof[2])}。三种情况程序都提示“输入格式不对”并结束。</p>")
    H.append(f"<h3>七、项目二评价表评分细则（{F['ev2']}）{pg('ev2')}</h3>")
    H.append(table(["评价项", "分值", "书中的验收证据", "评分细则（建议）"], [
        ["数据字典与选型", "25", "字段齐全；每项数据的类型、单位、范围都有理由",
         "以学生的数据字典（如训练 3 的 210 实训室）为依据：题目给出的 11 项数据齐全得 10 分，缺 1 项扣 2 分；类型选择正确、单位和范围写清、理由充分得 15 分，每错 1 项扣 3 分。各自扣完为止"],
        ["程序与输出", "30", "改正后能编译运行，输出与手算结果一致",
         "编译没有错误和警告、能运行，得 10 分；输出的各项与手算结果一致，得 20 分，每错 1 项扣 4 分，扣完为止"],
        ["调试与多组测试", "30", "保留编译提示原文；至少 3 组测试数据，含边界值和不合法的数据；只能编译诊断的问题不运行",
         f"保留编译提示原文 10 分；测试记录（如{F['labin']}）至少 3 组、含边界值和不合法的数据 15 分，缺边界值或不合法数据各扣 5 分；有类型或格式不匹配警告时没有运行、先改正 5 分"],
        ["独立解释与协作", "15", "能独立讲清一处修改；记录同伴互查或 AI 复核的过程",
         "不看资料讲清一处修改的原因和依据 10 分；有同伴互查或 AI 复核的记录（查出了什么、怎样验证的）5 分"],
    ], ["17%", "7%", "30%", None], "long"))
    H.append("<p class='pt'>达标：60 分及以上，且“程序与输出”不低于 18 分。是否使用 AI 不单独决定分数，独立解释、真实验证和迁移能力才是评价的依据。</p>")
    H.append(keep("<h4>项目二评分记录表</h4>", score_sheet([("数据字典", 25), ("程序输出", 30), ("调试测试", 30), ("解释协作", 15)])))

    return "\n".join(H)


CSS = """
@font-face { font-family: "BSerif"; src: url("../../fonts/NotoSerifSC-400.ttf"); font-weight: 400; }
@font-face { font-family: "BSerif"; src: url("../../fonts/NotoSerifSC-700.ttf"); font-weight: 700; }
@font-face { font-family: "BSans"; src: url("../../fonts/NotoSansSC-400.ttf"); font-weight: 400; }
@font-face { font-family: "BSans"; src: url("../../fonts/NotoSansSC-700.ttf"); font-weight: 700; }
@font-face { font-family: "BSans"; src: url("../../fonts/NotoSansSC-900.ttf"); font-weight: 900; }
@font-face { font-family: "BMonoH"; src: url("../../fonts/JetBrainsMono-400.ttf"); font-weight: 400; size-adjust: 83.34%; }
@font-face { font-family: "BMonoH"; src: url("../../fonts/JetBrainsMono-700.ttf"); font-weight: 700; size-adjust: 83.34%; }
@page { size: A4; margin: 17mm 17mm 18mm 17mm;
  @top-right { content: "参考答案与评分说明（教师用）"; font-family: "BSans"; font-size: 7.5pt; color: #858585; }
  @bottom-center { content: "第 " counter(page) " 页"; font-family: "BSans"; font-size: 8pt; color: #4D4D4D; } }
@page :first { @top-right { content: none; } }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; font-family: "BSerif"; font-size: 10pt; line-height: 1.6; color: #1A1A1A; }
.title { border-bottom: 2pt solid #1D4F91; padding-bottom: 4mm; margin-bottom: 4mm; }
.t0 { font-family: "BSans"; font-size: 10pt; color: #4D4D4D; }
h1 { font-family: "BSans"; font-weight: 900; font-size: 22pt; color: #153A6B; margin: 1mm 0 1mm; letter-spacing: 1pt; }
.t1 { font-family: "BSans"; font-size: 9pt; color: #1D4F91; }
h2 { font-family: "BSans"; font-weight: 900; font-size: 13.5pt; color: #153A6B; margin: 6mm 0 2mm; }
h2.proj { margin-top: 8mm; background: #1D4F91; color: #fff; padding: 2mm 4mm; border-radius: 1.5pt; }
h3 { font-family: "BSans"; font-weight: 700; font-size: 11.5pt; color: #153A6B; margin: 6mm 0 2mm; border-bottom: 0.6pt solid #C5D3E7; padding-bottom: 1mm; break-after: avoid; }
h4 { font-family: "BSans"; font-weight: 700; font-size: 10pt; color: #1A1A1A; margin: 4mm 0 1.5mm; break-after: avoid; }
.pg { font-family: "BSans"; font-weight: 400; font-size: 8.5pt; color: #1D4F91; background: #E8EEF7; padding: 0 4pt; border-radius: 2pt; margin-left: 4pt; white-space: nowrap; }
p { margin: 1.2mm 0; text-align: justify; }
p.pt { color: #333; }
ol.use { padding-left: 6mm; margin: 1mm 0; } ol.use li { margin: 0.8mm 0; }
table { border-collapse: collapse; width: 100%; margin: 1.5mm 0 2mm; font-size: 9pt; line-height: 1.5; }
th, td { border: 0.6pt solid #9FB3CF; padding: 1.2mm 2mm; text-align: left; vertical-align: top; }
th { font-family: "BSans"; font-weight: 700; background: #E8EEF7; color: #153A6B; }
tr { break-inside: avoid; }
table.ans td:nth-child(2) { font-family: "BSans"; font-weight: 700; color: #153A6B; }
td .k { color: #4D4D4D; font-size: 8.5pt; }
code { font-family: "BMonoH", "BSans"; color: #153A6B; background: #F0F4FA; padding: 0 1.5pt; border-radius: 1.5pt; }
.run { margin: 1.5mm 0 2mm; break-inside: avoid; }
.rl { font-family: "BSans"; font-size: 8pt; color: #4D4D4D; margin-bottom: 0.6mm; }
.run pre, pre.src { margin: 0; font-family: "BMonoH", "BSans"; font-size: 9pt; line-height: 1.45; white-space: pre-wrap; }
.run pre { background: #F2F2F2; color: #1A1A1A; border-left: 2pt solid #4D4D4D; padding: 1.6mm 3mm; }
pre.src { background: #F4F7FB; border: 0.6pt solid #C5D3E7; padding: 2mm 3mm; break-inside: avoid; }
pre.src .ln { color: #8A9AB0; }
.two { display: flex; gap: 4mm; } .two .run { flex: 1; min-width: 0; }
table.sheet { font-size: 8.5pt; } table.sheet th { text-align: center; padding: 1mm; } table.sheet td { height: 8.2mm; }
.nbw, .keep { break-inside: avoid; }
h2.proj.p2 { break-before: page; margin-top: 0; }
"""


def make(ver, check_dir=CHECK, dst=None):
    body = build(check_dir).replace("VER_PLACEHOLDER", html.escape(ver))
    doc = f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>参考答案与评分说明</title><style>{CSS}</style></head><body>{body}</body></html>'
    h = OUT / "teacher.html"
    h.write_text(doc, encoding="utf-8")
    pdf = pathlib.Path(dst) if dst else OUT / "teacher.pdf"
    subprocess.run(["node", str(ROOT / "render.js"), str(h), str(pdf)], check=True)
    return pdf


if __name__ == "__main__":
    print(make("v4（2026-10）", sys.argv[1] if len(sys.argv) > 1 else CHECK))
