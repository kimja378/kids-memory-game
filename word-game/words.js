/* 우리 아이 어휘 탐험대 — 학습 데이터
 *
 * 사진을 넣는 방법
 *   1) 사진을 word-game/photos/ 폴더에 아래 photo 이름 그대로 넣어요. (예: photos/bus.jpg)
 *   2) 게임의 '부모님 설정 → 터치 영역 만들기'에서 사진 위에 손가락으로 네모를 그려 부분 위치를 정해요.
 *      그 기기에 바로 저장되고, '코드 복사'로 나온 값을 아래 shape / zoom 자리에 붙여 넣으면 모든 기기에 적용돼요.
 *   3) 사진 출처는 word-game/photos/CREDITS.md 에 적어요.
 *
 * 좌표는 모두 사진 크기에 대한 비율(0~1)이라 화면 크기와 상관없이 맞아요.
 *   shape: {t:'rect', x, y, w, h} 또는 {t:'ellipse', cx, cy, rx, ry}
 *   zoom : {x, y, w, h}  (비워 두면 shape 주변을 자동으로 크게 보여줘요)
 * shape가 null인 부분은 '터치 영역 준비 중'으로 표시돼요. 사진이 없으면 '사진 필요'로 표시되고, 다른 그림으로 대신하지 않아요.
 *
 * 새 사물을 추가하려면 items 배열에 같은 모양으로 하나 더 넣으면 돼요.
 */
window.WORD_DATA = {
  categories: [
    {id:'vehicle', icon:'🚌', name:'탈것 탐험'},
    {id:'tool',    icon:'🪥', name:'생활도구 탐험'},
    {id:'home',    icon:'🏠', name:'집 안 물건 탐험'},
    {id:'around',  icon:'🎒', name:'주변 물건 탐험'}
  ],
  items: [
    { id:'bus', cat:'vehicle', name:'버스', photo:'photos/bus.jpg',
      intro:'이건 버스야. 많은 사람이 함께 타요.',
      parts: [
        { id:'wheel', name:'바퀴', shape:null, zoom:null,
          findQ:'버스의 바퀴는 어디 있을까요?',
          feature:'바퀴는 동그래요. 데굴데굴 굴러가요.',
          sentence:'버스 바퀴가 굴러가요.' },
        { id:'door', name:'문', shape:null, zoom:null,
          findQ:'버스의 문은 어디 있을까요?',
          feature:'문이 열리고 닫혀요. 문으로 타고 내려요.',
          sentence:'버스 문이 열려요.' }
      ],
      others: [ {id:'window', name:'창문', shape:null} ],
      quizB: { q:'버스의 바퀴는 어떻게 움직일까요?', ok:'굴러가요', wrong:['날아가요','녹아요'],
               yes:'맞아요! 버스 바퀴가 데굴데굴 굴러가요.' },
      quizC: { q:'버스는 무엇을 할 때 타요?', ok:'멀리 갈 때 타요', wrong:['잠을 잘 때 써요','옷을 빨 때 써요'],
               yes:'맞아요! 버스를 타고 멀리 가요.' }
    },
    { id:'helicopter', cat:'vehicle', name:'헬리콥터', photo:'photos/helicopter.jpg',
      intro:'이건 헬리콥터야. 하늘을 날아요.',
      parts: [
        { id:'rotor', name:'날개', shape:null, zoom:null,
          findQ:'헬리콥터의 날개는 어디 있을까요?',
          feature:'날개가 빙글빙글 돌아가요. 그래서 하늘로 올라가요.',
          sentence:'헬리콥터의 날개가 돌아가요.' },
        { id:'tail', name:'꼬리', shape:null, zoom:null,
          findQ:'헬리콥터의 꼬리는 어디 있을까요?',
          feature:'꼬리는 길쭉해요. 꼬리 끝에도 작은 날개가 있어요.',
          sentence:'헬리콥터 꼬리에 작은 날개가 있어요.' }
      ],
      others: [ {id:'window', name:'창문', shape:null} ],
      quizB: { q:'헬리콥터의 날개는 어떻게 움직일까요?', ok:'돌아가요', wrong:['녹아요','굴러가요'],
               yes:'맞아요! 헬리콥터의 날개가 빙글빙글 돌아가요.' },
      quizC: { q:'헬리콥터는 무엇을 할까요?', ok:'하늘을 날아요', wrong:['물속을 헤엄쳐요','옷을 빨아요'],
               yes:'맞아요! 헬리콥터는 날개를 돌려서 하늘을 날아요.' }
    },
    { id:'elevator', cat:'around', name:'엘리베이터', photo:'photos/elevator.jpg',
      intro:'이건 엘리베이터야. 위층과 아래층으로 데려다줘요.',
      parts: [
        { id:'button', name:'버튼', shape:null, zoom:null,
          findQ:'엘리베이터 버튼은 어디 있을까요?',
          feature:'버튼을 꾹 누르면 불이 켜져요.',
          sentence:'엘리베이터 버튼을 눌러요.' },
        { id:'door', name:'문', shape:null, zoom:null,
          findQ:'엘리베이터 문은 어디 있을까요?',
          feature:'문이 스르르 열리고 닫혀요.',
          sentence:'엘리베이터 문이 열려요.' }
      ],
      others: [],
      quizB: { q:'엘리베이터 문은 어떻게 움직일까요?', ok:'열리고 닫혀요', wrong:['굴러가요','빙글빙글 돌아가요'],
               yes:'맞아요! 엘리베이터 문이 스르르 열리고 닫혀요.' },
      quizC: { q:'엘리베이터는 무엇을 할 때 타요?', ok:'위층 아래층에 갈 때 타요', wrong:['하늘을 날 때 타요','머리를 말릴 때 써요'],
               yes:'맞아요! 엘리베이터를 타고 위층 아래층에 가요.' }
    },
    { id:'hairdryer', cat:'tool', name:'드라이기', photo:'photos/hairdryer.jpg',
      intro:'이건 드라이기야. 젖은 머리를 말려요. 뜨거우니까 어른이랑 같이 써요.',
      parts: [
        { id:'handle', name:'손잡이', shape:null, zoom:null,
          findQ:'드라이기의 손잡이는 어디 있을까요?',
          feature:'손잡이를 손으로 꼭 잡아요.',
          sentence:'손으로 드라이기 손잡이를 잡아요.' },
        { id:'nozzle', name:'바람 나오는 곳', shape:null, zoom:null,
          findQ:'드라이기에서 바람 나오는 곳은 어디 있을까요?',
          feature:'여기서 따뜻한 바람이 슝 나와요.',
          sentence:'드라이기에서 바람이 나와요.' }
      ],
      others: [ {id:'cord', name:'전선', shape:null} ],
      quizB: { q:'드라이기에서 무엇이 나올까요?', ok:'따뜻한 바람', wrong:['물','모래'],
               yes:'맞아요! 드라이기에서 따뜻한 바람이 나와요.' },
      quizC: { q:'드라이기는 무엇을 할 때 사용할까요?', ok:'머리를 말려요', wrong:['옷을 빨아요','하늘을 날아요'],
               yes:'맞아요! 드라이기로 젖은 머리를 말려요.' }
    },
    { id:'washer', cat:'home', name:'세탁기', photo:'photos/washer.jpg',
      intro:'이건 세탁기야. 옷을 깨끗하게 빨아요.',
      parts: [
        { id:'door', name:'문', shape:null, zoom:null,
          findQ:'세탁기 문은 어디 있을까요?',
          feature:'문은 동그래요. 문을 열고 옷을 넣어요.',
          sentence:'세탁기 문을 열고 옷을 넣어요.' },
        { id:'button', name:'버튼', shape:null, zoom:null,
          findQ:'세탁기 버튼은 어디 있을까요?',
          feature:'버튼을 누르면 세탁기가 움직여요.',
          sentence:'세탁기 버튼을 눌러요.' }
      ],
      others: [],
      quizB: { q:'세탁기 안에서 옷은 어떻게 움직일까요?', ok:'빙글빙글 돌아가요', wrong:['하늘로 날아가요','녹아요'],
               yes:'맞아요! 세탁기 안에서 옷이 빙글빙글 돌아가요.' },
      quizC: { q:'세탁기는 무엇을 할 때 사용할까요?', ok:'옷을 빨아요', wrong:['머리를 말려요','멀리 갈 때 타요'],
               yes:'맞아요! 세탁기로 옷을 깨끗하게 빨아요.' }
    }
  ],
  /* 틀린 보기를 눌렀을 때 부드럽게 알려주는 말 */
  wordInfo: {
    '날아가요':'날아가는 건 새나 비행기야.', '녹아요':'녹는 건 얼음이나 아이스크림이야.', '굴러가요':'굴러가는 건 공이나 바퀴야.',
    '빙글빙글 돌아가요':'빙글빙글 도는 건 팽이 같은 거야.', '하늘로 날아가요':'하늘로 날아가는 건 새나 비행기야.',
    '잠을 잘 때 써요':'잠은 침대에서 자.', '옷을 빨 때 써요':'옷은 세탁기로 빨아.', '옷을 빨아요':'옷은 세탁기로 빨아.',
    '물속을 헤엄쳐요':'물속에서 헤엄치는 건 물고기야.', '하늘을 날 때 타요':'하늘을 날 때는 비행기나 헬리콥터를 타.',
    '머리를 말릴 때 써요':'머리는 드라이기로 말려.', '머리를 말려요':'머리는 드라이기로 말려.', '하늘을 날아요':'하늘을 나는 건 새나 헬리콥터야.',
    '멀리 갈 때 타요':'멀리 갈 때는 버스나 기차를 타.', '물':'물은 수도꼭지에서 나와.', '모래':'모래는 놀이터 모래밭에 있어.'
  }
};
