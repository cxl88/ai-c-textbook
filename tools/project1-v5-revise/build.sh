set -e
cd /tmp/claude-0/-home-claude/eb12d1b1-b62e-5147-8680-f587d91346f6/scratchpad/r5
rm -rf w; mkdir w; (cd w && unzip -q ../in/rev.docx && find . -type l -delete)
python3 /root/.claude/skills/synced/0b39bead-c5f9-420e-8044-7ba13cd8eea1_3c4d6224-8be0-4166-bf98-1be4ebda660a/docx/scripts/merge_runs.py w/ | tail -1
python3 -I edit.py w fig ph
python3 -I replies.py /tmp/claude-0/-home-claude/eb12d1b1-b62e-5147-8680-f587d91346f6/scratchpad/r5/w /root/.claude/skills/synced/0b39bead-c5f9-420e-8044-7ba13cd8eea1_3c4d6224-8be0-4166-bf98-1be4ebda660a/docx/scripts/comment.py
rm -f out.docx; (cd w && zip -qXr ../out.docx .)
python3 /root/.claude/skills/synced/0b39bead-c5f9-420e-8044-7ba13cd8eea1_3c4d6224-8be0-4166-bf98-1be4ebda660a/docx/scripts/office/validate.py out.docx --original in/rev.docx 2>&1 | tail -8
rm -rf wc; cp -r w wc; python3 -I clean.py wc
rm -f clean.docx; (cd wc && zip -qXr ../clean.docx .)
python3 /root/.claude/skills/synced/0b39bead-c5f9-420e-8044-7ba13cd8eea1_3c4d6224-8be0-4166-bf98-1be4ebda660a/docx/scripts/office/validate.py clean.docx --original in/rev.docx 2>&1 | tail -1
rm -rf rd rc; mkdir rd rc
python3 /tmp/claude-0/-home-claude/eb12d1b1-b62e-5147-8680-f587d91346f6/scratchpad/wd/render.py /tmp/claude-0/-home-claude/eb12d1b1-b62e-5147-8680-f587d91346f6/scratchpad/r5/out.docx /tmp/claude-0/-home-claude/eb12d1b1-b62e-5147-8680-f587d91346f6/scratchpad/r5/rd >/dev/null 2>&1
python3 /tmp/claude-0/-home-claude/eb12d1b1-b62e-5147-8680-f587d91346f6/scratchpad/wd/render.py /tmp/claude-0/-home-claude/eb12d1b1-b62e-5147-8680-f587d91346f6/scratchpad/r5/clean.docx /tmp/claude-0/-home-claude/eb12d1b1-b62e-5147-8680-f587d91346f6/scratchpad/r5/rc >/dev/null 2>&1
pdfinfo rd/out.pdf 2>/dev/null | grep Pages; pdfinfo rc/clean.pdf 2>/dev/null | grep Pages
