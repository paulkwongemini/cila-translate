---
name: bible-verse-getter
description: Fetch Korean Bible verses from the Recovery Version website (rv.or.kr) using a dedicated script. Use when the user requests to "Search for a bible verse" or explicitly asks for a verse like "John 3:16".
---

# Bible Verse Getter

This skill provides a tool to fetch Korean Bible verses from the Recovery Version website.

## When to Use This Skill

Use this skill when:
- The user asks for a specific Bible verse (e.g., "Get me John 3:16").
- The user asks to "Search" for a verse.
- You need to retrieve Bible verse text for translation or other processing.

## Usage

### Fetching a Verse

Use the `get_verse.py` script to fetch a verse.

```bash
python3 skills/bible-verse-getter/scripts/get_verse.py --book "<Book Name>" --chapter <Chapter> --verse <Verse(s)>
```

**Parameters:**
- `--book`: The English name of the Bible book (e.g., "Genesis", "Matthew", "Revelation"). Case-insensitive.
- `--chapter`: The chapter number (integer).
- `--verse`: (Optional) The verse number or range (e.g., "1", "1-5", "1,3,5"). If omitted, it may fetch the whole chapter or default to verse 1 depending on the script logic (default is usually required for specific verse, check script).

**Example:**

```bash
# Fetch John 3:16
python3 skills/bible-verse-getter/scripts/get_verse.py --book "John" --chapter 3 --verse 16

# Fetch Genesis 1:1-3
python3 skills/bible-verse-getter/scripts/get_verse.py --book "Genesis" --chapter 1 --verse 1-3
```

## Output

The script prints the plain text of the requested verse(s) to standard output.
