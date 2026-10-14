#!/usr/bin/env python3
"""docx -> pdf with LibreOffice; bookmarks become PDF named destinations so page numbers can be read back."""
import sys
sys.path.insert(0, '/root/.claude/skills/synced/0b39bead-c5f9-420e-8044-7ba13cd8eea1_3c4d6224-8be0-4166-bf98-1be4ebda660a/docx/scripts')
from office.soffice import run_soffice
src, outdir = sys.argv[1], sys.argv[2]
flt = 'pdf:writer_pdf_Export:{"ExportBookmarksToPDFDestination":{"type":"boolean","value":"true"},"ExportBookmarks":{"type":"boolean","value":"true"},"IsSkipEmptyPages":{"type":"boolean","value":"false"}}'
r = run_soffice(['--headless', '--convert-to', flt, '--outdir', outdir, src], capture_output=True, text=True, timeout=900)
print(r.stdout[-2000:], r.stderr[-2000:])
