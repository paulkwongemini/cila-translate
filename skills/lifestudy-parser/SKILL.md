---
name: lifestudy-parser
description: Convert plain-text life study material into a markdown document with headings. Use when the user explicitly asks to use this skill.
---

# Lifestudy Parser Skill

This skill converts a plain-text life study material into a styled HTML fragment suitable for publication.

## When to Use

Use this skill when:
- The user explicitly asks to use this skill. The user will ask to convert a specific number of message. For example, if the user asks to convert message 37, you will convert message 37.

## Usage Procedure

### 1. Preparation

- The content of `skills/lifestudy-parser/assets/ephesians.txt` is a very long plain-text life study material. There are 97 messages in total. Each message starts with "메시지 1", "메시지 37", etc. 

### 2. manual Agentic Conversion

You will manually generate the HTML content file by processing the markdown according to the following rules:

1.  **Identify Structure**:
    - The message consists of headings and paragraphs. 
    - Identify headings based on these common patterns:
        -   **Roman Numerals**: `I.`, `II.`, `III.` (Top Level)
        -   **Capital Letters**: `A.`, `B.`, `C.` (Second Level)
        -   **Arabic Numerals**: `1.`, `2.`, `3.` (Third Level)
        -   **Lower Case Letters**: `a.`, `b.`, `c.` (Fourth Level)
    -   Translate these to Markdown styling:
        -   Start with `#` for the Message Title (e.g., `# Message 1`).
        -   Use `#` for Roman Numerals (e.g., `# I. Title`).
        -   Use `##` for Capital Letters (e.g., `## A. Subtitle`).
        -   Use `###` for All heading levels below Capital Letters.

2.  **Identify and Fetch Bible Verses**:
    As the Agent, you must first scan the input document for any Bible verse references (e.g., "John 3:16", "Matt. 5:3-5"). If the verse is referenced without mentioning the name of the book, it is highly likely that it is from Ephesians. However, you must check the context to confirm.

    For **each** unique reference found:
    - Determine the Book, Chapter, and Verse(s).
    - Use the `bible-verse-getter` skill to fetch the **Korean Recovery Version** text.
        - Run: `python3 skills/bible-verse-getter/scripts/get_verse.py --book "<Book>" --chapter <Chapter> --verse <Verse>`
        - **Strict Rule:** Do not guess or back-translate verses. You must fetch the exact text from the source.

3.  **Replace Bible Verses**:
    - The source text will have an old version of Bible verses. Replace them with the up-to-date Korean Recovery Version verses, fetched from Step 2.
    - On many occations, the Bible verses will not be a complete verse. If the source has a partial verse, you must identify which portion of the fetched verse should replace the source, and use only that portion. Do not replace a partial verse with a complete verse.

4.  **Refine Formatting**:
    - **Remove duplicate new lines**: The source text may have duplicate new lines between paragraphs and headings. Reduce them to just 1 new line between headings and paragraphs.
    - **Clean up Artifacts**: Ensure no stray underscores `_` or symbols are inserted, especially near Bible verse references (e.g., `(빌 1:20)`). Remove them if they appear unless they are valid Markdown italics.

5.  **Formatting Rules**:
    - **Sections**: Do not use `---` to separate sections. The paragraphs will have a space after them, so focus on getting the headers correctly.
    - **Bolds**: Do not bold the headers. Styling will be taken care of by the user.

### 3. Output

- Save the generated markdown content to `lifestudy-of-ephesians/eph-##.md`, where `##` is the message number in 2 digits. For example, `eph-01.md` for message 1, `eph-37.md` for message 37, etc.
