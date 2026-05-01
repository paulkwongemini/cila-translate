---
name: translator
description: Translate English church documents to Korean with accurate Bible verse references. Use when user says "번역해 줘" or requests document translation.
allowed-tools: Read, Write, Edit, Bash, Skill
---

# 교회 문서 번역 스킬

영어 교회 문서를 한국어로 번역합니다. 성경 구절은 정확한 한국어 회복역을 사용합니다.

## 사용 시점

다음과 같은 경우에 이 스킬을 사용하세요:
- 사용자가 "번역해 줘"라고 요청할 때
- `input.html` 또는 다른 교회 문서 번역이 필요할 때
- 성경 구절 참조가 포함된 문서를 번역할 때

## 번역 프로세스

### 1단계: 입력 파일 읽기
```bash
# 기본 입력 파일 읽기
input.html
```

### 2단계: 성경 구절 식별 및 가져오기

문서를 스캔하여 모든 성경 구절 참조를 찾습니다 (예: "John 3:16", "Matt. 5:3-5").

각 참조에 대해:
1. 책, 장, 절 정보를 파악합니다
2. `/bible-verse-getter` 스킬을 사용하여 정확한 한국어 텍스트를 가져옵니다
3. **중요**: 절대 추측하거나 역번역하지 마세요. 반드시 정확한 텍스트를 가져와야 합니다

### 3단계: 용어집 및 예시 참고

#### 3-A. 용어집

`${CLAUDE_SKILL_DIR}/resources/WORDS.csv`를 읽어 전문 용어 번역에 참고합니다:

주요 용어 예시:
- the Spirit → 그 영
- constitute → 조성
- redeem the time → 시간을 구속하다
- life study → 라이프스타디
- Young people → 영피플
- serving ones → 봉사자들
- blending → 섞임

#### 3-B. 과거 번역 예시 (반드시 참고)

`${CLAUDE_SKILL_DIR}/resources/examples.md`는 사람이 검토·완성한 영-한 페어링 모음입니다(2026년 3월~4월 주간 기도문 40개 섹션). 번역 전에 반드시 읽고, 다음을 학습 자료로 활용하세요:

- **어체와 톤**: 라이프스타디 인용은 평서형(`-이다`/`-한다`), 안내·기도 항목은 정중형(`-입니다`/`-합니다`)
- **반복 주제의 정착된 표현**: 이탈리아 복음/목양 여행, TSUF, 집회 안내(특별 집회·수련회·연합 집회), BfA, FTTA/ITERO 등
- **고유명사 표기**: 도시명·기관명·캠페인명의 한글 표기
- **기도 항목 어미 패턴**: 불릿 항목이 `~도록.`으로 끝나는 방식
- **성경 구절 도입부 문체**: 인용 표시와 출처 표기 형식

번역하려는 본문과 유사한 주제의 페어를 우선적으로 참고하면 일관성이 유지됩니다.

### 4단계: 번역 수행

#### 번역 원칙:
- **어체**: 정중하고 겸손한 영적인 어조 (지방교회/주의 회복에서 사용하는 기도문 어투)
- **어미**: `-입니다`, `-합니다`, `-습니다` 사용 (평서형 `-이다`, `-한다` 피하기)
- **성경 구절**: 2단계에서 가져온 정확한 한국어 텍스트 삽입
- **구조**: 영어와 한국어 섹션을 교대로 배치
  - 각 주제별로 영어 섹션 전체 → 한국어 번역 전체 순서로 배치
  - 단락별 교차 배치 금지

#### 지방교회 기도문 스타일 가이드:

**문맥**: 이 문서는 주의 회복(Lord's Recovery) 안에 있는 지방교회들의 주간 기도 게시물입니다.
위트니스 리(Witness Lee)와 워치만 니(Watchman Nee)의 사역에서 사용되는 한국어 번역 관례를 따릅니다.

**기도 항목 어미**:
- 기도 항목은 "~도록 기도합니다" 또는 "~하시기를 바랍니다" 패턴 사용
- 불릿 기도 항목은 "~도록." 으로 끝냄
- "May the Lord..." → "주님께서 ~하시기를 바랍니다"
- "Please pray that..." → "~도록 기도해 주십시오"
- "Please pray for..." → "~를 위해 기도해 주십시오"

**핵심 번역 관례** (용어집 외 추가 규칙):
- "minister" (동사) → "공급하다" (명사 "minister" → "직사")
- "able ministers of the New Testament" → "신약의 유능한 직사들"
- "supply" (명사) → "공급"
- "building up" → "건축"
- "edify/edification" → "건축하다/건축"
- "the good land" → "좋은 땅"
- "all-inclusive Christ" → "모든 것을 포함하시는 그리스도"
- "life-giving Spirit" → "생명 주는 영"
- "Triune God" → "삼일 하나님"
- "presence" → "임재"
- "inner man" → "속사람"
- "organic salvation" → "유기적인 구원"
- "preeminence" → "으뜸"
- "the rule of the heavens" → "하늘의 통치"
- "dispensing" → "분배"
- "economy" (God's economy) → "경륜"
- "consummate/consummation" → "완결/완결하다"
- "seeking ones" → "구도자들"
- "steward" → "청지기"
- "fellowship" (명사) → "교통"
- "function" (기능을 말할 때) → "기능"
- "equip" → "성취하다" 또는 "갖추다"
- "testimony" → "간증" 또는 "증거"
- "the church in [City]" → "[도시]에 있는 교회"
- "local churches" → "지방 교회들"
- "the Body of Christ" → "그리스도의 몸"
- "building material" → "건축 재료"
- "effective" (building material 앞) → "효력 있는"

**서적 제목 번역**:
- *Life-study of [Book]* → "[책] 라이프스타디"
- 책 제목은 이탤릭(*...*) 표기 유지

### 5단계: 형식 지정

#### 표준 형식:
- **날짜 제목**: `# **YYYY년 M월 D일 주간 기도문**`
- **섹션 헤더**: 모든 기도 섹션 제목에 `##` 사용
- **Announcements 섹션**: 제거
- **날짜 규칙**: 항상 일요일 날짜를 사용. 대부분의 경우, 화요일에 작업을 하는데 바로 직전 일요일 날짜를 사용 (예: 오늘이 3월 10일 화요일이라면 제목은 3월 8일 주간 기도문)

### 6단계: 결과 저장

번역된 내용을 `translated.md`에 저장합니다.

## 사용 예제

사용자가 "번역해 줘"라고 요청하면:

1. `input.html` 읽기
2. 성경 구절 참조 찾기 (예: "John 3:16")
3. `/bible-verse-getter John 3 16` 실행하여 한국어 구절 가져오기
4. 용어집(WORDS.csv) 및 예시(examples.md) 참고하여 번역
5. `translated.md`에 저장

## 참고 파일
- 용어집: `${CLAUDE_SKILL_DIR}/resources/WORDS.csv`
- 영-한 번역 예시: `${CLAUDE_SKILL_DIR}/resources/examples.md`
- 입력: `input.html`
- 출력: `translated.md`

## 예시 재생성

`examples.md`는 2026 기도문 아카이브 Google Doc에서 자동 추출됩니다. 아카이브에 새 페어가 추가되면 다음 명령으로 갱신:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/extract_pairs.py > ${CLAUDE_SKILL_DIR}/resources/examples.md
```