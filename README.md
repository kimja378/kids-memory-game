# 📷 사진 기억놀이 (kids-memory-game)

만 4세 아동을 위한 사진 기억놀이 웹앱입니다. 사진 카드 3장을 보고 기억한 뒤, 카드를 뒤집어 어디에 무엇이 있었는지 맞혀 봅니다.

- 배포 주소: https://kimja378.github.io/kids-memory-game/
- 대상 환경: iPad Safari (일반 데스크톱/모바일 브라우저에서도 동작)

## 폴더 구조

```
index.html                     게임 (HTML/CSS/JS 한 파일)
assets/images/catalog.json     사진 ↔ 한글 이름 ↔ 분류 ↔ 출처/라이선스 데이터
assets/images/fruits/          과일 사진       (예: apple.jpg)
assets/images/vegetables/      채소·식재료 사진 (예: carrot.jpg)
assets/images/animals/         동물 사진       (예: giraffe.jpg)
assets/images/vehicles/        탈것 사진       (예: fire_truck.jpg)
CREDITS.md                     사진 출처·저작자·라이선스 표 (catalog.json에서 자동 생성)
tools/validate_images.py       사진 누락·손상 검증 스크립트
tools/*.py                     사진 수집/변환용 개발 도구 (앱 실행에는 사용되지 않음)
tests/game.test.js             Playwright 자동 테스트
photo_01.jpg ~ photo_20.jpg    예전 버전 사진 원본 (보관용, 현재는 assets/images 복사본 사용)
```

- 앱은 **저장소 안의 사진만 상대경로로** 불러옵니다. 외부 이미지 서비스(Unsplash 등)에 의존하지 않습니다.
- 파일명은 영문 소문자와 `_`만 사용합니다.

## 사진 추가/교체 방법

1. 사진을 알맞은 폴더에 `영문소문자.jpg` 로 넣습니다 (긴 변 500px 정도, 200KB 이하 권장).
2. `assets/images/catalog.json` 의 `items` 에 항목을 추가합니다.
   ```json
   {"id": "apple", "name": "사과", "category": "fruit", "file": "assets/images/fruits/apple.jpg",
    "source": {"title": "...", "url": "...", "author": "...", "license": "...", "license_url": "...", "modified": "..."}}
   ```
   `category` 는 `fruit`, `veg`, `animal`, `vehicle` 중 하나입니다.
3. 검증을 실행합니다.
   ```
   python3 tools/validate_images.py --write-credits
   ```
   누락·손상·잘못된 파일명이 있으면 `ERROR` 로 표시되고 종료 코드 1을 돌려줍니다.

같은 이름(예: 토마토)의 사진이 여러 장 있어도 됩니다. 한 문제 안에서는 같은 이름·같은 사진이 겹치지 않게 골라집니다.

## 테스트

```
python3 tools/validate_images.py
node --test tests/game.test.js
```

Playwright(Chromium, iPad 화면 크기·터치 에뮬레이션)로 카테고리별 표시, 사진-이름 일치, 다음 문제 연타, 빠른 카테고리 변경,
뒤집기/모두 보기, 이름 보기/숨기기, 사진 누락·손상 시 동작, 외부 요청 없음 등을 확인합니다.
실제 iPad Safari(WebKit)에서의 테스트는 기기에서 직접 확인해야 합니다.

## 사진 라이선스

새로 추가한 사진은 Wikimedia Commons 에서 자유 라이선스(퍼블릭 도메인, CC0, CC BY, CC BY-SA)로 공개된 사진만 사용했고,
각 사진의 원본 링크·저작자·라이선스를 `CREDITS.md` 와 `catalog.json` 에 기록했습니다.
예전부터 있던 과일·채소 사진 20장은 저장소 소유자가 직접 올린 것으로 원 출처가 기록되어 있지 않습니다.
