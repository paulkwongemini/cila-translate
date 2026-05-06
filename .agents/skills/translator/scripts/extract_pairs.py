#!/usr/bin/env python3
"""Extract paired EN/KR sections from the 2026 prayer archive Google Doc."""

import json
import re
import subprocess
import sys

DOC_ID = "1cGD3pPm6FoiFWqL42pDkzu_QLz0UFvKgCqFoT60OGko"

def has_korean(text):
    return bool(re.search(r"[가-힯]", text))

def has_latin_letters(text):
    return bool(re.search(r"[a-zA-Z]", text))

def classify(text):
    text = text.strip()
    if not text:
        return "empty"
    k = has_korean(text)
    e = has_latin_letters(text)
    if k and not e:
        return "kr"
    if k and e:
        return "kr"  # mixed text usually means Korean with English terms inline
    if e:
        return "en"
    return "other"

def extract_paragraph_text(p):
    parts = []
    for el in p.get("elements", []):
        tr = el.get("textRun")
        if tr:
            parts.append(tr.get("content", ""))
    return "".join(parts)

def fetch_doc():
    result = subprocess.run(
        ["gws", "docs", "documents", "get",
         "--params", json.dumps({"documentId": DOC_ID}),
         "--format", "json"],
        capture_output=True, text=True, check=True,
    )
    return json.loads(result.stdout)

def walk_blocks(content, blocks):
    """Flatten doc body into a list of (heading_level, text) blocks."""
    for el in content:
        if "paragraph" in el:
            p = el["paragraph"]
            style = p.get("paragraphStyle", {}).get("namedStyleType", "NORMAL_TEXT")
            text = extract_paragraph_text(p).rstrip("\n")
            if not text.strip():
                continue
            level = 0
            if style == "HEADING_1":
                level = 1
            elif style == "HEADING_2":
                level = 2
            elif style == "HEADING_3":
                level = 3
            blocks.append((level, text))
        elif "table" in el:
            # Skip tables for simplicity (none expected in this doc)
            for row in el["table"].get("tableRows", []):
                for cell in row.get("tableCells", []):
                    walk_blocks(cell.get("content", []), blocks)

def group_into_sections(blocks):
    """Group blocks into sections by HEADING_2 boundaries within each week.

    A "section" is: one HEADING_2 + all NORMAL_TEXT until the next HEADING_2 or HEADING_1.
    Returns a flat list of (week_label, section_title, lang, body) tuples.
    """
    sections = []
    current_week = None
    current_section = None  # dict with title, lang, body_lines

    def flush():
        nonlocal current_section
        if current_section and current_section["body"]:
            sections.append((
                current_week,
                current_section["title"],
                current_section["lang"],
                "\n".join(current_section["body"]).strip(),
            ))
        current_section = None

    for level, text in blocks:
        if level == 1:
            flush()
            current_week = text.strip()
            continue
        if level == 2:
            flush()
            lang = classify(text)
            current_section = {"title": text.strip(), "lang": lang, "body": []}
            continue
        # Body text
        if current_section is None:
            # Body before any HEADING_2 - skip or attach to a synthetic section
            continue
        current_section["body"].append(text)
    flush()
    return sections

def section_body_lang(body):
    """Classify a section by its body content, not just title."""
    return classify(body)

def pair_sections(sections):
    """Pair adjacent EN/KR sections within the same week.

    Both title AND body must match the expected language to avoid false
    positives like Korean sections with English acronym titles (e.g. "GTCA").
    """
    pairs = []
    i = 0
    while i < len(sections):
        week, title, _title_lang, body = sections[i]
        body_lang = section_body_lang(body)
        if body_lang == "en" and i + 1 < len(sections):
            week2, title2, _title_lang2, body2 = sections[i + 1]
            body2_lang = section_body_lang(body2)
            if week2 == week and body2_lang == "kr":
                pairs.append({
                    "week": week,
                    "en_title": title,
                    "en_body": body,
                    "kr_title": title2,
                    "kr_body": body2,
                })
                i += 2
                continue
        i += 1
    return pairs

def render_markdown(pairs):
    out = []
    out.append("# 영-한 번역 페어링 예시 모음")
    out.append("")
    out.append("이 파일은 `translator` 스킬이 번역할 때 참고하는 학습 자료입니다.")
    out.append("실제 발행된 주간 기도문에서 추출되었으며, 모두 사람이 검토하고 다듬은 최종 번역본입니다.")
    out.append("")
    out.append("**활용 방법:**")
    out.append("- 어체·톤·기도 항목 어미 패턴 참고")
    out.append("- 반복되는 주제(이탈리아, TSUF, 집회 안내 등)의 정착된 번역 표현 참고")
    out.append("- WORDS.csv에 없는 용어/고유명사 표기 참고")
    out.append("- 라이프스타디 인용·성경 구절 도입부의 문체 참고")
    out.append("")
    out.append(f"수록 페어 수: **{len(pairs)}개**")
    out.append("")
    out.append("---")
    out.append("")

    current_week = None
    for idx, p in enumerate(pairs, 1):
        if p["week"] != current_week:
            current_week = p["week"]
            out.append(f"## {current_week}")
            out.append("")
        out.append(f"### {idx}. {p['en_title']} / {p['kr_title']}")
        out.append("")
        out.append("**English:**")
        out.append("")
        out.append(p["en_body"])
        out.append("")
        out.append("**한국어:**")
        out.append("")
        out.append(p["kr_body"])
        out.append("")
        out.append("---")
        out.append("")
    return "\n".join(out)

def main():
    doc = fetch_doc()
    blocks = []
    walk_blocks(doc["body"]["content"], blocks)
    sections = group_into_sections(blocks)
    pairs = pair_sections(sections)

    print(f"Total blocks: {len(blocks)}", file=sys.stderr)
    print(f"Total sections: {len(sections)}", file=sys.stderr)
    print(f"Total EN/KR pairs: {len(pairs)}", file=sys.stderr)

    # Print summary of pairs
    for p in pairs:
        print(f"  [{p['week']}] {p['en_title'][:50]} <-> {p['kr_title'][:50]}", file=sys.stderr)

    md = render_markdown(pairs)
    sys.stdout.write(md)

if __name__ == "__main__":
    main()
