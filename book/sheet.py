import sys, glob
from PIL import Image
# usage: sheet.py pdf first last out.png [dpi]
import subprocess, os, tempfile
pdf, a, b, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
dpi = sys.argv[5] if len(sys.argv) > 5 else "70"
d = tempfile.mkdtemp()
subprocess.run(["pdftoppm", "-r", dpi, "-f", str(a), "-l", str(b), "-png", pdf, d + "/p"], check=True)
ims = [Image.open(f) for f in sorted(glob.glob(d + "/*.png"))]
w, h = ims[0].size
cols = min(len(ims), 2)
rows = (len(ims) + cols - 1) // cols
S = Image.new("RGB", (cols * w + (cols - 1) * 8, rows * h + (rows - 1) * 8), "#888")
for i, im in enumerate(ims):
    S.paste(im, ((i % cols) * (w + 8), (i // cols) * (h + 8)))
S.save(out)
