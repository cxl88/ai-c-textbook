// Browser-side walker: turns the typeset HTML into a JSON block tree for the Word builder.
// Every visual decision is read from the computed styles, so the Word file follows the print CSS.
window.__extract = function (opts) {
  const PREF = opts.pref || {};          // page number shown in print -> anchor name
  const shots = [];
  let shotN = 0;
  const cs = (el) => getComputedStyle(el);
  const px = (v) => parseFloat(v) || 0;

  function hex(c) {
    if (!c) return null;
    const m = c.match(/rgba?\(([^)]+)\)/);
    if (!m) return null;
    const p = m[1].split(/[ ,/]+/).filter(Boolean).map(parseFloat);
    let [r, g, b] = p;
    const a = p.length > 3 ? p[3] : 1;
    if (a === 0) return null;
    if (a < 1) { r = r * a + 255 * (1 - a); g = g * a + 255 * (1 - a); b = b * a + 255 * (1 - a); }
    return [r, g, b].map((v) => Math.round(v).toString(16).padStart(2, '0')).join('').toUpperCase();
  }
  function fam(s) {
    const f = s.fontFamily;
    if (/BMono/.test(f)) return 'mono';
    if (/BSans|ZCOOL/.test(f)) return 'sans';
    return 'serif';
  }
  function shot(el, kind, extra) {
    const id = opts.prefix + String(shotN++).padStart(3, '0');
    el.setAttribute('data-shot', id);
    const r = el.getBoundingClientRect();
    shots.push(Object.assign({ id, kind, w: r.width, h: r.height }, extra || {}));
    return { id, w: +r.width.toFixed(2), h: +r.height.toFixed(2) };
  }
  const isInlineDisp = (d) => d.startsWith('inline') || d === 'contents';
  function side(s, k) {
    const w = px(s['border' + k + 'Width']);
    const st = s['border' + k + 'Style'];
    if (!w || st === 'none' || st === 'hidden') return null;
    return { w: +w.toFixed(2), c: hex(s['border' + k + 'Color']), st };
  }
  function borders(s) { return { t: side(s, 'Top'), r: side(s, 'Right'), b: side(s, 'Bottom'), l: side(s, 'Left') }; }
  function pads(s) { return { t: px(s.paddingTop), r: px(s.paddingRight), b: px(s.paddingBottom), l: px(s.paddingLeft) }; }
  function boxStyle(el) {
    const s = cs(el);
    return { bg: hex(s.backgroundColor), bd: borders(s), pad: pads(s), fs: px(s.fontSize) * 0.75, lh: s.lineHeight === 'normal' ? null : px(s.lineHeight) * 0.75, color: hex(s.color), font: fam(s), align: s.textAlign };
  }

  // ---------- inline runs ----------
  function decoOf(el, root) {
    // underline drawn by text-decoration or by an inline border-bottom (.slot)
    for (let e = el; e && e !== root.parentElement; e = e.parentElement) {
      const s = cs(e);
      if (/underline/.test(s.textDecorationLine)) return { u: s.textDecorationStyle === 'wavy' ? 'wave' : (s.textDecorationStyle === 'dashed' ? 'dash' : (s.textDecorationStyle === 'dotted' ? 'dotted' : 'single')), uc: hex(s.textDecorationColor) };
      if (e !== root && isInlineDisp(s.display) && s.borderBottomStyle !== 'none' && px(s.borderBottomWidth) > 0 && !(px(s.borderTopWidth) > 0))
        return { u: s.borderBottomStyle === 'dashed' ? 'dash' : (s.borderBottomStyle === 'dotted' ? 'dotted' : 'single'), uc: hex(s.borderBottomColor) };
      if (e === root) break;
    }
    return null;
  }
  function bgOf(el, root) {
    for (let e = el; e && e !== root; e = e.parentElement) {
      const s = cs(e);
      const b = hex(s.backgroundColor);
      if (b) return { bg: b, bd: (px(s.borderTopWidth) > 0 && s.borderTopStyle !== 'none') ? { c: hex(s.borderTopColor), w: px(s.borderTopWidth) } : null };
      if (!isInlineDisp(s.display)) break;
    }
    return null;
  }
  function mkRun(t, el, root) {
    const s = cs(el);
    const r = { t };
    const fw = parseInt(s.fontWeight, 10);
    if (fw >= 600) r.b = 1;
    if (s.fontStyle === 'italic') r.i = 1;
    r.f = fam(s);
    r.c = hex(s.color);
    r.sz = +(px(s.fontSize) * 0.75).toFixed(2);
    const bg = bgOf(el, root);
    if (bg) { r.bg = bg.bg; if (bg.bd) r.bd = bg.bd; }
    for (let e = el; e && e !== root.parentElement; e = e.parentElement) {
      const va = cs(e).verticalAlign;
      if (va === 'super') { r.sup = 1; break; }
      if (va === 'sub') { r.sub = 1; break; }
      if (e === root) break;
    }
    const d = decoOf(el, root);
    if (d) Object.assign(r, d);
    const ls = px(s.letterSpacing);
    if (ls) r.ls = +(ls * 0.75).toFixed(2);
    return r;
  }
  // collects runs of `root`; nested block-level elements are returned as {block: el} markers
  function runsOf(root, o) {
    o = o || {};
    const runs = [];
    function walk(node) {
      if (node.nodeType === 3) {
        const el = node.parentElement;
        const s = cs(el);
        let t = node.nodeValue;
        if (!/^pre/.test(s.whiteSpace) && !/break-spaces/.test(s.whiteSpace)) t = t.replace(/[\t\n\r ]+/g, ' ');
        if (t === '') return;
        runs.push(mkRun(t, el, root));
        return;
      }
      if (node.nodeType !== 1) return;
      const el = node;
      const s = cs(el);
      if (s.display === 'none' || s.visibility === 'hidden') return;
      const tag = el.tagName.toLowerCase();
      if (el.classList.contains('ckc')) return;
      if (tag === 'br') { runs.push({ br: 1 }); return; }
      if (tag === 'svg' || tag === 'img') {
        const sh = shot(el, 'inline');
        runs.push({ img: sh.id, w: sh.w, h: sh.h, va: s.verticalAlign });
        return;
      }
      if (el.classList.contains('pref')) {
        const num = el.textContent.trim();
        runs.push(mkRun('第 ', el, root));
        runs.push(Object.assign(mkRun(num, el, root), { pref: PREF[num] || null }));
        runs.push(mkRun(' 页', el, root));
        return;
      }
      if (o.stop && el !== root && !isInlineDisp(s.display)) { runs.push({ block: el }); return; }
      // empty inline-block with a bottom border = blank to fill in
      if (isInlineDisp(s.display) && !el.textContent.trim() && !el.querySelector('svg,img') && px(s.borderBottomWidth) > 0 && s.borderBottomStyle !== 'none') {
        const w = el.getBoundingClientRect().width;
        const em = px(cs(el.parentElement).fontSize);
        const n = Math.max(2, Math.round(w / (em * 0.5)));
        runs.push(Object.assign(mkRun(' '.repeat(n), el.parentElement, root), { u: 'single', uc: hex(s.borderBottomColor), blank: 1 }));
        return;
      }
      // badge-like inline boxes get a little padding as no-break spaces
      const padded = isInlineDisp(s.display) && s.display !== 'inline' && hex(s.backgroundColor) && px(s.paddingLeft) >= 2;
      if (padded) runs.push(mkRun(' ', el, root));
      for (const c of el.childNodes) walk(c);
      if (padded) runs.push(mkRun(' ', el, root));
    }
    for (const c of root.childNodes) walk(c);
    return runs;
  }
  function tidy(runs) {
    // merge, trim paragraph edges, collapse double spaces across run boundaries
    const out = [];
    for (const r of runs) {
      if (r.t === undefined) { out.push(r); continue; }
      const prev = out[out.length - 1];
      if (prev && prev.t !== undefined && !prev.blank && !r.blank && !prev.pref && !r.pref) {
        const a = Object.assign({}, prev); delete a.t;
        const b = Object.assign({}, r); delete b.t;
        if (JSON.stringify(a) === JSON.stringify(b)) { prev.t += r.t; continue; }
      }
      out.push(Object.assign({}, r));
    }
    // collapse spaces at boundaries
    for (let i = 1; i < out.length; i++) {
      const p = out[i - 1], r = out[i];
      if (p.t !== undefined && r.t !== undefined && !p.blank && !r.blank && /[ ]$/.test(p.t) && /^[ ]/.test(r.t) && !/^pre/.test(r.ws || '')) r.t = r.t.replace(/^ +/, '');
    }
    // trim edges (and around line breaks)
    const trimStart = (i) => { for (; i < out.length; i++) { const r = out[i]; if (r.br) return; if (r.t === undefined) return; if (r.blank) return; r.t = r.t.replace(/^ +/, ''); if (r.t) return; } };
    const trimEnd = (i) => { for (; i >= 0; i--) { const r = out[i]; if (r.br) return; if (r.t === undefined) return; if (r.blank) return; r.t = r.t.replace(/ +$/, ''); if (r.t) return; } };
    trimStart(0); trimEnd(out.length - 1);
    for (let i = 0; i < out.length; i++) if (out[i].br) { trimEnd(i - 1); trimStart(i + 1); }
    return out.filter((r) => r.t === undefined || r.t !== '');
  }
  // splits mixed content (inline + nested blocks) into paragraphs and blocks
  function mixed(el, o) {
    const raw = runsOf(el, Object.assign({ stop: true }, o || {}));
    const parts = [];
    let cur = [];
    const flush = () => { const t = tidy(cur); if (t.length) parts.push({ t: 'runs', runs: t }); cur = []; };
    for (const r of raw) {
      if (r.block) { flush(); const b = block(r.block); if (b) parts.push(...[].concat(b)); }
      else cur.push(r);
    }
    flush();
    return parts;
  }

  // ---------- geometry helpers ----------
  function rect(el) { const r = el.getBoundingClientRect(); return { x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height }; }
  function withGap(arr, container) {
    // vertical gap above each block, measured from the layout (margins already collapsed)
    let prevBottom = null;
    const cr = container ? rect(container) : null;
    const cpad = container ? px(cs(container).paddingTop) + px(cs(container).borderTopWidth) : 0;
    for (const b of arr) {
      if (!b || (!b._el && !b._rect)) continue;
      const r = b._rect || rect(b._el);
      if (prevBottom === null) b.gap = cr ? Math.max(0, r.y - (cr.y + cpad)) : 0;
      else b.gap = Math.max(0, r.y - prevBottom);
      b.gap = +b.gap.toFixed(2);
      prevBottom = r.y + r.h;
    }
    return arr;
  }

  // ---------- block handlers ----------
  function paraBlock(el, type, extra) {
    const s = cs(el);
    const b = Object.assign({
      t: type || 'p', cls: el.className || '', tag: el.tagName.toLowerCase(), _el: el,
      runs: tidy(runsOf(el)), align: s.textAlign, indent: +(px(s.textIndent) * 0.75).toFixed(2),
      fs: +(px(s.fontSize) * 0.75).toFixed(2), lh: s.lineHeight === 'normal' ? null : +(px(s.lineHeight) * 0.75).toFixed(2),
      color: hex(s.color), font: fam(s), bg: hex(s.backgroundColor), bd: borders(s), pad: pads(s),
      ml: +(px(s.marginLeft) * 0.75).toFixed(2), mr: +(px(s.marginRight) * 0.75).toFixed(2),
      anchor: el.getAttribute('data-anchor') || (el.querySelector('[data-anchor]') ? el.querySelector('[data-anchor]').getAttribute('data-anchor') : null),
    }, extra || {});
    return b;
  }
  function heading(el) {
    const b = paraBlock(el, 'h');
    b.level = +el.tagName[1];
    return b;
  }
  function listBlock(el) {
    const cl = el.classList;
    let kind = el.tagName === 'OL' ? 'decimal' : 'bullet';
    if (cl.contains('paren')) kind = 'paren';
    if (cl.contains('dash')) kind = 'dash';
    if (cl.contains('check') || el.closest('.accept')) kind = 'check';
    const s = cs(el);
    const items = [];
    for (const li of el.children) {
      if (li.tagName !== 'LI') continue;
      const ls = cs(li);
      items.push({ parts: mixed(li), fs: +(px(ls.fontSize) * 0.75).toFixed(2), lh: ls.lineHeight === 'normal' ? null : +(px(ls.lineHeight) * 0.75).toFixed(2), color: hex(ls.color), font: fam(ls), _el: li });
    }
    withGap(items, null);
    for (const it of items) delete it._el;
    // marker geometry: where the text starts relative to the list box
    const lr = rect(el);
    const first = el.children[0];
    const indentPx = first ? (rect(first).x - lr.x) + px(cs(first).paddingLeft) : 0;
    return { t: 'list', kind, items, _el: el, indent: +(indentPx * 0.75).toFixed(2), ml: +(px(s.marginLeft) * 0.75).toFixed(2), fs: +(px(s.fontSize) * 0.75).toFixed(2), lh: s.lineHeight === 'normal' ? null : +(px(s.lineHeight) * 0.75).toFixed(2) };
  }
  function tableBlock(el) {
    const s = cs(el);
    const tr = rect(el);
    const rows = [];
    const xs = new Set();
    let maxCols = 0;
    for (const row of el.rows) {
      let n = 0;
      for (const c of row.cells) n += c.colSpan;
      maxCols = Math.max(maxCols, n);
    }
    const allCells = [];
    for (const row of el.rows) {
      const rs = cs(row);
      const r = { cells: [], h: +rect(row).h.toFixed(2), header: row.parentElement.tagName === 'THEAD', bg: hex(rs.backgroundColor) };
      for (const c of row.cells) {
        const ccs = cs(c);
        const cr = rect(c);
        xs.add(Math.round(cr.x - tr.x)); xs.add(Math.round(cr.x + cr.w - tr.x));
        const parts = mixed(c);
        const cell = { cs: c.colSpan, rs: c.rowSpan, th: c.tagName === 'TH', bg: hex(ccs.backgroundColor) || r.bg, align: ccs.textAlign, valign: ccs.verticalAlign, bd: borders(ccs), pad: pads(ccs), parts, fs: +(px(ccs.fontSize) * 0.75).toFixed(2), lh: ccs.lineHeight === 'normal' ? null : +(px(ccs.lineHeight) * 0.75).toFixed(2), color: hex(ccs.color), font: fam(ccs), x: cr.x - tr.x, w: cr.w, empty: !c.textContent.trim() && !c.querySelector('img,svg') };
        r.cells.push(cell);
        allCells.push(cell);
      }
      rows.push(r);
    }
    // grid columns from cell edges
    const edges = [...xs].sort((a, b) => a - b).filter((v, i, a) => i === 0 || v - a[i - 1] > 1);
    let cols = [];
    for (let i = 1; i < edges.length; i++) cols.push(edges[i] - edges[i - 1]);
    if (cols.length !== maxCols) {
      // fall back: widths of the first row that has every column
      const full = [...el.rows].find((row) => row.cells.length === maxCols);
      cols = full ? [...full.cells].map((c) => rect(c).w) : Array(maxCols).fill(tr.w / maxCols);
    }
    const parent = el.parentElement;
    const pr = rect(parent);
    const centered = tr.w < pr.w - 4 && Math.abs((tr.x - pr.x) - (pr.x + pr.w - tr.x - tr.w)) < 3;
    return { t: 'table', cls: el.className, rows, cols: cols.map((v) => +v.toFixed(2)), w: +tr.w.toFixed(2), centered, fs: +(px(s.fontSize) * 0.75).toFixed(2), _el: el };
  }
  function codeLines(el) {
    // per-line runs; line numbers marked ln:1; continuation labels skipped
    const lines = [[]];
    function walk(node, chunkStart) {
      if (node.nodeType === 3) {
        const parts = node.nodeValue.split('\n');
        parts.forEach((p, i) => {
          if (i > 0) lines.push([]);
          if (p) {
            const r = mkRun(p, node.parentElement, el);
            if (node.parentElement.classList.contains('ln')) r.ln = 1;
            lines[lines.length - 1].push(r);
          }
        });
        return;
      }
      if (node.nodeType !== 1) return;
      const c = node.classList;
      if (c.contains('fn') || c.contains('ckc') || c.contains('bar')) return;
      if (c.contains('ck') && lines[lines.length - 1].length) lines.push([]);
      for (const ch of node.childNodes) walk(ch);
    }
    for (const ch of el.childNodes) walk(ch);
    while (lines.length && !lines[lines.length - 1].length) lines.pop();
    return lines.map((l) => tidyCode(l));
  }
  function tidyCode(runs) {
    const out = [];
    for (const r of runs) {
      const prev = out[out.length - 1];
      if (prev) {
        const a = Object.assign({}, prev); delete a.t; const b = Object.assign({}, r); delete b.t;
        if (JSON.stringify(a) === JSON.stringify(b)) { prev.t += r.t; continue; }
      }
      out.push(Object.assign({}, r));
    }
    return out;
  }
  function codeBlock(el) {
    const fn = el.querySelector(':scope > .fn');
    const s = boxStyle(el);
    const fs = fn ? Object.assign(boxStyle(fn), { runs: tidy(runsOf(fn)) }) : null;
    const lines = codeLines(el);
    return { t: 'code', cls: el.className, title: fs, lines, style: s, ln: el.classList.contains('withln'), bad: el.classList.contains('bad'), _el: el, h: rect(el).h };
  }
  function consoleBlock(el) {
    const bar = el.querySelector(':scope > .bar');
    return { t: 'console', cls: el.className, label: bar ? Object.assign(boxStyle(bar), { runs: tidy(runsOf(bar)) }) : null, lines: codeLines(el), style: boxStyle(el), _el: el, h: rect(el).h };
  }
  function conwin(fig) {
    const win = fig.querySelector('.conwin');
    const bar = win.querySelector('.cw-bar');
    const ico = bar.querySelector('.cw-ico');
    const btn = bar.querySelector('.cw-btn');
    const body = win.querySelector('.cw-body');
    return {
      t: 'conwin', _el: win,
      bar: Object.assign(boxStyle(bar), { h: rect(bar).h, title: tidy(runsOf(bar.querySelector('.cw-t'))), ico: ico ? shot(ico, 'inline') : null, btn: btn ? shot(btn, 'inline') : null }),
      body: Object.assign(boxStyle(body), { lines: codeLines(body) }), style: boxStyle(win), h: rect(win).h,
    };
  }
  function imageOf(el, hide) {
    // screenshot el with given descendants hidden (captions)
    const sh = shot(el, 'block', { hide: hide || [] });
    return { t: 'img', id: sh.id, w: sh.w, h: sh.h, _el: el };
  }
  function figure(el) {
    const cap = el.querySelector(':scope > figcaption');
    const kids = [...el.children].filter((c) => c.tagName !== 'FIGCAPTION');
    const out = [];
    if (el.classList.contains('cwf') || (kids.length === 1 && kids[0].classList.contains('conwin'))) {
      out.push(conwin(el));
    } else if (kids.length && kids.every((k) => k.tagName === 'FIGURE' || k.tagName === 'PRE' || (k.tagName === 'DIV' && (k.classList.contains('two') || k.classList.contains('code'))))) {
      for (const k of kids) out.push(...[].concat(block(k) || []));
    } else if (kids.length) {
      const capH = cap ? rect(cap).h + px(cs(cap).marginTop) : 0;
      const img = imageOf(el, cap ? ['figcaption'] : []);
      img.h = +(img.h - capH).toFixed(2);
      img._rect = { y: rect(el).y, h: img.h };
      const r0 = rect(kids[0]), fr = rect(el), pr = rect(el.parentElement);
      img.centered = true;
      out.push(img);
    }
    if (cap) out.push(paraBlock(cap, 'cap'));
    return out;
  }
  function boxCommon(el, kind, head) {
    // generic framed box: own style + optional title row + inner blocks
    const inner = [...el.children].filter((c) => !head || !head.includes(c));
    const blocks = [];
    for (const c of inner) { const b = block(c); if (b) blocks.push(...[].concat(b)); }
    withGap(blocks, el);
    return { t: 'box', kind, style: boxStyle(el), blocks, _el: el, h: rect(el).h };
  }
  function titleRow(bt) {
    // .bt row: icon + text + optional <small> note on the right
    const small = bt.querySelector(':scope > small');
    const right = small ? tidy(runsOf(small)) : null;
    if (small) small.style.display = 'none';
    const runs = tidy(runsOf(bt));
    if (small) small.style.display = '';
    return Object.assign(boxStyle(bt), { runs, right, h: rect(bt).h });
  }
  function headBar(h) {
    const sp = [...h.children];
    return Object.assign(boxStyle(h), { left: sp[0] ? tidy(runsOf(sp[0])) : [], right: sp[1] ? tidy(runsOf(sp[1])) : [], h: rect(h).h });
  }
  function divBlock(el) {
    const c = el.classList;
    if (c.contains('blankpage') || c.contains('toc')) return null;
    if (c.contains('box') || c.contains('accept')) {
      const bt = el.querySelector(':scope > .bt');
      const b = boxCommon(el, c.contains('accept') ? 'accept' : (c.contains('warn') ? 'warn' : 'box'), bt ? [bt] : []);
      if (bt) b.title = titleRow(bt);
      return b;
    }
    if (c.contains('taskdesc')) return boxCommon(el, 'taskdesc');
    if (c.contains('try') || c.contains('prompt')) {
      const h = el.querySelector(':scope > .th, :scope > .ph');
      const bd = el.querySelector(':scope > .tbd, :scope > .pbd');
      const b = boxCommon(bd, c.contains('try') ? 'try' : 'prompt');
      b.style = boxStyle(el); b.bodyStyle = boxStyle(bd); b.head = headBar(h); b._el = el; b.h = rect(el).h;
      withGap(b.blocks, bd);
      return b;
    }
    if (c.contains('pnote')) return paraBlock(el, 'p');
    if (c.contains('chat')) {
      const h = el.querySelector(':scope > .cbar');
      const body = el.querySelector(':scope > .cbody');
      const msgs = [];
      for (const m of body.querySelectorAll(':scope > .msg')) {
        const av = m.querySelector(':scope > svg, :scope > img');
        const bub = m.querySelector(':scope > .bub');
        const parts = [];
        for (const ch of bub.children) { const b = block(ch); if (b) parts.push(...[].concat(b)); }
        withGap(parts, bub);
        msgs.push({ who: m.classList.contains('user') ? 'user' : 'ai', av: av ? shot(av, 'inline') : null, bub: Object.assign(boxStyle(bub), { w: rect(bub).w, x: rect(bub).x - rect(m).x }), avx: av ? rect(av).x - rect(m).x : 0, mw: rect(m).w, parts, _el: m });
      }
      withGap(msgs, body);
      const note = el.querySelector(':scope > .cnote');
      return { t: 'chat', head: headBar(h), msgs, style: boxStyle(el), bodyStyle: boxStyle(body), note: note ? paraBlock(note, 'p') : null, _el: el, h: rect(el).h };
    }
    if (c.contains('talk')) {
      const items = [];
      for (const say of el.querySelectorAll(':scope > .say')) {
        const av = say.querySelector(':scope > svg, :scope > img');
        const b = say.querySelector(':scope > .b');
        items.push({ av: av ? shot(av, 'inline') : null, bub: Object.assign(boxStyle(b), { w: rect(b).w }), runs: tidy(runsOf(b)), _el: say, avw: av ? rect(av).w : 0, gapx: av ? rect(b).x - rect(av).x - rect(av).w : 0, sw: rect(say).w });
      }
      withGap(items, el);
      return { t: 'talk', items, _el: el };
    }
    if (c.contains('goals')) {
      const cols = [];
      for (const d of el.children) {
        const gh = d.querySelector(':scope > .gh');
        const ul = d.querySelector(':scope > ul');
        cols.push({ title: Object.assign(boxStyle(gh), { runs: tidy(runsOf(gh)) }), list: listBlock(ul), style: boxStyle(d), w: rect(d).w, x: rect(d).x - rect(el).x });
      }
      return { t: 'goals', cols, _el: el, w: rect(el).w };
    }
    if (c.contains('ipo')) {
      const rows = [];
      const kids = [...el.children];
      for (let i = 0; i < kids.length; i += 2) rows.push({ k: Object.assign(boxStyle(kids[i]), { runs: tidy(runsOf(kids[i])), w: rect(kids[i]).w }), v: Object.assign(boxStyle(kids[i + 1]), { runs: tidy(runsOf(kids[i + 1])) }) });
      return { t: 'ipo', rows, style: boxStyle(el), _el: el, w: rect(el).w };
    }
    if (c.contains('two')) {
      const cols = [];
      for (const k of el.children) {
        const bs = [].concat(block(k) || []);
        cols.push({ blocks: bs, w: rect(k).w, x: rect(k).x - rect(el).x });
      }
      return { t: 'two', cols, _el: el, w: rect(el).w };
    }
    if (c.contains('grid3') || c.contains('zoomrow')) {
      const items = [];
      for (const f of el.children) {
        const img = f.querySelector('img');
        const cap = f.querySelector('figcaption');
        items.push({ img: Object.assign(shot(img, 'block'), { x: rect(img).x - rect(f).x }), cap: cap ? paraBlock(cap, 'cap') : null, w: rect(f).w, x: rect(f).x - rect(el).x, y: rect(f).y - rect(el).y });
      }
      return { t: 'grid', items, _el: el, w: rect(el).w, cols: c.contains('grid3') ? 3 : items.length };
    }
    if (c.contains('figcap')) return paraBlock(el, 'cap');
    if (c.contains('fmt')) return paraBlock(el, 'fmt');
    if (c.contains('step')) {
      const b = paraBlock(el, 'step');
      return b;
    }
    if (c.contains('opts')) {
      // option rows: group by line (same y)
      const kids = [...el.children];
      const er = rect(el);
      const rowsMap = [];
      for (const k of kids) {
        const r = rect(k);
        let row = rowsMap.find((x) => Math.abs(x.y - r.y) < 3);
        if (!row) { row = { y: r.y, items: [] }; rowsMap.push(row); }
        row.items.push({ x: +(r.x - er.x).toFixed(2), runs: tidy(runsOf(k)) });
      }
      const s = cs(el);
      return { t: 'opts', rows: rowsMap.map((r) => r.items), ml: +(px(s.marginLeft) * 0.75 + px(s.paddingLeft) * 0.75).toFixed(2), w: er.w, fs: +(px(s.fontSize) * 0.75).toFixed(2), _el: el };
    }
    if (c.contains('cols')) {
      const items = [];
      for (const d of el.children) {
        const ic = d.querySelector(':scope > svg, :scope > img');
        const tx = d.querySelector(':scope > div');
        items.push({ icon: ic ? shot(ic, 'inline') : null, parts: mixed(tx), x: rect(d).x - rect(el).x, w: rect(d).w, tx: rect(tx).x - rect(d).x });
      }
      return { t: 'cols', items, _el: el, w: rect(el).w };
    }
    if (c.contains('ftitle')) return paraBlock(el, 'ftitle');
    if (c.contains('ex') || c.contains('tbd') || c.contains('pbd') || !c.length) {
      // plain container
      const blocks = [];
      for (const ch of el.children) { const b = block(ch); if (b) blocks.push(...[].concat(b)); }
      // a container that only holds inline content becomes a paragraph
      if (!el.children.length || [...el.children].every((ch) => isInlineDisp(cs(ch).display))) return paraBlock(el, 'p');
      return blocks;
    }
    // anything else: graphic -> image
    return imageOf(el);
  }
  function block(el) {
    const tag = el.tagName.toLowerCase();
    const s = cs(el);
    if (s.display === 'none') return null;
    const c = el.classList;
    let b = null;
    if (/^h[1-6]$/.test(tag)) b = heading(el);
    else if (tag === 'p') b = paraBlock(el, 'p');
    else if (tag === 'ul' || tag === 'ol') b = listBlock(el);
    else if (tag === 'table') b = tableBlock(el);
    else if ((tag === 'pre' || tag === 'div') && c.contains('code')) b = codeBlock(el);
    else if (tag === 'pre' && c.contains('console')) b = consoleBlock(el);
    else if (tag === 'pre') b = consoleBlock(el);
    else if (tag === 'figure') b = figure(el);
    else if (tag === 'div') b = divBlock(el);
    else if (tag === 'svg' || tag === 'img') b = imageOf(el);
    else if (tag === 'section') { const arr = []; for (const ch of el.children) { const x = block(ch); if (x) arr.push(...[].concat(x)); } b = arr; }
    else b = paraBlock(el, 'p');
    return b;
  }

  // ---------- special pages ----------
  function overlayPage(el, textSel) {
    // background picture of a designed page (text hidden) + the text items with their positions
    const er = rect(el);
    const items = [];
    for (const t of el.querySelectorAll(textSel)) {
      const r = rect(t);
      const s = cs(t);
      items.push({ cls: t.className, runs: tidy(runsOf(t)), x: r.x - er.x, y: r.y - er.y, w: r.w, h: r.h, fs: px(s.fontSize) * 0.75, lh: s.lineHeight === 'normal' ? null : px(s.lineHeight) * 0.75, color: hex(s.color), font: fam(s), fw: parseInt(s.fontWeight, 10), ls: px(s.letterSpacing) * 0.75, align: s.textAlign, bd: borders(s) });
    }
    return { items, w: er.w, h: er.h };
  }

  const result = { shots, sections: [] };
  for (const sec of opts.sections) {
    const root = document.querySelector(sec.sel);
    if (!root) continue;
    if (sec.kind === 'opener' || sec.kind === 'titlepage') {
      const o = overlayPage(root, sec.text);
      // hide text for the background shot
      const sh = shot(root, 'page', { hideText: sec.text });
      result.sections.push({ name: sec.name, kind: sec.kind, bg: sh, page: o });
      continue;
    }
    const blocks = [];
    for (const ch of root.children) {
      if (sec.skip && ch.matches(sec.skip)) continue;
      if (ch.classList.contains('opener')) {
        const o = overlayPage(ch, '.oc > div, .nav .nh, .nav .it .n, .nav .it .t, .nav .it .d, .meta > span');
        const sh = shot(ch, 'page', { hideText: '.oc, .nav, .meta' });
        blocks.push({ t: 'opener', bg: sh, page: o, _el: ch, nav: [...ch.querySelectorAll('.nav .it')].map((it) => ({ n: tidy(runsOf(it.querySelector('.n'))), t: tidy(runsOf(it.querySelector('.t'))), d: tidy(runsOf(it.querySelector('.d'))) })) });
        continue;
      }
      const b = block(ch);
      if (b) blocks.push(...[].concat(b));
    }
    withGap(blocks, null);
    result.sections.push({ name: sec.name, kind: sec.kind || 'flow', blocks });
  }
  // strip element refs
  const seen = new WeakSet();
  const clean = (o) => {
    if (Array.isArray(o)) { o.forEach(clean); return; }
    if (o && typeof o === 'object') { if (seen.has(o)) return; seen.add(o); delete o._el; delete o._rect; for (const k of Object.keys(o)) clean(o[k]); }
  };
  clean(result.sections);
  return result;
};
