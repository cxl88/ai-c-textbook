#!/usr/bin/env python3
"""生成配套资源包（学生用、教师用）和程序验证记录。

用法：python3 pack.py 验证结果目录 [-Wconversion 补充验证目录 [答案核对目录]]
  验证结果目录：把 code/ 下的程序复制过去后，用 wrun.sh（CODE_DIR=该目录）重新编译、运行得到的结果
  答案核对目录：把 check/ 下的程序复制过去后同样重新运行的结果（check/ 中是为核对参考答案而改动过一处的程序）
输出：out/pack/学生用/、out/pack/教师用/ 以及两个 zip；教师用中的《参考答案与评分说明》由 teacher_doc.py 生成
"""
import csv, datetime, difflib, html, io, pathlib, re, shutil, subprocess, sys, zipfile
import teacher_doc

ROOT = pathlib.Path(__file__).resolve().parent
CODE, OUT = ROOT / "code", ROOT / "out"
VER = "v4（2026-10）"
VER_TAG = "v4"
BOOK_VER = "印刷版 v4"
BOOK = "人工智能助力C语言程序设计（项目一～项目二）"
CFLAGS = "-finput-charset=UTF-8 -fexec-charset=gbk -g3 -fno-ms-extensions -pipe -Wall -Werror=implicit-int -Werror=return-type -Werror=vla"

# 文件名: (文件夹, 类别, 用途)。类别：示例 / 分步 / 挖空 / 待诊断 / 只编译 / 答案 / 验收用 / 中间稿
# 答案、验收用、中间稿只进教师用：验收用是课堂验收时由教师当场发给学生的程序，中间稿只在程序验证记录中
P = {
    # ---------------- 项目一
    "hello2": ("project01", "示例", "5 分钟体验：改一句话再运行"),
    "hello": ("project01", "示例", "例1-1 第一个程序"),
    "count": ("project01", "示例", "例1-2 输出整数"),
    "line": ("project01", "示例", "例1-3 自己编写函数（选学）"),
    "age": ("project01", "示例", "逐行读程序：用变量输出年龄"),
    "types": ("project01", "示例", "常用格式说明符（速查）"),
    "escape": ("project01", "示例", "常用转义字符（速查）"),
    "messy": ("project01", "示例", "书写规范对比：不规范的写法（能运行）"),
    "frame": ("project01", "分步", "档案卡片第一步：程序框架"),
    "profile": ("project01", "示例", "任务二完整程序：个人专属档案卡片"),
    "slip": ("project01", "挖空", "训练：新生报到凭条（待补充）"),
    "bad_semi": ("project01", "只编译", "书写规则①：语句末尾漏写分号"),
    "bad_cnsemi": ("project01", "只编译", "书写规则②：用了中文分号"),
    "bad_case": ("project01", "只编译", "书写规则③：printf 写成 Printf"),
    "bad_paren": ("project01", "只编译", "书写规则④：少了右括号"),
    "bad_mian": ("project01", "只编译", "书写规则⑤：main 写成 mian"),
    "bad_twomain": ("project01", "只编译", "书写规则⑤：写了两个 main 函数"),
    "height_f": ("project01", "示例", "AI升华：验证 AI 关于身高输出的建议"),
    "profile7": ("project01", "示例", "AI升华：七项信息的档案卡片"),
    "hello2_ok": ("project01", "答案", "5 分钟体验：改过第 7 行之后的 hello2.c"),
    "slip2": ("project01", "答案", "报到凭条：改一项需求"),
    "club": ("project01", "答案", "训练 3 独立完成：社团活动通知"),
    "profile8": ("project01", "答案", "离开 AI 再做：为另一位同学输出档案卡片"),
    # ---------------- 项目二
    "const_demo": ("project02", "示例", "例2-1 符号常量与只读变量"),
    "radix": ("project02", "示例", "整数的十进制、八进制、十六进制写法"),
    "bad_const": ("project02", "只编译", "给只读变量赋值"),
    "assign": ("project02", "示例", "例2-2 变量的赋值"),
    "sizeof_demo": ("project02", "示例", "例2-3 各类型占用的字节数"),
    "float_demo": ("project02", "示例", "例2-4 float 与 double 的精度"),
    "bool_demo": ("project02", "示例", "布尔型变量（选学）"),
    "seat204": ("project02", "挖空", "训练 1：204 实训室空座位（待补充）"),
    "lab": ("project02", "示例", "任务一完整程序：203 实训室数据档案"),
    "char_code": ("project02", "示例", "例2-5 字符与 ASCII 码"),
    "escape2": ("project02", "示例", "转义字符的其他写法（选学）"),
    "str_len": ("project02", "示例", "字符型变量与字符串的字节数、长度"),
    "getchar_demo": ("project02", "示例", "例2-6 getchar 与 putchar"),
    "alarm_given": ("project02", "分步", "任务二第三步：用给定的告警字母测试"),
    "alarm": ("project02", "示例", "任务二完整程序：告警字符加密"),
    "alarm_nocheck": ("project02", "示例", "删去检查 2 的版本（观察缺少检查的后果）"),
    "decode": ("project02", "挖空", "训练 1：告警报文还原（待补充）"),
    "digit": ("project02", "示例", "训练 2：数字字符与整数（先预测，再运行）"),
    "bad_lab": ("project02", "只编译", "任务三：某同学的程序（初稿）"),
    "lab_draft2": ("project02", "待诊断", "任务三：某同学的第二稿（能运行，结果有异常）"),
    "overflow": ("project02", "示例", "超出范围的赋值（溢出）"),
    "convert": ("project02", "示例", "赋值时的类型转换"),
    "div_test": ("project02", "示例", "座位使用率的三种写法（整数除法）"),
    "bad_noamp": ("project02", "只编译", "表2-20：scanf 中漏写 &"),
    "scanf_types": ("project02", "示例", "例2-7 一次输入多个数据并检查"),
    "lab_full": ("project02", "示例", "任务三完整程序：203 实训室完整数据档案"),
    "lab_input": ("project02", "示例", "任务三：键盘输入版（含读入检查、范围检查的完整模板）"),
    "fix205": ("project02", "待诊断", "训练 1：205 实训室数据诊断"),
    "volt_ai": ("project02", "示例", "AI升华：用边界值验证建议③"),
    "bad_scanf_f": ("project02", "只编译", "AI升华：验证建议②（%f 读入 double）"),
    "scanf_lf": ("project02", "示例", "AI升华：改用 %lf 读入并检查"),
    "bad_204": ("project02", "只编译", "离开 AI 再做：204 实训室数据（待诊断）"),
    "seat204b": ("project02", "答案", "训练 1：空座位程序改一项需求"),
    "temp_avg": ("project02", "答案", "训练 2：计算平均温度"),
    "zone": ("project02", "答案", "训练 3 独立完成：楼层区号换码"),
    "fix205_ok": ("project02", "答案", "训练 1：205 实训室数据诊断（改正后）"),
    "lab210": ("project02", "答案", "训练 3 独立完成：210 实训室数据档案"),
    "lab204_ok": ("project02", "答案", "离开 AI 再做：bad_204.c 改正后"),
    "lab204_mid": ("project02", "中间稿", "离开 AI 再做：bad_204.c 只改正编译提示指出的问题（仍有逻辑错误）"),
    "bad_206": ("project02", "验收用", "任务三课堂验收：教师当场发给学生的待诊断程序"),
    "lab206_mid": ("project02", "中间稿", "bad_206.c 只改正编译提示指出的问题（仍有逻辑错误）"),
    "lab206_ok": ("project02", "答案", "任务三课堂验收：bad_206.c 改正后"),
}
TEACHER_ONLY = {"答案", "验收用", "中间稿"}
# check/ 中的程序改自哪个程序（记录中列出改动的行）
ORIG = {"bad_ex125b": "bad_ex125", "profile19": "profile", "bad_profile14": "profile", "lab48": "lab", "alarm_k": "alarm",
        "scanf_eof": "scanf_types", "lab210_40": "lab210", "lab210_0": "lab210", "labfull48": "lab_full", "labfull0": "lab_full"}
TPL_ANSWER = {"slip": "project01", "seat204": "project02", "decode": "project02"}     # 挖空练习：完整版进教师用答案
TPL_SRC = {"slip": "10_ch1.html", "seat204": "20_ch2a.html", "decode": "20_ch2b.html"}
AFTER_FIX = {"fix205": "fix205_ok", "bad_204": "lab204_ok"}                          # 待诊断程序改正后的预期输出
STUDENT_OUT_FROM_ANSWER = {"club", "temp_avg", "zone", "lab210"}                      # 书中给出了预期结果的独立练习
NO_OUTPUT_FOR_STUDENT = {"digit"}                                                      # 先预测再运行：学生用不附结果
ANSWER_FOR = {"hello2_ok": "hello2", "slip2": "slip", "seat204b": "seat204", "fix205_ok": "fix205", "lab204_ok": "bad_204"}
PAGE_HINT = {"frame": "第一步：程序框架", "messy": "不规范：挤在一起", "height_f": "验证身高的输出", "profile8": "5.离开AI再做",
             "bad_noamp": "（漏写&）", **{b: "编译器提示（节选）" for b in ("bad_semi", "bad_cnsemi", "bad_case", "bad_paren", "bad_mian", "bad_twomain")}}


def crlf(t):
    return t.replace("\r\n", "\n").replace("\n", "\r\n")


def write(path, text, bom=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((b"\xef\xbb\xbf" if bom else b"") + crlf(text).encode("utf-8"))


def runs(vdir, n):
    """该程序的各次运行：[(序号后缀, 输入文本或 None, 输出文本, 返回值)]"""
    res = []
    for o in sorted(vdir.glob(f"{n}.wout*")):
        s = o.name[len(n) + 5:]
        i = vdir / f"{n}.in{s}"
        res.append((s, i.read_text(encoding="utf-8") if i.exists() else None, o.read_text(encoding="utf-8"),
                    (vdir / f"{n}.wret{s}").read_text().strip()))
    return res


def book_pages():
    """各程序在正文中的页码：优先找程序框的标题（如“例2-7　scanf_types.c”），没有程序框的找文件名的第一次出现"""
    t = subprocess.run(["pdftotext", "-layout", str(OUT / "body.pdf"), "-"], capture_output=True, text=True).stdout.split("\f")
    sq = [re.sub(r"[\s\u2060]+", "", p) for p in t]
    fns = re.findall(r'<span class="fn">(.*?)</span>', (OUT / "body.html").read_text(encoding="utf-8"))
    pages = {}
    for n in P:
        name = ANSWER_FOR.get(n, n)
        own = [f for f in fns if re.search(r"(?<![A-Za-z0-9_])" + re.escape(name) + r"\.c(?![A-Za-z0-9_])", html.unescape(f))]
        if n in PAGE_HINT:
            pat = re.escape(re.sub(r"\s+", "", PAGE_HINT[n]))
        elif own:
            pat = re.escape(re.sub(r"\s+", "", html.unescape(own[0])))
        else:
            pat = r"(?<![A-Za-z_])" + re.escape(name) + r"\.(?:c|exe)"
        hit = [i + 1 for i, p in enumerate(sq) if re.search(pat, p)]
        pages[n] = hit[0] if hit else None
    return pages


def diag_summary(d):
    e = len(re.findall(r"^\S+:\d+:\d+: error: ", d, flags=re.M))
    w = len(re.findall(r"^\S+:\d+:\d+: warning: ", d, flags=re.M))
    link = "ld returned 1 exit status" in d
    return "无提示" if not d.strip() else "、".join(x for x in (f"{e} 个错误" if e else "", f"{w} 个警告" if w else "",
                                                             "连接失败" if link else "") if x)


def main():
    vdir = pathlib.Path(sys.argv[1]).resolve()
    wdir = pathlib.Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None
    kdir = pathlib.Path(sys.argv[3]).resolve() if len(sys.argv) > 3 else None
    dst = OUT / "pack"
    shutil.rmtree(dst, ignore_errors=True)
    stu, tea = dst / "学生用", dst / "教师用"
    pages = book_pages()
    missing = [n for n in P if not (CODE / f"{n}.c").exists()]
    assert not missing, missing
    # 先核对：重新运行的结果与排版时使用的结果一致（链接器临时文件名除外）
    def compare(rerun, ref, names):
        same, diff = 0, []
        for f in sorted(rerun.glob("*.w*")):
            n = f.name.split(".")[0]
            if n not in names:
                continue
            g = ref / f.name
            a = re.sub(r"\\Temp\\cc\w+\.o", r"\\Temp\\cc*.o", f.read_text(encoding="utf-8"))
            if g.exists():
                b = re.sub(r"\\Temp\\cc\w+\.o", r"\\Temp\\cc*.o", g.read_text(encoding="utf-8"))
                if a == b:
                    same += 1
                else:
                    diff.append(f.name)
        return same, diff
    same, diff = compare(vdir, CODE, P)
    print(f"与排版用结果一致的文件 {same} 个；不一致：{diff or '无'}")
    if kdir:
        missing = [n for n in teacher_doc.CHECK_INFO if not (kdir / f"{n}.wdiag").exists()]
        assert not missing, missing
        ksame, kdiff = compare(kdir, teacher_doc.CHECK, teacher_doc.CHECK_INFO)
        print(f"答案核对程序：与 check/ 中的结果一致的文件 {ksame} 个；不一致：{kdiff or '无'}")

    # ---------------- 学生用
    for n, (folder, kind, use) in P.items():
        src = (CODE / f"{n}.c").read_text(encoding="utf-8")
        if kind in TEACHER_ONLY:
            continue
        if kind == "挖空":                                   # 学生用：书中的挖空版；完整版进教师用答案
            part = (ROOT / "parts" / TPL_SRC[n]).read_text(encoding="utf-8")
            m = re.search(r'<snip title="' + re.escape(n) + r'\.c（待补充）"[^>]*>(.*?)</snip>', part, flags=re.S)
            write(stu / folder / f"{n}.c", html.unescape(m.group(1)).rstrip("\n") + "\n")
        else:
            write(stu / folder / f"{n}.c", src)
        if kind == "只编译" and n not in AFTER_FIX or n in NO_OUTPUT_FOR_STUDENT:
            continue
        td = stu / "测试数据与预期输出" / folder
        rr = runs(vdir, n)
        for s, inp, out, ret in rr:
            k = s or ("1" if len(rr) > 1 else "")
            if inp is not None:
                write(td / f"{n}-输入{k}.txt", inp)
            if out.strip():
                write(td / f"{n}-{'当前输出' if kind == '待诊断' else '预期输出'}{k}.txt", out, bom=True)
        if n in AFTER_FIX:
            for s, inp, out, ret in runs(vdir, AFTER_FIX[n]):
                write(td / f"{n}-改正后的预期输出.txt", out, bom=True)
    for n in STUDENT_OUT_FROM_ANSWER:
        folder = P[n][0]
        rr = runs(vdir, n)
        for s, inp, out, ret in rr:
            k = s or ("1" if len(rr) > 1 else "")
            if inp is not None:
                write(stu / "测试数据与预期输出" / folder / f"{n}-输入{k}.txt", inp)
            write(stu / "测试数据与预期输出" / folder / f"{n}-预期输出{k}.txt", out, bom=True)

    def listing(kinds):
        rows = []
        for folder in ("project01", "project02"):
            rows.append(f"\n【{folder}】")
            for n, (f, kind, use) in sorted(P.items(), key=lambda kv: pages.get(kv[0]) or 999):
                if f == folder and kind in kinds:
                    pg = f"第 {pages[n]} 页" if pages.get(n) else ""
                    rows.append(f"  {n + '.c':<18}{pg:<10}{use}")
        return "\n".join(rows)

    write(stu / "使用说明.txt", f"""{BOOK}
配套资源（学生用）  资源版本 {VER}，对应教材{BOOK_VER}
获取方式见教材“本书使用说明”中的“5. 配套资源”；版本变化见“版本说明.txt”。

一、本书环境
  开发环境：小熊猫C++ 3.4（64 位 Windows 版），编译器配置方案“MinGW-w64 GCC 11.5.0 64-bit Debug”
  编译选项：小熊猫C++ 的默认设置
            {CFLAGS}
  C 语言标准：未另行指定，按 GCC 11.5.0 的默认标准（C17，含 GNU 扩展）
  字符编码：源程序为 UTF-8，程序输出的中文转为 GBK 显示
  换用其他编译器或其他版本时，编译提示的文字、数据类型的大小等可能与书中不同。

二、使用方法
  把 project01、project02 两个文件夹复制到 D:\\CStudy 下（没有 D 盘时见项目一任务三中的常见问题），
  就可以按书中的路径打开程序。在小熊猫C++ 中用“文件 → 打开”选中 .c 文件，按 F11 编译运行。

三、文件分类
  1. 普通文件名：书中的示例程序，可以直接编译运行，和书中的运行结果对照。
  2. 待补充的练习：slip.c、seat204.c、decode.c 是挖空版，与书中一样，打开后把 ①②③④ 处补全再编译。
  3. 待诊断的练习：fix205.c、lab_draft2.c 能编译运行，但结果有异常，需要找出并改正。
  4. 文件名以 bad_ 开头：含有编译错误或“未定义行为”，只编译、看编译器提示，不要运行。
     bad_204.c 是项目二“离开 AI 再做”的诊断材料，同样先编译、按书中的步骤处理。
  5. 本资源不含练习的参考答案，答案由任课教师提供。

四、测试数据与预期输出
  “测试数据与预期输出”文件夹中：
    xxx-输入N.txt      运行时要从键盘输入的内容（照着在运行窗口中键入，再按 Enter）
    xxx-预期输出N.txt  用这组输入运行时，程序应该输出的内容
    xxx-当前输出.txt    待诊断的程序现在的输出（结果有异常，需要你找出原因）
    xxx-改正后的预期输出.txt  待诊断的程序改正后应该输出的内容
  说明：预期输出是把输入文件交给程序自动运行得到的，所以其中不显示你键入的文字；
  在运行窗口中手动输入时，你键入的内容会出现在提示文字的后面，这是正常的。
  “训练 2　数字字符与整数”（digit.c）要求先预测再运行，所以不附预期输出。

五、文件与书中位置对照（页码为{BOOK_VER} 正文页码）
{listing({"示例", "分步", "挖空", "待诊断", "只编译"})}
""", bom=True)
    write(stu / "版本说明.txt", f"""{BOOK}
配套资源（学生用）版本说明

资源版本：{VER}，2026-10-02 生成
对应教材：{BOOK_VER}（书中页码均为{BOOK_VER} 的正文页码）
核对方法：书中“本书使用说明·5. 配套资源”写明了配套资源的版本，与本资源的版本一致才能配套使用。

v4 相对 v3 的变化
  project02\\scanf_types.c（例2-7）：第 12 行改为显示 scanf 的返回值（第 8 行的注释随之修改）
      printf("scanf 返回值：%d\\n", n);
      对应的预期输出随之更新。读入失败或输入结束时，scanf 的返回值可能是 0 或 EOF（本书环境中是 -1），
      EOF 不是读入的数据个数，书中第 {pages["scanf_types"]} 页起有说明。
  其他程序与 v3 相同。
""", bom=True)

    # ---------------- 教师用
    for n, (folder, kind, use) in P.items():
        if kind == "答案":
            write(tea / "参考答案" / folder / f"{n}.c", (CODE / f"{n}.c").read_text(encoding="utf-8"))
    for n, folder in TPL_ANSWER.items():
        write(tea / "参考答案" / folder / f"{n}.c", (CODE / f"{n}.c").read_text(encoding="utf-8"))
    for s, inp, out, ret in runs(vdir, "digit"):
        write(tea / "参考答案" / "project02" / "digit-运行结果.txt", out, bom=True)
    for n, (folder, kind, use) in P.items():
        if kind == "验收用":
            write(tea / "课堂验收程序" / folder / f"{n}.c", (CODE / f"{n}.c").read_text(encoding="utf-8"))
    if not kdir:
        print("注意：没有给出答案核对目录，参考答案与评分说明使用 check/ 中保存的结果")
    teacher_doc.make(VER, kdir or teacher_doc.CHECK, dst=tea / "参考答案与评分说明.pdf")

    # 程序验证记录：原始记录
    raw = tea / "程序验证记录" / "原始记录"
    rows, detail = [], []
    nrun = nin = nonly = 0
    for n, (folder, kind, use) in P.items():
        src = (CODE / f"{n}.c").read_text(encoding="utf-8")
        d = (vdir / f"{n}.wdiag").read_text(encoding="utf-8")
        write(raw / folder / f"{n}.c", src)
        write(raw / folder / f"{n}-编译提示.txt", d if d.strip() else "（没有任何提示）\n", bom=True)
        rr = runs(vdir, n)
        for s, inp, out, ret in rr:
            k = s or ("1" if len(rr) > 1 else "")
            if inp is not None:
                write(raw / folder / f"{n}-输入{k}.txt", inp)
            write(raw / folder / f"{n}-输出{k}.txt", out, bom=True)
            write(raw / folder / f"{n}-返回值{k}.txt", ret + "\n")
        nrun += bool(rr)
        nin += sum(1 for r in rr if r[1] is not None)
        nonly += not rr
        how = "只编译，不运行" if not rr else (f"运行 {len(rr)} 次（键盘输入用输入文件）" if rr[0][1] is not None else "运行 1 次")
        rows.append([folder, f"{n}.c", f"第 {pages[n]} 页" if pages.get(n) else "", kind, use, diag_summary(d), how,
                     "、".join(r[3] for r in rr) if rr else "—"])
        detail.append((n, folder, kind, use.replace("（待补充）", "（这里验证的是补全后的完整程序）"), pages.get(n), src, d, rr))
    shutil.copy(ROOT / "wrun.sh", tea / "程序验证记录" / "wrun.sh")
    wrows = []
    if wdir:
        for f in sorted(wdir.glob("*.wdiag")):
            n = f.stem
            write(raw / "加-Wconversion补充验证" / f"{n}-编译提示.txt", f.read_text(encoding="utf-8"), bom=True)
            wrows.append((n, f.read_text(encoding="utf-8")))
    krows = []
    if kdir:
        for n, (where, use) in teacher_doc.CHECK_INFO.items():
            src = (teacher_doc.CHECK / f"{n}.c").read_text(encoding="utf-8")
            d = (kdir / f"{n}.wdiag").read_text(encoding="utf-8")
            kraw = raw / "补充验证-参考答案中改动过的程序"
            write(kraw / f"{n}.c", src)
            write(kraw / f"{n}-编译提示.txt", d if d.strip() else "（没有任何提示）\n", bom=True)
            rr = runs(kdir, n)
            for s, inp, out, ret in rr:
                k = s or ("1" if len(rr) > 1 else "")
                if inp is not None:
                    write(kraw / f"{n}-输入{k}.txt", inp)
                write(kraw / f"{n}-输出{k}.txt", out, bom=True)
                write(kraw / f"{n}-返回值{k}.txt", ret + "\n")
            o = ORIG.get(n)
            ch = []
            if o:
                a = (teacher_doc.CHECK if o in teacher_doc.CHECK_INFO else CODE) / f"{o}.c"
                ch = [l for l in difflib.unified_diff(a.read_text(encoding="utf-8").split("\n"), src.split("\n"), lineterm="", n=0)
                      if l[:1] in "+-" and not l.startswith(("+++", "---"))]
            krows.append((n, where, use, o, ch, src, d, rr))
            rows.append(["补充验证", f"{n}.c", where, "答案核对", use, diag_summary(d),
                         "只编译，不运行" if not rr else f"运行 {len(rr)} 次", "、".join(r[3] for r in rr) if rr else "—"])
    with io.StringIO() as b:
        csv.writer(b).writerows([["文件夹", "程序", "书中位置", "类别", "用途", "编译结果（默认选项）", "运行方式", "返回值"]] + rows)
        write(tea / "程序验证记录" / "程序验证清单.csv", b.getvalue(), bom=True)

    today = datetime.date(2026, 10, 2).isoformat()
    esc = html.escape
    parts = [f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>程序验证记录</title>
<style>
body{{font-family:"Microsoft YaHei","PingFang SC","Noto Sans CJK SC",sans-serif;max-width:1100px;margin:24px auto;padding:0 16px;color:#1d2733;line-height:1.6}}
h1{{font-size:24px;margin:0 0 4px}} h2{{font-size:18px;margin:28px 0 8px;border-bottom:2px solid #1f4e8c;padding-bottom:4px}}
h3{{font-size:15px;margin:22px 0 6px;color:#1f4e8c}} table{{border-collapse:collapse;width:100%;font-size:13px}}
th,td{{border:1px solid #c9d3df;padding:4px 6px;text-align:left;vertical-align:top}} th{{background:#eef3f9}}
pre{{background:#f6f8fb;border:1px solid #dde4ec;padding:6px 8px;font:12.5px/1.45 Consolas,"Courier New",monospace;white-space:pre-wrap;margin:4px 0}}
.k{{color:#5b6b7d;font-size:13px}} .tag{{display:inline-block;padding:0 6px;border-radius:3px;background:#eef3f9;font-size:12px}}
</style></head><body>
<h1>程序验证记录</h1><div class="k">{esc(BOOK)}　{VER}　记录日期：{today}</div>
<h2>一、验证环境与方法</h2>
<table>
<tr><th style="width:18%">编译器</th><td>小熊猫C++ 3.4 自带的 MinGW-w64 GCC 11.5.0（x86_64-posix-seh-rev0，目标 x86_64-w64-mingw32，MinGW-w64 运行库 9.0.0）</td></tr>
<tr><th>编译命令</th><td><code>gcc.exe 文件名.c -o 文件名.exe {CFLAGS}</code><br>与小熊猫C++ 3.4 默认的“MinGW-w64 GCC 11.5.0 64-bit Debug”配置相同</td></tr>
<tr><th>C 语言标准</th><td>未另行指定，GCC 11.5.0 默认 gnu17（预定义宏 __STDC_VERSION__ = 201710L，已用该编译器实测）</td></tr>
<tr><th>运行方式</th><td>用 cmd 批处理逐个编译；能运行的程序在控制台运行，需要键盘输入的用输入文件重定向（<code>程序.exe &lt; 输入.txt</code>），程序输出（GBK）转为 UTF-8 记录，同时记录返回值（ERRORLEVEL）</td></tr>
<tr><th>只编译的程序</th><td>文件名以 bad_ 开头的程序含有编译错误或未定义行为（格式与参数类型不匹配等），只记录编译提示，不运行</td></tr>
<tr><th>验证平台</th><td>Linux 上用 Wine 9.0 运行上述 Windows 版编译器和程序（编译器、编译选项与 Windows 机房环境相同）。书中的界面截图来自同一环境中的小熊猫C++ 3.4。建议首次使用前在学校机房的 Windows 计算机上抽查复核</td></tr>
<tr><th>与书中结果核对</th><td>{len(P)} 个程序全部重新编译；{nrun} 个运行（其中 {nin} 次使用输入文件），{nonly} 个只编译。重新运行的编译提示、输出和返回值与排版时使用的结果逐字节一致（链接器提示中的临时文件名每次不同，不计）。{f"另有 {len(krows)} 个为核对参考答案而改动过一处的程序，见“补充验证：参考答案中改动过的程序”。" if krows else ""}</td></tr>
</table>
<h2>二、程序清单</h2>
<table><tr><th>文件夹</th><th>程序</th><th>书中位置</th><th>类别</th><th>用途</th><th>编译结果</th><th>运行方式</th><th>返回值</th></tr>"""]
    for r in rows:
        parts.append("<tr>" + "".join(f"<td>{esc(str(c))}</td>" for c in r) + "</tr>")
    parts.append("</table>")
    if wrows:
        parts.append("<h2>三、补充验证：加 -Wconversion 选项</h2><p>正文说明“默认编译选项下没有提示，加上 -Wconversion 后会提示”的程序，另加 <code>-Wconversion</code> 重新编译，提示如下（程序输出与默认选项相同）：</p>")
        for n, d in wrows:
            parts.append(f"<h3>{esc(n)}.c　+ -Wconversion</h3><pre>{esc(d)}</pre>")
    sec = iter("三四五六")
    if wrows:
        next(sec)
    if krows:
        parts.append(f"<h2>{next(sec)}、补充验证：参考答案中改动过的程序</h2><p>《参考答案与评分说明》中的一些结果，要把书中的程序改动一处才能得到（如把年龄改为 19、输入 Z），或者要模拟“输入结束”。这些程序同样用上面的环境编译、运行，结果如下。程序在“原始记录\\补充验证-参考答案中改动过的程序”中。</p>")
        def show(x):
            return "（空：没有任何输入，一运行就结束输入）" if x == "" else x.replace("\x1a", "^Z（Ctrl+Z）")
        for n, where, use, o, ch, src, d, rr in krows:
            parts.append(f"<h3>{esc(n)}.c　<span class='tag'>{esc(where)}</span>　{esc(use)}</h3>")
            if ch:
                parts.append(f"<div class='k'>与 {esc(o)}.c 相比改动的行（- 原来，+ 改后）：</div><pre>{esc(chr(10).join(ch))}</pre>")
            elif not o:
                parts.append(f"<div class='k'>源程序：</div><pre>{esc(src)}</pre>")
            else:
                parts.append(f"<div class='k'>源程序与 {esc(o)}.c 相同，只是输入不同。</div>")
            parts.append(f"<div class='k'>编译提示：</div><pre>{esc(d) if d.strip() else '（没有任何提示）'}</pre>")
            for s, inp, out, ret in rr:
                k = s or "1"
                if inp is not None:
                    parts.append(f"<div class='k'>第 {k} 次运行，输入：</div><pre>{esc(show(inp))}</pre>")
                parts.append(f"<div class='k'>{'' if inp is not None else '运行'}输出（返回值 {esc(ret)}）：</div><pre>{esc(out)}</pre>")
            if not rr:
                parts.append("<div class='k'>只编译，不运行。</div>")
    parts.append(f"<h2>{next(sec)}、逐个程序的记录</h2>")
    for n, folder, kind, use, pg, src, d, rr in detail:
        parts.append(f"<h3>{esc(folder)}\\{esc(n)}.c　<span class='tag'>{esc(kind)}</span>　{esc(use)}{f'（第 {pg} 页）' if pg else ''}</h3>")
        parts.append(f"<div class='k'>编译提示：</div><pre>{esc(d) if d.strip() else '（没有任何提示）'}</pre>")
        for s, inp, out, ret in rr:
            k = s or "1"
            if inp is not None:
                parts.append(f"<div class='k'>第 {k} 次运行，输入：</div><pre>{esc(inp)}</pre>")
            parts.append(f"<div class='k'>{'' if inp is not None else '运行'}输出（返回值 {esc(ret)}）：</div><pre>{esc(out)}</pre>")
        if not rr:
            parts.append("<div class='k'>只编译，不运行。</div>")
    parts.append("</body></html>")
    write(tea / "程序验证记录" / "程序验证记录.html", "\n".join(parts))

    answers = [(n, P[n][0], P[n][2]) for n in P if P[n][1] == "答案"] + [(n, f, P[n][2].replace("（待补充）", "（补全后）")) for n, f in TPL_ANSWER.items()]
    write(tea / "教师用说明.txt", f"""{BOOK}
配套资源（教师用）  资源版本 {VER}，对应教材{BOOK_VER}

本资源供任课教师使用，请勿与学生用资源放在同一个文件夹中发给学生。
学校资源平台开通之前，学生用资源（配套资源-学生用-{VER_TAG}.zip）由任课教师直接发给学生。

一、参考答案与评分说明.pdf（A4，可直接打印）
  课堂练习的参考答案；技能训练的填空答案、预期结果和评分要点；课堂验收的检查要点和通过标准；
  “离开 AI 再做”的参考结果；项目一、项目二评价表的评分细则和评分记录表。页码为{BOOK_VER} 正文页码。

二、参考答案（“参考答案”文件夹，页码为{BOOK_VER} 正文页码）
""" + "\n".join(f"  {f}\\{n + '.c':<16}{('第 ' + str(pages[n]) + ' 页') if pages.get(n) else '':<10}{use}" for n, f, use in answers) + f"""
  project02\\digit-运行结果.txt   训练 2“数字字符与整数”的实际运行结果（学生先预测，再运行核对）

  说明：挖空练习（slip.c、seat204.c、decode.c）在学生用资源中是挖空版，这里是补全后的完整程序；
  独立完成类练习（club.c、temp_avg.c、zone.c、lab210.c）的写法不唯一，输出与书中的预期结果一致即可。

三、课堂验收程序（“课堂验收程序”文件夹）
  project02\\bad_206.c   项目二任务三课堂验收时当场发给学生的待诊断程序（学生用资源中没有）。
                         诊断要点见《参考答案与评分说明》，改正后的程序是 参考答案\\project02\\lab206_ok.c。

四、程序验证记录（“程序验证记录”文件夹）
  程序验证记录.html   验证环境、编译命令、C 标准、每个程序的编译提示、输入、输出和返回值（用浏览器打开）
  程序验证清单.csv    一行一个程序的汇总表（可用 Excel/WPS 打开）
  原始记录\\           每个程序的源文件、编译提示、输入、输出、返回值的原始文本；
                      其中“补充验证-参考答案中改动过的程序”是《参考答案与评分说明》中改动一处再运行的结果
                      （如年龄改为 19、输入 Z）和 scanf 遇到输入结束时的返回值
  wrun.sh             批量编译、运行用的脚本
  验证方法：在 Linux 上用 Wine 9.0 运行小熊猫C++ 3.4 自带的 Windows 版 MinGW-w64 GCC 11.5.0，
  编译选项与小熊猫C++ 默认配置相同。建议在学校机房的 Windows 计算机上按书中步骤抽查复核，
  特别是安装、中文显示和键盘输入部分。

五、课堂验收与评分
  每个任务的“课堂验收”要求学生从 .c 源文件当场重新编译、运行，不以截图代替；
  分值和达标条件以书中的项目评价表为准，评分细则和评分记录表见《参考答案与评分说明》。
""", bom=True)
    write(tea / "版本说明.txt", f"""{BOOK}
配套资源（教师用）版本说明

资源版本：{VER}，2026-10-02 生成
对应教材：{BOOK_VER}（书中页码均为{BOOK_VER} 的正文页码）

v4 相对 v3 的变化
  1. 新增《参考答案与评分说明》（PDF）。
  2. 新增“课堂验收程序\\project02\\bad_206.c”及其参考答案 lab206_ok.c。
  3. 程序验证记录新增 lab204_mid.c、lab206_mid.c（只改正编译提示指出的问题、仍有逻辑错误的中间稿），
     以及“补充验证-参考答案中改动过的程序”。
  4. project02\\scanf_types.c（例2-7）第 12 行改为显示 scanf 的返回值，学生用资源中的预期输出随之更新。
  其他程序与 v3 相同。
""", bom=True)

    # 压缩包
    for name, folder in (("学生用", stu), ("教师用", tea)):
        zp = dst / f"人工智能助力C语言程序设计-项目一至二-配套资源-{name}-{VER_TAG}.zip"
        with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(folder.rglob("*")):
                if f.is_file():
                    z.write(f, pathlib.Path(f"配套资源-{name}") / f.relative_to(folder))
        print(zp.name, zp.stat().st_size, "bytes,", sum(1 for f in folder.rglob('*') if f.is_file()), "files")


if __name__ == "__main__":
    main()
