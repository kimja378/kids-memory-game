// Playwright tests for situation-game/ (served under /kids-memory-game/ like GitHub Pages).
// Run: node --test tests/situation-game.test.js
const { test, before, after } = require('node:test');
const assert = require('node:assert/strict');
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { chromium, devices } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const GAME = path.join(ROOT, 'situation-game');
const BASE = '/kids-memory-game/situation-game/';
const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml' };
const ctxData = { window: {} };
vm.runInNewContext(fs.readFileSync(path.join(GAME, 'data.js'), 'utf8'), ctxData);
const { OBJECTS, SITUATIONS, LEVELS } = ctxData.window;

let server, browser, origin;
before(async () => {
  server = http.createServer((req, res) => {
    const u = new URL(req.url, 'http://x');
    let rel = decodeURIComponent(u.pathname.replace('/kids-memory-game/', ''));
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

// Speech is stubbed so the test can read what the game says.
const STUB = () => {
  window.__said = [];
  const fake = { speaking: false, pending: false, speak(u) { window.__said.push(u.text); setTimeout(() => u.onend && u.onend(), 250); },
    cancel() {}, resume() {}, getVoices() { return []; }, addEventListener() {} };
  Object.defineProperty(window, 'speechSynthesis', { value: fake, configurable: true });
  window.SpeechSynthesisUtterance = function (t) { this.text = t; };
};

async function open(device = 'iPad (gen 7) landscape') {
  const ctx = await browser.newContext({ ...devices[device] });
  await ctx.addInitScript(STUB);
  const page = await ctx.newPage();
  const errors = [], external = [], failed = [];
  page.on('pageerror', e => errors.push(String(e)));
  page.on('request', r => { if (!r.url().startsWith(origin)) external.push(r.url()); });
  page.on('response', r => { if (r.status() >= 400) failed.push(r.url()); });
  await page.goto(origin + BASE);
  return { ctx, page, errors, external, failed };
}
const said = page => page.evaluate(() => window.__said.slice());
const cur = page => page.evaluate(() => { const c = window.__game.cur; return { sit: c.sit.id, correct: c.correct, options: c.options }; });

test('data: ids valid, lists disjoint, every level has enough items, all pictures exist', () => {
  for (const [id, o] of Object.entries(OBJECTS)) {
    for (const k of ['name', 'use', 'when', 'hint']) assert.ok(o[k], `${id}.${k}`);
    assert.ok(!o.hint.includes(o.name), `hint must not name the answer: ${id}`);
    assert.ok(fs.existsSync(path.join(GAME, 'assets/objects', id + '.svg')), id);
    assert.ok(fs.existsSync(path.join(GAME, 'assets/usage', (o.usage || id) + '.svg')), 'usage ' + id);
  }
  for (const s of SITUATIONS) {
    const all = [...s.correct, ...s.accept, ...s.distractors];
    all.forEach(id => assert.ok(OBJECTS[id], `${s.id}: unknown object ${id}`));
    assert.equal(new Set(all).size, all.length, `${s.id}: correct/accept/distractors overlap`);
    for (const L of Object.values(LEVELS)) {
      assert.ok(s.correct.length >= L.correct && s.distractors.length >= L.wrong, `${s.id} ${L.label}`);
    }
    for (let v = 1; v <= s.scenes; v++) assert.ok(fs.existsSync(path.join(GAME, 'assets/scenes', `${s.id}-${v}.svg`)));
  }
});

test('no emoji anywhere in the game (pictures are SVG illustrations)', () => {
  const emoji = /[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}\u{1F000}-\u{1F2FF}]/u;
  for (const f of ['index.html', 'game.js', 'data.js', 'style.css']) {
    assert.ok(!emoji.test(fs.readFileSync(path.join(GAME, f), 'utf8')), f);
  }
});

test('scene pictures never contain an answer object (scenes are composed only of scene parts)', () => {
  // The generator draws scenes from people/background parts only; check scene files do not embed object drawings.
  const src = fs.readFileSync(path.join(ROOT, 'tools/situation_art.py'), 'utf8');
  const scenePart = src.slice(src.indexOf('# ------------------------------------------------------------------ situation scenes'), src.indexOf('SCENES = {'));
  for (const fn of ['o_toothbrush', 'o_toothpaste', 'o_cup', 'o_spoon', 'o_chopsticks', 'o_plate', 'o_bed', 'o_blanket', 'o_pillow', 'o_pajamas', 'o_broom', 'o_dustpan', 'o_vacuum', 'o_mop', 'o_cake', 'o_party_hat', 'o_gift']) {
    assert.ok(!scenePart.includes(fn + '('), 'scene uses ' + fn);
  }
});

for (const level of Object.keys(LEVELS)) {
  test(`level ${level}: every situation plays through with correct option counts, feedback, usage scene and log`, async () => {
    const { ctx, page, errors, external, failed } = await open();
    await page.click(`.level[data-level="${level}"]`);
    await page.click('#go');
    const L = LEVELS[level];
    const seen = new Set();
    for (let q = 0; q < SITUATIONS.length; q++) {
      const c = await cur(page);
      seen.add(c.sit);
      const sit = SITUATIONS.find(s => s.id === c.sit);
      assert.equal(c.options.length, L.correct + L.wrong);
      assert.equal(c.correct.length, L.correct);
      assert.equal(await page.$$eval('.card', x => x.length), L.correct + L.wrong);
      for (const o of c.options) assert.ok(!sit.accept.includes(o), 'acceptable object shown as option: ' + o);
      for (const o of c.options) if (!c.correct.includes(o)) assert.ok(sit.distractors.includes(o));
      await page.waitForFunction(() => [...document.querySelectorAll('.card img, #sceneImg')].every(i => i.complete && i.naturalWidth > 0));
      // question is spoken
      assert.ok((await said(page)).some(t => t.includes(sit.story)));
      // one wrong pick on the first question: gentle message, card stays tappable
      if (q === 0) {
        const wrong = c.options.find(o => !c.correct.includes(o));
        await page.click(`.card[data-id="${wrong}"]`);
        assert.ok((await page.textContent('#feedback')).includes('다시 찾아볼까요'));
        assert.ok(await page.$eval(`.card[data-id="${wrong}"]`, e => e.classList.contains('tried')));
      }
      for (const id of c.correct) {
        await page.click(`.card[data-id="${id}"]`);
        assert.ok(await page.$eval(`.card[data-id="${id}"]`, e => e.classList.contains('found')));
        // usage scene appears (it closes again after the praise is spoken)
        assert.equal(await page.evaluate(() => window.__lastUsage), id, 'usage scene shown for ' + id);
      }
      await page.waitForSelector('#next:not(.hidden)');
      assert.ok((await said(page)).some(t => t.startsWith('잘했어요!') && t.includes(sit.when)));
      await page.click('#next', { force: true });
    }
    assert.equal(seen.size, SITUATIONS.length, 'each situation once per round');
    await page.waitForSelector('#done:not(.hidden)');
    const log = await page.evaluate(k => JSON.parse(localStorage.getItem(k)), 'situationGame.log.v1');
    assert.equal(log.length, SITUATIONS.length);
    assert.equal(log.filter(x => !x.firstTry).length, 1);
    assert.ok(log.every(x => x.level === level));
    assert.deepEqual(errors, []); assert.deepEqual(external, []); assert.deepEqual(failed, []);
    await ctx.close();
  });
}

test('hints: 1 repeats the question, 2 explains a function, 3 highlights the remaining answers', async () => {
  const { ctx, page } = await open();
  await page.click('.level[data-level="hard"]'); await page.click('#go');
  const c = await cur(page);
  await page.click(`.card[data-id="${c.correct[0]}"]`);
  const before = (await said(page)).length;
  await page.click('#hint');
  const s1 = (await said(page)).slice(before);
  assert.ok(s1.some(t => t.includes('무엇이 필요할까요')));
  await page.click('#hint');
  const s2 = (await said(page)).slice(-1)[0];
  const hints = c.correct.slice(1).map(id => OBJECTS[id].hint);
  assert.ok(hints.some(h => s2.includes(h)), s2);
  await page.click('#hint');
  const glow = await page.$$eval('.card.glow', x => x.map(e => e.dataset.id));
  assert.deepEqual(glow.sort(), c.correct.slice(1).sort());
  for (const id of c.correct.slice(1)) await page.click(`.card[data-id="${id}"]`);
  const log = await page.evaluate(() => JSON.parse(localStorage.getItem('situationGame.log.v1')));
  assert.equal(log[0].hint, 3);
  await ctx.close();
});

test('scene variants alternate between plays of the same situation', async () => {
  const { ctx, page } = await open();
  const variants = {};
  for (let r = 0; r < 3; r++) {
    await page.click('#go');
    for (let q = 0; q < SITUATIONS.length; q++) {
      const v = await page.evaluate(() => [window.__game.cur.sit.id, window.__game.cur.variant]);
      (variants[v[0]] = variants[v[0]] || []).push(v[1]);
      const c = await cur(page);
      for (const id of c.correct) await page.click(`.card[data-id="${id}"]`);
      await page.waitForSelector('#next:not(.hidden)');
      await page.click('#next', { force: true });
    }
    await page.click('#home2');
  }
  for (const [sit, vs] of Object.entries(variants)) {
    for (let i = 1; i < vs.length; i++) assert.notEqual(vs[i], vs[i - 1], `${sit} repeated the same picture`);
  }
  await ctx.close();
});

test('parent report shows per-situation results and recent records; child screen shows no score', async () => {
  const { ctx, page } = await open();
  await page.click('#go');
  const c = await cur(page);
  const wrong = c.options.find(o => !c.correct.includes(o));
  await page.click(`.card[data-id="${wrong}"]`);
  for (const id of c.correct) await page.click(`.card[data-id="${id}"]`);
  const childText = await page.textContent('#game');
  assert.ok(!/%|점수|오답/.test(childText));
  await page.click('#openReport2');
  const rep = await page.textContent('#reportBody');
  const title = SITUATIONS.find(s => s.id === c.sit).title;
  assert.ok(rep.includes('상황별 결과') && rep.includes('최근 기록') && rep.includes(title));
  assert.ok(rep.includes('0%'));   // first-try rate for that situation
  await ctx.close();
});

test('a missing picture never stops the game', async () => {
  const ctx = await browser.newContext({ ...devices['iPad (gen 7) landscape'] });
  await ctx.addInitScript(STUB);
  const page = await ctx.newPage();
  const errors = []; page.on('pageerror', e => errors.push(String(e)));
  await page.route('**/assets/usage/**', r => r.fulfill({ status: 404, body: '' }));
  await page.goto(origin + BASE);
  await page.click('#go');
  for (let q = 0; q < SITUATIONS.length; q++) {
    const c = await cur(page);
    for (const id of c.correct) await page.click(`.card[data-id="${id}"]`);
    await page.waitForSelector('#next:not(.hidden)');
    await page.click('#next', { force: true });
  }
  await page.waitForSelector('#done:not(.hidden)');
  assert.deepEqual(errors, []);
  await ctx.close();
});

test('portrait iPad layout fits without horizontal scrolling', async () => {
  const { ctx, page } = await open('iPad (gen 7)');
  await page.click('#go');
  const over = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
  assert.ok(over <= 1, 'horizontal overflow ' + over);
  await ctx.close();
});

test('every usage scene picture loads in the browser', async () => {
  const { ctx, page } = await open();
  const files = [...new Set(Object.entries(OBJECTS).map(([id, o]) => 'assets/usage/' + (o.usage || id) + '.svg'))];
  const bad = await page.evaluate(async fs => {
    const out = [];
    await Promise.all(fs.map(f => new Promise(r => { const i = new Image(); i.onload = () => { if (!i.naturalWidth) out.push(f); r(); }; i.onerror = () => { out.push(f); r(); }; i.src = f; })));
    return out;
  }, files);
  assert.deepEqual(bad, []);
  await ctx.close();
});

test('the next button still appears when Safari never reports the end of speech', async () => {
  const ctx = await browser.newContext({ ...devices['iPad (gen 7) landscape'] });
  await ctx.addInitScript(() => {
    const fake = { speaking: false, pending: false, speak() {}, cancel() {}, resume() {}, getVoices() { return []; }, addEventListener() {} };
    Object.defineProperty(window, 'speechSynthesis', { value: fake, configurable: true });
    window.SpeechSynthesisUtterance = function (t) { this.text = t; };
  });
  const page = await ctx.newPage();
  await page.goto(origin + BASE);
  await page.click('#go');
  const c = await cur(page);
  for (const id of c.correct) await page.click(`.card[data-id="${id}"]`);
  await page.waitForSelector('#next:not(.hidden)', { timeout: 15000 });
  await ctx.close();
});

test('tapping start speaks the first question right away (inside the tap), with no silent warm-up utterance', async () => {
  const ctx = await browser.newContext({ ...devices['iPad (gen 7) landscape'] });
  await ctx.addInitScript(() => {
    window.__calls = [];
    const fake = { speaking: false, pending: false, speak(u) { window.__calls.push({ text: u.text, inTap: !!window.__inTap }); }, cancel() { window.__calls.push({ cancel: true }); },
      resume() {}, getVoices() { return []; }, addEventListener() {} };
    Object.defineProperty(window, 'speechSynthesis', { value: fake, configurable: true });
    window.SpeechSynthesisUtterance = function (t) { this.text = t; };
    document.addEventListener('click', () => { window.__inTap = true; setTimeout(() => { window.__inTap = false; }, 0); }, true);
  });
  const page = await ctx.newPage();
  await page.goto(origin + BASE);
  await page.click('#go');
  const calls = await page.evaluate(() => window.__calls);
  assert.ok(calls.length >= 1);
  assert.ok(!calls[0].cancel && calls[0].text.trim().length > 0 && calls[0].inTap, JSON.stringify(calls));
  await page.click('#soundCheck', { force: true }).catch(() => {});
  await ctx.close();
});
