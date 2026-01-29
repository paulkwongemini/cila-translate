import argparse
import sys
import os
import re

# CSS Block from specs/parser/SKILL.md (or legacy parser)
# Assuming it's a fixed block.
CSS_BLOCK = """<style>
@import url('https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@400;700;800&display=swap');
.korean-section {
    font-family: 'Nanum Myeongjo', serif;
    line-height: 1.8;
    color: #333;
}
.korean-section h3 {
    color: #2c3e50;
    border-bottom: 2px solid #eee;
    padding-bottom: 10px;
    margin-top: 30px;
    font-weight: 800;
}
.korean-section ul {
    list-style-type: none;
    padding-left: 0;
}
.korean-section li {
    margin-bottom: 15px;
    padding-left: 20px;
    position: relative;
    text-align: justify;
}
.korean-section li::before {
    content: "•";
    position: absolute;
    left: 0;
    color: #7f8c8d;
}
.korean-section .p {
    margin-bottom: 15px;
    text-align: justify;
}
.korean-section a {
    color: #3498db;
    text-decoration: none;
}
.korean-section a:hover {
    text-decoration: underline;
}
</style>"""

def parse_markdown(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' not found.")
        sys.exit(1)

    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    html_parts = []
    
    # Logic to filter English sections
    # Spec: "Ignore Top Title: Skip lines starting with # if they contain '주간 기도문'."
    # Spec: "English Filter: If sections are interleaved ... exclude all English sections. Keep only Korean titles and content."
    
    # Heuristic: 
    # - If H1 (#) or H2 (##) line has non-Korean text mostly, it's English Title?
    # - "주간 기도문" line is ignored.
    # - Sections usually alternate: English Title -> English Content -> Korean Title -> Korean Content
    # - Or maybe the spec implies existing translated.md structure:
    #   # English Title
    #   ...
    #   # 한글 제목
    #   ...
    
    # Implementation strategy:
    # 1. Identify section headers.
    # 2. Classify sections as Korean or English.
    # 3. Only keep Korean sections.
    # 4. If content is just one block (already translated only?), keep it.
    
    # Simple Heuristic check for Korean characters in header
    def is_korean_string(s):
        # Check if line has Hangul characters
        return bool(re.search(r'[가-힣]', s))

    # Process line by line statefully?
    # Or just process structure.
    
    current_section_is_korean = True # Default to True unless we detect English header
    # However, standard translated.md usually starts with English, then Korean.
    # Let's inspect headers.
    
    filtered_lines = []
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
            
        # Ignore top title if specific
        if stripped.startswith('#') and "주간 기도문" in stripped:
            continue
            
        if stripped.startswith('#') or stripped.startswith('##'):
            # It's a header
            if is_korean_string(stripped):
                current_section_is_korean = True
                filtered_lines.append(line) # Keep the Korean header
            else:
                # English header?
                current_section_is_korean = False
                # Skip this line and subsequent lines until next header
        else:
            # Content line
            if current_section_is_korean:
                filtered_lines.append(line)
    
    # Convert filtered lines to HTML
    converted_html = []
    
    in_list = False
    
    for line in filtered_lines:
        stripped = line.strip()
        
        # Header -> H3
        if stripped.startswith('#'):
            if in_list:
                converted_html.append("</ul>")
                in_list = False
            
            # Remove MD bold markers ** from title if present
            clean_title = stripped.lstrip('#').strip().replace('**', '')
            converted_html.append(f"<h3>{clean_title}</h3>")
            
        # List Item -> li
        elif stripped.startswith('* ') or stripped.startswith('- '):
            if not in_list:
                converted_html.append("<ul>")
                in_list = True
            
            content = stripped[2:].strip()
            # Process links in content [text](url) -> <a href="url" target="_blank">text</a>
            content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank">\1</a>', content)
            
            converted_html.append(f"<li>{content}</li>")
            
        else:
            if in_list:
                converted_html.append("</ul>")
                in_list = False
            
            # Paragraph
            content = stripped
            # Process links
            content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank">\1</a>', content)
            converted_html.append(f'<div class="p">{content}</div>')
            
    if in_list:
        converted_html.append("</ul>")

    # Combine
    final_html = CSS_BLOCK + '<div class="korean-section">\n' + '\n'.join(converted_html) + '\n</div>'
    
    # Write output
    dirname = os.path.dirname(output_path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"Recursively converted {len(filtered_lines)} lines to HTML at {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Markdown to HTML Fragment.")
    parser.add_argument("--input", default="workspace/translated.md", help="Path to input markdown file")
    parser.add_argument("--output", default="outputs/final.html", help="Path to output html file")
    
    args = parser.parse_args()
    
    parse_markdown(args.input, args.output)
