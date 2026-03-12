---
name: bible-verse-getter
description: Fetch Korean Bible verses from rv.or.kr. Use when user requests specific Bible verses (e.g., "John 3:16") or asks to search/get Bible verses.
allowed-tools: Bash, Read
---

# Bible Verse Getter

이 스킬은 한국어 회복역 성경 구절을 rv.or.kr에서 가져옵니다.

## 사용 시점

다음과 같은 경우에 이 스킬을 사용하세요:
- 사용자가 특정 성경 구절을 요청할 때 (예: "요한복음 3:16", "John 3:16")
- 성경 구절 검색이 필요할 때
- 번역 작업에서 정확한 한국어 성경 구절이 필요할 때

## 사용법

스크립트 실행 명령:
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/get_verse.py --book "<Book Name>" --chapter <Chapter> --verse <Verse(s)>
```

### 매개변수
- `--book`: 영어 책 이름 (예: "Genesis", "Matthew", "Revelation"). 대소문자 구분 없음
- `--chapter`: 장 번호 (정수)
- `--verse`: (선택사항) 절 번호 또는 범위:
  - 단일 절: "16"
  - 범위: "1-5"
  - 여러 절: "1,3,5"

### 예제

```bash
# 요한복음 3:16
python3 ${CLAUDE_SKILL_DIR}/scripts/get_verse.py --book "John" --chapter 3 --verse 16

# 창세기 1:1-3
python3 ${CLAUDE_SKILL_DIR}/scripts/get_verse.py --book "Genesis" --chapter 1 --verse 1-3

# 마태복음 5장 3,5,7절
python3 ${CLAUDE_SKILL_DIR}/scripts/get_verse.py --book "Matthew" --chapter 5 --verse 3,5,7
```

## 지원 성경 책

### 구약 (Old Testament)
Genesis, Exodus, Leviticus, Numbers, Deuteronomy, Joshua, Judges, Ruth,
1 Samuel, 2 Samuel, 1 Kings, 2 Kings, 1 Chronicles, 2 Chronicles,
Ezra, Nehemiah, Esther, Job, Psalms, Proverbs, Ecclesiastes, Song of Songs,
Isaiah, Jeremiah, Lamentations, Ezekiel, Daniel, Hosea, Joel, Amos,
Obadiah, Jonah, Micah, Nahum, Habakkuk, Zephaniah, Haggai, Zechariah, Malachi

### 신약 (New Testament)
Matthew, Mark, Luke, John, Acts, Romans, 1 Corinthians, 2 Corinthians,
Galatians, Ephesians, Philippians, Colossians, 1 Thessalonians, 2 Thessalonians,
1 Timothy, 2 Timothy, Titus, Philemon, Hebrews, James, 1 Peter, 2 Peter,
1 John, 2 John, 3 John, Jude, Revelation

## 출력

요청한 구절의 한국어 텍스트를 표준 출력으로 반환합니다.
각 절은 번호와 함께 별도 줄로 출력됩니다.