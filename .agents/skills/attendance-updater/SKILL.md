---
name: attendance-updater
description: Read LA Church attendance data from Google Sheet and update the newsletter Google Doc. Use when user says "출석 업데이트", "인수 통계 업데이트", or "update attendance".
---

# Attendance Updater (인수 통계 업데이트)

이 스킬은 엘에이 교회 출석 통계를 Google Sheet에서 읽어 소식지 Google Doc에 업데이트합니다.

Codex에서 `scripts/` 경로는 이 `SKILL.md`가 있는 스킬 디렉터리를 기준으로 확인합니다.

## 날짜 범위 규칙

- "한 주"는 **월요일 ~ 일요일**을 의미합니다.
- "한 주 전"은 오늘이 속한 주의 바로 이전 주입니다.
- 예시: 오늘이 2026년 3월 13일(금)이면, 오늘이 속한 주는 3/9(월)~3/15(일)이므로, 한 주 전은 **3/2(월) ~ 3/8(일)**입니다.
- 예시: 오늘이 2026년 3월 9일(월)이면, 오늘이 속한 주는 3/9(월)~3/15(일)이므로, 한 주 전은 **3/2(월) ~ 3/8(일)**입니다.
- 예시: 오늘이 2026년 3월 8일(일)이면, 오늘이 속한 주는 3/2(월)~3/8(일)이므로, 한 주 전은 **2/23(월) ~ 3/1(일)**입니다.

## Workflow (반드시 이 순서대로 실행하고, 각 단계에서 자동 검증)

### Step 1: Sheet에서 데이터 읽기 + 검증

```bash
python3 scripts/update_attendance.py --read-only
```

실행 후 **직접 검증**:
- 날짜 범위가 위 규칙에 따라 올바른지 확인
- 합계 테이블의 기도/소그룹/주일/신언 수치가 출력되었는지 확인
- 소그룹 인수에서 빈 값이 "미집계"로 표시되는지 확인
- 값이 비정상적이지 않은지 (예: 전체 합계가 하위 합계보다 작다거나) 확인

문제가 있으면 사용자에게 알리고 중단. 문제가 없으면 다음 단계 진행.

### Step 2: Dry Run으로 변경사항 검증

```bash
python3 scripts/update_attendance.py --dry-run
```

실행 후 **직접 검증**:
- Step 1에서 읽은 수치와 dry run에서 삽입하려는 값이 일치하는지 대조
- 날짜 범위 텍스트가 올바르게 생성되었는지 확인
- 모든 테이블 셀에 대한 update request가 존재하는지 확인

문제가 있으면 사용자에게 알리고 중단. 문제가 없으면 다음 단계 진행.

### Step 3: 실제 업데이트 실행

```bash
python3 scripts/update_attendance.py
```

## 주의사항

- Google Workspace CLI (`gws`)가 설치되어 있어야 합니다
- `gws auth login -s sheets,docs,drive`로 인증이 완료되어야 합니다
- **3단계 워크플로우를 반드시 따르세요. 검증 없이 다음 단계로 넘어가면 안 됩니다.**
