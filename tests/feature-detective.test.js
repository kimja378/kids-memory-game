// Playwright tests for feature-detective/ (served under /kids-memory-game/ like GitHub Pages).
// Run: node --test tests/feature-detective.test.js
const { test, before, after } = require('node:test');
const assert = require('node:assert/strict');
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const { chromium, devices } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const BASE = '/kids-memory-game/feature-detective/';
const TYPES = { '.html': 'text/html; charset=utf-8', '.json': 'application/json', '.jpg': 'image/jpeg' };
const html = fs.readFileSync(path.join(ROOT, 'feature-detective/index.html'), 'utf8');
const objects = JSON.parse('[' + html.slice(html.indexOf('const objects=[') + 15, html.indexOf('];let section=')) + ']');

let server, browser, origin;
before(async () => {
  server = http.createServer((req, res) => {
    const u = new URL(req.url, 'http://x');
    if (!u.pathname.startsWith('/kids-memory-game/')) { res.writeHead(404); return res.end(); }
    let rel = decodeURIComponent(u.pathname.slice('/kids-memory-game/'.length));
    if (rel === '' || rel.endsWith('/')) rel += 'index.html';
    const file = path.join(ROOT, rel);
    if (!file.startsWith(ROOT) || !fs.existsSync(file)) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { 'Content-Type': TYPES[path.extname(file)] || 'application/octet-stream' });
    fs.createReadStream(file).pipe(res);
  });
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  origin = `http://127.0.0.1:${server.address().port}`;
  browser = await chromium.launch();
});
after(async () => { await browser?.close(); server?.close(); });

async function open() {
  const ctx = await browser.newContext({ ...devices['iPad (gen 7)'] });
  const page = await ctx.newPage();
  const errors = [], external = [], failed = [];
  page.on('pageerror', e => errors.push(String(e)));
  page.on('request', r => { if (!r.url().startsWith(origin)) external.push(r.url()); });
  page.on('response', r => { if (r.status() >= 400) failed.push(r.url()); });
  await page.goto(origin + BASE);
  return { ctx, page, errors, external, failed };
}
const photoOk = img => img.complete && img.naturalWidth > 50;

test('data: 24 objects, photo files exist, riddles never contain the answer', () => {
  assert.equal(objects.length, 24);
  for (const o of objects) {
    assert.equal(o.length, 7, o[0]);
    if (o[1].endsWith('.jpg')) {
      assert.match(o[1], /^assets\/images\/[a-z-]+\.jpg$/);
      assert.ok(fs.existsSync(path.join(ROOT, 'feature-detective', o[1])), o[1]);
    }
    assert.ok(!(o[4] + o[5]).includes(o[0]), 'answer in riddle: ' + o[0]);
  }
  assert.ok(!/https?:\/\//.test(html.slice(html.indexOf('<script>'))), 'no external URL in script');
});

test('feature mode: every object shows its own photo (or emoji) with 2 steps and feedback', async () => {
  const { ctx, page, errors, external, failed } = await open();
  await page.click('#objectSection');
  for (const o of objects) {
    const prompt = await page.textContent('.prompt');
    assert.ok(prompt.startsWith(o[0]), `expected ${o[0]}, got ${prompt}`);
    if (o[1].endsWith('.jpg')) {
      await page.waitForFunction(() => { const i = document.querySelector('.picture img'); return i && i.complete && i.naturalWidth > 50; });
      assert.equal(await page.getAttribute('.picture img', 'src'), o[1]);
      assert.equal(await page.getAttribute('.picture img', 'alt'), o[0]);
    } else {
      assert.equal((await page.textContent('.picture')).trim(), o[1]);
    }
    // step 1: location (wrong then right), step 2: purpose
    const wrong = await page.$(`.choice:not([data-answer="${o[2]}"])`);
    await wrong.click();
    assert.equal(await page.textContent('#feedback'), '다시 생각해 보자! 💛');
    await page.click(`.choice[data-answer="${o[2]}"]`);
    assert.equal(await page.textContent('#feedback'), '잘했어! 최고야! ⭐');
    await page.waitForSelector('.pill:text("2 / 2")');
    await page.click(`.choice[data-answer="${o[3]}"]`);
    assert.equal(await page.textContent('#feedback'), '잘했어! 최고야! ⭐');
    await page.click('#next');
  }
  assert.deepEqual(errors, []); assert.deepEqual(external, []); assert.deepEqual(failed, []);
  await ctx.close();
});

test('riddle mode: pictures hidden first, hint shows photos, answers checked, hide again', async () => {
  const { ctx, page, errors, external, failed } = await open();
  await page.click('#objectSection');
  await page.click('#riddle');
  for (let n = 0; n < objects.length; n++) {
    const o = objects[n];
    assert.ok((await page.textContent('.riddle')).includes(o[4]));
    assert.ok(await page.isHidden('#answers'));
    assert.ok(await page.isVisible('#cover'));
    await page.click('#showHint');
    assert.ok(await page.isVisible('#answers'));
    await page.waitForFunction(() => [...document.querySelectorAll('#answers img')].every(i => i.complete && i.naturalWidth > 50));
    const btns = await page.$$eval('#answers button', bs => bs.map(b => b.dataset.answer));
    assert.equal(btns.length, 3); assert.ok(btns.includes(o[0]));
    const wrong = btns.find(b => b !== o[0]);
    await page.click(`#answers button[data-answer="${wrong}"]`);
    assert.equal(await page.textContent('#feedback'), '다시 생각해 보자! 💛');
    await page.click(`#answers button[data-answer="${o[0]}"]`);
    assert.equal(await page.textContent('#feedback'), '잘했어! 최고야! ⭐');
    if (n === 0) { await page.click('#hideHint button'); assert.ok(await page.isHidden('#answers')); }
    await page.click('#next');
  }
  await page.click('#reset');
  assert.ok((await page.textContent('.riddle')).includes(objects[0][4]));
  assert.deepEqual(errors, []); assert.deepEqual(external, []); assert.deepEqual(failed, []);
  await ctx.close();
});

test('fruit/vegetable section unchanged: emoji pictures, kind and color steps, riddles', async () => {
  const { ctx, page, errors } = await open();
  assert.equal((await page.textContent('.prompt')), '토마토는 어떤 종류일까?');
  assert.equal((await page.textContent('.picture')).trim(), '🍅');
  await page.click('.choice[data-answer="채소"]');
  await page.waitForSelector('.pill:text("2 / 2")');
  assert.equal(await page.textContent('.prompt'), '토마토는 무슨 색깔일까?');
  await page.click('#riddle');
  await page.click('#showHint');
  assert.equal(await page.$$eval('#answers button', b => b.length), 3);
  assert.deepEqual(errors, []);
  await ctx.close();
});

test('josa: 컵은 / 시계는', async () => {
  const { ctx, page } = await open();
  await page.click('#objectSection');
  for (let i = 0; i < objects.length; i++) {
    const p = await page.textContent('.prompt');
    if (p.startsWith('컵')) assert.ok(p.startsWith('컵은 '), p);
    if (p.startsWith('시계')) assert.ok(p.startsWith('시계는 '), p);
    await page.click('#next');
  }
  await ctx.close();
});
