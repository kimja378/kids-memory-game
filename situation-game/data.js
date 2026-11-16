/* 상황에 필요한 물건 찾기 — 문제 데이터
 *
 * 새 물건 추가: OBJECTS 에 항목을 넣고 assets/objects/<id>.svg (선택지 그림)와
 *   assets/usage/<usage 또는 id>.svg (맞혔을 때 보여 줄 사용 장면)를 준비합니다.
 *   name  : 물건 이름
 *   use   : 맞혔을 때 들려줄 문장 (물건의 쓰임)
 *   when  : 틀렸을 때 들려줄 문장 (이 물건은 언제 쓰는지)
 *   hint  : 힌트 2단계에서 들려줄 문장 (이름을 말하지 않고 기능만 설명)
 *
 * 새 상황 추가: SITUATIONS 에 항목을 넣고 assets/scenes/<id>-1.svg, -2.svg ... 를 준비합니다.
 *   상황 그림에는 정답 물건을 그리지 않습니다.
 *   when        : '이를 닦을 때는' 처럼 칭찬·힌트 문장에 들어갈 말
 *   correct     : 이 상황에 필요한 물건 (난이도에 따라 1~3개를 골라 냅니다)
 *   accept      : 이 상황에서도 쓸 수 있어서 오답으로 처리하면 안 되는 물건 → 선택지에 아예 나오지 않음
 *   distractors : 이 상황과 분명히 관계없는 물건 (오답 선택지)
 */
window.OBJECTS = {
  toothbrush: { name: '칫솔', use: '칫솔로 이를 닦아요.', when: '이를 닦을 때 써요.', hint: '이에 대고 슥슥 문지르는, 솔이 달린 물건이 있어요.' },
  toothpaste: { name: '치약', use: '치약을 칫솔에 짜서 이를 닦아요.', when: '이를 닦을 때 써요.', hint: '칫솔 위에 쭉 짜서 쓰는 것이 있어요.' },
  cup:        { name: '컵', use: '컵에 물을 담아 입을 헹궈요.', when: '물을 마실 때 써요.', hint: '물을 담아서 입을 헹굴 때 쓰는 것이 있어요.' },
  spoon:      { name: '숟가락', use: '숟가락으로 밥을 떠먹어요.', when: '밥을 먹을 때 써요.', hint: '밥과 국을 떠먹는 것이 있어요.' },
  chopsticks: { name: '젓가락', use: '젓가락으로 반찬을 집어 먹어요.', when: '밥을 먹을 때 써요.', hint: '반찬을 집는 길쭉한 막대 두 개가 있어요.' },
  plate:      { name: '접시', use: '접시에 음식을 담아요.', when: '음식을 담을 때 써요.', hint: '음식을 올려놓는 넓적한 그릇이 있어요.' },
  bed:        { name: '침대', use: '침대에 누워서 쿨쿨 자요.', when: '잠을 잘 때 써요.', hint: '누워서 잠을 자는 곳이 있어요.', usage: 'sleep' },
  blanket:    { name: '이불', use: '이불을 덮고 따뜻하게 자요.', when: '잠을 잘 때 써요.', hint: '몸 위에 덮는 포근한 것이 있어요.', usage: 'sleep' },
  pillow:     { name: '베개', use: '베개를 베고 자요.', when: '잠을 잘 때 써요.', hint: '머리를 올려놓는 푹신한 것이 있어요.', usage: 'sleep' },
  pajamas:    { name: '잠옷', use: '잠옷으로 갈아입고 자요.', when: '잠을 잘 때 입어요.', hint: '잘 때 입는 옷이 있어요.', usage: 'sleep' },
  broom:      { name: '빗자루', use: '빗자루로 바닥을 쓱쓱 쓸어요.', when: '청소할 때 써요.', hint: '바닥의 먼지를 쓱쓱 쓰는 것이 있어요.' },
  dustpan:    { name: '쓰레받기', use: '쓸어 모은 먼지를 쓰레받기에 담아요.', when: '청소할 때 써요.', hint: '쓸어 모은 먼지를 담는 것이 있어요.' },
  vacuum:     { name: '청소기', use: '청소기가 윙 하고 먼지를 빨아들여요.', when: '청소할 때 써요.', hint: '윙 소리를 내며 먼지를 빨아들이는 것이 있어요.' },
  mop:        { name: '밀대', use: '밀대로 바닥을 반짝반짝 닦아요.', when: '청소할 때 써요.', hint: '바닥을 반짝반짝 닦는 것이 있어요.' },
  cake:       { name: '케이크', use: '케이크에 촛불을 켜고 후 불어요.', when: '생일을 축하할 때 먹어요.', hint: '촛불을 꽂는 달콤한 것이 있어요.' },
  party_hat:  { name: '고깔모자', use: '고깔모자를 쓰고 생일을 축하해요.', when: '생일 파티 때 써요.', hint: '머리에 쓰는 뾰족한 모자가 있어요.' },
  gift:       { name: '선물', use: '생일 선물을 열어 봐요.', when: '생일에 주고받아요.', hint: '리본으로 예쁘게 묶은 상자가 있어요.' },
};

window.SITUATIONS = [
  {
    id: 'brushing', when: '이를 닦을 때는', title: '양치하기', scenes: 2,
    story: '밥을 다 먹었어요. 이제 이를 닦을 시간이에요.',
    correct: ['toothbrush', 'toothpaste', 'cup'],
    accept: [],
    distractors: ['pillow', 'broom', 'party_hat', 'cake', 'vacuum', 'gift'],
  },
  {
    id: 'eating', when: '밥을 먹을 때는', title: '밥 먹기', scenes: 2,
    story: '맛있는 밥이 다 됐어요. 이제 밥을 먹을 거예요.',
    correct: ['spoon', 'chopsticks', 'plate'],
    accept: ['cup'],
    distractors: ['pillow', 'broom', 'vacuum', 'pajamas', 'mop', 'party_hat', 'dustpan'],
  },
  {
    id: 'sleeping', when: '잠을 잘 때는', title: '잠자기', scenes: 2,
    story: '깜깜한 밤이 되었어요. 하품이 나와요. 이제 잘 시간이에요.',
    correct: ['bed', 'blanket', 'pillow', 'pajamas'],
    accept: [],
    distractors: ['spoon', 'chopsticks', 'broom', 'vacuum', 'cake', 'plate', 'mop'],
  },
  {
    id: 'cleaning', when: '청소할 때는', title: '청소하기', scenes: 2,
    story: '바닥에 먼지와 부스러기가 가득해요. 깨끗하게 청소해요.',
    correct: ['broom', 'vacuum', 'mop', 'dustpan'],
    accept: [],
    distractors: ['cake', 'pillow', 'spoon', 'toothbrush', 'party_hat', 'pajamas', 'chopsticks'],
  },
  {
    id: 'birthday', when: '생일 파티를 할 때는', title: '생일 파티', scenes: 2,
    story: '오늘은 내 생일이에요. 친구들과 생일 파티를 해요.',
    correct: ['cake', 'party_hat', 'gift'],
    accept: ['plate', 'spoon', 'cup'],
    distractors: ['broom', 'toothbrush', 'pillow', 'vacuum', 'mop', 'toothpaste'],
  },
];

/* 난이도: 정답 개수 + 오답 개수 */
window.LEVELS = {
  easy:   { label: '쉬움',   correct: 1, wrong: 1 },
  normal: { label: '보통',   correct: 2, wrong: 2 },
  hard:   { label: '어려움', correct: 3, wrong: 3 },
};
