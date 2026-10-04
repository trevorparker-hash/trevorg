// usage: node render.mjs jobs.json   jobs: [{html, out, w, h}]
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require('/tmp/claude-0/-home-user-Ninefold/aced07b5-8bf6-5d5f-83ea-056e9f0c83cb/scratchpad/art/node_modules/playwright-core');
import fs from 'fs';
const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const page = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
for (const j of jobs) {
  await page.setViewportSize({ width: j.w, height: j.h });
  await page.goto('file://' + j.html);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(150);
  await page.screenshot({ path: j.out, type: 'png' });
  console.log('rendered', j.out);
}
await browser.close();
