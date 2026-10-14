# 生成“预处理在做什么”动画帧（1280×720，25 帧/秒）
import os
import sys
from PIL import Image, ImageDraw, ImageFont

F = sys.argv[1]  # 字体目录
OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)
W, H, FPS = 1280, 720, 25
C, CDK, CLT, CBG = (29, 79, 145), (21, 58, 107), (197, 211, 231), (244, 247, 251)
YEL, YELB = (255, 244, 209), (229, 185, 74)
sans = lambda s, b=False: ImageFont.truetype(f'{F}/NotoSansSC-{"700" if b else "400"}.ttf', s)
mono = lambda s: ImageFont.truetype(f'{F}/JetBrainsMono-400.ttf', s)
cjkm = lambda s: ImageFont.truetype(f'{F}/NotoSansSC-400.ttf', s)


def mtext(d, xy, s, size, fill=(31, 31, 31)):
    """等宽代码里混排中文：英文用 JetBrains Mono，中文用思源黑体"""
    x, y = xy
    fm, fc = mono(size), cjkm(size)
    for ch in s:
        f = fm if ord(ch) < 128 else fc
        d.text((x, y), ch, font=f, fill=fill)
        x += size * 0.6 if ord(ch) < 128 else size * 1.0
    return x


def ease(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


CODE = ['int main()', '{', '    printf("hi\\n");', '    return 0;', '}']
HDR = ['/* stdio.h 的内容（节选） */', 'int printf(const char *, ...);', '……（共几百行）']
scenes = [('title', 1.8), ('src', 2.4), ('fetch', 2.6), ('replace', 2.6), ('done', 2.2), ('compile', 2.8), ('sum', 3.6)]


def frame(name, t, total_t):
    im = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 64], fill=C)
    d.text((40, 14), '预处理在做什么？', font=sans(28, True), fill='white')
    d.text((W - 360, 22), '人工智能助力C语言程序设计 · 项目一', font=sans(18), fill=(220, 230, 243))
    if name == 'title':
        a = ease(t / 0.6)
        d.text((W // 2, 300), '#include <stdio.h> 这一行，', font=sans(44, True), fill=mix((255, 255, 255), CDK, a), anchor='mm')
        d.text((W // 2, 370), '在编译之前发生了什么？', font=sans(44, True), fill=mix((255, 255, 255), CDK, a), anchor='mm')
        return im
    # 左：源程序框
    sx, sy = 70, 130
    d.text((sx, sy - 40), '源程序 hello.c', font=sans(24, True), fill=CDK)
    rep = name in ('replace', 'done', 'compile', 'sum')
    rp = ease(t / 1.6) if name == 'replace' else (1.0 if rep else 0.0)
    boxh = 300 + int(130 * rp)
    d.rectangle([sx, sy, sx + 480, sy + boxh], fill=CBG, outline=CLT, width=2)
    lh = 40
    # 第一行 #include
    if rp < 1:
        hl = name in ('src', 'fetch', 'replace')
        blink = (int(total_t * 3) % 2 == 0) if name == 'src' else True
        col = mix((31, 31, 31), (255, 255, 255), rp)
        if hl and blink:
            d.rectangle([sx + 12, sy + 16, sx + 340, sy + 16 + 34], fill=mix((255, 233, 168), (244, 247, 251), rp))
        mtext(d, (sx + 20, sy + 20), '#include <stdio.h>', 24, col)
    off = int(130 * rp)
    if rp > 0:
        d.rectangle([sx + 12, sy + 14, sx + 468, sy + 14 + int(140 * rp)], fill=YEL, outline=YELB, width=2)
        if rp > 0.6:
            for i, s in enumerate(HDR):
                mtext(d, (sx + 24, sy + 24 + i * 38), s, 21, (90, 74, 26))
    for i, s in enumerate(CODE):
        mtext(d, (sx + 20, sy + 20 + (i + 1.5) * lh + off), s, 24)
    # 右：stdio.h 文件
    if name in ('fetch', 'replace'):
        fx, fy = 760, 150
        a = ease(t / 0.8) if name == 'fetch' else 1.0
        if name == 'replace':
            fx = int(760 + (sx + 12 - 760) * rp)
            fy = int(150 + (sy + 14 - 150) * rp)
        if not (name == 'replace' and rp > 0.6):
            d.rectangle([fx, fy, fx + 456, fy + 140], fill=mix((255, 255, 255), YEL, a), outline=mix((255, 255, 255), YELB, a), width=2)
            for i, s in enumerate(HDR):
                mtext(d, (fx + 12, fy + 10 + i * 38), s, 21, mix((255, 255, 255), (90, 74, 26), a))
            if name == 'fetch':
                d.text((fx, fy - 36), '头文件 stdio.h（编译器自带）', font=sans(22, True), fill=mix((255, 255, 255), CDK, a))
    msg = {
        'src': '以 # 开头的行是预处理指令，它不是 C 语句，末尾没有分号',
        'fetch': '预处理器找到 #include 指定的头文件 stdio.h',
        'replace': '把 stdio.h 的内容“抄”进来，替换掉 #include 这一行',
        'done': '得到一个完整的源程序：里面有 printf 的声明，编译器才“认识”printf',
        'compile': '编译器再把完整的源程序翻译成二进制的目标程序 hello.o',
    }.get(name)
    if name == 'compile' or name == 'sum':
        a = ease(t / 0.8) if name == 'compile' else 1.0
        d.line([(580, 330), (580 + int(140 * a), 330)], fill=C, width=5)
        if a > 0.9:
            d.polygon([(730, 330), (712, 320), (712, 340)], fill=C)
            d.text((610, 290), '编译', font=sans(24, True), fill=CDK)
        if a > 0.5:
            bx = 760
            d.text((bx, 90), '目标程序 hello.o', font=sans(24, True), fill=CDK)
            d.rectangle([bx, 130, bx + 450, 430], fill=CBG, outline=CLT, width=2)
            rows = ['01001000 10001011', '00000101 11101000', '00110000 00000000', '11001001 11000011', '……']
            n = int(len(rows) * ease((t - 0.8) / 1.2)) if name == 'compile' else len(rows)
            for i in range(n):
                mtext(d, (bx + 30, 160 + i * 46), rows[i], 26, C)
    if msg:
        d.rectangle([0, H - 110, W, H], fill=(232, 238, 247))
        d.text((W // 2, H - 56), msg, font=sans(30, True), fill=CDK, anchor='mm')
    if name == 'sum':
        a = ease(t / 0.8)
        ov = Image.new('RGB', (W, H), 'white')
        im = Image.blend(im, ov, 0.95 * a)
        d = ImageDraw.Draw(im)
        if a > 0.5:
            d.text((W // 2, 250), '记住两步', font=sans(40, True), fill=CDK, anchor='mm')
            d.text((W // 2, 340), '① 预处理：把 #include 指定的头文件内容抄进源程序', font=sans(32), fill=(31, 31, 31), anchor='mm')
            d.text((W // 2, 410), '② 编译：把完整的源程序翻译成目标程序（.o / .obj）', font=sans(32), fill=(31, 31, 31), anchor='mm')
            d.text((W // 2, 500), '在小熊猫C++ 中按 F9，这两步会自动依次完成', font=sans(26), fill=(90, 90, 90), anchor='mm')
    return im


k = 0
tt = 0.0
for name, dur in scenes:
    n = int(dur * FPS)
    for i in range(n):
        frame(name, i / FPS, tt + i / FPS).save(f'{OUT}/f{k:04d}.png')
        k += 1
    tt += dur
print(k, 'frames')
