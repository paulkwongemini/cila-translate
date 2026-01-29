---
name: translator
description: Start a translation task. This skill helps the Agent translate English church documents into Korean by guiding the context preparation and translation process.
---

# Translator Skill

This skill assists in translating English church documents into Korean. It relies on the **Agent** to identify and fetch Bible verses using the `bible-verse-getter` skill to ensure accuracy.

## When to Use

Use this skill when:
- You need to translate a document (e.g., `inputs/raw.html`, prayer outlines) from English to Korean.
- The document contains Bible verse references that need to be quoted exactly.

## Usage Procedure

### 1. Identify and Fetch Bible Verses

As the Agent, you must first scan the input document for any Bible verse references (e.g., "John 3:16", "Matt. 5:3-5").

For **each** unique reference found:
1.  Determine the Book, Chapter, and Verse(s).
2.  Use the `bible-verse-getter` skill to fetch the **Korean Recovery Version** text.
    -   Run: `python3 skills/bible-verse-getter/scripts/get_verse.py --book "<Book>" --chapter <Chapter> --verse <Verse>`
    -   **Strict Rule:** Do not guess or back-translate verses. You must fetch the exact text from the source.

### 2. Prepare Resources

-   **Glossary**: Read `skills/translator/resources/WORDS.csv` for specific term usage.

### 3. Translate

Perform the translation using the fetched verses and the glossary.

-   **Bible Verses**: Insert the exact Korean text you fetched in Step 1.
-   **Tone**: Humble, sincere, spiritual.
-   **Output**: Save the translated content to `workspace/translated.md` (or the user-specified output path).

### 4. Formatting

Ensure the output follows the standard format:
-   **Date Title**: `# **YYYY년 M월 D일 주간 기도문**`
-   **Structure**: English Section followed by Korean Section.
-   **Announcement**: Remove any "Announcements" sections.

## Example Workflow

1.  **Read Input**: User asks to translate `inputs/raw.html`.
2.  **Scan**: You see "John 3:16" in the text.
3.  **Fetch**: You run `python3 skills/bible-verse-getter/scripts/get_verse.py --book "John" --chapter 3 --verse 16`.
4.  **Translate**: You write the Korean translation, pasting the fetched verse text where "John 3:16" appears.
