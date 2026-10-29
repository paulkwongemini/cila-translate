---
name: translator
description: Translate the repo-root prayer.pdf church document from English to Korean with accurate Bible verse references. Use when user says "번역해 줘" or requests the weekly prayer PDF translation.
---

# 교회 문서 번역 스킬

영어 교회 문서를 한국어로 번역합니다. 성경 구절은 정확한 한국어 회복역을 사용합니다. 초안 작성 후 한국어 퇴고와 원문 재대조를 거친 최종본을 제공합니다.

Codex에서 `resources/`와 `scripts/` 경로는 이 `SKILL.md`가 있는 스킬 디렉터리를 기준으로 확인합니다.

## 사용 시점

다음과 같은 경우에 이 스킬을 사용하세요:
- 사용자가 "번역해 줘"라고 요청할 때
- Repo 루트의 `prayer.pdf` 영문 교회 문서 번역이 필요할 때
- 성경 구절 참조가 포함된 문서를 번역할 때

## 번역 프로세스

### 1단계: `prayer.pdf` 입력 파일 읽기

Repo 루트의 `prayer.pdf`를 유일한 원문으로 사용합니다. 날짜나 다른 태그를 파일명에 붙이지 않습니다. `input.html`은 사용하지 않습니다.

1. `pdf` 스킬을 사용하여 PDF 정보와 페이지 수를 확인합니다.
2. `pdftotext -layout`으로 전체 텍스트를 추출합니다.
3. `pdftoppm`으로 모든 페이지를 이미지로 렌더링하고, 추출된 텍스트를 각 페이지 원본과 대조합니다.
4. 텍스트 레이어가 없거나 추출 결과가 불완전한 스캔 PDF이면 OCR 또는 렌더링된 페이지의 시각 판독으로 원문을 복원합니다.
5. 합자(`fi`, `ff` 등), 특수문자, 불릿, 줄바꿈, 제목, 날짜, 링크가 추출 과정에서 누락되거나 깨진 경우 렌더링된 페이지를 기준으로 복원합니다.
6. PDF에 포함된 하이퍼링크는 가능한 경우 PDF 주석/링크 메타데이터에서 실제 URL을 확인하여 결과에 유지합니다.

```bash
# PDF 정보와 텍스트 확인
pdfinfo prayer.pdf
pdftotext -layout prayer.pdf -

# 전체 페이지 렌더링 후 시각적으로 대조
mkdir -p tmp/pdfs
pdftoppm -png -r 150 prayer.pdf tmp/pdfs/translator-input
```

### 2단계: 성경 구절 식별 및 가져오기

문서를 스캔하여 모든 성경 구절 참조를 찾습니다 (예: "John 3:16", "Matt. 5:3-5").

각 참조에 대해:
1. 책, 장, 절 정보를 파악합니다
2. `bible-verse-getter` 스킬을 사용하여 정확한 한국어 텍스트를 가져옵니다
3. **중요**: 절대 추측하거나 역번역하지 마세요. 반드시 정확한 텍스트를 가져와야 합니다

### 3단계: 용어집 및 예시 참고

#### 3-A. 용어집

`resources/WORDS.csv`를 읽어 전문 용어 번역에 참고합니다:

주요 용어 예시:
- the Spirit → 그 영
- constitute → 조성
- redeem the time → 시간을 구속하다
- life study → 라이프스타디
- Young people → 영피플
- serving ones → 봉사자들
- blending → 섞임

#### 3-B. 과거 번역 예시 (반드시 참고)

`resources/examples.md`는 사람이 검토·완성한 영-한 페어링 모음입니다(2026년 3월 15일~9월 6일 주간 기도문 146개 섹션). 번역 전에 반드시 읽고, 다음을 학습 자료로 활용하세요:

- **어체와 톤**: 문장 리듬과 어휘를 참고하되, 어미는 4단계의 문장 유형별 기준을 따릅니다
- **반복 주제의 정착된 표현**: 이탈리아 복음/목양 여행, TSUF, 집회 안내(특별 집회·수련회·연합 집회), BfA, FTTA/ITERO 등
- **고유명사 표기**: 도시명·기관명·캠페인명의 한글 표기
- **기도 항목 어미 패턴**: 불릿 항목이 `~도록.`으로 끝나는 방식
- **성경 구절 도입부 문체**: 인용 표시와 출처 표기 형식

번역하려는 본문과 유사한 주제의 페어를 우선적으로 참고하면 일관성이 유지됩니다.

#### 3-C. 승인된 퇴고 사례

[resources/revision-examples.md](resources/revision-examples.md)를 읽고, 영어 원문 → 초안 → 승인된 수정본 → 수정 이유를 비교합니다. 표현을 일괄 치환하는 규칙이 아니라, 문장 구조와 문맥을 판단하는 기준으로 활용합니다. 이 파일은 `examples.md`와 별도로 관리하며, 아카이브 재생성 시에도 유지합니다.

### 4단계: 번역 수행

#### 번역 원칙:
- **어체**: 정중하고 겸손한 영적인 어조 (지방교회/주의 회복에서 사용하는 기도문 어투)
- **성경 구절**: 2단계에서 가져온 정확한 한국어 텍스트 삽입
- **구조**: 영어와 한국어 섹션을 교대로 배치
  - 각 주제별로 영어 섹션 전체 → 한국어 번역 전체 순서로 배치
  - 단락별 교차 배치 금지

#### 문장 유형별 어체:

| 문장 유형 | 기준 |
| --- | --- |
| 성경 인용 | 2단계에서 확인한 회복역 본문의 어미와 표현을 그대로 유지합니다. |
| 사역 인용(라이프스타디·전집·훈련 개요 등) | 평서형(`-이다`, `-한다`)을 사용합니다. 확인된 한국어 인용문이 있으면 그 문체를 보존합니다. |
| 집회 안내·설명·일반 기도 요청 | 정중형(`-입니다`, `-합니다`, `-습니다`)을 사용합니다. |
| 불릿 기도 항목 | `~도록.`으로 끝냅니다. |

사용자가 문체를 지정하면 그 지정을 우선합니다.

#### 지방교회 기도문 스타일 가이드:

**문맥**: 이 문서는 주의 회복(Lord's Recovery) 안에 있는 지방교회들의 주간 기도 게시물입니다.
위트니스 리(Witness Lee)와 워치만 니(Watchman Nee)의 사역에서 사용되는 한국어 번역 관례를 따릅니다.

**일반 문장으로 된 기도 요청**:
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

### 5단계: 한국어 퇴고 및 원문 재대조

초안을 완성한 뒤 모든 한국어 섹션을 다시 읽고, 실제 주간 기도문에 실을 문장으로 다듬습니다. 사용자의 별도 검토 요청을 기다리지 않고 이 과정을 수행합니다.

#### 5-A. 한국어 문장 검토

- 먼저 한국어만 읽어도 누가 무엇을 하는지, 수식어가 무엇을 가리키는지 바로 이해되도록 주어와 서술어를 정리합니다.
- 일정·대상·장소·마감일이 한 문장에 겹쳐 읽기 어려우면 문장이나 문단을 나누고, 각 정보의 대응 관계를 유지합니다.
- 문맥상 대상이 분명한 반복 주어와 소유격은 간결하게 다듬습니다. 의미 구별이나 강조에 필요한 반복은 유지합니다.
- 영어의 어순과 전치사 표현은 문맥에 맞는 한국어로 옮깁니다. 등록 상태와 시작 시점처럼 원문이 구별하는 의미를 살립니다.
- 교회 용어와 4단계의 문체 기준을 유지하면서 조사와 연결 어미를 자연스럽게 다듬습니다.
- 이미 정확하고 자연스러운 문장은 유지합니다. 수정 이유는 구체적인 의미·문법·가독성 문제로 설명할 수 있어야 합니다.

#### 5-B. 원문 재대조

- 다듬은 번역을 영어 원문과 대조하여 행위의 주체·대상, 시제, 목적, 강조, 포함 관계와 신학적 의미를 보존했는지 확인합니다.
- 날짜·장소·인원·등록 마감일이 정확히 대응하는지, 본문과 기도 항목에 누락이나 원문에 없는 내용이 생기지 않았는지 확인합니다.
- 성경 인용은 확인한 회복역 본문과 대조하고, 인용 출처·구절 참조·링크를 유지합니다.
- 의미가 달라진 부분은 바로잡고 해당 문장을 다시 확인합니다. 확인을 마친 문장이 최종본입니다.

### 6단계: 형식 지정

#### 표준 형식:
- **날짜 제목**: Google Docs의 `Title` 스타일을 목표로 합니다. Markdown에서는 첫 줄에 `**YYYY년 M월 D일 주간 기도문**`을 독립된 문단으로 쓰고, 앞에 `#`을 붙이지 않습니다.
- **섹션 헤더**: 영어·한국어의 모든 기도 섹션 제목은 `##### **섹션 제목**` 형식으로 씁니다. Google Docs의 “Paste from Markdown”에서 `Heading 5`(h5)가 되도록 해시 기호 다섯 개와 공백을 사용합니다.
- **Announcements 섹션**: 제거
- **날짜 규칙**: 항상 일요일 날짜를 사용. 대부분의 경우, 화요일에 작업을 하는데 바로 직전 일요일 날짜를 사용 (예: 오늘이 3월 10일 화요일이라면 제목은 3월 8일 주간 기도문)

#### Google Docs 붙여넣기:

Google Docs의 “Paste from Markdown”은 `#`부터 `######`까지를 `Heading 1`부터 `Heading 6`으로 변환합니다. 별도의 `Title` 스타일을 지정하는 Markdown 문법은 지원하지 않습니다.

- Markdown 파일을 전달할 때는 날짜 줄을 선택하고 **서식 → 단락 스타일 → Title → 적용**으로 설정해야 한다는 점을 완료 안내에 짧게 알립니다. 이 안내는 기도문 본문에 넣지 않습니다.
- 사용자가 Google Docs에 직접 작성하거나 편집하도록 요청한 경우에는 날짜 문단에 `Title`을, 각 섹션 제목에 `Heading 5`를 적용하고 실제 스타일을 확인합니다.

참고: [Google Docs Markdown 안내](https://support.google.com/docs/answer/12014036?hl=en), [Title·Heading 스타일 적용 안내](https://support.google.com/docs/answer/116338?hl=en).

### 7단계: 결과 저장

5단계의 검토와 6단계의 형식 지정을 마친 최종본을 `translated.md`에 저장합니다. 영어 섹션의 원문을 유지하고, 한국어 섹션에는 퇴고를 반영합니다.

## 사용 예제

사용자가 "번역해 줘"라고 요청하면:

1. Repo 루트의 `prayer.pdf`를 텍스트로 추출하고 (혹은 사용자가 직접 전달한 원문 사용) 모든 페이지 렌더링과 대조하기
2. 성경 구절 참조 찾기 (예: "John 3:16")
3. `bible-verse-getter`로 John 3:16 한국어 구절 가져오기
4. 용어집(WORDS.csv), 과거 번역(examples.md), 승인된 퇴고 사례(revision-examples.md)를 참고하여 초안 작성
5. 모든 한국어 섹션을 퇴고하고 원문과 재대조하여 수정 반영
6. `Announcements` 섹션을 제거하고 형식을 지정한 최종본을 `translated.md`에 저장

## 참고 파일
- 용어집: `resources/WORDS.csv`
- 영-한 번역 예시: `resources/examples.md`
- 승인된 퇴고 사례: [resources/revision-examples.md](resources/revision-examples.md)
- 입력: Repo 루트의 `prayer.pdf`
- 출력: `translated.md`

## 예시 재생성

`examples.md`는 2026 기도문 아카이브 Google Doc에서 자동 추출됩니다. `gws`는 사용하지 않습니다.

아카이브 URL: `https://docs.google.com/document/d/1cGD3pPm6FoiFWqL42pDkzu_QLz0UFvKgCqFoT60OGko`

아카이브에 새 페어가 추가되면 Codex의 Google Drive 플러그인으로 해당 Google Doc을 `text/markdown` 형식으로 export/fetch하고, 반환된 `download_url`의 Markdown 파일을 임시 경로에 내려받은 뒤 다음 명령으로 갱신합니다:

```bash
python3 scripts/extract_pairs.py /tmp/translator-archive.md > resources/examples.md
```
