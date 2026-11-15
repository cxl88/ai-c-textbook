const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const [, , src, outdir, ...ids] = process.argv;
  const b = await chromium.launch();
  const p = await b.newPage({ deviceScaleFactor: 4, viewport: { width: 700, height: 900 } });
  await p.goto('file://' + require('path').resolve(src), { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready);
  for (const id of ids) { await p.locator('#' + id).screenshot({ path: `${outdir}/${id}.png` }); }
  await b.close();
})();
