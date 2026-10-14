"""统计正文每页版心底部的空白高度（mm），用于排版检查。用法：python3 gaps.py out/body.pdf [阈值mm]"""
import sys, subprocess, tempfile, glob
from PIL import Image
pdf = sys.argv[1]; th = float(sys.argv[2]) if len(sys.argv) > 2 else 30
d = tempfile.mkdtemp()
subprocess.run(["pdftoppm", "-r", "40", "-gray", "-png", pdf, d + "/p"], check=True)
mm = 40 / 25.4
top, bot = int(26 * mm), int(242.5 * mm)
res = []
for f in sorted(glob.glob(d + "/*.png")):
    im = Image.open(f).convert("L"); w, h = im.size; px = im.load()
    last = None
    for y in range(bot, top, -1):
        if any(px[x, y] < 235 for x in range(int(15 * mm), w - int(15 * mm))):
            last = y; break
    n = int(f.rsplit("-", 1)[1].split(".")[0])
    # 整页满版底色（项目首页）跳过
    if px[w // 2, int(10 * mm)] < 200:
        continue
    gap = (bot - last) / mm if last else 999
    res.append((n, gap))
tot = sum(g for n, g in res if g < 999)
for n, g in res:
    if g >= th:
        print(f"p{n:3d}  空 {g:5.1f} mm")
print(f"pages={len(res)}  total_gap={tot:.0f} mm  big(>={th:.0f})={sum(1 for n,g in res if g>=th)}")
