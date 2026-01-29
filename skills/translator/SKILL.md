---
name: translator
description: Instructions for the Agent to translate documents manually, using subagents for resources.
---

# Translator Skill (Agent Instruction)

This skill provides the **Standard Operating Procedure (SOP)** for the Agent to perform translations without running a python script.

## Procedure

1.  **Analyze Input**:
    -   Read the file at `inputs/raw.html` (or specified path).
    -   Identify any Bible verse references (e.g., "John 3:16", "Rev. 19:7").

2.  **Fetch Bible Verses**:
    -   For each identified verse, use the **Bible Verse Scraper Skill**.
    -   **Strict Rule**: Do not guess or back-translate verses. You must fetch the exact text from the **Korean Recovery Version** (rv.or.kr).

3.  **Prepare Resources**:
    -   Read `skills/translator/resources/WORDS.csv` for the glossary.

4.  **Translate (LLM Task)**:
    -   Perform the translation following the **Translation Guidelines** below.
    -   Integrate the fetched Bible verses exactly as they are.
    -   Save the result to `workspace/translated.md` (or specified path).

## Translation Guidelines

### 1. Purpose and Tone
*   **Purpose**: Clear communication for church prayer meetings and services.
*   **Tone**:
    *   Humble and sincere (겸손하고 진지한 어조).
    *   Warm and comforting.
    *   Spiritual and appropriate for a faith context.

### 2. Glossary Usage
*   Use the `WORDS.csv` file for specific terms.
*   If a term is not in the glossary, use the most appropriate spiritual term in context.

### 3. Sentence Structure
*   Stay faithful to the English original but ensure natural Korean flow.
*   Long English sentences can be split into two or more Korean sentences if needed.
*   **Do not omit** any English words.
*   **Do not replace** specific terms with pronouns (e.g., Translate "the Son of God" fully, not just "He").

### 4. Output Formatting (Markdown)
The final `translated.md` should be structured as follows:

*   **Date Title**: `# **YYYY년 M월 D일 주간 기도문**` (at the top)
*   **Sections**: Separate each section with a blank line.
    1.  **English Title**: `# **English Title**`
    2.  [English Content] (Scriptures, Body, Prayer Burdens)
    3.  **Korean Title**: `# **한글 제목**`
    4.  [Korean Content] (Scriptures, Body, Prayer Burdens)

**Formatting Rules**:
*   Use `#` for headings (H1/H2).
*   Use `*` for list items.
*   Remove bold/italic styling from references if present.
*   **Announcements**: Do NOT translate content labeled `<h3>Announcements</h3>`. Remove it entirely from the output.
