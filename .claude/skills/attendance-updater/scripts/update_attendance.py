#!/usr/bin/env python3
"""
Reads attendance data from LA Church Google Sheet and updates the newsletter Google Doc.

Sheet: 134f4yt7zk0Dvu3d9JOAOvJNJz5JJ_XET52z3G5A98VI (tab: 2025-2026)
Doc:   1qa6ZUtqT1vdfIXMFdVwKvkt12PcvtkrLsXplEFdnG7A

Usage:
    python3 update_attendance.py [--dry-run]
"""

import json
import subprocess
import sys
from datetime import datetime, timedelta

SPREADSHEET_ID = "134f4yt7zk0Dvu3d9JOAOvJNJz5JJ_XET52z3G5A98VI"
SHEET_NAME = "2025-2026"
DOC_ID = "1qa6ZUtqT1vdfIXMFdVwKvkt12PcvtkrLsXplEFdnG7A"

# Row indices (0-based) for summary rows
SUMMARY_ROWS = {
    "1지역 합계": 9,   # Row 10
    "2지역 합계": 20,  # Row 21
    "홀2 합계": 25,    # Row 26
    "한국어 합계": 27,  # Row 28
}

# Mapping: doc label -> sheet row name
DOC_LABEL_MAP = {
    "홀1-1": "1지역 합계",
    "홀1-2": "2지역 합계",
    "홀2": "홀2 합계",
    "전체": "한국어 합계",
}

# Group rows for small group attendance (0-based row index -> doc label)
GROUP_ROWS = {
    2: "LA1-1",   # 1-1
    3: "LA1-2",   # 1-2
    4: "LA1-3",   # 1-3
    5: "LA1-4",   # 1-4
    6: "LA1-5",   # 1-5
    7: "LA1-6",   # 1-6
    8: "LA1-7",   # 1-7
    12: "LA2-1",  # 2-1
    13: "LA2-2",  # 2-2
    14: "LA2-3",  # 2-3
    15: "LA2-4",  # 2-4
    16: "LA2-5",  # 2-5
    17: "LA2-6",  # 2-6
    18: "LA2-7",  # 2-7
    19: "LA2-8",  # 2-8
    23: "VA",     # VA
    24: "GD",     # GD
}


def run_gws(args):
    """Run a gws command and return parsed JSON output."""
    cmd = ["gws"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout
    # gws may print "Using keyring backend: keyring" before JSON
    json_start = output.find("{")
    if json_start == -1:
        print(f"ERROR: No JSON in gws output.\nstdout: {output}\nstderr: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return json.loads(output[json_start:])


def get_last_week_date_range():
    """Get last week's Monday-Sunday date range."""
    today = datetime.now()
    # Find this week's Monday
    this_monday = today - timedelta(days=today.weekday())
    # Last week
    last_monday = this_monday - timedelta(weeks=1)
    last_sunday = last_monday + timedelta(days=6)
    return last_monday, last_sunday


def find_date_columns(date_row, target_monday, target_sunday):
    """Find the column index for the target date range in row 0.

    Date row format: ['', '3/9', '~', '3/15', '', '3/2', '~', '3/8', ...]
    Each date range occupies: start_date, '~', end_date, then blank separator.
    The corresponding data columns (기도, 소그룹, 주일, 신언) are at the same
    indices in row 1.

    We look for the start date (e.g., '3/2') which corresponds to the Monday.
    """
    target_str = f"{target_monday.month}/{target_monday.day}"
    target_end_str = f"{target_sunday.month}/{target_sunday.day}"

    for i, val in enumerate(date_row):
        if val == target_str:
            # Verify the end date
            if i + 2 < len(date_row) and date_row[i + 1] == "~" and date_row[i + 2] == target_end_str:
                # The data columns start at this index in the categories row
                # Row 1 at index i = 기도, i+1 = 소그룹, i+2 = 주일, i+3 = 신언
                return i
    return None


def read_sheet_data():
    """Read the attendance sheet and extract last week's data."""
    data = run_gws([
        "sheets", "spreadsheets", "values", "get",
        "--params", json.dumps({
            "spreadsheetId": SPREADSHEET_ID,
            "range": SHEET_NAME
        })
    ])

    rows = data["values"]
    date_row = rows[0]
    cat_row = rows[1]

    last_monday, last_sunday = get_last_week_date_range()
    print(f"Target date range: {last_monday.strftime('%Y/%m/%d')} - {last_sunday.strftime('%Y/%m/%d')}")
    print(f"Looking for: {last_monday.month}/{last_monday.day} ~ {last_sunday.month}/{last_sunday.day}")

    col_idx = find_date_columns(date_row, last_monday, last_sunday)
    if col_idx is None:
        print("ERROR: Could not find the target date range in the sheet.", file=sys.stderr)
        sys.exit(1)

    print(f"Found date range at column index {col_idx}")
    print(f"Categories: {cat_row[col_idx:col_idx+4]}")

    # Extract summary data (기도, 소그룹, 주일, 신언)
    summary_data = {}
    for name, row_idx in SUMMARY_ROWS.items():
        row = rows[row_idx]
        vals = row[col_idx:col_idx + 4] if len(row) > col_idx else ["", "", "", ""]
        # Pad if needed
        while len(vals) < 4:
            vals.append("")
        summary_data[name] = {
            "기도": "-" if (not vals[0] or vals[0] == "0") else vals[0],
            "소그룹": "-" if (not vals[1] or vals[1] == "0") else vals[1],
            "주일": "-" if (not vals[2] or vals[2] == "0") else vals[2],
            "신언": "-" if (not vals[3] or vals[3] == "0") else vals[3],
        }
        print(f"  {name}: 기도={vals[0]}, 소그룹={vals[1]}, 주일={vals[2]}, 신언={vals[3]}")

    # Extract group small group data
    group_data = {}
    for row_idx, label in GROUP_ROWS.items():
        row = rows[row_idx]
        sg_val = ""
        if len(row) > col_idx + 1:
            sg_val = row[col_idx + 1] or ""
        group_data[label] = sg_val if sg_val else "미집계"
        print(f"  {label} 소그룹: {sg_val}")

    return summary_data, group_data, last_monday, last_sunday


def read_doc():
    """Read the Google Doc and return full document JSON."""
    return run_gws([
        "docs", "documents", "get",
        "--params", json.dumps({"documentId": DOC_ID})
    ])


def find_attendance_section(doc):
    """Find the 인수 통계 section and extract positions for updates."""
    body = doc["body"]["content"]

    updates = {
        "date_range": None,       # (startIndex, endIndex) of date range text
        "summary_table": {},      # {label: {category: (startIndex, endIndex)}}
        "group_table": {},        # {label: (startIndex, endIndex)}
    }

    for elem in body:
        if "table" not in elem:
            continue

        table = elem["table"]
        for row in table.get("tableRows", []):
            for cell in row.get("tableCells", []):
                cell_content = cell.get("content", [])
                has_attendance = False

                for c_elem in cell_content:
                    if "paragraph" in c_elem:
                        for el in c_elem["paragraph"].get("elements", []):
                            if "textRun" in el and "인수 통계" in el["textRun"]["content"]:
                                has_attendance = True
                                break

                if not has_attendance:
                    continue

                # Found the attendance cell - now parse it
                for c_elem in cell_content:
                    if "paragraph" in c_elem:
                        for el in c_elem["paragraph"].get("elements", []):
                            if "textRun" in el:
                                text = el["textRun"]["content"]
                                # Date range line (e.g., "2026/3/2(월) - 2026/3/8(주)\n")
                                if "/" in text and "(" in text and ")" in text and "인수" not in text:
                                    updates["date_range"] = (
                                        el["startIndex"],
                                        el["endIndex"]
                                    )

                    elif "table" in c_elem:
                        inner_table = c_elem["table"]
                        rows_count = inner_table["rows"]
                        cols_count = inner_table["columns"]

                        if cols_count == 5:
                            # Summary table (5 cols: label, 기도, 소그룹, 주일, 신언)
                            for ri, trow in enumerate(inner_table.get("tableRows", [])):
                                if ri == 0:
                                    continue  # header row
                                cells = trow.get("tableCells", [])
                                # Get label from first cell
                                label = ""
                                for ce in cells[0].get("content", []):
                                    if "paragraph" in ce:
                                        for el in ce["paragraph"].get("elements", []):
                                            if "textRun" in el:
                                                label += el["textRun"]["content"].strip()

                                if not label:
                                    continue

                                updates["summary_table"][label] = {}
                                categories = ["기도", "소그룹", "주일", "신언"]
                                for ci in range(1, 5):
                                    cell_data = cells[ci]
                                    for ce in cell_data.get("content", []):
                                        if "paragraph" in ce:
                                            for el in ce["paragraph"].get("elements", []):
                                                start = el["startIndex"]
                                                end = el["endIndex"]
                                                updates["summary_table"][label][categories[ci - 1]] = (start, end)

                        elif cols_count == 2 and rows_count > 10:
                            # Group small group table
                            for ri, trow in enumerate(inner_table.get("tableRows", [])):
                                if ri == 0:
                                    continue  # header row
                                cells = trow.get("tableCells", [])
                                # Get label
                                label = ""
                                for ce in cells[0].get("content", []):
                                    if "paragraph" in ce:
                                        for el in ce["paragraph"].get("elements", []):
                                            if "textRun" in el:
                                                label += el["textRun"]["content"].strip()

                                if not label:
                                    continue

                                # Get value cell position
                                for ce in cells[1].get("content", []):
                                    if "paragraph" in ce:
                                        for el in ce["paragraph"].get("elements", []):
                                            start = el["startIndex"]
                                            end = el["endIndex"]
                                            updates["group_table"][label] = (start, end)

    return updates


def build_batch_update_requests(updates, summary_data, group_data, last_monday, last_sunday):
    """Build Google Docs batchUpdate requests to update the attendance section.

    IMPORTANT: Process replacements from highest index to lowest to avoid
    invalidating indices.
    """
    replacements = []  # list of (startIndex, endIndex, newText)

    # 1. Date range
    if updates["date_range"]:
        start, end = updates["date_range"]
        mon_day_kr = "월"
        sun_day_kr = "주"
        new_date = (
            f"{last_monday.year}/{last_monday.month}/{last_monday.day}({mon_day_kr}) - "
            f"{last_sunday.year}/{last_sunday.month}/{last_sunday.day}({sun_day_kr})\n"
        )
        replacements.append((start, end, new_date))

    # 2. Summary table
    for doc_label, sheet_name in DOC_LABEL_MAP.items():
        if doc_label in updates["summary_table"] and sheet_name in summary_data:
            for cat in ["기도", "소그룹", "주일", "신언"]:
                if cat in updates["summary_table"][doc_label]:
                    start, end = updates["summary_table"][doc_label][cat]
                    val = summary_data[sheet_name][cat]
                    replacements.append((start, end, f"{val}\n"))

    # 3. Group table
    for label, (start, end) in updates["group_table"].items():
        if label in group_data:
            val = group_data[label]
            replacements.append((start, end, f"{val}\n"))

    # Sort by startIndex descending (process from end to start)
    replacements.sort(key=lambda x: x[0], reverse=True)

    requests = []
    for start, end, new_text in replacements:
        # Delete existing content
        if end > start + 1:  # More than just a newline
            requests.append({
                "deleteContentRange": {
                    "range": {
                        "startIndex": start,
                        "endIndex": end - 1  # Keep the trailing newline structure
                    }
                }
            })
            requests.append({
                "insertText": {
                    "location": {"index": start},
                    "text": new_text.rstrip("\n")
                }
            })
        else:
            # Cell is empty (just newline), insert before it
            requests.append({
                "insertText": {
                    "location": {"index": start},
                    "text": new_text.rstrip("\n")
                }
            })

    return requests


def main():
    read_only = "--read-only" in sys.argv
    dry_run = "--dry-run" in sys.argv

    print("=" * 50)
    print("LA Church Attendance Updater")
    print("=" * 50)

    # Step 1: Read sheet data
    print("\n[Step 1] Reading attendance data from Google Sheet...")
    summary_data, group_data, last_monday, last_sunday = read_sheet_data()

    print(f"\n--- 합계 테이블 ---")
    print(f"{'':12s} {'기도':>6s} {'소그룹':>6s} {'주일':>6s} {'신언':>6s}")
    for doc_label, sheet_name in DOC_LABEL_MAP.items():
        d = summary_data[sheet_name]
        print(f"{doc_label:12s} {d['기도']:>6s} {d['소그룹']:>6s} {d['주일']:>6s} {d['신언']:>6s}")

    print(f"\n--- 소그룹 인수 ---")
    for label, val in group_data.items():
        print(f"  {label}: {val}")

    if read_only:
        print("\n[Read-only mode] Sheet 데이터 읽기 완료.")
        return

    # Step 2: Read the doc
    print("\n[Step 2] Reading newsletter Google Doc...")
    doc = read_doc()

    # Step 3: Find positions in the doc
    print("[Step 3] Analyzing document structure...")
    updates = find_attendance_section(doc)

    if updates["date_range"]:
        print(f"  Date range found at index {updates['date_range']}")
    else:
        print("  WARNING: Date range not found!")

    print(f"  Summary table labels: {list(updates['summary_table'].keys())}")
    print(f"  Group table labels: {list(updates['group_table'].keys())}")

    # Step 4: Build update requests
    print("\n[Step 4] Building update requests...")
    requests = build_batch_update_requests(
        updates, summary_data, group_data, last_monday, last_sunday
    )

    print(f"  Total update requests: {len(requests)}")

    if dry_run:
        print("\n[DRY RUN] Would send these requests:")
        for r in requests:
            print(f"  {json.dumps(r, ensure_ascii=False)}")
        print("\nDry run complete. No changes made.")
        return

    if not requests:
        print("No updates needed.")
        return

    # Execute batchUpdate
    print("  Sending batchUpdate to Google Docs...")
    result = run_gws([
        "docs", "documents", "batchUpdate",
        "--params", json.dumps({"documentId": DOC_ID}),
        "--json", json.dumps({"requests": requests})
    ])

    print("\nDone! Attendance data updated successfully.")
    print(f"  Date range: {last_monday.month}/{last_monday.day} ~ {last_sunday.month}/{last_sunday.day}")
    print(f"  Summary: 홀1-1(1지역), 홀1-2(2지역), 홀2, 전체(한국어)")
    print(f"  Groups: {len(group_data)} groups updated")


if __name__ == "__main__":
    main()
