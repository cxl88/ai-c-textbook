# contact sheets: sheets.py dir  (pages p-NNN.png, 8 per sheet)
import glob, os, sys
from PIL import Image, ImageDraw
d0 = sys.argv[1]
files = sorted(glob.glob(os.path.join(d0, 'p-*.png')))
per = 8
for s in range(0, len(files), per):
    ims = [Image.open(f) for f in files[s:s+per]]
    w, h = ims[0].size
    sheet = Image.new('RGB', (4*(w+10)+10, 2*(h+30)+10), (128,128,128))
    d = ImageDraw.Draw(sheet)
    for i, im in enumerate(ims):
        x = 10 + (i%4)*(w+10); y = 30 + (i//4)*(h+30)
        sheet.paste(im, (x, y))
        d.text((x, y-22), os.path.basename(files[s+i])[2:5].lstrip('0'), fill=(255,255,255))
    sheet.save(os.path.join(d0, 'sheet%02d.png' % (s//per)))
print('sheets', (len(files)+per-1)//per)
