/* QA renders for the First Device Models Third Edition pack:
 * desktop + true-390-width screenshots of the paper HTML and the
 * demo, a demo interaction smoke test (open an abstainer question
 * cell), and horizontal-scroll checks.
 */
const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..', '..');
const DIST = path.join(ROOT, 'dist');
const QA = __dirname;
const PAPER = 'file://' + path.join(DIST, 'THOX_First_Device_Models_Trained_In-House_Whitepaper_v3.0.html');
const DEMO = 'file://' + path.join(DIST, 'FirstDeviceModels_Demo_v3.0.html');

(async () => {
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_BIN });
  const report = {};
  for (const [name, url] of [['paper', PAPER], ['demo', DEMO]]) {
    for (const w of [1280, 390]) {
      const page = await browser.newPage({ viewport: { width: w, height: 900 }, colorScheme: 'light' });
      await page.goto(url, { waitUntil: 'networkidle' });
      report[`${name}-${w}`] = await page.evaluate(() => ({
        scrollW: document.documentElement.scrollWidth,
        innerW: window.innerWidth,
        title: document.title,
      }));
      await page.screenshot({ path: path.join(QA, `${name}-${w}.png`) });
      if (name === 'paper' && w === 1280) {
        await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight * 0.45));
        await page.waitForTimeout(300);
        await page.screenshot({ path: path.join(QA, 'paper-1280-mid.png') });
      }
      if (name === 'demo' && w === 1280) {
        const cell = await page.$('.q');
        if (cell) await cell.click();
        await page.waitForTimeout(200);
        report['demo-interaction'] = (await page.textContent('#qOut') || '').slice(0, 200);
        await page.screenshot({ path: path.join(QA, 'demo-1280-interaction.png') });
      }
      await page.close();
    }
  }
  await browser.close();
  fs.writeFileSync(path.join(QA, 'render-metrics.json'), JSON.stringify(report, null, 1));
  console.log(JSON.stringify(report, null, 1));
})().catch(e => { console.error(e); process.exit(1); });
