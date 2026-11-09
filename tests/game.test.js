// Playwright E2E tests for the photo memory game.
// Run: node --test tests/          (uses the pre-installed `playwright` package, Chromium)
// The repo is served under /kids-memory-game/ to mimic the GitHub Pages path.
const { test, before, after } = require('node:test');
const assert = require('node:assert/strict');
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const { chromium, devices } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const BASE = '/kids-memory-game/';
const catalog = JSON.parse(fs.readFileSync(path.join(ROOT, 'assets/images/catalog.json'), 'utf8'));
const byFile = new Map(catalog.items.map(i => [i.file, i]));
const CATS = ['fruit', 'veg', 'animal', 'vehicle'];
const TYPES = { '.html': 'text/html; charset=utf-8', '.json': 'application/json', '.jpg': 'image/jpeg', '.js': 'text/javascript' };

let server, browser, origin;
before(async () => {
  server = http.createServer((req, res) => {
    const u = new URL(req.url, 'http://x');
    if (!u.pathname.startsWith(BASE)) { res.writeHead(404); return res.end(); }
    let rel = decodeURIComponent(u.pathname.slice(BASE.length)) || 'index.html';
    const file = path.join(ROOT, rel);
    if (!file.startsWith(ROOT) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { 'Content-Type': TYPES[path.extname(file)] || 'application/octet-stream' });
    fs.createReadStream(file).pipe(res);
  });
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  origin = `http://127.0.0.1:${server.address().port}`;
  browser = await chromium.launch();
});
after(async () => { await browser?.close(); server?.close(); });

async function openGame(setup) {
  const ctx = await browser.newContext({ ...devices['iPad (gen 7)'] });
  const page = await ctx.newPage();
  if (setup) await setup(page);
  const errors = [], external = [];
  page.on('pageerror', e => errors.push(String(e)));
  page.on('request', r => { if (!r.url().startsWith(origin)) external.push(r.url()); });
  await page.goto(origin + BASE);
  await page.waitForSelector('body[data-ready]');
  return { ctx, page, errors, external };
}

// Returns the 3 visible cards after the latest question finished loading.
async function cardsState(page) {
  await page.waitForFunction(() => !document.body.hasAttribute('data-loading'));
  return page.$$eval('.card', cs => cs.map(c => {
    const img = c.querySelector('.face img');
    return { src: img.getAttribute('src'), alt: img.alt, name: c.querySelector('.name').textContent,
      ok: img.complete && img.naturalWidth > 20, flipped: c.classList.contains('flipped') };
  }));
}

function checkThree(state, category) {
  assert.equal(state.length, 3);
  assert.equal(new Set(state.map(s => s.src)).size, 3, 'duplicate photo in one question');
  assert.equal(new Set(state.map(s => s.name)).size, 3, 'duplicate name in one question');
  for (const s of state) {
    assert.ok(s.ok, `image not loaded: ${s.src}`);
    assert.match(s.src, /^assets\/images\/[a-z]+\/[a-z0-9_]+\.jpg$/, 'must be a local relative path');
    const item = byFile.get(s.src);
    assert.ok(item, `not in catalog: ${s.src}`);
    assert.equal(s.name, item.name, 'name/photo mismatch');
    assert.equal(s.alt, item.name);
    if (category && category !== 'all') assert.equal(item.category, category, `wrong category for ${s.src}`);
  }
}

test('initial load shows 3 local photos, no external requests, no JS errors', async () => {
  const { ctx, page, errors, external } = await openGame();
  checkThree(await cardsState(page), 'fruit');
  assert.deepEqual(external, []);
  assert.deepEqual(errors, []);
  await ctx.close();
});

test('every category (and all-mix) shows 3 correct photos, 15 rounds each', async () => {
  const { ctx, page, errors } = await openGame();
  for (const cat of [...CATS, 'all']) {
    await page.selectOption('#category', cat);
    for (let i = 0; i < 15; i++) {
      checkThree(await cardsState(page), cat);
      await page.click('#new');
    }
    checkThree(await cardsState(page), cat);
  }
  assert.deepEqual(errors, []);
  await ctx.close();
});

test('pressing next rapidly 40 times ends in a consistent question', async () => {
  const { ctx, page, errors } = await openGame();
  await page.selectOption('#category', 'animal');
  for (let i = 0; i < 40; i++) await page.click('#new', { delay: 0 });
  await page.waitForTimeout(300);
  checkThree(await cardsState(page), 'animal');
  assert.deepEqual(errors, []);
  await ctx.close();
});

test('rapid category switching: stale loads never overwrite the newest category', async () => {
  const { ctx, page, errors } = await openGame();
  // Slow down images of every category except the final one so stale results arrive late.
  await page.route('**/assets/images/**/*.jpg', async route => {
    if (!route.request().url().includes('/vegetables/')) await new Promise(r => setTimeout(r, 700));
    route.continue();
  });
  for (const cat of ['animal', 'vehicle', 'fruit', 'all', 'animal', 'veg']) {
    await page.selectOption('#category', cat);
  }
  await page.waitForTimeout(2000);
  checkThree(await cardsState(page), 'veg');
  assert.deepEqual(errors, []);
  await ctx.close();
});

test('flip one card, flip all, show all, and praise text', async () => {
  const { ctx, page } = await openGame();
  await page.click('.card >> nth=1');
  assert.deepEqual((await cardsState(page)).map(s => s.flipped), [false, true, false]);
  assert.equal(await page.textContent('#status'), '무엇이 숨어 있을까요?');
  await page.click('.card >> nth=1');
  assert.equal(await page.textContent('#status'), '잘했어! 최고야! ⭐');
  await page.click('#hide');
  assert.deepEqual((await cardsState(page)).map(s => s.flipped), [true, true, true]);
  assert.equal(await page.textContent('#status'), '어디에 어떤 사진이 있었을까요?');
  await page.click('#show');
  assert.deepEqual((await cardsState(page)).map(s => s.flipped), [false, false, false]);
  assert.equal(await page.textContent('#status'), '잘했어! 최고야! ⭐');
  // a new question un-flips cards
  await page.click('#hide');
  await page.click('#new');
  assert.deepEqual((await cardsState(page)).map(s => s.flipped), [false, false, false]);
  await ctx.close();
});

test('name show/hide toggle', async () => {
  const { ctx, page } = await openGame();
  const vis = () => page.$eval('.card .name', e => getComputedStyle(e).visibility);
  assert.equal(await vis(), 'hidden');
  assert.equal(await page.textContent('#names'), '이름 보기');
  await page.click('#names');
  assert.equal(await vis(), 'visible');
  assert.equal(await page.textContent('#names'), '이름 숨기기');
  await page.click('#names');
  assert.equal(await vis(), 'hidden');
  await ctx.close();
});

test('missing/broken image files are skipped and the game keeps working', async () => {
  const fruits = catalog.items.filter(i => i.category === 'fruit').map(i => i.file);
  const missing = fruits.slice(0, 2), corrupt = fruits[2];
  const { ctx, page, errors } = await openGame(async page => {
    await page.route('**/assets/images/**', route => {
      const u = route.request().url();
      if (missing.some(b => u.endsWith(b))) return route.fulfill({ status: 404, body: '' });
      if (u.endsWith(corrupt)) return route.fulfill({ status: 200, contentType: 'image/jpeg', body: 'not a jpeg' });
      route.continue();
    });
  });
  for (let i = 0; i < 15; i++) {
    const st = await cardsState(page);
    checkThree(st, 'fruit');
    for (const s of st) assert.ok(![...missing, corrupt].includes(s.src), 'broken image shown: ' + s.src);
    await page.click('#new');
  }
  const failed = await page.evaluate(() => Object.keys(window.__memoryGame.failed));
  for (const f of failed) assert.ok([...missing, corrupt].includes(f), 'unexpected failure ' + f);
  assert.deepEqual(errors, []);
  await ctx.close();
});

test('a category without enough photos hides cards instead of showing a stale question', async () => {
  const { ctx, page } = await openGame(async page => {
    await page.route('**/assets/images/vehicles/**', r => r.fulfill({ status: 404, body: '' }));
  });
  await page.selectOption('#category', 'vehicle');
  await page.waitForFunction(() => document.getElementById('status').textContent.includes('충분히'));
  assert.equal(await page.$eval('#cards', e => getComputedStyle(e).visibility), 'hidden');
  await page.selectOption('#category', 'animal');
  checkThree(await cardsState(page), 'animal');
  assert.equal(await page.$eval('#cards', e => getComputedStyle(e).visibility), 'visible');
  await ctx.close();
});

test('catalog failure shows a friendly message instead of crashing', async () => {
  const ctx = await browser.newContext();
  const page = await ctx.newPage();
  await page.route('**/catalog.json*', r => r.fulfill({ status: 500, body: '' }));
  await page.goto(origin + BASE);
  await page.waitForFunction(() => document.getElementById('status').textContent.includes('새로고침'), null, { timeout: 8000 });
  await ctx.close();
});

test('every catalog image decodes in the browser', async () => {
  const { ctx, page } = await openGame();
  const bad = await page.evaluate(async files => {
    const out = [];
    await Promise.all(files.map(f => new Promise(res => {
      const img = new Image();
      img.onload = () => { if (img.naturalWidth < 50) out.push(f); res(); };
      img.onerror = () => { out.push(f); res(); };
      img.src = f;
    })));
    return out;
  }, catalog.items.map(i => i.file));
  assert.deepEqual(bad, []);
  await ctx.close();
});
