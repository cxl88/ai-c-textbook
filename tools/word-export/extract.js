// Node driver: load a typeset HTML page, run walker.js, save JSON + screenshots
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
const path = require('path');
(async () => {
  const [, , src, cfgJson, outJson, imgDir] = process.argv;
  const cfg = JSON.parse(cfgJson);
  fs.mkdirSync(imgDir, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 559, height: 1000 }, deviceScaleFactor: 3 });
  await page.emulateMedia({ media: 'print' });
  await page.goto('file://' + src, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.addScriptTag({ path: path.join(__dirname, 'walker.js') });
  // anchors for page references
  await page.evaluate((anchors) => {
    for (const a of anchors) {
      const els = [...document.querySelectorAll(a.sel)].filter((e) => e.textContent.replace(/\s+/g, '').includes(a.text));
      if (els.length !== 1) throw new Error('anchor ' + a.name + ' matched ' + els.length);
      els[0].setAttribute('data-anchor', a.name);
    }
  }, cfg.anchors || []);
  const data = await page.evaluate((o) => window.__extract(o), cfg);
  // screenshots: normal ones first at the text-block width
  const later = [];
  for (const s of data.shots) {
    if (s.kind === 'page') { later.push(s); continue; }
    const el = await page.$(`[data-shot="${s.id}"]`);
    if (s.hide && s.hide.length) await el.evaluate((e, h) => h.forEach((sel) => e.querySelectorAll(':scope > ' + sel).forEach((x) => { x.dataset.d = x.style.display; x.style.display = 'none'; })), s.hide);
    await el.screenshot({ path: path.join(imgDir, s.id + '.png'), omitBackground: s.kind === 'inline' });
    if (s.hide && s.hide.length) await el.evaluate((e, h) => h.forEach((sel) => e.querySelectorAll(':scope > ' + sel).forEach((x) => { x.style.display = x.dataset.d || ''; })), s.hide);
  }
  if (later.length) {
    await page.setViewportSize({ width: 760, height: 1100 });
    for (const s of later) {
      const el = await page.$(`[data-shot="${s.id}"]`);
      await el.evaluate((e, sel) => e.querySelectorAll(sel).forEach((x) => { x.style.visibility = 'hidden'; }), s.hideText);
      await el.screenshot({ path: path.join(imgDir, s.id + '.png') });
    }
  }
  fs.writeFileSync(outJson, JSON.stringify(data, null, 1));
  console.log('sections', data.sections.length, 'shots', data.shots.length);
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
