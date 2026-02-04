---
name: parser
description: Convert translated Markdown documents into styled HTML fragments for publication using an agentic workflow. Use when the user asks to "Convert" a document.
---

# Parser Skill

This skill converts a translated Markdown document (usually `workspace/translated.md`) into a styled HTML fragment suitable for publication.

## When to Use

Use this skill when:
- The user asks to "Convert" or "Format" the translated document.
- You need to generate the legacy HTML format from a Markdown source.

## Usage Procedure

### 1. Preparation

- Read the content of `workspace/translated.md`.
- Read the content of `skills/parser/assets/style.css`.

### 2. manual Agentic Conversion

You will manually generate the HTML content file by processing the markdown according to the following rules:

1.  **Structure**:
    - Read the content of `skills/parser/assets/style.css`.
    - **Minify the CSS**: Remove all empty newlines and extra whitespace from the read CSS content.
    - Start the file with this minified CSS block.


    - Wrap the entire body content in a `<div class="korean-section">` container.
    - End the file with `</div>`.

2.  **Content Filtering**:
    - **Ignore English Sections**: Do not include any headers or paragraphs that are in English.
    - **Keep Korean Sections**: Identify headers and paragraphs that are in Korean.
    - **Ignore Top Title**: Do not include the top-level title (e.g., `# 2026년 2월 1일 주간 기도문`) if it looks like a document title. Start with the first section header (H2/H3).

3.  **HTML Mapping Rules**:
    - **Headers**: Convert Markdown headers (e.g., `## Title`) to `<h3>Title</h3>`.
        - Remove any bold markers (`**`) from the title text.
    - **Lists**: Convert bullet points (`*` or `-`) to `<ul>` and `<li>` items.
    - **Paragraphs**: Convert regular text paragraphs to `<div class="p">Content</div>`.
    - **Links**: Convert Markdown links `[text](url)` to `<a href="url" target="_blank">text</a>`.

4.  **Announcements**:
    - Ensure any "Announcements" sections are removed (usually handled during translation, but verify).

### 3. Output

- Save the generated HTML content to `outputs/final.html` (or the location specified by the user).

### 4. Verify Output

- Check `outputs/final.html` to ensure:
    - It starts with the CSS block.
    - It contains only Korean content.
    - All tags are properly closed.
