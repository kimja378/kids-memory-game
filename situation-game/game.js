(function () {
'use strict';
const $ = id => document.getElementById(id);
const OBJ = window.OBJECTS, SITS = window.SITUATIONS, LEVELS = window.LEVELS;
const LOG_KEY = 'situationGame.log.v1', PREF_KEY = 'situationGame.prefs.v1';

/* ---------------- storage (never let a storage error stop the game) ---------------- */
function load(key, def) { try { const v = JSON.parse(localStorage.getItem(key)); return v == null ? def : v; } catch (e) { return def; } }
function save(key, v) { try { localStorage.setItem(key, JSON.stringify(v)); } catch (e) {} }
const prefs = Object.assign({ level: 'easy', names: true, lastScene: {} }, load(PREF_KEY, {}));
function savePrefs() { save(PREF_KEY, prefs); }

/* ---------------- speech (same approach as the storybooks, tested on iPad Safari) ---------------- */
const hasTTS = 'speechSynthesis' in window;
const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
let koVoice = null, unlocked = false;
function pickVoice() {
  try {
    const vs = speechSynthesis.getVoices().filter(v => v.lang && v.lang.toLowerCase().replace('_', '-').startsWith('ko'));
    koVoice = vs.find(v => v.localService && v.default) || vs.find(v => v.localService) || vs[0] || null;
  } catch (e) {}
}
if (hasTTS) { pickVoice(); try { speechSynthesis.addEventListener('voiceschanged', pickVoice); } catch (e) {} }
function unlockSpeech() {
  if (unlocked || !hasTTS) return;
  unlocked = true;
  try { const u = new SpeechSynthesisUtterance(' '); u.lang = 'ko-KR'; u.volume = 0; speechSynthesis.speak(u); } catch (e) {}
}
document.addEventListener('touchend', unlockSpeech, { passive: true });
document.addEventListener('click', unlockSpeech);
let speakToken = 0;
function speak(text, onend) {
  const token = ++speakToken;
  let fired = false;
  const done = () => { if (fired) return; fired = true; if (token === speakToken && onend) onend(); };
  /* Safari가 말하기 끝 신호를 주지 않는 경우에도 게임이 멈추지 않게 */
  if (onend) setTimeout(done, 1500 + text.length * 180);
  if (!hasTTS) { setTimeout(done, 1200); return; }
  try {
    const say = () => {
      const u = new SpeechSynthesisUtterance(text);
      u.lang = 'ko-KR';
      if (koVoice && !isIOS) u.voice = koVoice;
      u.rate = 0.85; u.pitch = 1.1; u.volume = 1;
      u.onend = done; u.onerror = done;
      try { speechSynthesis.resume(); } catch (e) {}
      speechSynthesis.speak(u);
    };
    if (speechSynthesis.speaking || speechSynthesis.pending) { speechSynthesis.cancel(); setTimeout(say, 150); }
    else say();
  } catch (e) { setTimeout(done, 1200); }
}
window.__speak = speak;

/* ---------------- helpers ---------------- */
function shuffle(a) { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }
function josa(w, a, b) { const c = w.charCodeAt(w.length - 1) - 44032; return w + (c >= 0 && c < 11172 && c % 28 ? a : b); }
function objImg(id) { return 'assets/objects/' + id + '.svg'; }
function usageImg(id) { return 'assets/usage/' + (OBJ[id].usage || id) + '.svg'; }
function sceneImg(sit, v) { return 'assets/scenes/' + sit.id + '-' + v + '.svg'; }
function show(id) { ['start', 'game', 'done'].forEach(s => $(s).classList.toggle('hidden', s !== id)); }

/* ---------------- start screen ---------------- */
function renderLevels() {
  $('levels').innerHTML = Object.entries(LEVELS).map(([k, L], i) =>
    `<button class="level${prefs.level === k ? ' sel' : ''}" data-level="${k}">
       <span class="dots">${[0, 1, 2].map(n => `<i class="${n <= i ? 'on' : ''}"></i>`).join('')}</span>
       ${L.label}<small>물건 ${L.correct + L.wrong}개 중 ${L.correct}개</small></button>`).join('');
  $('levels').querySelectorAll('.level').forEach(b => b.onclick = () => { prefs.level = b.dataset.level; savePrefs(); renderLevels(); });
}

/* ---------------- game state ---------------- */
let queue = [], qi = 0, cur = null;

function startRound() {
  queue = shuffle(SITS);
  qi = 0;
  show('game');
  newQuestion();
}

function pickScene(sit) {
  const last = prefs.lastScene[sit.id];
  const options = [];
  for (let v = 1; v <= sit.scenes; v++) if (v !== last || sit.scenes === 1) options.push(v);
  const v = options[Math.floor(Math.random() * options.length)];
  prefs.lastScene[sit.id] = v; savePrefs();
  return v;
}

function newQuestion() {
  const sit = queue[qi];
  const L = LEVELS[prefs.level];
  const correct = shuffle(sit.correct).slice(0, Math.min(L.correct, sit.correct.length));
  const blocked = new Set([...sit.correct, ...(sit.accept || [])]);
  const wrong = shuffle(sit.distractors.filter(d => !blocked.has(d))).slice(0, L.wrong);
  const options = shuffle([...correct, ...wrong]);
  const variant = pickScene(sit);
  cur = { sit, level: prefs.level, correct, options, variant, found: new Set(), tried: new Set(),
          wrongCount: 0, hintLevel: 0, firstPickCorrect: null, startedAt: Date.now(), finished: false };

  $('sceneImg').src = sceneImg(sit, variant);
  $('sceneImg').alt = sit.title + ' 상황 그림';
  $('title').textContent = sit.title;
  $('storyText').textContent = sit.story;
  $('question').textContent = correct.length === 1 ? '필요한 물건을 골라요.' : `필요한 물건 ${correct.length}개를 모두 골라요.`;
  $('feedback').textContent = '';
  $('next').classList.add('hidden'); $('next').classList.remove('pulse');
  closeUsage();
  const cards = $('cards');
  cards.className = 'cards n' + options.length;
  cards.innerHTML = options.map(id =>
    `<button class="card" data-id="${id}" aria-label="${OBJ[id].name}">
       <img src="${objImg(id)}" alt=""><span class="nm">${OBJ[id].name}</span>
       <span class="check"><svg viewBox="0 0 24 24"><use href="#i-check"/></svg></span></button>`).join('');
  cards.querySelectorAll('.card').forEach(b => b.onclick = () => pick(b));
  $('round').innerHTML = queue.map((s, i) => `<i class="${i < qi ? 'done' : i === qi ? 'now' : ''}"></i>`).join('');
  document.body.dataset.question = sit.id;
  speakQuestion();
}

function questionSpeech() {
  const n = cur.correct.length;
  return cur.sit.story + ' ' + (n === 1 ? '무엇이 필요할까요?' : `무엇이 필요할까요? ${n}개를 찾아봐요.`);
}
function speakQuestion() { speak(questionSpeech()); }

function pick(btn) {
  if (!cur || cur.finished) return;
  const id = btn.dataset.id;
  if (cur.found.has(id)) { showUsage(id); return; }
  const isCorrect = cur.correct.includes(id);
  if (cur.firstPickCorrect === null) cur.firstPickCorrect = isCorrect;
  if (isCorrect) {
    cur.found.add(id);
    btn.classList.add('found'); btn.classList.remove('glow', 'tried');
    const all = cur.found.size === cur.correct.length;
    showUsage(id);
    $('feedback').textContent = '맞아요! ' + OBJ[id].use;
    speak('맞아요! ' + OBJ[id].use, all ? finish : null);
    if (all) { cur.finished = true; record(); }
  } else {
    cur.wrongCount++;
    cur.tried.add(id);
    btn.classList.remove('shake'); void btn.offsetWidth; btn.classList.add('shake', 'tried');
    const o = OBJ[id];
    const msg = `${josa(o.name, '은', '는')} ${o.when} 다시 찾아볼까요?`;
    $('feedback').textContent = msg;
    speak(msg);
  }
}

function finish() {
  const names = cur.correct.map(id => OBJ[id].name);
  const list = names.length === 1 ? names[0] : names.slice(0, -2).map(n => n + ', ').join('') + josa(names[names.length - 2], '과', '와') + ' ' + names[names.length - 1];
  const msg = `잘했어요! ${cur.sit.when} ${josa(list, '이', '가')} 필요해요.`;
  $('feedback').textContent = '잘했어요!';
  closeUsage();
  $('next').classList.remove('hidden'); $('next').classList.add('pulse');
  speak(msg);
}

/* ---------------- usage scene (how the object is used) ---------------- */
let usageTimer = 0;
function showUsage(id) {
  closeUsage();
  const d = document.createElement('div');
  d.className = 'usage'; d.id = 'usage';
  d.innerHTML = `<img src="${usageImg(id)}" alt="${OBJ[id].name} 사용 장면"><div class="cap">${OBJ[id].use}</div>`;
  d.onclick = closeUsage;
  window.__lastUsage = id;
  $('scene').appendChild(d);
  clearTimeout(usageTimer);
  usageTimer = setTimeout(closeUsage, 4200);
}
function closeUsage() { clearTimeout(usageTimer); const u = $('usage'); if (u) u.remove(); }

/* ---------------- hints: 1) ask again 2) describe the function 3) highlight ---------------- */
function hint() {
  if (!cur || cur.finished) return;
  const remaining = cur.correct.filter(id => !cur.found.has(id));
  cur.hintLevel = Math.min(cur.hintLevel + 1, 3);
  if (cur.hintLevel === 1) {
    $('feedback').textContent = '그림을 잘 보고 다시 들어 봐요.';
    speakQuestion();
  } else if (cur.hintLevel === 2) {
    const o = OBJ[remaining[0]];
    $('feedback').textContent = o.hint;
    speak(cur.sit.when + ' ' + o.hint);
  } else {
    remaining.forEach(id => { const c = document.querySelector(`.card[data-id="${id}"]`); if (c) c.classList.add('glow'); });
    $('feedback').textContent = '반짝이는 물건을 눌러 봐요.';
    speak('반짝이는 물건을 눌러 봐요.');
  }
}

/* ---------------- learning log (parents only) ---------------- */
function record() {
  const log = load(LOG_KEY, []);
  log.push({ t: Date.now(), sit: cur.sit.id, level: cur.level, variant: cur.variant,
             firstTry: cur.wrongCount === 0, firstPickCorrect: cur.firstPickCorrect,
             wrong: cur.wrongCount, hint: cur.hintLevel, n: cur.correct.length,
             secs: Math.round((Date.now() - cur.startedAt) / 1000) });
  while (log.length > 1000) log.shift();
  save(LOG_KEY, log);
}

function pct(a, b) { return b ? Math.round(a * 100 / b) + '%' : '-'; }
function renderReport() {
  const log = load(LOG_KEY, []);
  const byId = Object.fromEntries(SITS.map(s => [s.id, s]));
  if (!log.length) { $('reportBody').innerHTML = '<p class="note">아직 기록이 없어요. 게임을 한 번 해 보세요.</p>'; return; }
  const rows = SITS.map(s => {
    const r = log.filter(x => x.sit === s.id);
    const first = r.filter(x => x.firstTry).length, hinted = r.filter(x => x.hint > 0).length;
    const wrong = r.reduce((a, x) => a + x.wrong, 0);
    return { s, n: r.length, first, hinted, wrong, rate: r.length ? first / r.length : 1 };
  });
  const weak = rows.filter(r => r.n >= 2 && r.rate < 0.7).sort((a, b) => a.rate - b.rate);
  const lvl = k => (LEVELS[k] || {}).label || k;
  const recent = log.slice(-15).reverse();
  const fmt = t => { const d = new Date(t); return `${d.getMonth() + 1}/${d.getDate()} ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`; };
  $('reportBody').innerHTML = `
    <h3>상황별 결과</h3>
    <table><tr><th>상황</th><th>푼 횟수</th><th>한 번에 맞힘</th><th>힌트 사용</th><th>틀린 선택(합계)</th></tr>
    ${rows.map(r => `<tr><td>${r.s.title}</td><td>${r.n}</td><td>${pct(r.first, r.n)}</td><td>${pct(r.hinted, r.n)}</td><td>${r.wrong}</td></tr>`).join('')}</table>
    <h3>자주 어려워하는 상황</h3>
    <p class="note">${weak.length ? weak.map(r => `${r.s.title} (한 번에 맞힘 ${pct(r.first, r.n)})`).join(', ') : '2번 이상 푼 상황 중 한 번에 맞힌 비율이 70%보다 낮은 상황이 없어요.'}</p>
    <h3>최근 기록</h3>
    <table><tr><th>시간</th><th>상황</th><th>난이도</th><th>한 번에 맞힘</th><th>틀린 선택</th><th>힌트</th></tr>
    ${recent.map(x => `<tr><td>${fmt(x.t)}</td><td>${(byId[x.sit] || {}).title || x.sit}</td><td>${lvl(x.level)}</td><td>${x.firstTry ? 'O' : 'X'}</td><td>${x.wrong}</td><td>${x.hint ? x.hint + '단계' : '-'}</td></tr>`).join('')}</table>
    <p class="note">「한 번에 맞힘」은 틀린 물건을 하나도 고르지 않고 필요한 물건을 모두 찾은 경우예요. 힌트 1단계: 질문 다시 듣기, 2단계: 쓰임 설명 듣기, 3단계: 정답 물건 반짝임.</p>`;
}
function openReport() { renderReport(); $('toggleNames').textContent = prefs.names ? '물건 이름 숨기기' : '물건 이름 보이기'; $('report').classList.remove('hidden'); }

/* ---------------- wiring ---------------- */
function applyNames() { document.body.classList.toggle('noNames', !prefs.names); }
$('go').onclick = () => { unlockSpeech(); startRound(); };
$('again').onclick = startRound;
$('home').onclick = $('home2').onclick = () => { speakToken++; try { speechSynthesis.cancel(); } catch (e) {} show('start'); };
$('speak').onclick = speakQuestion;
$('hint').onclick = hint;
$('next').onclick = () => { qi++; if (qi >= queue.length) { show('done'); speak('모두 찾았어요! 정말 잘했어요!'); } else newQuestion(); };
$('openReport1').onclick = $('openReport2').onclick = openReport;
$('closeReport').onclick = () => $('report').classList.add('hidden');
$('clearLog').onclick = () => { if (confirm('학습 기록을 모두 지울까요?')) { save(LOG_KEY, []); renderReport(); } };
$('toggleNames').onclick = () => { prefs.names = !prefs.names; savePrefs(); applyNames(); $('toggleNames').textContent = prefs.names ? '물건 이름 숨기기' : '물건 이름 보이기'; };
window.addEventListener('error', () => { /* keep the game alive */ });
renderLevels(); applyNames(); show('start');
window.__game = { get cur() { return cur; }, LOG_KEY };
})();
