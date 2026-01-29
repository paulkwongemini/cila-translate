---
name: parser
description: Convert translated Markdown documents into styled HTML fragments for publication. Use when the user asks to "Convert" a document.
---

# Parser Skill

This skill converts a translated Markdown document (usually `workspace/translated.md`) into a styled HTML fragment suitable for publication.

## When to Use

Use this skill when:
- The user asks to "Convert" or "Format" the translated document.
- You need to generate the legacy HTML format from a Markdown source.

## Usage Procedure

### 1. Run Conversion Script

Use the `parse_doc.py` script to perform the conversion.

```bash
python3 skills/parser/scripts/parse_doc.py --input <path_to_markdown> --output <path_to_html>
```

-   **Defaults**:
    -   `--input`: `workspace/translated.md`
    -   `--output`: `outputs/final.html`

### 2. Verify Output

-   Check `outputs/final.html` to ensure:
    -   It is a valid HTML fragment (starts with `<style>...`, ends with `</div>`).
    -   English sections are excluded.
    -   Korean titles and content are preserved and styled.
    -   Announcements are removed (if not already handled by translator).

## Example

```bash
python3 skills/parser/scripts/parse_doc.py
```
