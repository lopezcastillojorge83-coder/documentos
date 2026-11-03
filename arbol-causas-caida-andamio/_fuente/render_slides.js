// Uso: node render_slides.js escala diapo1.html [diapo2.html ...]
// Captura cada diapositiva HTML (1920x1080) como PNG junto al HTML e informa
// en JSON de los textos que se desbordan.
const path = require('path');
const PW = '/root/.nvm/versions/node/v22.23.4/lib/node_modules/@playwright/mcp/node_modules/playwright-core';
const pw = require(PW);

(async () => {
  const [escala, ...archivos] = process.argv.slice(2);
  const browser = await pw.chromium.launch({
    executablePath: '/usr/local/bin/chrome',
    args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage', '--headless=new'],
  });
  const ctx = await browser.newContext({
    deviceScaleFactor: +escala, viewport: { width: 1920, height: 1080 },
  });
  const informe = {};
  for (const f of archivos) {
    const page = await ctx.newPage();
    await page.goto('file://' + path.resolve(f), { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    const rep = await page.evaluate(() => (window.__report ? window.__report() : null));
    await page.screenshot({ path: f.replace(/\.html$/, '.png') });
    informe[path.basename(f)] = rep ? rep.desbordadas : [];
    await page.close();
  }
  await browser.close();
  console.log(JSON.stringify(informe));
})().catch((e) => { console.error('ERR', e.message); process.exit(1); });
