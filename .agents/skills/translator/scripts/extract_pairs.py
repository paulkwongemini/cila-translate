#!/usr/bin/env python3
"""Extract paired EN/KR sections from an exported prayer archive Markdown file."""

import re
import sys

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

def clean_exported_markdown(text):
    """Undo Google Docs Markdown escaping that is noisy in translation examples."""
    text = text.strip()
    text = re.sub(r"^(\*\*|__)(.*)(\*\*|__)$", r"\2", text)
    return re.sub(r"\\([\\`*_{}\[\]()#+\-.!|>])", r"\1", text)

def read_markdown_blocks(markdown):
    """Flatten exported Markdown into a list of (heading_level, text) blocks."""
    blocks = []
    body_lines = []

    def flush_body():
        nonlocal body_lines
        while body_lines and not body_lines[0].strip():
            body_lines.pop(0)
        while body_lines and not body_lines[-1].strip():
            body_lines.pop()
        if body_lines:
            text = "\n".join(body_lines)
            blocks.append((0, clean_exported_markdown(text)))
        body_lines = []

    for line in markdown.splitlines():
        heading = re.match(r"^(#{1,3})\s+(.*)$", line)
        if heading:
            flush_body()
            level = len(heading.group(1))
            text = clean_exported_markdown(heading.group(2))
            if text:
                blocks.append((level, text))
            continue
        if re.match(r"^\s*-{3,}\s*$", line):
            continue
        body_lines.append(line.rstrip())
    flush_body()
    return blocks

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
        if current_section is None:
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
    if len(sys.argv) > 2:
        print("Usage: extract_pairs.py [archive.md]", file=sys.stderr)
        sys.exit(2)
    if len(sys.argv) == 2:
        with open(sys.argv[1], encoding="utf-8") as f:
            markdown = f.read()
    else:
        markdown = sys.stdin.read()
    if not markdown.strip():
        print("No Markdown input provided.", file=sys.stderr)
        sys.exit(2)

    blocks = read_markdown_blocks(markdown)
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
