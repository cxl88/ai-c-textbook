// Visible text of the typeset HTML, minus the parts that became images in the Word file.
// usage: node textcheck.js page.html cfg.json out.txt
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
const path = require('path');
(async () => {
  const [, , src, cfgPath, out] = process.argv;
  const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 559, height: 1000 } });
  await page.emulateMedia({ media: 'print' });
  await page.goto('file://' + src, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.addScriptTag({ path: path.join(__dirname, 'walker.js') });
  await page.evaluate((anchors) => {
    for (const a of anchors) {
      const els = [...document.querySelectorAll(a.sel)].filter((e) => e.textContent.replace(/\s+/g, '').includes(a.text));
      if (els.length === 1) els[0].setAttribute('data-anchor', a.name);
    }
  }, cfg.anchors || []);
  const text = await page.evaluate((o) => {
    const data = window.__extract(o);
    const kinds = {};
    data.shots.forEach((s) => { kinds[s.id] = s.kind; });
    document.querySelectorAll('[data-shot]').forEach((e) => { if (kinds[e.dataset.shot] !== 'page') e.style.display = 'none'; });
    return o.sections.map((s) => [...document.querySelectorAll(s.sel)].map((e) => e.innerText).join('\n')).join('\n');
  }, cfg);
  fs.writeFileSync(out, text);
  console.log(out, text.length);
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
