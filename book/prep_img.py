#!/usr/bin/env python3
"""Crop the real Red Panda C++ screenshots (wine, 2x DPI) into book figures."""
from PIL import Image
import pathlib
S = pathlib.Path(__file__).resolve().parent.parent / "rp" / "shots"
D = pathlib.Path(__file__).resolve().parent / "img"
D.mkdir(exist_ok=True)
CROPS = {
    "ide_tour":        ("F_ide_hello_compiled.png", None),
    "ide_log_hello":   ("F_ide_hello_compiled.png", (0, 925, 2540, 1470)),
    "ide_err_semi":    ("c_semi.png", (0, 150, 1700, 1120)),
    "ide_err_case":    ("c_case.png", (0, 150, 1900, 1280)),
    "ide_opt_set":     ("F_opt_compilerset_dd.png", (600, 320, 1920, 1280)),
    "ide_opt_font":    ("F_opt_font.png", (600, 320, 1920, 1280)),
    "ide_menu_run":    ("F_runmenu.png", (380, 40, 1250, 780)),
    "ide_menu_new":    ("F_filenew.png", (0, 40, 1140, 640)),
    "ide_edit_profile":("F_edit_profile.png", (600, 150, 2300, 1180)),
    "ide_log_profile": ("F_profile_compiled.png", (0, 925, 2540, 1470)),
    "ide_badlab":      ("H_badlab.png", (0, 150, 2290, 1210)),
    "inst0":           ("inst0_lang.png", None),
    "inst1":           ("inst1.png", None),
    "inst2":           ("inst2.png", None),
    "inst3":           ("inst3.png", None),
    "inst4":           ("inst4.png", None),
    "inst5":           ("inst5.png", None),
    "inst6":           ("inst6.png", None),
    "inst7":           ("inst7_theme.png", None),
}
for name, (src, box) in CROPS.items():
    im = Image.open(S / src).convert("RGB")
    if box: im = im.crop(box)
    im.save(D / f"{name}.png", optimize=True)
    print(name, im.size)
