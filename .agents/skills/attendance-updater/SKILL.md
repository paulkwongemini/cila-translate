---
name: attendance-updater
description: Use when the user asks for LA Church attendance, 인수 통계, 출석 업데이트, or update attendance in the newsletter Google Doc from the attendance Google Sheet.
---

# Attendance Updater (인수 통계 업데이트)

엘에이 교회 출석 통계를 Google Sheet에서 읽어 소식지 Google Doc의 `인수 통계` 표에 업데이트한다. Google Drive Codex Plugin connector tools를 사용한다. `gws` CLI나 로컬 스크립트는 사용하지 않는다.

## Target Files

- Spreadsheet: `134f4yt7zk0Dvu3d9JOAOvJNJz5JJ_XET52z3G5A98VI`
- Sheet tab: `2025-2026`
- Read range: `A1:GL29`
- Newsletter Doc: `1qa6ZUtqT1vdfIXMFdVwKvkt12PcvtkrLsXplEFdnG7A`

## 날짜 범위 규칙

- "한 주"는 월요일부터 일요일까지다.
- "한 주 전"은 오늘이 속한 주의 바로 이전 월요일-일요일이다.
- 예시: 오늘이 2026년 3월 13일(금)이면 한 주 전은 2026년 3월 2일(월) - 2026년 3월 8일(일)이다.
- 예시: 오늘이 2026년 3월 9일(월)이면 한 주 전은 2026년 3월 2일(월) - 2026년 3월 8일(일)이다.
- 예시: 오늘이 2026년 3월 8일(일)이면 한 주 전은 2026년 2월 23일(월) - 2026년 3월 1일(일)이다.

## Sheet Extraction

Use `mcp__codex_apps__google_drive._get_spreadsheet_metadata` first to confirm the spreadsheet title and tab, then use `mcp__codex_apps__google_drive._get_spreadsheet_range` with:

- `spreadsheet_id`: target spreadsheet id
- `sheet_name`: `2025-2026`
- `range`: `A1:GL29`
- `value_render_option`: `FORMATTED_VALUE`

Find the target week in row 1 (0-based `rows[0]`) by matching:

- start date text: `M/D` for the target Monday
- next cell: `~`
- following cell: `M/D` for the target Sunday

The matched start column is the `기도` column. The next three columns are `소그룹`, `주일`, `신언`.

Summary rows, using 0-based row indexes:

| Sheet label | Row index |
| --- | ---: |
| `1지역 합계` | 9 |
| `2지역 합계` | 20 |
| `홀2 합계` | 25 |
| `한국어 합계` | 27 |

Doc summary label mapping:

| Doc label | Sheet label |
| --- | --- |
| `홀1-1` | `1지역 합계` |
| `홀1-2` | `2지역 합계` |
| `홀2` | `홀2 합계` |
| `전체` | `한국어 합계` |

For summary values, convert empty or `0` to `-`.

Small group rows, using 0-based row indexes and the target week's `소그룹` column:

| Row index | Doc label |
| ---: | --- |
| 2 | `LA1-1` |
| 3 | `LA1-2` |
| 4 | `LA1-3` |
| 5 | `LA1-4` |
| 6 | `LA1-5` |
| 7 | `LA1-6` |
| 8 | `LA1-7` |
| 12 | `LA2-1` |
| 13 | `LA2-2` |
| 14 | `LA2-3` |
| 15 | `LA2-4` |
| 16 | `LA2-5` |
| 17 | `LA2-6` |
| 18 | `LA2-7` |
| 19 | `LA2-8` |
| 23 | `VA` |
| 24 | `GD` |

For small group values, convert empty values to `미집계`. Preserve non-empty displayed values as-is, including `-`.

## Doc Targeting

Use `mcp__codex_apps__google_drive._get_document` on the newsletter Doc before every write batch. Confirm:

- document id is `1qa6ZUtqT1vdfIXMFdVwKvkt12PcvtkrLsXplEFdnG7A`
- title is the expected newsletter working doc
- if the response has `tabs`, use the tab containing the body content and carry its `tabId`

Find the outer table cell containing `인수 통계`. Inside that cell:

- Date range paragraph: text containing `/`, `(`, `)`, and not `인수`
- Summary table: nested table with 5 columns; rows after the header map first-cell labels to `기도`, `소그룹`, `주일`, `신언`
- Small group table: nested table with 2 columns and more than 10 rows; rows after the header map first-cell labels to the second-cell value

For each target value cell, use the first paragraph element `startIndex` and the last paragraph element `endIndex`.

## Required Workflow

### Step 1: Read Sheet + Verify

Read the Sheet and compute the target week. Verify before continuing:

- date range follows the Monday-Sunday rule
- the matching date columns exist
- category row at the matched columns is `기도`, `소그룹`, `주일`, `신언`
- summary values for `홀1-1`, `홀1-2`, `홀2`, `전체` are present after conversion
- small group values are present, with blanks converted to `미집계`
- values are not obviously inconsistent, such as `전체` being smaller than a visible subtotal for the same category

If verification fails, stop and report the problem.

### Step 2: Dry Run + Verify

Read the Doc and build the planned Google Docs batchUpdate requests, but do not write yet.

Replacement rules:

- Date text format: `YYYY/M/D(월) - YYYY/M/D(주)`
- Process replacements from highest `startIndex` to lowest.
- To replace existing cell text, use `deleteContentRange` from `startIndex` to `endIndex - 1`, then `insertText` at `startIndex`.
- Insert text without the trailing newline. Keep the cell paragraph newline intact.
- If a Doc `tabId` is present, include it in every `deleteContentRange.range` and `insertText.location`.

Verify before continuing:

- planned values exactly match Step 1 values
- date range text is correct
- all 16 summary cells are targeted
- all 17 small group cells are targeted
- total requests are expected: 68 value requests plus 2 date requests when every replacement has existing text

If verification fails, stop and report the problem.

### Step 3: Write

Before writing, re-read the Doc and re-confirm the target document id, title, and `tabId`. Rebuild request indexes from this fresh read.

Use `mcp__codex_apps__google_drive._batch_update_document` with:

- `document_id`: newsletter Doc id
- `requests`: structured request objects, not stringified JSON
- `write_control`: prefer the latest `revisionId` from the fresh `_get_document` read when available

### Step 4: Readback Verification

After writing, read the Doc again and verify:

- target Doc id and title are still correct
- date range in `인수 통계` matches the updated week
- summary table values match the Sheet-derived values
- small group table values match the Sheet-derived values

Only report completion after readback verification succeeds. If rendered layout cannot be inspected through connector data, do not claim visual verification.

## Notes

- Do not ask the user for a Google Drive URL unless the hard-coded target files are inaccessible.
- Do not use `gws auth login`; the Google Drive Codex Plugin connection is the source of authentication.
