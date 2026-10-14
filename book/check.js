// 版面检查：按版心宽度（148 mm）以打印媒体排版，找出横向溢出版心或被裁掉的元素
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const src = process.argv[2];
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: Math.round(148 / 25.4 * 96), height: 1000 } });
  await page.emulateMedia({ media: 'print' });
  await page.goto('file://' + require('path').resolve(src), { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(() => Promise.all(Array.from(document.images).map(i => i.complete ? null : new Promise(r => { i.onload = i.onerror = r; }))));
  const res = await page.evaluate(() => {
    const W = document.documentElement.clientWidth, out = [];
    const skip = el => el.closest('.opener, .titlepage, svg, .mk');
    for (const el of document.body.querySelectorAll('*')) {
      if (skip(el)) continue;
      const r = el.getBoundingClientRect();
      if (r.width === 0 && r.height === 0) continue;
      const cls = (el.className && el.className.baseVal === undefined ? el.className : '') || '';
      const tag = el.tagName.toLowerCase() + (cls ? '.' + cls.split(' ').join('.') : '');
      const txt = (el.innerText || el.textContent || '').replace(/\s+/g, ' ').slice(0, 60);
      if (r.right > W + 0.5 || r.left < -0.5) out.push(`OUT  ${tag} [${r.left.toFixed(1)}..${r.right.toFixed(1)} / ${W}] ${txt}`);
      const cs = getComputedStyle(el);
      if ((cs.overflowX === 'hidden' || cs.whiteSpace === 'pre' || cs.whiteSpace === 'nowrap') && el.scrollWidth > el.clientWidth + 1 && el.clientWidth > 0)
        out.push(`CLIP ${tag} scroll ${el.scrollWidth} > ${el.clientWidth}: ${txt}`);
    }
    return out;
  });
  // 只报最内层的问题，避免父元素重复
  console.log(res.length ? res.join('\n') : 'OK: no overflow');
  await browser.close();
})();
