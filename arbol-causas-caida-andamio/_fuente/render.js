// Uso: node render.js png|pdf entrada.html salida [escala]
// Renderiza HTML con Chromium (playwright-core). Sin dependencias de pip.
const path = require('path');
const PW = '/root/.nvm/versions/node/v22.23.4/lib/node_modules/@playwright/mcp/node_modules/playwright-core';
const pw = require(PW);

(async () => {
  const [mode, input, output, scale = '2'] = process.argv.slice(2);
  const browser = await pw.chromium.launch({
    executablePath: '/usr/local/bin/chrome',
    args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage', '--headless=new'],
  });
  const ctx = await browser.newContext({
    deviceScaleFactor: +scale,
    viewport: { width: 1700, height: 1200 },
  });
  const page = await ctx.newPage();
  await page.goto('file://' + path.resolve(input), { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  if (mode === 'png') {
    const rep = await page.evaluate(() => (window.__report ? window.__report() : null));
    console.log(JSON.stringify(rep));
    const el = await page.$('#lienzo');
    await el.screenshot({ path: output });
  } else if (mode === 'pdf') {
    await page.emulateMedia({ media: 'print' });
    await page.pdf({ path: output, preferCSSPageSize: true, printBackground: true });
  }
  await browser.close();
})().catch((e) => { console.error('ERR', e.message); process.exit(1); });
