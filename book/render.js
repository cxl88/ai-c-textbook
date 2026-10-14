const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const [, , src, dst] = process.argv;
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + require('path').resolve(src), { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(() => Promise.all(Array.from(document.images).map(i => i.complete ? null : new Promise(r => { i.onload = i.onerror = r; }))));
  await page.evaluate(() => {
    // 不可拆分的装饰块外包一层普通 div，避免整块被推到下一页时在上一页留下空的边框碎片
    document.querySelectorAll('.box, .prompt, .chat, pre.code, pre.console, .conwin, .taskdesc, .ipo, table, .goals, h3').forEach(el => {
      if (el.closest('.opener, .titlepage') || el.parentElement.classList.contains('nbw')) return;
      if (el.classList.contains('long')) return;          // 长表格、长程序允许跨页，不加整体不拆分的外层
      if (el.parentElement.closest('.box, .prompt, .chat, .two, .grid2, figure, .taskdesc')) return;
      const w = document.createElement('div');
      w.className = 'nbw';
      el.parentNode.insertBefore(w, el);
      w.appendChild(el);
    });
  });
  await page.pdf({ path: dst, preferCSSPageSize: true, printBackground: true, displayHeaderFooter: false });
  await browser.close();
})();
