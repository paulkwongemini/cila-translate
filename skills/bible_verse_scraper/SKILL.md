---
name: bible_verse_scraper
description: Instructions for the Agent to fetch Korean Bible verses from rv.or.kr using system tools.
---

# Bible Verse Scraper Skill (Agent Instruction)

This skill provides the **Standard Operating Procedure (SOP)** for the Agent to fetch Bible verses from the Korean Recovery Version website (`rv.or.kr`) without using custom Python scripts.

## Procedure

When you need to fetch a bible verse (e.g., "요한복음 3장 16절"):

1.  **Identify the Book Index and Chapter**:
    -   Refer to the mapped index values (New Testament starts at 1, Old Testament at 0).
    -   Example: John (요한복음) is New Testament (Ver=1), Index=4. Chapter 3.

2.  **Construct the URL**:
    -   Format: `http://rv.or.kr/read_recovery.php?bibleVer={ver}&bibleSelOp={book_index}&bibChapt={chapter}`
    -   Example: `http://rv.or.kr/read_recovery.php?bibleVer=1&bibVerse=&bibOutline=&bibleSelOp=4&bibChapt=3`

3.  **Fetch and Extract**:
    -   Use `curl` to fetch the page source.
    -   Use `grep` or `sed` to extract the verse text. The HTML structure is usually `<div class="num" id="{verse}">...</div>...<div class="text">TARGET TEXT</div>`.
    -   **Command Pattern**:
        ```bash
        curl -s "URL" | grep -A 5 "id=\"{verse}\""
        ```
    -   Clean up the output to get just the text.

## Bible Book Index Mapping

**New Testament (bibleVer=1)**
- Matthew (마태복음): 1
- Mark (마가복음): 2
- Luke (누가복음): 3
- John (요한복음): 4
- Acts (사도행전): 5
- Romans (로마서): 6
- ... (Standard Protestant Order)
- Revelation (요한계시록): 27

**Old Testament (bibleVer=0)**
- Genesis (창세기): 1
- Exodus (출애굽기): 2
- ...
- Malachi (말라기): 39
