---
name: parser
description: Instructions for the Agent to convert Markdown to HTML fragment manually.
---

# Parser Skill (Agent Instruction)

This skill provides the **Standard Operating Procedure (SOP)** for the Agent to convert the translated Markdown file into the final HTML fragment without using a script.

## Procedure

1.  **Read Input**:
    -   Read `workspace/translated.md` (or specified file).

2.  **Filter & Prepare**:
    -   **Ignore Top Title**: If the first non-empty line starts with `#` and contains "주간 기도문", ignore it (do not include in output).
    -   **Filter English**: If the document contains interleaved English and Korean, **exclude all English content**. Keep only the Korean sections.

3.  **Apply HTML Conversion**:
    -   **Headers**: Convert lines starting with `#` to `<h3>`. Remove bold `**` markers if present.
    -   **Lists**: Convert lines starting with `* ` (asterisk + space) into `<ul>` with `<li>`. Combine consecutive list items into a single `<ul>`.
    -   **Paragraphs**: Wrap other non-empty lines in `<div class="p">`.
    -   **Links**: Convert `[text](url)` to `<a href="url" target="_blank">text</a>`.

4.  **Final Assembly**:
    -   Do **not** create a full HTML skeleton (`<html>`, `<body>`).
    -   Prepend the **CSS Block** (see below).
    -   Wrap the entire converted content in a `<div class="korean-section">` container.
    -   Ensure there is **no newline** between the CSS block and the `<div class="korean-section">`.

5.  **Output**:
    -   Save the result to `outputs/final.html`.

## Reference: CSS Block

Use this exact code block at the top of the file:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nanum+Myeongjo&display=swap" rel="stylesheet">
<style>
.korean-section { 
  h3, .p, li { font-family: "Nanum Myeongjo", serif !important; } 
  h3:not(:first-child) { margin-top: 72px; }
  h3 { margin-bottom: 24px; }
  table {
    th, td { padding: 8px; }
  }
  .p { margin-bottom: 24px; }
}
</style>
```
