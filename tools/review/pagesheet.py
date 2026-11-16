# 把预览 PDF 拼成缩略图版面：每张 8 页（4×2），左上角红字为页码。逐页检查版面（页底留白、跨页、插图位置）用。
# 用法：python3 tools/review/pagesheet.py 预览.pdf 输出目录 [分辨率，默认 45]
# 需要 pdftoppm（poppler-utils）和 Pillow，生成环境容器中都已安装。
import glob
import os
import subprocess
import sys
import tempfile
from PIL import Image, ImageDraw

pdf, out = sys.argv[1:3]
dpi = sys.argv[3] if len(sys.argv) > 3 else '45'
os.makedirs(out, exist_ok=True)
with tempfile.TemporaryDirectory() as tmp:
    subprocess.run(['pdftoppm', '-r', dpi, '-png', pdf, f'{tmp}/p'], check=True)
    pages = sorted(glob.glob(f'{tmp}/p-*.png'))  # pdftoppm 按总页数补零，字典序即页序
    for k in range(0, len(pages), 8):
        ims = [Image.open(f) for f in pages[k:k + 8]]
        w, h = ims[0].size
        sheet = Image.new('RGB', (w * 4 + 30, h * 2 + 20), 'white')
        for i, im in enumerate(ims):
            x, y = (i % 4) * (w + 10), (i // 4) * (h + 20)
            sheet.paste(im, (x, y + 16))
            ImageDraw.Draw(sheet).text((x + 4, y), str(k + i + 1), fill='red')
        sheet.save(f'{out}/s{k // 8 + 1:02d}.png')
print(len(pages), 'pages ->', out)
