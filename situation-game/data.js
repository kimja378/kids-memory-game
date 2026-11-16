/* 상황에 필요한 물건 찾기 — 문제 데이터
 *
 * 새 물건 추가: OBJECTS 에 항목을 넣고 assets/objects/<id>.svg (선택지 그림)와
 *   assets/usage/<usage 또는 id>.svg (맞혔을 때 보여 줄 사용 장면)를 준비합니다.
 *   사용 장면 그림이 없으면 usage: false 로 두면 물건 그림이 움직이며 나와요.
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
  /* ---- 2차 추가 물건 (usage: false → 사용 장면 대신 물건 그림이 움직여요) ---- */
  book: { name: "책", use: "책을 펴서 읽어요.", when: "공부하거나 책을 읽을 때 써요.", hint: "글자와 그림이 있는, 펼쳐서 읽는 것이 있어요.", usage: false },
  pencil: { name: "연필", use: "연필로 글씨를 써요.", when: "글씨를 쓸 때 써요.", hint: "글씨를 쓰는 끝이 뾰족한 것이 있어요.", usage: false },
  eraser: { name: "지우개", use: "틀린 글씨는 지우개로 지워요.", when: "글씨를 지울 때 써요.", hint: "틀린 글씨를 쓱쓱 지우는 것이 있어요.", usage: false },
  mat: { name: "돗자리", use: "돗자리를 펴고 앉아요.", when: "밖에서 앉을 때 바닥에 깔아요.", hint: "풀밭에 펴고 앉는 것이 있어요.", usage: false },
  lunchbox: { name: "도시락", use: "도시락을 열어 맛있게 먹어요.", when: "밖에서 밥을 먹을 때 싸 가요.", hint: "밥과 반찬을 담아 가는 통이 있어요.", usage: false },
  water_bottle: { name: "물병", use: "목마르면 물병의 물을 마셔요.", when: "물을 담아 다닐 때 써요.", hint: "마실 물을 담아 가는 것이 있어요.", usage: false },
  soap: { name: "비누", use: "비누로 몸을 깨끗이 씻어요.", when: "몸이나 손을 씻을 때 써요.", hint: "문지르면 거품이 나는 것이 있어요.", usage: false },
  shampoo: { name: "샴푸", use: "샴푸로 머리를 감아요.", when: "머리를 감을 때 써요.", hint: "머리카락을 감을 때 쓰는 거품이 있어요.", usage: false },
  towel: { name: "수건", use: "수건으로 물기를 닦아요.", when: "씻고 나서 물기를 닦을 때 써요.", hint: "젖은 몸을 닦는 보송보송한 천이 있어요.", usage: false },
  umbrella: { name: "우산", use: "우산을 쓰면 비를 맞지 않아요.", when: "비가 올 때 써요.", hint: "머리 위로 펼쳐서 비를 막는 것이 있어요.", usage: false },
  rain_boots: { name: "장화", use: "장화를 신으면 물웅덩이도 괜찮아요.", when: "비가 올 때 신어요.", hint: "물웅덩이에서도 발이 젖지 않는 신발이 있어요.", usage: false },
  raincoat: { name: "우비", use: "우비를 입으면 옷이 젖지 않아요.", when: "비가 올 때 입어요.", hint: "비 오는 날 옷 위에 입는 것이 있어요.", usage: false },
  pot: { name: "냄비", use: "냄비에 국을 보글보글 끓여요.", when: "요리할 때 써요.", hint: "국을 보글보글 끓이는 것이 있어요.", usage: false },
  frying_pan: { name: "프라이팬", use: "프라이팬에 달걀을 부쳐요.", when: "요리할 때 써요.", hint: "달걀을 지글지글 부치는 넓적한 것이 있어요.", usage: false },
  spatula: { name: "뒤집개", use: "뒤집개로 달걀을 휙 뒤집어요.", when: "요리할 때 써요.", hint: "익힌 음식을 휙 뒤집는 것이 있어요.", usage: false },
  crayons: { name: "크레파스", use: "크레파스로 알록달록 색칠해요.", when: "그림을 그릴 때 써요.", hint: "여러 가지 색으로 칠하는 것이 있어요.", usage: false },
  sketchbook: { name: "스케치북", use: "스케치북에 그림을 그려요.", when: "그림을 그릴 때 써요.", hint: "그림을 그리는 하얀 종이 묶음이 있어요.", usage: false },
  paint: { name: "물감", use: "붓에 물감을 묻혀 칠해요.", when: "그림을 그릴 때 써요.", hint: "붓에 묻혀 칠하는 알록달록한 것이 있어요.", usage: false },
  winter_hat: { name: "털모자", use: "털모자를 쓰면 머리가 따뜻해요.", when: "추운 날 써요.", hint: "머리를 따뜻하게 감싸는 모자가 있어요.", usage: false },
  mittens: { name: "장갑", use: "장갑을 끼면 손이 따뜻해요.", when: "추운 날 손에 껴요.", hint: "손을 따뜻하게 감싸는 것이 있어요.", usage: false },
  scarf: { name: "목도리", use: "목도리를 두르면 목이 따뜻해요.", when: "추운 날 목에 둘러요.", hint: "목에 두르는 길고 따뜻한 것이 있어요.", usage: false },
  padded_jacket: { name: "패딩", use: "두꺼운 패딩을 입으면 따뜻해요.", when: "추운 날 입어요.", hint: "푹신하고 두꺼운 겉옷이 있어요.", usage: false },
  swim_ring: { name: "튜브", use: "튜브를 끼면 물에 둥둥 떠요.", when: "물놀이할 때 써요.", hint: "물에 둥둥 뜨게 해 주는 동그란 것이 있어요.", usage: false },
  sand_bucket: { name: "모래 놀이 세트", use: "양동이와 삽으로 모래성을 쌓아요.", when: "모래 놀이를 할 때 써요.", hint: "모래를 퍼 담는 양동이와 삽이 있어요.", usage: false },
  swimsuit: { name: "수영복", use: "수영복으로 갈아입고 물놀이해요.", when: "물놀이할 때 입어요.", hint: "물에 들어갈 때 입는 옷이 있어요.", usage: false },
  cart: { name: "카트", use: "카트에 살 물건을 담아요.", when: "장을 볼 때 써요.", hint: "물건을 담아 미는, 바퀴 달린 것이 있어요.", usage: false },
  shopping_bag: { name: "장바구니", use: "장바구니에 산 물건을 넣어 와요.", when: "장을 볼 때 써요.", hint: "산 물건을 담아 들고 오는 가방이 있어요.", usage: false },
  wallet: { name: "지갑", use: "지갑에서 돈을 꺼내 계산해요.", when: "물건을 살 때 써요.", hint: "돈을 넣어 다니는 것이 있어요.", usage: false },
  backpack: { name: "가방", use: "가방에 준비물을 넣고 메요.", when: "외출할 때 메요.", hint: "준비물을 넣어 등에 메는 것이 있어요.", usage: false },
  sneakers: { name: "운동화", use: "운동화를 신고 씩씩하게 걸어요.", when: "밖에 나갈 때 신어요.", hint: "밖에 나갈 때 발에 신는 것이 있어요.", usage: false },
  comb: { name: "빗", use: "빗으로 머리를 가지런히 빗어요.", when: "머리를 빗을 때 써요.", hint: "머리카락을 가지런히 하는, 살이 많은 것이 있어요.", usage: false },
  mirror: { name: "거울", use: "거울에 내 모습을 비춰 봐요.", when: "내 모습을 볼 때 써요.", hint: "내 얼굴이 비치는 것이 있어요.", usage: false },
  hair_dryer: { name: "드라이기", use: "드라이기로 머리를 말려요.", when: "젖은 머리를 말릴 때 써요.", hint: "따뜻한 바람이 나오는 것이 있어요.", usage: false },
  scissors: { name: "가위", use: "가위로 머리카락을 싹둑 잘라요.", when: "무언가를 자를 때 써요.", hint: "싹둑싹둑 자르는 것이 있어요.", usage: false },
  watering_can: { name: "물뿌리개", use: "물뿌리개로 물을 줘요.", when: "식물에 물을 줄 때 써요.", hint: "식물에 물을 솔솔 뿌려 주는 것이 있어요.", usage: false },
  trowel: { name: "모종삽", use: "모종삽으로 흙을 파요.", when: "흙을 팔 때 써요.", hint: "흙을 퍼내는 작은 삽이 있어요.", usage: false },
  flower_pot: { name: "화분", use: "화분에 씨앗을 심어요.", when: "식물을 심을 때 써요.", hint: "흙을 담아 식물을 키우는 통이 있어요.", usage: false },
  washing_machine: { name: "세탁기", use: "세탁기가 빙글빙글 옷을 빨아요.", when: "빨래할 때 써요.", hint: "옷을 넣으면 빙글빙글 돌며 빨아 주는 것이 있어요.", usage: false },
  detergent: { name: "세제", use: "세제를 넣어 옷을 깨끗하게 빨아요.", when: "빨래할 때 써요.", hint: "빨래할 때 넣는 거품 나는 것이 있어요.", usage: false },
  drying_rack: { name: "빨래 건조대", use: "빨래 건조대에 젖은 옷을 널어 말려요.", when: "빨래를 말릴 때 써요.", hint: "젖은 옷을 걸어 말리는 것이 있어요.", usage: false },
  tent: { name: "텐트", use: "텐트를 치고 그 안에서 자요.", when: "캠핑할 때 써요.", hint: "밖에서 잠잘 수 있는 작은 집이 있어요.", usage: false },
  flashlight: { name: "손전등", use: "깜깜할 때 손전등을 켜요.", when: "어두울 때 써요.", hint: "어두운 곳을 환하게 비추는 것이 있어요.", usage: false },
  sleeping_bag: { name: "침낭", use: "침낭 속에 쏙 들어가 자요.", when: "밖에서 잘 때 써요.", hint: "쏙 들어가서 자는 포근한 주머니가 있어요.", usage: false },
  baby_bottle: { name: "젖병", use: "젖병으로 아기에게 우유를 줘요.", when: "아기가 우유를 먹을 때 써요.", hint: "아기가 쪽쪽 우유를 먹는 병이 있어요.", usage: false },
  diaper: { name: "기저귀", use: "젖은 기저귀를 새것으로 갈아 줘요.", when: "아기에게 채워 줘요.", hint: "아기 엉덩이에 채우는 것이 있어요.", usage: false },
  pacifier: { name: "쪽쪽이", use: "쪽쪽이를 물면 아기가 울음을 그쳐요.", when: "아기가 입에 물어요.", hint: "아기 입에 쏙 물려 주는 것이 있어요.", usage: false },
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
  {
    id: 'study', when: '공부할 때는', title: '공부하기', scenes: 2,
    story: '의자에 앉았어요. 이제 공부를 시작할 거예요.',
    correct: ['book', 'pencil', 'eraser'],
    accept: ['crayons', 'sketchbook', 'backpack'],
    distractors: ['frying_pan', 'swim_ring', 'pillow', 'broom', 'shampoo', 'rain_boots', 'tent'],
  },
  {
    id: 'picnic', when: '소풍 갈 때는', title: '소풍 가기', scenes: 2,
    story: '날씨가 좋아요. 가족과 공원으로 소풍을 왔어요.',
    correct: ['mat', 'lunchbox', 'water_bottle'],
    accept: ['backpack', 'cup', 'plate', 'spoon', 'chopsticks', 'sneakers'],
    distractors: ['vacuum', 'frying_pan', 'washing_machine', 'shampoo', 'toothbrush', 'bed', 'detergent'],
  },
  {
    id: 'bath', when: '목욕할 때는', title: '목욕하기', scenes: 2,
    story: '몸이 더러워졌어요. 욕조에 따뜻한 물을 받았어요.',
    correct: ['soap', 'shampoo', 'towel'],
    accept: [],
    distractors: ['pencil', 'frying_pan', 'cart', 'tent', 'crayons', 'umbrella', 'wallet'],
  },
  {
    id: 'rain', when: '비 오는 날 나갈 때는', title: '비 오는 날', scenes: 2,
    story: '밖에 비가 주룩주룩 와요. 그래도 밖에 나가야 해요.',
    correct: ['umbrella', 'rain_boots', 'raincoat'],
    accept: ['sneakers', 'backpack'],
    distractors: ['swim_ring', 'frying_pan', 'pillow', 'crayons', 'shampoo', 'sleeping_bag', 'sand_bucket'],
  },
  {
    id: 'cooking', when: '요리할 때는', title: '요리하기', scenes: 2,
    story: '엄마가 맛있는 요리를 하려고 해요.',
    correct: ['pot', 'frying_pan', 'spatula'],
    accept: ['plate', 'spoon', 'chopsticks', 'cup'],
    distractors: ['broom', 'pencil', 'rain_boots', 'comb', 'swim_ring', 'tent', 'crayons'],
  },
  {
    id: 'drawing', when: '그림을 그릴 때는', title: '그림 그리기', scenes: 2,
    story: '그림을 그리고 싶어요. 무엇을 그릴까요?',
    correct: ['crayons', 'sketchbook', 'paint'],
    accept: ['pencil', 'eraser', 'book'],
    distractors: ['frying_pan', 'pillow', 'toothbrush', 'wallet', 'shampoo', 'broom', 'rain_boots'],
  },
  {
    id: 'cold', when: '추운 날 나갈 때는', title: '추운 날 외출', scenes: 2,
    story: '밖에 눈이 오고 아주 추워요. 이제 밖에 나가요.',
    correct: ['winter_hat', 'mittens', 'scarf', 'padded_jacket'],
    accept: ['sneakers', 'backpack'],
    distractors: ['swimsuit', 'swim_ring', 'frying_pan', 'pillow', 'toothpaste', 'crayons', 'sand_bucket'],
  },
  {
    id: 'beach', when: '바닷가에서 놀 때는', title: '바닷가 놀이', scenes: 2,
    story: '바닷가에 놀러 왔어요. 바다에서 신나게 놀 거예요.',
    correct: ['swim_ring', 'sand_bucket', 'swimsuit'],
    accept: ['water_bottle', 'mat', 'umbrella', 'towel', 'lunchbox'],
    distractors: ['padded_jacket', 'mittens', 'pencil', 'frying_pan', 'vacuum', 'pillow', 'winter_hat'],
  },
  {
    id: 'shopping', when: '장을 볼 때는', title: '장보기', scenes: 2,
    story: '엄마와 마트에 장을 보러 왔어요.',
    correct: ['cart', 'shopping_bag', 'wallet'],
    accept: ['backpack'],
    distractors: ['pillow', 'toothbrush', 'swim_ring', 'broom', 'sleeping_bag', 'shampoo', 'rain_boots'],
  },
  {
    id: 'daycare', when: '어린이집에 갈 때는', title: '어린이집 가기', scenes: 2,
    story: '아침이 되었어요. 이제 어린이집에 갈 시간이에요.',
    correct: ['backpack', 'sneakers', 'water_bottle'],
    accept: ['lunchbox', 'winter_hat', 'umbrella', 'book', 'crayons'],
    distractors: ['frying_pan', 'vacuum', 'swim_ring', 'washing_machine', 'shampoo', 'detergent', 'tent'],
  },
  {
    id: 'haircut', when: '머리를 자를 때는', title: '미용실 가기', scenes: 2,
    story: '머리카락이 너무 길게 자랐어요. 미용실에 왔어요.',
    correct: ['scissors', 'comb', 'hair_dryer'],
    accept: ['mirror', 'towel'],
    distractors: ['spatula', 'watering_can', 'tent', 'crayons', 'lunchbox', 'frying_pan', 'swim_ring'],
  },
  {
    id: 'planting', when: '씨앗을 심을 때는', title: '씨앗 심기', scenes: 2,
    story: '씨앗을 받았어요. 씨앗을 심어서 키워 볼 거예요.',
    correct: ['trowel', 'watering_can', 'flower_pot'],
    accept: [],
    distractors: ['pillow', 'shampoo', 'frying_pan', 'toothbrush', 'wallet', 'swimsuit', 'comb'],
  },
  {
    id: 'laundry', when: '빨래할 때는', title: '빨래하기', scenes: 2,
    story: '옷이 더러워졌어요. 냄새도 나요. 깨끗하게 빨래해요.',
    correct: ['washing_machine', 'detergent', 'drying_rack'],
    accept: [],
    distractors: ['frying_pan', 'crayons', 'swim_ring', 'toothbrush', 'tent', 'cake', 'pencil'],
  },
  {
    id: 'camping', when: '캠핑할 때는', title: '캠핑', scenes: 2,
    story: '숲으로 캠핑을 왔어요. 밤에 여기서 잘 거예요.',
    correct: ['tent', 'flashlight', 'sleeping_bag'],
    accept: ['mat', 'lunchbox', 'water_bottle', 'pot', 'frying_pan', 'blanket', 'pillow'],
    distractors: ['vacuum', 'washing_machine', 'cart', 'crayons', 'mop', 'party_hat', 'detergent'],
  },
  {
    id: 'baby', when: '아기를 돌볼 때는', title: '아기 돌보기', scenes: 2,
    story: '아기가 앙앙 울고 있어요. 아기를 돌봐 줘요.',
    correct: ['baby_bottle', 'diaper', 'pacifier'],
    accept: ['blanket', 'pillow', 'towel', 'cup'],
    distractors: ['pencil', 'broom', 'tent', 'frying_pan', 'sand_bucket', 'wallet', 'rain_boots'],
  },
];

/* 난이도: 정답 개수 + 오답 개수 */
window.LEVELS = {
  easy:   { label: '쉬움',   correct: 1, wrong: 1 },
  normal: { label: '보통',   correct: 2, wrong: 2 },
  hard:   { label: '어려움', correct: 3, wrong: 3 },
};
