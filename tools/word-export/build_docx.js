'use strict';
// Builds the editable Word version of the textbook from the JSON that walker.js extracted from the typeset HTML.
// Usage: node build_docx.js out.docx   (reads body.json, front.json, img/, and pages.json when present)
const docx = require('/opt/node22/lib/node_modules/docx');
const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell, WidthType, BorderStyle,
  ShadingType, AlignmentType, LineRuleType, TabStopType, Header, Footer, PageNumber, SectionType,
  NumberFormat, TableLayoutType, VerticalAlign, HorizontalPositionRelativeFrom, VerticalPositionRelativeFrom,
  BookmarkStart, BookmarkEnd, TableOfContents, LevelFormat, HeightRule, LeaderType, Tab,
} = docx;
// bookmarks are written as start/end markers with document-wide unique ids (docx-js Bookmark reuses id 1)
let bmSeq = 0;
function bmWrap(name, kids) { const id = ++bmSeq; return [new BookmarkStart(name, id), ...kids, new BookmarkEnd(id)]; }

const WD = __dirname;
const IMG = path.join(WD, 'img');
const OUT = process.argv[2] || path.join(WD, 'book.docx');
const PAGES = fs.existsSync(path.join(WD, 'pages.json')) ? JSON.parse(fs.readFileSync(path.join(WD, 'pages.json'), 'utf8')) : null;
const body = JSON.parse(fs.readFileSync(path.join(WD, 'body.json'), 'utf8'));
const front = JSON.parse(fs.readFileSync(path.join(WD, 'front.json'), 'utf8'));

// ---------------------------------------------------------------- units and page
const tw = (px) => Math.round((px || 0) * 15);          // CSS px -> twips
const ptw = (pt) => Math.round((pt || 0) * 20);         // pt -> twips
const hp = (pt) => Math.max(2, Math.round(pt * 2));     // pt -> half-points
const mmw = (mm) => Math.round(mm * 1440 / 25.4);       // mm -> twips
const PX_MM = 96 / 25.4;
const PAGE_W = mmw(185), PAGE_H = mmw(260);
const MAR = { top: mmw(21), bottom: mmw(20), inside: mmw(20), outside: mmw(17), header: mmw(12), footer: mmw(10) };
const TEXT_W = PAGE_W - MAR.inside - MAR.outside;
const TEXT_PX = TEXT_W / 15;
const BOOK = '人工智能助力C语言程序设计';

const FONT = {
  serif: { ascii: 'Times New Roman', hAnsi: 'Times New Roman', eastAsia: '宋体', cs: 'Times New Roman', hint: 'eastAsia' },
  sans: { ascii: 'Arial', hAnsi: 'Arial', eastAsia: '微软雅黑', cs: 'Arial', hint: 'eastAsia' },
  monoL: { ascii: 'Consolas', hAnsi: 'Consolas', eastAsia: '微软雅黑', cs: 'Consolas' },
  monoW: { ascii: 'Consolas', hAnsi: 'Consolas', eastAsia: '微软雅黑', cs: 'Consolas', hint: 'eastAsia' },
};
const fontOf = (f) => FONT[f] || FONT.serif;
const AL = { justify: AlignmentType.JUSTIFIED, left: AlignmentType.LEFT, start: AlignmentType.LEFT, center: AlignmentType.CENTER, right: AlignmentType.RIGHT, end: AlignmentType.RIGHT };
const VA = { top: VerticalAlign.TOP, middle: VerticalAlign.CENTER, bottom: VerticalAlign.BOTTOM };
const EXACT = LineRuleType.EXACT, ATLEAST = LineRuleType.AT_LEAST, AUTO = LineRuleType.AUTO;
const NIL = { style: BorderStyle.NONE, size: 0, color: 'auto' };
const NOB = { top: NIL, bottom: NIL, left: NIL, right: NIL, insideHorizontal: NIL, insideVertical: NIL };
const shd = (c) => (c ? { type: ShadingType.CLEAR, fill: c, color: 'auto' } : undefined);

// ---------------------------------------------------------------- borders
function bsz(px) { return px <= 1.01 ? 4 : Math.max(4, Math.round(px * 0.75 * 8)); }
function bstyle(st) { return st === 'dashed' ? BorderStyle.DASHED : st === 'dotted' ? BorderStyle.DOTTED : st === 'double' ? BorderStyle.DOUBLE : BorderStyle.SINGLE; }
function bor(side, spacePt) {
  if (!side || !side.c) return undefined;
  const o = { style: bstyle(side.st), size: bsz(side.w), color: side.c };
  if (spacePt !== undefined) o.space = Math.max(0, Math.min(31, Math.round(spacePt)));
  return o;
}
function cellBorders(bd, over) {
  bd = bd || {};
  const o = { top: bor(bd.t) || NIL, bottom: bor(bd.b) || NIL, left: bor(bd.l) || NIL, right: bor(bd.r) || NIL };
  return Object.assign(o, over || {});
}
const padTw = (p) => ({ top: tw(p && p.t), bottom: tw(p && p.b), left: tw(p && p.l), right: tw(p && p.r) });
const bw = (side) => (side && side.c ? side.w : 0);

// ---------------------------------------------------------------- images
const imgCache = {};
function imgData(name) {
  if (!imgCache[name]) imgCache[name] = fs.readFileSync(path.join(IMG, name));
  return imgCache[name];
}
function imageRun(id, wpx, hpx, extra) {
  const name = /\./.test(id) ? id : id + '.png';
  return new ImageRun(Object.assign({ type: /\.jpe?g$/.test(name) ? 'jpg' : 'png', data: imgData(name), transformation: { width: +wpx.toFixed(2), height: +hpx.toFixed(2) } }, extra || {}));
}

// ---------------------------------------------------------------- runs
const UL = { single: 'single', wave: 'wave', dash: 'dash', dotted: 'dotted' };
// characters that the print font draws at full width inside code (CJK, full-width forms, circled numbers, ℃)
const WIDE = /[℃①-⓿⺀-鿿ꀀ-꓏가-힯豈-﫿︐-︟︰-﹏＀-｠￠-￦]/;
function splitWide(t) {
  const out = [];
  for (const ch of t) {
    const w = WIDE.test(ch);
    const last = out[out.length - 1];
    if (last && last.w === w) last.t += ch; else out.push({ t: ch, w });
  }
  return out;
}
// base: the run formatting of the paragraph style; matching properties are left to the style so that
// editing the style in Word changes the text (and the TOC does not pick up heading formatting)
function runOpts(r, text, extra, base) {
  const x = { text };
  if (!base || (r.f || 'serif') !== base.f) x.font = fontOf(r.f);
  if (!base || Math.abs((r.sz || 10.5) - base.sz) > 0.01) x.size = hp(r.sz || 10.5);
  if (r.c && !(base && r.c === base.c)) x.color = r.c;
  if (r.b && !(base && base.b)) x.bold = true;
  if (r.i) x.italics = true;
  if (r.bg) x.shading = shd(r.bg);
  if (r.bd && r.bd.c) x.border = { style: BorderStyle.SINGLE, size: 4, color: r.bd.c, space: 0 };
  if (r.sup) x.superScript = true;
  if (r.sub) x.subScript = true;
  if (r.u) x.underline = { type: UL[r.u] || 'single', color: r.uc || undefined };
  if (r.ls) x.characterSpacing = Math.round(r.ls * 20);
  return Object.assign(x, extra || {});
}
const half = (v) => Math.round(v * 2) / 2;
function inlineMono(sz) { return { L: half((sz || 10.5) * 0.9), W: half(sz || 10.5) }; }
function monoRuns(r, sizes) {
  return splitWide(r.t).map((s) => new TextRun(runOpts(r, s.t, { font: s.w ? FONT.monoW : FONT.monoL, size: hp(s.w ? sizes.W : sizes.L) })));
}
const bmName = (anchor) => 'ref_' + anchor.replace(/[^A-Za-z0-9]/g, '_');
function refPage(anchor, fallback) {
  if (PAGES && PAGES.bm && PAGES.bm[bmName(anchor)] !== undefined) return String(PAGES.bm[bmName(anchor)]);
  return fallback;
}
const usedRefs = new Set();
function children(runs, ctx) {
  const out = [];
  const base = ctx && ctx.base;
  (runs || []).forEach((r, i) => {
    out.push(...runKids(r, ctx, base));
    // a shaded label padded with no-break spaces keeps a clear gap before the unshaded text after it
    const nx = runs[i + 1];
    if (r.bg && /\u00a0$/.test(r.t || '') && nx && nx.t && !nx.bg && !/^\s/.test(nx.t)) out.push(new TextRun(runOpts({ f: r.f, sz: r.sz }, '\u00a0', undefined, base)));
  });
  return out;
}
function runKids(r, ctx, base) {
  if (r.br) return [new TextRun({ break: 1 })];
  if (r.cs) return [new TextRun({ text: r.t, style: r.cs })];
  if (r.tab) return [new TextRun({ children: [new Tab()] })];
  if (r.node) return [r.node];
  if (r.img) return [imageRun(r.img, r.w, r.h)];
  if (r.t === undefined || r.t === '') return [];
  if (r.pref) {
    usedRefs.add(bmName(r.pref));
    return [new TextRun(runOpts(r, `⟦PAGEREF:${bmName(r.pref)}:${refPage(r.pref, r.t)}⟧`, undefined, base))];
  }
  if (r.f === 'mono') return monoRuns(r, (ctx && ctx.mono) || inlineMono(r.sz));
  return [new TextRun(runOpts(r, r.t, undefined, base))];
}
const plain = (runs) => (runs || []).map((r) => (r.t !== undefined ? r.t : (r.br ? '\n' : ''))).join('');

// ---------------------------------------------------------------- items -> docx objects
// An item is {k:'p', o: paragraph options, gap} or {k:'t', o: table spec, gap}; gaps are twips above the item.
function P(o, gap) { return { k: 'p', o, gap }; }
function spacer(h) {
  return P({ children: [], spacing: { before: 0, after: 0, line: Math.max(20, Math.round(h)), lineRule: EXACT }, run: { size: 2 } }, 0);
}
function realize(items, opt) {
  opt = opt || {};
  const seq = [];
  items.forEach((it, idx) => {
    let gap = Math.max(0, Math.round(it.gap || 0));
    if (idx === 0 && opt.dropFirstGap) gap = 0;
    const prev = seq[seq.length - 1];
    if (it.k === 'p') {
      it.o.spacing = Object.assign({ before: 0, after: 0 }, it.o.spacing || {});
      it.o.spacing.before = (it.o.spacing.before || 0) + gap;
      seq.push(it);
    } else {
      if (prev && prev.k === 'p') prev.o.spacing.after = (prev.o.spacing.after || 0) + gap;
      else if (prev) seq.push(spacer(gap));
      else if (gap > 0) seq.push(spacer(gap));
      seq.push(it);
    }
  });
  if (opt.cell && (!seq.length || seq[seq.length - 1].k === 't')) seq.push(spacer(20));
  return seq.map((it) => (it.k === 'p' ? new Paragraph(it.o) : buildTable(it.o)));
}
function buildTable(s) {
  const rows = s.rows.map((r) => new TableRow({
    children: r.cells.map((c) => new TableCell({
      children: realize(c.items, { cell: true }),
      width: { size: c.w, type: WidthType.DXA },
      columnSpan: c.span > 1 ? c.span : undefined,
      rowSpan: c.rowSpan > 1 ? c.rowSpan : undefined,
      borders: c.borders || cellBorders(null),
      shading: c.shading,
      margins: c.margins || { top: 0, bottom: 0, left: 0, right: 0 },
      verticalAlign: c.valign,
    })),
    cantSplit: !!r.cantSplit,
    tableHeader: !!r.header,
    height: r.height,
  }));
  const total = s.cols.reduce((a, b) => a + b, 0);
  return new Table({
    rows, columnWidths: s.cols, width: { size: total, type: WidthType.DXA }, layout: TableLayoutType.FIXED,
    borders: NOB, margins: { top: 0, bottom: 0, left: 0, right: 0 },
    indent: s.indent ? { size: s.indent, type: WidthType.DXA } : undefined,
    alignment: s.align,
  });
}
function T(spec, gap) { return { k: 't', o: spec, gap }; }
function fitCols(pxList, totalTw) {
  // integer twips that add up exactly to totalTw
  const sum = pxList.reduce((a, b) => a + b, 0);
  const out = pxList.map((v) => Math.floor((v / sum) * totalTw));
  out[out.length - 1] += totalTw - out.reduce((a, b) => a + b, 0);
  return out;
}

// ---------------------------------------------------------------- paragraphs
const BODY_BASE = { f: 'serif', sz: 10.5, c: '1F1F1F', b: false };
function isBody(b, ctx) {
  return !ctx.inner && b.t === 'p' && Math.abs(b.fs - 10.5) < 0.01 && Math.abs(b.indent - 21) < 0.5 && b.font === 'serif' && b.align === 'justify' && !b.bg && !(b.bd && (b.bd.t || b.bd.b || b.bd.l || b.bd.r)) && !b.ml;
}
function pItem(b, ctx, extra) {
  extra = extra || {};
  const runs = extra.runs || b.runs || [];
  const hasImg = runs.some((r) => r.img);
  const fs0 = b.fs || 10.5;
  const lh = b.lh || fs0 * 1.5;
  const body = !extra.forceDirect && isBody(b, ctx);
  let kids = children(runs, body ? Object.assign({}, ctx, { base: BODY_BASE }) : ctx);
  if (b.anchor) kids = [...bmWrap(bmName(b.anchor), kids)];
  const o = { children: kids };
  if (body) {
    o.style = 'BodyText';
  } else {
    o.alignment = AL[extra.align || b.align] || AlignmentType.LEFT;
    o.spacing = { before: 0, after: 0, line: ptw(lh), lineRule: hasImg ? ATLEAST : EXACT };
    o.run = { font: fontOf(b.font), size: hp(fs0), color: b.color || undefined };
    const ind = {};
    if (b.indent) ind.firstLine = ptw(b.indent);
    if (b.ml) ind.left = ptw(b.ml);
    if (b.mr) ind.right = ptw(b.mr);
    if (Object.keys(ind).length) o.indent = ind;
    if (b.bg) o.shading = shd(b.bg);
    const bd = b.bd || {};
    const p = b.pad || {};
    if (bd.t || bd.b || bd.l || bd.r) {
      o.border = {};
      if (bd.t) o.border.top = bor(bd.t, (p.t || 0) * 0.75);
      if (bd.b) o.border.bottom = bor(bd.b, (p.b || 0) * 0.75);
      if (bd.l) o.border.left = bor(bd.l, (p.l || 0) * 0.75);
      if (bd.r) o.border.right = bor(bd.r, (p.r || 0) * 0.75);
    }
    if (extra.style) o.style = extra.style;
  }
  if (extra.keepNext) o.keepNext = true;
  return P(o);
}
// badge runs (white text on the main colour) get no-break spaces inside the shading
function padBadge(r, n) {
  const sp = Object.assign({}, r, { t: ' '.repeat(n) });
  delete sp.ls;
  return [sp, Object.assign({}, r, { t: r.t.replace(/^ +| +$/g, '') }), sp];
}
function gapRun(r) { return { t: '　', f: r.f, sz: r.sz }; }
function stepItem(b, ctx) {
  const runs = [];
  b.runs.forEach((r, i) => {
    if (i === 0 && r.bg) { runs.push(...padBadge(r, 2), gapRun(r)); } else runs.push(r);
  });
  return pItem(Object.assign({}, b, { align: 'left' }), ctx, { runs, keepNext: true, forceDirect: true });
}
function capItem(b, ctx, style) {
  const runs = [];
  b.runs.forEach((r, i) => {
    runs.push(r);
    const nx = b.runs[i + 1];
    if (i === 0 && r.b && nx && nx.t && !/^\s/.test(nx.t)) runs.push({ t: '  ', f: r.f, sz: r.sz });
  });
  return pItem(b, ctx, { runs, style: style || 'FigCap', keepNext: style === 'TabCap', forceDirect: true });
}

// ---------------------------------------------------------------- headings and TOC entries
const tocEntries = [];
let tocN = 0;
function tocBookmark(title, level) {
  const id = '_Toc' + String(100000 + (++tocN));
  tocEntries.push({ title, level, href: id });
  return id;
}
const HBASE = {
  2: { f: 'sans', sz: 15, c: '153A6B', b: true }, 3: { f: 'sans', sz: 12, c: '1D4F91', b: true },
  4: { f: 'sans', sz: 11, c: '153A6B', b: true }, 5: { f: 'sans', sz: 10.5, c: '1F1F1F', b: true },
};
function headingItem(b, ctx) {
  let level = b.level;
  let runs = b.runs;
  const isTask = runs.length > 1 && runs[0].bg;
  if (isTask) runs = [{ t: '\u00a0' + runs[0].t.replace(/^[\s\u00a0]+|[\s\u00a0]+$/g, '') + '\u00a0', cs: 'TaskBadge' }, gapRun(runs[0]), ...runs.slice(1)];
  let kids = children(runs, Object.assign({}, ctx, { base: HBASE[Math.min(5, level)] }));
  const style = 'Heading' + Math.min(5, level);
  const o = { style, children: kids };
  if (b.ml) o.indent = { left: ptw(b.ml) };
  if (b.anchor) o.children = [...bmWrap(bmName(b.anchor), o.children)];
  if (level === 2 && !ctx.noToc) {
    const title = isTask ? b.runs[0].t.replace(/ /g, '').trim() + '　' + plain(b.runs.slice(1)).trim() : plain(b.runs).trim();
    o.children = bmWrap(tocBookmark(title, 2), o.children);
  }
  return P(o);
}
function appendixTitle(b, ctx) {
  // the appendix title is a level-1 TOC entry but looks like the h2 headings
  const title = plain(b.runs).replace(/\s+/g, ' ').trim().replace(/^(附录A)\s*/, '$1　');
  const o = { style: 'AppendixTitle', children: bmWrap(tocBookmark(title, 1), children(b.runs, Object.assign({}, ctx, { base: HBASE[2] }))) };
  if (b.anchor) o.children = [...bmWrap(bmName(b.anchor), o.children)];
  return P(o);
}

// ---------------------------------------------------------------- lists
const LIST = {
  decimal: { format: LevelFormat.DECIMAL, text: '%1.', run: {} },
  paren: { format: LevelFormat.DECIMAL, text: '（%1）', run: { font: FONT.sans } },
  bullet: { format: LevelFormat.BULLET, text: '•', run: { font: { ascii: 'Arial', hAnsi: 'Arial', eastAsia: 'Arial', cs: 'Arial' } } },
  dash: { format: LevelFormat.BULLET, text: '—', run: { color: '1D4F91', font: FONT.serif } },
  check: { format: LevelFormat.BULLET, text: '□', run: { color: '1D4F91', font: FONT.sans } },
};
let listInst = 0;
function listItems(b, ctx) {
  const inst = ++listInst;
  const ref = 'L-' + b.kind;
  const leftPt = (b.ml || 0) + (b.indent || 0);
  const out = [];
  b.items.forEach((it, i) => {
    let first = true;
    for (const part of it.parts) {
      const gap = first ? (i === 0 ? undefined : tw(it.gap || 0)) : 0;
      if (part.t === 'runs') {
        const p = pItem({ runs: part.runs, align: ctx.inBox ? 'left' : 'justify', fs: it.fs, lh: it.lh, color: it.color, font: it.font }, ctx, { forceDirect: true });
        p.o.indent = first ? { left: ptw(leftPt), hanging: ptw(b.indent || 0) } : { left: ptw(leftPt) };
        if (first) p.o.numbering = { reference: ref, level: 0, instance: inst };
        p.gap = gap;
        out.push(p);
      } else if (part.t === 'opts') {
        const os = optsItems(part, ctx, leftPt / 0.75, it.lh);
        out.push(...os);
      } else {
        const sub = blockItems(part, Object.assign({}, ctx, { w: ctx.w - leftPt / 0.75, inner: true }));
        sub.forEach((s, k) => {
          if (s.k === 't') s.o.indent = (s.o.indent || 0) + ptw(leftPt);
          else s.o.indent = Object.assign({}, s.o.indent || {}, { left: ((s.o.indent && s.o.indent.left) || 0) + ptw(leftPt) });
          if (k === 0) s.gap = first ? gap : (part.t === 'code' ? ptw(4) : 0);
        });
        out.push(...sub);
      }
      first = false;
    }
  });
  return out;
}
function optsItems(b, ctx, leftPx, lh) {
  return b.rows.map((row, ri) => {
    const runs = [];
    row.forEach((it, i) => { if (i > 0) runs.push({ tab: 1 }); runs.push(...it.runs); });
    const p = pItem({ runs, align: 'left', fs: b.fs, lh: lh || b.fs * 1.68, font: 'serif', color: '333333' }, ctx, { forceDirect: true });
    p.o.indent = { left: tw(leftPx + row[0].x) };
    p.o.tabStops = row.slice(1).map((it) => ({ type: TabStopType.LEFT, position: tw(leftPx + it.x) }));
    p.gap = ri === 0 ? (b.gap !== undefined ? tw(b.gap) : 0) : 0;
    return p;
  });
}

// ---------------------------------------------------------------- tables
function tableItems(b, ctx) {
  const width = Math.min(ctx.w, b.w);
  const totalTw = Math.min(tw(width), tw(ctx.w));
  const cols = fitCols(b.cols, totalTw);
  const long = /\blong\b/.test(b.cls);
  const occupied = [];
  const rows = b.rows.map((r, ri) => {
    let col = 0;
    const cells = [];
    for (const c of r.cells) {
      while (occupied[ri] && occupied[ri].has(col)) col++;
      const span = c.cs || 1;
      const w = cols.slice(col, col + span).reduce((a, x) => a + x, 0);
      for (let k = 1; k < (c.rs || 1); k++) {
        occupied[ri + k] = occupied[ri + k] || new Set();
        for (let j = col; j < col + span; j++) occupied[ri + k].add(j);
      }
      const pad = c.pad || {};
      const cctx = Object.assign({}, ctx, { w: w / 15 - (pad.l || 0) - (pad.r || 0), inner: true, inBox: false });
      const items = [];
      for (const part of c.parts) {
        if (part.t === 'runs') items.push(pItem({ runs: part.runs, align: c.align, fs: c.fs, lh: c.lh, color: c.color, font: c.font }, cctx, { forceDirect: true }));
        else items.push(...blockItems(part, cctx));
      }
      if (!items.length) items.push(pItem({ runs: [], align: c.align, fs: c.fs, lh: c.lh, font: c.font }, cctx, { forceDirect: true }));
      if (!long && ri < b.rows.length - 1) items.forEach((it) => { if (it.k === 'p') it.o.keepNext = true; });
      cells.push({ items, w, span, rowSpan: c.rs || 1, borders: cellBorders(c.bd), shading: shd(c.bg), margins: padTw(pad), valign: VA[c.valign] });
      col += span;
    }
    const blankRow = r.cells.some((c) => c.empty);
    return { cells, header: r.header, cantSplit: true, height: blankRow ? { value: tw(r.h), rule: HeightRule.ATLEAST } : undefined };
  });
  const spec = { cols, rows };
  if (b.centered || width < ctx.w - 4) spec.align = AlignmentType.CENTER;
  return [T(spec)];
}

// ---------------------------------------------------------------- code, console, run window
// Consolas advances 0.55 em; the fit check uses 0.6 em so lines also fit when a wider fallback font is used
const MONO_ADV = 0.6;
function lineUnits(runs, lnDigits) {
  let n = lnDigits ? lnDigits + 2 : 0;
  for (const r of runs) { if (r.ln) continue; for (const ch of r.t || '') n += WIDE.test(ch) ? 2 : 1; }
  return n;
}
function monoSizes(lines, availPt, cssFs, lnDigits) {
  let L = cssFs >= 9.9 ? 9 : 8.5;   // print: Latin code text about 9 pt
  const units = Math.max(1, ...lines.map((l) => lineUnits(l, lnDigits)));
  while (L > 6.5 && L * MONO_ADV * units > availPt - 1.5) L -= 0.5;
  return { L, W: L + 1 };
}
function codeLine(runs, sizes, lhPt, lnDigits, color) {
  const out = [];
  for (const r of runs) {
    if (r.ln) {
      out.push(new TextRun(runOpts(r, r.t.padStart(lnDigits, ' ') + '  ', { font: FONT.monoL, size: hp(sizes.L) })));
      continue;
    }
    if (!r.t) continue;
    out.push(...monoRuns(r, sizes));
  }
  return P({
    style: 'Code', children: out, alignment: AlignmentType.LEFT,
    spacing: { before: 0, after: 0, line: ptw(lhPt), lineRule: EXACT },
    run: { font: FONT.monoL, size: hp(sizes.L), color: color || undefined },
  });
}
function barPara(st, left, right, innerPx, extra) {
  const runs = [...(left || [])];
  if (right && right.length) { runs.push({ tab: 1 }, ...right); }
  const p = pItem({ runs, align: 'left', fs: st.fs, lh: st.lh || st.fs * 1.4, font: st.font, color: st.color }, { inner: true }, { forceDirect: true });
  if (right && right.length) p.o.tabStops = [{ type: TabStopType.RIGHT, position: tw(innerPx) }];
  Object.assign(p.o, extra || {});
  return p;
}
function codeItems(b, ctx) {
  const st = b.style;
  const bd = st.bd || {};
  const pad = st.pad || {};
  const wPx = ctx.w;
  const innerPx = wPx - (pad.l || 0) - (pad.r || 0) - bw(bd.l) - bw(bd.r);
  const lnDigits = b.ln ? String(b.lines.length).length : 0;
  const sizes = monoSizes(b.lines, innerPx * 0.75, st.fs, lnDigits);
  const lines = b.lines.map((l) => codeLine(l, sizes, st.lh, lnDigits, st.color));
  const rows = [];
  const chunks = codeChunks(b.lines);
  if (b.title) {
    const t = b.title;
    const tp = barPara(t, t.runs, null, innerPx, { keepNext: true });
    rows.push({ cells: [{ items: [tp], w: tw(wPx), borders: { top: bor(bd.t) || NIL, left: bor(bd.l) || NIL, right: bor(bd.r) || NIL, bottom: bor(t.bd && t.bd.b) || NIL }, shading: shd(t.bg), margins: { top: tw(t.pad.t), bottom: tw(t.pad.b), left: tw(pad.l), right: tw(pad.r) } }], cantSplit: true, header: chunks.length > 1 });
  }
  chunks.forEach(([s, e], ci) => {
    const part = lines.slice(s, e);
    part.slice(0, -1).forEach((l) => { l.o.keepNext = true; });
    const first = ci === 0, last = ci === chunks.length - 1;
    rows.push({ cells: [{ items: part, w: tw(wPx), borders: { top: first && !b.title ? (bor(bd.t) || NIL) : NIL, left: bor(bd.l) || NIL, right: bor(bd.r) || NIL, bottom: last ? (bor(bd.b) || NIL) : NIL }, shading: shd(st.bg), margins: { top: first ? tw(pad.t) : 0, bottom: last ? tw(pad.b) : 0, left: tw(pad.l), right: tw(pad.r) } }], cantSplit: true });
  });
  return [T({ cols: [tw(wPx)], rows })];
}
// as in print: programs of 21 lines or more may break only at blank lines, leaving at least 8 lines on each side
const LONG_CODE = 21, MIN_CHUNK = 8;
function codeChunks(lines) {
  const n = lines.length;
  if (n < LONG_CODE) return [[0, n]];
  const blank = (l) => !l.some((r) => !r.ln && r.t && r.t.trim());
  const out = [];
  let start = 0;
  lines.forEach((l, i) => {
    const end = i + 1;   // the blank line ends its chunk
    if (blank(l) && end - start >= MIN_CHUNK && n - end >= MIN_CHUNK) { out.push([start, end]); start = end; }
  });
  out.push([start, n]);
  return out;
}
function consoleItems(b, ctx) {
  const st = b.style;
  const bd = st.bd || {};
  const pad = st.pad || {};
  const wPx = ctx.w;
  const innerPx = wPx - (pad.l || 0) - (pad.r || 0) - bw(bd.l) - bw(bd.r);
  const sizes = monoSizes(b.lines, innerPx * 0.75, st.fs, 0);
  const lines = b.lines.map((l) => codeLine(l, sizes, st.lh, 0, st.color));
  lines.slice(0, -1).forEach((l) => { l.o.keepNext = true; });
  const rows = [];
  if (b.label) {
    const lb = b.label;
    const lp = barPara(lb, lb.runs, null, innerPx, { keepNext: true });
    rows.push({ cells: [{ items: [lp], w: tw(wPx), borders: { top: bor(bd.t) || NIL, left: bor(bd.l) || NIL, right: bor(bd.r) || NIL, bottom: bor(lb.bd && lb.bd.b) || NIL }, shading: shd(st.bg), margins: { top: tw(pad.t), bottom: tw(lb.pad.b), left: tw(pad.l), right: tw(pad.r) } }], cantSplit: true });
  }
  rows.push({ cells: [{ items: lines, w: tw(wPx), borders: { top: b.label ? NIL : (bor(bd.t) || NIL), left: bor(bd.l) || NIL, right: bor(bd.r) || NIL, bottom: bor(bd.b) || NIL }, shading: shd(st.bg), margins: { top: tw(b.label ? 5.33 : pad.t), bottom: tw(pad.b), left: tw(pad.l), right: tw(pad.r) } }], cantSplit: true });
  return [T({ cols: [tw(wPx)], rows })];
}
function conwinItems(b, ctx) {
  const winPx = ctx.w * 0.96;
  const st = b.style;
  const bd = st.bd || {};
  const bar = b.bar;
  const bodyS = b.body;
  const bpad = bodyS.pad || {};
  const innerPx = winPx - (bpad.l || 0) - (bpad.r || 0) - bw(bd.l) - bw(bd.r);
  const sizes = monoSizes(bodyS.lines, innerPx * 0.75, bodyS.fs, 0);
  const lines = bodyS.lines.map((l) => codeLine(l, sizes, bodyS.lh, 0, bodyS.color));
  lines.slice(0, -1).forEach((l) => { l.o.keepNext = true; });
  // title bar: icon, title, window buttons at the right
  const barInner = winPx - (bar.pad.l || 0) - bw(bd.l) - bw(bd.r);
  const left = [];
  if (bar.ico) left.push({ img: bar.ico.id, w: bar.ico.w, h: bar.ico.h }, { t: '  ', f: 'sans', sz: bar.fs });
  left.push(...bar.title);
  const right = bar.btn ? [{ img: bar.btn.id, w: bar.btn.w, h: bar.btn.h }] : [];
  const bp = barPara(Object.assign({}, bar, { lh: bar.h * 0.75 - 1 }), left, right, barInner - 2, { keepNext: true });
  bp.o.spacing = { before: 0, after: 0, line: ptw(bar.h * 0.75 - 1), lineRule: EXACT };
  const rows = [
    { cells: [{ items: [bp], w: tw(winPx), borders: { top: bor(bd.t) || NIL, left: bor(bd.l) || NIL, right: bor(bd.r) || NIL, bottom: bor(bar.bd && bar.bd.b) || NIL }, shading: shd(bar.bg), margins: { top: 0, bottom: 0, left: tw(bar.pad.l), right: 0 }, valign: VerticalAlign.CENTER }], cantSplit: true, height: { value: tw(bar.h), rule: HeightRule.EXACT } },
    { cells: [{ items: lines, w: tw(winPx), borders: { top: NIL, left: bor(bd.l) || NIL, right: bor(bd.r) || NIL, bottom: bor(bd.b) || NIL }, shading: shd(bodyS.bg), margins: padTw(bpad) }], cantSplit: true },
  ];
  return [T({ cols: [tw(winPx)], rows, align: AlignmentType.CENTER })];
}

// ---------------------------------------------------------------- figures
function imgItem(b, ctx) {
  const s = Math.min(1, ctx.w / b.w);
  return P({ alignment: AlignmentType.CENTER, keepNext: true, spacing: { before: 0, after: 0, line: 240, lineRule: AUTO }, children: [imageRun(b.id, b.w * s, b.h * s)] });
}
function gridItems(b, ctx) {
  const rowsMap = [];
  for (const it of b.items) {
    let row = rowsMap.find((r) => Math.abs(r.y - it.y) < 3);
    if (!row) { row = { y: it.y, items: [] }; rowsMap.push(row); }
    row.items.push(it);
  }
  // column layout from the first full row
  const ref = rowsMap.reduce((a, r) => (r.items.length > a.items.length ? r : a), rowsMap[0]);
  const colPx = [];
  let x = 0;
  ref.items.forEach((it, i) => {
    if (i > 0) colPx.push(it.x - x);
    colPx.push(it.w);
    x = it.x + it.w;
  });
  const scale = Math.min(1, ctx.w / x);
  const cols = fitCols(colPx, tw(x * scale));
  const rows = rowsMap.map((r) => {
    const cells = [];
    ref.items.forEach((slot, i) => {
      if (i > 0) cells.push({ items: [spacer(20)], w: cols[cells.length], borders: cellBorders(null) });
      const it = r.items[i];
      const w = cols[cells.length];
      const items = [];
      if (it) {
        const s = Math.min(1, (w / 15) / it.img.w);
        items.push(P({ alignment: AlignmentType.CENTER, spacing: { before: 0, after: 0, line: 240, lineRule: AUTO }, keepNext: true, children: [imageRun(it.img.id, it.img.w * s, it.img.h * s)] }));
        if (it.cap) { const cp = capItem(it.cap, Object.assign({}, ctx, { w: w / 15, inner: true })); cp.gap = ptw(3); items.push(cp); }
      } else items.push(spacer(20));
      cells.push({ items, w, borders: cellBorders(null) });
    });
    return { cells, cantSplit: true };
  });
  rows.forEach((r, i) => { if (i > 0) r.cells.forEach((c) => { c.items[0].gap = ptw(7); }); });
  return [T({ cols, rows })];
}

// ---------------------------------------------------------------- boxes
function blocksItems(blocks, ctx) {
  const out = [];
  for (const b of blocks || []) out.push(...blockItems(b, ctx));
  return out;
}
function titlePara(t, innerPx) {
  const p = barPara(t, t.runs, t.right, innerPx, { keepNext: true });
  if (t.runs.some((r) => r.img)) p.o.spacing = { before: 0, after: 0, line: ptw(t.lh || 16), lineRule: ATLEAST };
  return p;
}
function boxItems(b, ctx) {
  const st = b.style;
  const bd = st.bd || {};
  const wPx = ctx.w;
  const rows = [];
  const canSplit = (b.h || 0) > 450;
  if (b.head) {
    const h = b.head;
    const bs = b.bodyStyle || {};
    const bpad = bs.pad || {};
    const hInner = wPx - (h.pad.l || 0) - (h.pad.r || 0) - bw(bd.l) - bw(bd.r);
    const hp0 = barPara(h, h.left, h.right, hInner, { keepNext: true });
    rows.push({ cells: [{ items: [hp0], w: tw(wPx), borders: { top: bor(bd.t) || NIL, left: bor(bd.l) || NIL, right: bor(bd.r) || NIL, bottom: bor(h.bd && h.bd.b) || NIL }, shading: shd(h.bg), margins: padTw(h.pad) }], cantSplit: true });
    const inner = wPx - (bpad.l || 0) - (bpad.r || 0) - bw(bd.l) - bw(bd.r);
    const items = blocksItems(b.blocks, Object.assign({}, ctx, { w: inner, inner: true, inBox: true }));
    rows.push({ cells: [{ items, w: tw(wPx), borders: { top: NIL, left: bor(bd.l) || NIL, right: bor(bd.r) || NIL, bottom: bor(bd.b) || NIL }, shading: shd(bs.bg), margins: padTw(bpad) }], cantSplit: !canSplit });
  } else {
    const pad = st.pad || {};
    const inner = wPx - (pad.l || 0) - (pad.r || 0) - bw(bd.l) - bw(bd.r);
    const items = [];
    if (b.title) items.push(titlePara(b.title, inner));
    const inn = blocksItems(b.blocks, Object.assign({}, ctx, { w: inner, inner: true, inBox: true }));
    if (b.title && inn.length) inn[0].gap = Math.max(0, (inn[0].gap || 0) - tw(b.title.h));
    items.push(...inn);
    rows.push({ cells: [{ items, w: tw(wPx), borders: cellBorders(bd), shading: shd(st.bg), margins: padTw(pad) }], cantSplit: !canSplit });
  }
  return [T({ cols: [tw(wPx)], rows })];
}
function chatItems(b, ctx) {
  const st = b.style;
  const bd = st.bd || {};
  const wPx = ctx.w;
  const h = b.head;
  const bs = b.bodyStyle;
  const hInner = wPx - (h.pad.l || 0) - (h.pad.r || 0) - bw(bd.l) - bw(bd.r);
  const rows = [];
  rows.push({ cells: [{ items: [barPara(h, h.left, h.right, hInner, { keepNext: true })], w: tw(wPx), borders: { top: bor(bd.t) || NIL, left: bor(bd.l) || NIL, right: bor(bd.r) || NIL, bottom: bor(h.bd && h.bd.b) || NIL }, shading: shd(h.bg), margins: padTw(h.pad) }], cantSplit: true });
  const inner = wPx - (bs.pad.l || 0) - (bs.pad.r || 0) - bw(bd.l) - bw(bd.r);
  const items = [];
  b.msgs.forEach((m, i) => {
    const scale = Math.min(1, inner / m.mw);
    const av = m.av;
    const segs = [{ kind: 'bub', x: m.bub.x, w: m.bub.w }];
    if (av) segs.push({ kind: 'av', x: m.avx, w: av.w });
    segs.sort((a, c) => a.x - c.x);
    const colPx = [];
    const kinds = [];
    let x = 0;
    for (const s of segs) {
      if (s.x > x + 0.5) { colPx.push(s.x - x); kinds.push('gap'); }
      colPx.push(s.w); kinds.push(s.kind);
      x = s.x + s.w;
    }
    if (m.mw > x + 0.5) { colPx.push(m.mw - x); kinds.push('gap'); }
    const cols = fitCols(colPx, Math.floor(tw(m.mw * scale)));
    const cells = kinds.map((k, j) => {
      if (k === 'av') return { items: [P({ spacing: { before: 0, after: 0, line: 240, lineRule: AUTO }, children: [imageRun(av.id, av.w, av.h)] })], w: cols[j], borders: cellBorders(null) };
      if (k === 'bub') {
        const bp = m.bub.pad || {};
        const binner = cols[j] / 15 - (bp.l || 0) - (bp.r || 0);
        const its = blocksItems(m.parts, Object.assign({}, ctx, { w: binner, inner: true, inBox: true }));
        return { items: its.length ? its : [spacer(20)], w: cols[j], borders: cellBorders(m.bub.bd), shading: shd(m.bub.bg), margins: padTw(bp) };
      }
      return { items: [spacer(20)], w: cols[j], borders: cellBorders(null) };
    });
    items.push(T({ cols, rows: [{ cells, cantSplit: true }] }, i === 0 ? 0 : tw(m.gap || 0)));
  });
  rows.push({ cells: [{ items, w: tw(wPx), borders: { top: NIL, left: bor(bd.l) || NIL, right: bor(bd.r) || NIL, bottom: b.note ? NIL : (bor(bd.b) || NIL) }, shading: shd(st.bg), margins: padTw(bs.pad) }], cantSplit: true });
  if (b.note) {
    const n = b.note;
    const np = pItem(n, { inner: true }, { forceDirect: true });
    rows.push({ cells: [{ items: [np], w: tw(wPx), borders: { top: NIL, left: bor(bd.l) || NIL, right: bor(bd.r) || NIL, bottom: bor(bd.b) || NIL }, shading: shd(st.bg), margins: padTw(n.pad) }], cantSplit: true });
  }
  return [T({ cols: [tw(wPx)], rows })];
}
function talkItems(b, ctx) {
  return b.items.map((it, i) => {
    const colPx = [it.avw, it.gapx, it.bub.w];
    const total = colPx.reduce((a, c) => a + c, 0);
    const cols = fitCols(colPx, Math.min(tw(total), tw(ctx.w)));
    const bp = it.bub.pad || {};
    const para = pItem({ runs: it.runs, align: 'justify', fs: it.bub.fs, lh: it.bub.lh, font: 'serif', color: it.bub.color }, Object.assign({}, ctx, { inner: true }), { forceDirect: true });
    const cells = [
      { items: [P({ spacing: { before: 0, after: 0, line: 240, lineRule: AUTO }, children: [imageRun(it.av.id, it.av.w, it.av.h)] })], w: cols[0], borders: cellBorders(null) },
      { items: [spacer(20)], w: cols[1], borders: cellBorders(null) },
      { items: [para], w: cols[2], borders: cellBorders(null), shading: shd(it.bub.bg), margins: padTw(bp) },
    ];
    return T({ cols, rows: [{ cells, cantSplit: true }] }, i === 0 ? undefined : tw(it.gap || 0));
  });
}
function goalsItems(b, ctx) {
  const colPx = [];
  const kinds = [];
  let x = 0;
  b.cols.forEach((c) => {
    if (c.x > x + 0.5) { colPx.push(c.x - x); kinds.push(null); }
    colPx.push(c.w); kinds.push(c);
    x = c.x + c.w;
  });
  const scale = Math.min(1, ctx.w / x);
  const cols = fitCols(colPx, tw(x * scale));
  const cells = kinds.map((c, j) => {
    if (!c) return { items: [spacer(20)], w: cols[j], borders: cellBorders(null) };
    const pad = c.style.pad || {};
    const inner = cols[j] / 15 - (pad.l || 0) - (pad.r || 0);
    const cctx = Object.assign({}, ctx, { w: inner, inner: true, inBox: true });
    const items = [pItem(Object.assign({ runs: c.title.runs }, c.title, { align: 'left' }), cctx, { forceDirect: true })];
    const li = listItems(c.list, cctx);
    if (li.length) li[0].gap = tw(4);
    items.push(...li);
    return { items, w: cols[j], borders: cellBorders(c.style.bd), shading: shd(c.style.bg), margins: padTw(pad) };
  });
  return [T({ cols, rows: [{ cells, cantSplit: true }] })];
}
function ipoItems(b, ctx) {
  const st = b.style;
  const bd = st.bd || {};
  const kw = Math.max(...b.rows.map((r) => r.k.w));
  const cols = fitCols([kw, b.w - kw], tw(Math.min(b.w, ctx.w)));
  const n = b.rows.length;
  const rows = b.rows.map((r, i) => {
    const mk = (s, w, isK) => {
      const pad = s.pad || {};
      const p = pItem({ runs: s.runs, align: 'left', fs: s.fs, lh: s.lh, font: s.font, color: s.color }, Object.assign({}, ctx, { inner: true }), { forceDirect: true });
      return {
        items: [p], w, shading: shd(s.bg), margins: padTw(pad),
        borders: { top: i === 0 ? (bor(bd.t) || NIL) : NIL, bottom: i === n - 1 ? (bor(bd.b) || NIL) : (bor(s.bd && s.bd.b) || NIL), left: isK ? (bor(bd.l) || NIL) : NIL, right: isK ? NIL : (bor(bd.r) || NIL) },
      };
    };
    return { cells: [mk(r.k, cols[0], true), mk(r.v, cols[1], false)], cantSplit: true };
  });
  rows.slice(0, -1).forEach((r) => r.cells.forEach((c) => c.items.forEach((it) => { it.o.keepNext = true; })));
  return [T({ cols, rows })];
}
function twoItems(b, ctx) {
  const colPx = [];
  const kinds = [];
  let x = 0;
  b.cols.forEach((c) => {
    if (c.x > x + 0.5) { colPx.push(c.x - x); kinds.push(null); }
    colPx.push(c.w); kinds.push(c);
    x = c.x + c.w;
  });
  const scale = Math.min(1, ctx.w / x);
  const cols = fitCols(colPx, tw(x * scale));
  const cells = kinds.map((c, j) => {
    if (!c) return { items: [spacer(20)], w: cols[j], borders: cellBorders(null) };
    const items = blocksItems(c.blocks, Object.assign({}, ctx, { w: cols[j] / 15, inner: true }));
    items.forEach((it, k) => { if (k === 0) it.gap = 0; });
    return { items, w: cols[j], borders: cellBorders(null), valign: VerticalAlign.TOP };
  });
  return [T({ cols, rows: [{ cells, cantSplit: true }] })];
}
function colsItems(b, ctx) {
  // the guide's two-column list of feature icons
  const items = b.items;
  const per = 2;
  const first = items[0];
  const second = items.find((it) => it.x > first.x + 1) || first;
  const gapPx = second.x - (first.x + first.w);
  const iconW = first.tx;
  const textW = first.w - first.tx;
  const colPx = [iconW, textW, gapPx, iconW, textW];
  const cols = fitCols(colPx, tw(Math.min(b.w, ctx.w)));
  const rows = [];
  for (let i = 0; i < items.length; i += per) {
    const cells = [];
    for (let j = 0; j < per; j++) {
      const it = items[i + j];
      if (j > 0) cells.push({ items: [spacer(20)], w: cols[cells.length], borders: cellBorders(null) });
      if (!it) { cells.push({ items: [spacer(20)], w: cols[cells.length], borders: cellBorders(null) }, { items: [spacer(20)], w: cols[cells.length + 1], borders: cellBorders(null) }); continue; }
      cells.push({ items: [P({ spacing: { before: ptw(1), after: 0, line: 240, lineRule: AUTO }, children: it.icon ? [imageRun(it.icon.id, it.icon.w, it.icon.h)] : [] })], w: cols[cells.length], borders: cellBorders(null) });
      const tctx = Object.assign({}, ctx, { w: textW, inner: true, inBox: true });
      const its = [];
      for (const part of it.parts) {
        if (part.t === 'runs') its.push(pItem({ runs: part.runs, align: 'left', fs: 9, lh: 13.95, font: 'serif', color: '1F1F1F' }, tctx, { forceDirect: true }));
        else its.push(...blockItems(Object.assign({}, part, { gap: 0, align: 'left' }), tctx));
      }
      cells.push({ items: its, w: cols[cells.length], borders: cellBorders(null) });
    }
    rows.push({ cells, cantSplit: true });
  }
  rows.forEach((r, i) => { if (i > 0) r.cells.forEach((c) => { c.items[0].gap = ptw(6); }); });
  return [T({ cols, rows })];
}

// ---------------------------------------------------------------- dispatcher
function blockItems(b, ctx) {
  let items;
  switch (b.t) {
    case 'p': items = [b.cls && /\btcap\b/.test(b.cls) ? capItem(b, ctx, 'TabCap') : pItem(b, ctx, { keepNext: /\bexh\b/.test(b.cls || '') })]; break;
    case 'fmt': items = [pItem(b, ctx, { forceDirect: true })]; break;
    case 'cap': items = [capItem(b, ctx)]; break;
    case 'step': items = [stepItem(b, ctx)]; break;
    case 'ftitle': items = [pItem(b, ctx, { style: 'FrontTitle', forceDirect: true })]; break;
    case 'h': items = [headingItem(b, ctx)]; break;
    case 'list': items = listItems(b, ctx); break;
    case 'table': items = tableItems(b, ctx); break;
    case 'code': items = codeItems(b, ctx); break;
    case 'console': items = consoleItems(b, ctx); break;
    case 'conwin': items = conwinItems(b, ctx); break;
    case 'img': items = [imgItem(b, ctx)]; break;
    case 'box': items = boxItems(b, ctx); break;
    case 'chat': items = chatItems(b, ctx); break;
    case 'talk': items = talkItems(b, ctx); break;
    case 'goals': items = goalsItems(b, ctx); break;
    case 'ipo': items = ipoItems(b, ctx); break;
    case 'two': items = twoItems(b, ctx); break;
    case 'grid': items = gridItems(b, ctx); break;
    case 'opts': items = optsItems(b, ctx, 0); break;
    case 'cols': items = colsItems(b, ctx); break;
    default: throw new Error('unknown block ' + b.t);
  }
  if (items.length && items[0].gap === undefined) items[0].gap = tw(b.gap || 0);
  return items;
}

// ---------------------------------------------------------------- headers and footers
function hdrPara(text, odd) {
  return new Paragraph({
    style: 'Header', alignment: odd ? AlignmentType.RIGHT : AlignmentType.LEFT,
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: 'B5B5B5', space: 4 } },
    children: [new TextRun({ text, font: FONT.sans, size: 15, color: odd ? '1D4F91' : '858585' })],
  });
}
function pageHeaders(part) {
  return {
    headers: { default: new Header({ children: [hdrPara(part, true)] }), even: new Header({ children: [hdrPara(BOOK, false)] }) },
    footers: {
      default: new Footer({ children: [new Paragraph({ style: 'Footer', alignment: AlignmentType.RIGHT, children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT.sans, size: 17, color: '4D4D4D' })] })] }),
      even: new Footer({ children: [new Paragraph({ style: 'Footer', alignment: AlignmentType.LEFT, children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT.sans, size: 17, color: '4D4D4D' })] })] }),
    },
  };
}
const emptyHF = () => ({
  headers: { default: new Header({ children: [new Paragraph({ style: 'Header' })] }), even: new Header({ children: [new Paragraph({ style: 'Header' })] }) },
  footers: { default: new Footer({ children: [new Paragraph({ style: 'Footer' })] }), even: new Footer({ children: [new Paragraph({ style: 'Footer' })] }) },
});
function pageProps(extra) {
  return Object.assign({
    page: {
      size: { width: PAGE_W, height: PAGE_H },
      margin: { top: MAR.top, bottom: MAR.bottom, left: MAR.inside, right: MAR.outside, header: MAR.header, footer: MAR.footer, gutter: 0 },
    },
  }, extra || {});
}

// ---------------------------------------------------------------- designed pages (cover, title page, project openers)
const BLEED_PX = 3 * PX_MM;
const PAGE_PX = { w: 185 * PX_MM, h: 260 * PX_MM };
const TOP_PX = MAR.top / 15;
function bgImage(file) {
  return imageRun(file, PAGE_PX.w, PAGE_PX.h, {
    floating: {
      horizontalPosition: { relative: HorizontalPositionRelativeFrom.PAGE, offset: 0 },
      verticalPosition: { relative: VerticalPositionRelativeFrom.PAGE, offset: 0 },
      behindDocument: true, allowOverlap: true, lockAnchor: true,
    },
    altText: { name: 'page background', description: '版面底图', title: '版面底图' },
  });
}
function coverSection() {
  const p = new Paragraph({ children: [bgImage('cover.jpg')], spacing: { before: 0, after: 0, line: 240, lineRule: AUTO } });
  // the inside of the cover stays blank, so the title page is a right-hand page as in print
  const blank = new Paragraph({ pageBreakBefore: true, children: [], spacing: { before: 0, after: 0, line: 240, lineRule: AUTO } });
  return Object.assign({ properties: pageProps({ titlePage: false }), children: [p, blank] }, emptyHF());
}
// front matter (preface, guide, contents) continues the title page's lower-roman numbering
function frontProps() {
  const props = pageProps({ type: SectionType.ODD_PAGE });
  props.page.pageNumbers = { formatType: NumberFormat.LOWER_ROMAN };
  return props;
}
function titlePageSection(sec) {
  const items = sec.page.items;
  const get = (c) => items.find((i) => i.cls === c);
  const kids = [];
  let cursor = TOP_PX;
  const rightPx = 3 * PX_MM;   // centre on the trimmed page, not on the (asymmetric) text block
  const line = (it, extra) => {
    const y = it.y - BLEED_PX;
    const lhPx = it.lh / 0.75;
    const before = Math.max(0, y - cursor);
    cursor = y + it.h;
    const runs = it.runs.map((r) => Object.assign({}, r, { ls: it.ls }));
    const o = Object.assign({
      alignment: AlignmentType.CENTER, children: children(runs),
      spacing: { before: tw(before), after: 0, line: ptw(it.lh), lineRule: EXACT },
      indent: { left: ptw(it.ls), right: tw(rightPx) },
    }, extra || {});
    kids.push(new Paragraph(o));
    void lhPx;
  };
  const t1 = get('tp-t1');
  const firstY = t1.y - BLEED_PX;
  const runs1 = t1.runs.map((r) => Object.assign({}, r, { ls: t1.ls }));
  kids.push(new Paragraph({ alignment: AlignmentType.CENTER, children: [bgImage('f000_trim.jpg'), ...children(runs1)], spacing: { before: tw(firstY - cursor), after: 0, line: ptw(t1.lh), lineRule: EXACT }, indent: { left: ptw(t1.ls), right: tw(rightPx) } }));
  cursor = firstY + t1.h;
  line(get('tp-t2'));
  line(get('tp-en'));
  const ln = get('tp-ln');
  const lnY = ln.y - BLEED_PX;
  kids.push(new Paragraph({
    children: [], spacing: { before: tw(lnY - cursor - 1.33), after: 0, line: 20, lineRule: EXACT },
    indent: { left: tw(ln.x - BLEED_PX - MAR.inside / 15), right: tw(TEXT_PX - (ln.x - BLEED_PX - MAR.inside / 15) - ln.w) },
    border: { bottom: { style: BorderStyle.SINGLE, size: 10, color: '1D4F91', space: 0 } }, run: { size: 2 },
  }));
  cursor = lnY + ln.h;
  line(get('tp-au'));
  const props = pageProps({ type: SectionType.NEXT_PAGE });
  props.page.pageNumbers = { start: 1, formatType: NumberFormat.LOWER_ROMAN };
  return Object.assign({ properties: props, children: kids }, emptyHF());
}
function openerSection(op, partTitle, startNumber) {
  const items = op.page.items;
  const get = (c) => items.filter((i) => i.cls === c);
  const leftPx = (get('kick')[0].x - BLEED_PX) - MAR.inside / 15;   // the opener text block starts 3 mm inside the margin
  const kids = [];
  let cursor = TOP_PX;
  const kick = get('kick')[0];
  const pno = get('pno')[0];
  const otitle = get('otitle')[0];
  const oline = get('oline')[0];
  const osub = get('osub')[0];
  const nh = get('nh')[0];
  const ky = kick.y - BLEED_PX;
  kids.push(new Paragraph({
    children: [bgImage(op.bg.id + '_trim.jpg'), ...children(kick.runs.map((r) => Object.assign({}, r, { ls: kick.ls })))],
    spacing: { before: tw(ky - cursor), after: 0, line: ptw(kick.lh), lineRule: EXACT }, indent: { left: tw(leftPx) },
  }));
  cursor = ky + kick.h;
  // project number + title form one level-1 heading (two lines of the title's height)
  const tLinePx = otitle.lh / 0.75;
  const titleBottom = otitle.y - BLEED_PX + otitle.h;
  const headTop = titleBottom - 2 * tLinePx + (otitle.h - tLinePx) / 2 + 6;
  const toc = partTitle.replace(/^(项目.)\s*/, '$1　');
  // one Heading 1 paragraph, both lines in the style's formatting, so the TOC entry stays clean after an update
  const hRuns = [new TextRun(plain(pno.runs)), new TextRun({ break: 1 }), new TextRun(plain(otitle.runs))];
  kids.push(new Paragraph({
    style: 'Heading1', alignment: AlignmentType.LEFT, children: bmWrap(tocBookmark(toc, 1), hRuns),
    spacing: { before: tw(Math.max(0, headTop - cursor)), after: 0, line: ptw(otitle.lh), lineRule: EXACT }, indent: { left: tw(leftPx) },
  }));
  cursor = headTop + 2 * tLinePx;
  const ly = oline.y - BLEED_PX;
  kids.push(new Paragraph({
    children: [], run: { size: 2 }, spacing: { before: tw(Math.max(0, ly - cursor - 1.33)), after: 0, line: 20, lineRule: EXACT },
    indent: { left: tw(leftPx), right: tw(TEXT_PX - leftPx - oline.w) },
    border: { bottom: { style: BorderStyle.SINGLE, size: 10, color: 'FFFFFF', space: 0 } },
  }));
  cursor = ly + oline.h;
  const sy = osub.y - BLEED_PX;
  kids.push(new Paragraph({
    alignment: AlignmentType.LEFT, children: children(osub.runs),
    spacing: { before: tw(Math.max(0, sy - cursor)), after: 0, line: ptw(osub.lh), lineRule: EXACT },
    indent: { left: tw(leftPx), right: tw(TEXT_PX - leftPx - osub.w) },
  }));
  cursor = sy + osub.h;
  const hy = nh.y - BLEED_PX;
  kids.push(new Paragraph({
    alignment: AlignmentType.LEFT, children: children(nh.runs.map((r) => Object.assign({}, r, { ls: nh.ls }))), keepNext: true,
    spacing: { before: tw(Math.max(0, hy - cursor)), after: tw(3 * PX_MM), line: ptw(nh.lh), lineRule: EXACT },
    indent: { left: tw(leftPx), right: tw(TEXT_PX - leftPx - nh.w) },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: '1D4F91', space: 7 } },
  }));
  // learning navigation: number | task | description
  const n0 = get('n')[0], t0 = get('t')[0], d0 = get('d')[0];
  const colPx = [n0.w, t0.x - (n0.x + n0.w), t0.w, d0.x - (t0.x + t0.w), d0.w];
  const cols = fitCols(colPx, tw(colPx.reduce((a, b) => a + b, 0)));
  const rowB = { style: BorderStyle.SINGLE, size: 4, color: 'D9D9D9' };
  const cellP = (runs, fs, lh) => P({ children: children(runs), alignment: AlignmentType.LEFT, spacing: { before: 0, after: 0, line: ptw(lh), lineRule: EXACT } });
  const rows = op.nav.map((it) => ({
    cantSplit: true,
    cells: [
      { items: [cellP(it.n, 11, n0.lh)], w: cols[0] },
      { items: [spacer(20)], w: cols[1] },
      { items: [cellP(it.t, 10, t0.lh)], w: cols[2] },
      { items: [spacer(20)], w: cols[3] },
      { items: [cellP(it.d, 9, d0.lh)], w: cols[4] },
    ].map((c) => Object.assign(c, { borders: { top: NIL, left: NIL, right: NIL, bottom: rowB }, margins: { top: tw(2.2 * PX_MM), bottom: tw(2.2 * PX_MM), left: 0, right: 0 } })),
  }));
  const nav = realize([T({ cols, rows, indent: tw(leftPx) })]);
  kids.push(...nav);
  // meta line (hours, environment, AI tools) sits in this page's footer at its printed position
  const metas = items.filter((i) => !i.cls);
  const mx0 = metas[0].x;
  const metaRuns = [];
  metas.forEach((m, i) => {
    if (i > 0) metaRuns.push({ tab: 1 });
    m.runs.forEach((r, k) => { metaRuns.push(r); if (k === 0) metaRuns.push({ t: '  ', f: r.f, sz: r.sz }); });
  });
  const metaP = new Paragraph({
    style: 'Footer', children: children(metaRuns), alignment: AlignmentType.LEFT,
    indent: { left: tw(leftPx) }, tabStops: metas.slice(1).map((m) => ({ type: TabStopType.LEFT, position: tw(leftPx + m.x - mx0) })),
    spacing: { before: 0, after: 0, line: ptw(metas[0].lh), lineRule: EXACT },
  });
  const metaBottomPx = PAGE_PX.h - (metas[0].y - BLEED_PX + metas[0].h);
  const hf = emptyHF();
  hf.footers.default = new Footer({ children: [metaP] });
  const props = pageProps({ type: SectionType.ODD_PAGE });
  props.page.margin.footer = tw(metaBottomPx);
  if (startNumber) props.page.pageNumbers = { start: startNumber, formatType: NumberFormat.DECIMAL };
  return Object.assign({ properties: props, children: kids }, hf);
}

// ---------------------------------------------------------------- flow sections
function flowSection(blocks, part, props, opts) {
  opts = opts || {};
  const ctx = { w: TEXT_PX, noToc: !!opts.noToc };
  const items = [];
  blocks.forEach((b, i) => {
    if (opts.appendix && i === 0 && b.t === 'h') { const it = appendixTitle(b, ctx); it.gap = 0; items.push(it); return; }
    items.push(...blockItems(b, ctx));
  });
  const kids = realize(items, { dropFirstGap: true });
  return Object.assign({ properties: props, children: kids }, pageHeaders(part));
}

// ---------------------------------------------------------------- assemble
const secByName = (d, n) => d.sections.find((s) => s.name === n);
const ch1 = secByName(body, 'ch1');
const ch2 = secByName(body, 'ch2');
const appx = secByName(body, 'appx');
const sections = [];
sections.push(coverSection());
sections.push(titlePageSection(secByName(front, 'titlepage')));
sections.push(flowSection(secByName(front, 'front').blocks, '前　言', frontProps(), { noToc: true }));
sections.push(flowSection(secByName(front, 'guide').blocks, '本书使用说明', frontProps(), { noToc: true }));
const tocIndex = sections.length;
sections.push(null); // the TOC section is filled in once all headings are known
const op1 = ch1.blocks[0];
sections.push(openerSection(op1, '项目一 搭建个人专属档案', 1));
sections.push(flowSection(ch1.blocks.slice(1), '项目一　搭建个人专属档案', pageProps({ type: SectionType.NEXT_PAGE })));
const op2 = ch2.blocks[0];
sections.push(openerSection(op2, '项目二 读懂身边多样数据', 0));
sections.push(flowSection(ch2.blocks.slice(1), '项目二　读懂身边多样数据', pageProps({ type: SectionType.NEXT_PAGE })));
sections.push(flowSection(appx.blocks, '附录A　ASCII 字符集', pageProps({ type: SectionType.ODD_PAGE }), { appendix: true }));

// table of contents with cached entries (page numbers from the previous render when available)
const PRINT_TOC = [1, 2, 3, 4, 4, 10, 25, 36, 37, 43, 44, 45, 45, 46, 63, 80, 100, 101, 107];
const cached = tocEntries.map((e, i) => ({ title: e.title, level: e.level, href: e.href, page: PAGES && PAGES.bm && PAGES.bm[e.href] !== undefined ? PAGES.bm[e.href] : PRINT_TOC[i] }));
if (tocEntries.length !== PRINT_TOC.length) console.warn('TOC entries', tocEntries.length, 'print', PRINT_TOC.length);
const tocTitle = new Paragraph({ style: 'FrontTitle', children: [new TextRun({ text: '目　录', font: FONT.sans, bold: true, size: 36, color: '153A6B', characterSpacing: 120 })], spacing: { before: ptw(5.7), after: ptw(17) } });
sections[tocIndex] = Object.assign({
  properties: frontProps(),
  children: [tocTitle, new TableOfContents('目录', { hyperlink: true, headingStyleRange: '1-2', useAppliedParagraphOutlineLevel: true, hideTabAndPageNumbersInWebView: true, cachedEntries: cached })],
}, pageHeaders('目　录'));

// numbering definitions
const numbering = {
  config: Object.entries(LIST).map(([k, v]) => ({
    reference: 'L-' + k,
    levels: [{ level: 0, format: v.format, text: v.text, alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 420, hanging: 420 } }, run: v.run } }],
  })),
};

const H = (size, color, extra) => Object.assign({ run: { font: FONT.sans, bold: true, size, color } }, extra || {});
const doc = new Document({
  creator: '冯丽娜',
  title: BOOK + '（第一至二章）可编辑版 v4',
  description: '由印刷版 v4 排版文件转换的可编辑 Word 版本',
  features: { updateFields: true },
  evenAndOddHeaderAndFooters: true,
  numbering,
  styles: {
    default: {
      document: { run: { font: FONT.serif, size: 21 }, paragraph: { spacing: { after: 0, line: 240 } } },
      heading1: { run: { font: FONT.sans, bold: true, size: 62, color: 'FFFFFF', characterSpacing: 30 }, paragraph: { alignment: AlignmentType.LEFT, keepNext: true, keepLines: true, outlineLevel: 0, spacing: { before: 0, after: 0, line: 744, lineRule: EXACT } } },
      heading2: H(30, '153A6B', { paragraph: { keepNext: true, keepLines: true, outlineLevel: 1, spacing: { before: 0, after: 0, line: 420, lineRule: EXACT }, border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: '1D4F91', space: 4 } } } }),
      heading3: H(24, '1D4F91', { paragraph: { keepNext: true, keepLines: true, outlineLevel: 2, spacing: { before: 0, after: 0, line: 336, lineRule: EXACT }, indent: { left: 180 }, border: { left: { style: BorderStyle.SINGLE, size: 24, color: '1D4F91', space: 6 }, bottom: { style: BorderStyle.SINGLE, size: 4, color: 'C5D3E7', space: 2 } } } }),
      heading4: H(22, '153A6B', { paragraph: { keepNext: true, keepLines: true, outlineLevel: 3, spacing: { before: 0, after: 0, line: 308, lineRule: EXACT } } }),
      heading5: H(21, '1F1F1F', { paragraph: { keepNext: true, keepLines: true, outlineLevel: 4, spacing: { before: 0, after: 0, line: 294, lineRule: EXACT } } }),
    },
    paragraphStyles: [
      { id: 'Normal', name: 'Normal', quickFormat: true, run: { font: FONT.serif, size: 21 }, paragraph: { spacing: { after: 0, line: 361, lineRule: EXACT }, alignment: AlignmentType.JUSTIFIED } },
      { id: 'BodyText', name: '正文首行缩进', basedOn: 'Normal', next: 'BodyText', quickFormat: true, run: { font: FONT.serif, size: 21, color: '1F1F1F' }, paragraph: { indent: { firstLine: 420, firstLineChars: 200 }, spacing: { after: 0, line: 361, lineRule: EXACT }, alignment: AlignmentType.JUSTIFIED } },
      { id: 'FigCap', name: '图题', basedOn: 'Normal', next: 'BodyText', quickFormat: true, run: { font: FONT.sans, size: 18, color: '4D4D4D' }, paragraph: { alignment: AlignmentType.CENTER, spacing: { line: 270, lineRule: EXACT } } },
      { id: 'TabCap', name: '表题', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FONT.sans, size: 18, color: '4D4D4D' }, paragraph: { alignment: AlignmentType.CENTER, keepNext: true, spacing: { line: 270, lineRule: EXACT } } },
      { id: 'Code', name: '程序代码', basedOn: 'Normal', next: 'Code', quickFormat: true, run: { font: FONT.monoL, size: 19, color: '1A1A1A' }, paragraph: { alignment: AlignmentType.LEFT, spacing: { line: 313, lineRule: EXACT } } },
      { id: 'FrontTitle', name: '前置标题', basedOn: 'Normal', next: 'BodyText', quickFormat: true, run: { font: FONT.sans, size: 36, bold: true, color: '153A6B', characterSpacing: 120 }, paragraph: { alignment: AlignmentType.CENTER, spacing: { line: 480, lineRule: AUTO } } },
      { id: 'Header', name: 'header', basedOn: 'Normal', run: { font: FONT.sans, size: 15 }, paragraph: { spacing: { line: 240, lineRule: AUTO } } },
      { id: 'Footer', name: 'footer', basedOn: 'Normal', run: { font: FONT.sans, size: 17 }, paragraph: { spacing: { line: 240, lineRule: AUTO } } },
      { id: 'AppendixTitle', name: '附录标题', basedOn: 'Normal', next: 'BodyText', quickFormat: true, run: { font: FONT.sans, bold: true, size: 30, color: '153A6B' }, paragraph: { alignment: AlignmentType.LEFT, keepNext: true, keepLines: true, outlineLevel: 0, spacing: { before: 0, after: 0, line: ptw(21), lineRule: EXACT }, border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: '1D4F91', space: 4 } } } },
      { id: 'TOC1', name: 'toc 1', basedOn: 'Normal', next: 'Normal', run: { font: FONT.sans, bold: true, size: 21, color: '153A6B' }, paragraph: { spacing: { before: mmw(3.5), after: 0, line: 400, lineRule: EXACT } } },
      { id: 'TOC2', name: 'toc 2', basedOn: 'Normal', next: 'Normal', run: { font: FONT.serif, size: 20, color: '1F1F1F' }, paragraph: { indent: { left: 400 }, spacing: { before: 0, after: 0, line: 382, lineRule: EXACT } } },
    ],
    characterStyles: [
      { id: 'TaskBadge', name: '任务标签', basedOn: 'DefaultParagraphFont', quickFormat: true, run: { font: FONT.sans, bold: true, size: 21, color: 'FFFFFF', shading: { type: ShadingType.CLEAR, fill: '1D4F91', color: 'auto' }, characterSpacing: 20 } },
    ],
  },
  sections,
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(OUT, buf);
  fs.writeFileSync(OUT.replace(/\.docx$/, '.meta.json'), JSON.stringify({ toc: tocEntries, refs: [...usedRefs], textW: TEXT_W }, null, 1));
  console.log('wrote', OUT, (buf.length / 1048576).toFixed(2) + ' MB', 'toc', tocEntries.length, 'lists', listInst);
});
