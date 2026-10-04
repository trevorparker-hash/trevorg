import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require('/tmp/claude-0/-home-user-Ninefold/aced07b5-8bf6-5d5f-83ea-056e9f0c83cb/scratchpad/art/node_modules/playwright-core');
import fs from 'fs'; import path from 'path';
const ROOT = '/home/user/trevorg', BASE = 'https://trevorparker-hash.github.io/trevorg/';
const OUT = '/tmp/claude-0/-home-user/aced07b5-8bf6-5d5f-83ea-056e9f0c83cb/scratchpad/site_shots';
const T = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.jpg': 'image/jpeg', '.png': 'image/png', '.woff2': 'font/woff2', '.ico': 'image/x-icon', '.mp4': 'video/mp4' };
async function route(ctx, served) {
  await ctx.route('**/*', async (r) => {
    const u = new URL(r.request().url());
    if (u.host === 'trevorparker-hash.github.io') {
      let rel = decodeURIComponent(u.pathname.slice(9)); let f = path.join(ROOT, rel);
      if (rel === '' || rel.endsWith('/')) f = path.join(f, 'index.html');
      if (!fs.existsSync(f)) f = path.join(ROOT, '404.html');
      const body = fs.readFileSync(f); if (served) served.push([rel, body.length, r.request().resourceType()]);
      return r.fulfill({ status: 200, body, headers: { 'content-type': T[path.extname(f)] || 'application/octet-stream' } });
    }
    if (u.host === 'store.steampowered.com') return r.fulfill({ status: 200, contentType: 'text/html', body: '<body style="background:#1b2838"></body>' });
    return r.abort();
  });
}
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const out = {};
// 1. lightbox on desktop
{
  const ctx = await b.newContext({ viewport: { width: 1440, height: 900 } }); await route(ctx);
  const p = await ctx.newPage(); await p.goto(BASE + 'games/fight/');
  await p.locator('a.shot').nth(2).scrollIntoViewIfNeeded(); await p.locator('a.shot').nth(2).click();
  await p.waitForTimeout(400);
  out.lb_open = await p.evaluate(() => ({ open: document.querySelector('dialog.lightbox').open, count: document.querySelector('.lb-count').textContent, src: document.querySelector('.lb-stage img').getAttribute('src'), alt: document.querySelector('.lb-stage img').alt, nat: document.querySelector('.lb-stage img').naturalWidth }));
  await p.screenshot({ path: OUT + '/lightbox_desktop.png' });
  await p.keyboard.press('ArrowRight'); await p.waitForTimeout(150);
  out.lb_right = await p.evaluate(() => document.querySelector('.lb-count').textContent);
  await p.keyboard.press('End'); out.lb_end = await p.evaluate(() => document.querySelector('.lb-count').textContent);
  await p.keyboard.press('ArrowRight'); out.lb_wrap = await p.evaluate(() => document.querySelector('.lb-count').textContent);
  await p.keyboard.press('Escape'); await p.waitForTimeout(150);
  out.lb_closed = await p.evaluate(() => ({ open: document.querySelector('dialog.lightbox').open, focusIsThumb: document.activeElement === document.querySelectorAll('a.shot')[2], htmlClass: document.documentElement.className }));
  // keyboard: Tab to a thumb, Enter opens
  await p.keyboard.press('Enter'); await p.waitForTimeout(150);
  out.lb_enter = await p.evaluate(() => document.querySelector('dialog.lightbox').open);
  await p.keyboard.press('Escape');
  // play button
  const btn = p.locator('.clip-wide .play-btn');
  out.play_before = await p.evaluate(() => { const v = document.querySelector('.clip-wide video'); return { controls: v.hasAttribute('controls'), btn: !!document.querySelector('.clip-wide .play-btn') }; });
  await btn.scrollIntoViewIfNeeded(); await btn.click(); await p.waitForTimeout(500);
  out.play_after = await p.evaluate(() => { const v = document.querySelector('.clip-wide video'); return { started: v.closest('.player').classList.contains('is-started'), controls: v.hasAttribute('controls'), paused: v.paused, err: v.error && v.error.code, canMp4: v.canPlayType('video/mp4; codecs="avc1.640028"') }; });
  // focus ring screenshot: tab from top
  await p.goto(BASE); for (let i = 0; i < 6; i++) await p.keyboard.press('Tab');
  out.focused = await p.evaluate(() => document.activeElement.textContent.trim().slice(0, 40));
  await p.screenshot({ path: OUT + '/focus_desktop.png', clip: { x: 0, y: 0, width: 1440, height: 560 } });
  await ctx.close();
}
// 2. swipe on mobile
{
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 }); await route(ctx);
  const p = await ctx.newPage(); await p.goto(BASE + 'games/street-takeover/');
  await p.locator('a.shot').first().scrollIntoViewIfNeeded(); await p.locator('a.shot').first().tap(); await p.waitForTimeout(400);
  const before = await p.evaluate(() => document.querySelector('.lb-count').textContent);
  const box = await p.locator('.lb-stage').boundingBox();
  const cdp = await ctx.newCDPSession(p);
  const y = box.y + box.height / 2;
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: 300, y }] });
  for (let x = 280; x >= 80; x -= 40) await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x, y }] });
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
  await p.waitForTimeout(400);
  out.swipe = { before, after: await p.evaluate(() => document.querySelector('.lb-count').textContent), stillOpen: await p.evaluate(() => document.querySelector('dialog.lightbox').open) };
  await p.screenshot({ path: OUT + '/lightbox_mobile.png' });
  await ctx.close();
}
// 3. home weight before the trailer plays, at several pixel ratios
for (const [name, w, h, dpr, mob] of [['desktop-1x', 1440, 900, 1, false], ['desktop-2x', 1440, 900, 2, false], ['phone-3x', 390, 844, 3, true]]) {
  const served = [];
  const ctx = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: dpr, isMobile: mob, hasTouch: mob }); await route(ctx, served);
  const p = await ctx.newPage(); await p.goto(BASE, { waitUntil: 'load' });
  const H = await p.evaluate(() => document.documentElement.scrollHeight);
  for (let yy = 0; yy <= H; yy += 300) { await p.evaluate(v => window.scrollTo({ top: v, behavior: 'instant' }), yy); await p.waitForTimeout(80); }
  await p.waitForTimeout(800);
  const total = served.reduce((a, s) => a + s[1], 0);
  out['weight_' + name] = { kb: Math.round(total / 1024), files: served.map(s => s[0] + ' ' + Math.round(s[1] / 1024) + 'KB') };
  await ctx.close();
}
await b.close();
console.log(JSON.stringify(out, null, 1));
