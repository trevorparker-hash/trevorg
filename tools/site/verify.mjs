import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require('/tmp/claude-0/-home-user-Ninefold/aced07b5-8bf6-5d5f-83ea-056e9f0c83cb/scratchpad/art/node_modules/playwright-core');
import fs from 'fs'; import path from 'path';
const ROOT = '/home/user/trevorg';
const BASE = 'https://trevorparker-hash.github.io/trevorg/';
const OUT = '/tmp/claude-0/-home-user/aced07b5-8bf6-5d5f-83ea-056e9f0c83cb/scratchpad/site_shots';
const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.jpg': 'image/jpeg', '.png': 'image/png', '.woff2': 'font/woff2', '.ico': 'image/x-icon', '.mp4': 'video/mp4', '.xml': 'application/xml', '.txt': 'text/plain' };
const pages = (process.env.PAGES || 'index:,engagement:games/engagement/,fight:games/fight/,street-takeover:games/street-takeover/,field-surgeon:games/field-surgeon/,press:press/,404:no/such/page/here').split(',').map(s => s.split(':'));
const sizes = (process.env.SIZES || 'desktop:1440x900x1,mobile:390x844x1').split(',').map(s => { const [n, d] = s.split(':'); const [w, h, r] = d.split('x').map(Number); return { n, w, h, r }; });
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const report = [];
for (const sz of sizes) {
  const ctx = await browser.newContext({ viewport: { width: sz.w, height: sz.h }, deviceScaleFactor: sz.r, isMobile: sz.n.startsWith('mobile'), hasTouch: sz.n.startsWith('mobile') });
  await ctx.route('**/*', async (route) => {
    const url = new URL(route.request().url());
    if (url.host === 'trevorparker-hash.github.io' && url.pathname.startsWith('/trevorg/')) {
      let rel = decodeURIComponent(url.pathname.slice('/trevorg/'.length));
      let file = path.join(ROOT, rel);
      if (rel === '' || rel.endsWith('/')) file = path.join(file, 'index.html');
      let status = 200;
      if (!fs.existsSync(file) || fs.statSync(file).isDirectory()) { file = path.join(ROOT, '404.html'); status = 404; }
      const body = fs.readFileSync(file);
      return route.fulfill({ status, body, headers: { 'content-type': TYPES[path.extname(file)] || 'application/octet-stream', 'content-length': String(body.length) } });
    }
    if (url.host === 'store.steampowered.com' && url.pathname.startsWith('/widget/')) {
      return route.fulfill({ status: 200, contentType: 'text/html', body: '<body style="margin:0;background:#1b2838;color:#c7d5e0;font:14px Arial;display:grid;place-items:center;height:190px">Steam store widget (mocked in this test)</body>' });
    }
    return route.abort();
  });
  for (const [name, rel] of pages) {
    const page = await ctx.newPage();
    const bytes = { total: 0, list: [] };
    const errors = [];
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    page.on('pageerror', e => errors.push('pageerror ' + e.message));
    page.on('requestfinished', async (req) => {
      const u = req.url();
      if (!u.startsWith(BASE)) return;
      const res = await req.response();
      const len = Number((await res.allHeaders())['content-length'] || 0);
      bytes.total += len; bytes.list.push([u.slice(BASE.length), len]);
    });
    await page.goto(BASE + rel, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    // scroll through to trigger lazy images
    const H = await page.evaluate(() => document.documentElement.scrollHeight);
    for (let y = 0; y < H; y += Math.floor(sz.h * 0.8)) { await page.evaluate(yy => window.scrollTo({ top: yy, behavior: 'instant' }), y); await page.waitForTimeout(120); }
    await page.evaluate(() => window.scrollTo({ top: document.documentElement.scrollHeight, behavior: 'instant' }));
    await page.waitForTimeout(400);
    await page.evaluate(async () => { await Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; }))); });
    await page.evaluate(() => window.scrollTo({ top: 0, behavior: 'instant' }));
    await page.waitForTimeout(300);
    const info = await page.evaluate(() => {
      const de = document.documentElement;
      const wide = [...document.querySelectorAll('body *')].filter(el => { const r = el.getBoundingClientRect(); return r.right > de.clientWidth + 1 && getComputedStyle(el).position !== 'fixed' && !el.closest('.clip-row'); }).slice(0, 8).map(el => el.tagName + '.' + el.className + ' ' + Math.round(el.getBoundingClientRect().right));
      const broken = [...document.images].filter(i => !i.naturalWidth && !i.closest('dialog')).map(i => i.currentSrc || i.src);
      const small = [...document.querySelectorAll('a, button')].filter(el => { const r = el.getBoundingClientRect(); return r.width > 0 && (r.height < 44 || r.width < 24) && !el.closest('.prose') && !el.closest('.press-head p'); }).slice(0, 12).map(el => (el.textContent || el.getAttribute('aria-label') || '').trim().slice(0, 30) + ' ' + Math.round(el.getBoundingClientRect().width) + 'x' + Math.round(el.getBoundingClientRect().height));
      return { scrollW: de.scrollWidth, clientW: de.clientWidth, height: de.scrollHeight, title: document.title, base: document.baseURI, wide, broken, small,
        fold: (() => { const v = document.querySelector('.hero-video video'); if (!v) return null; const r = v.getBoundingClientRect(); return { top: Math.round(r.top), bottom: Math.round(r.bottom) }; })() };
    });
    await page.screenshot({ path: `${OUT}/${name}_${sz.n}.png`, fullPage: true });
    report.push({ page: name, size: sz.n, bytes: bytes.total, n: bytes.list.length, errors, ...info, top: bytes.list.sort((a, b) => b[1] - a[1]).slice(0, 6) });
    await page.close();
  }
  await ctx.close();
}
await browser.close();
fs.writeFileSync(`${OUT}/report.json`, JSON.stringify(report, null, 1));
for (const r of report) console.log(JSON.stringify({ page: r.page, size: r.size, kb: Math.round(r.bytes / 1024), reqs: r.n, scrollW: r.scrollW, clientW: r.clientW, h: r.height, fold: r.fold, errors: r.errors, wide: r.wide, broken: r.broken, small: r.small, base: r.base }));
