import argparse
import sys
import urllib.request
import urllib.parse
import urllib.error
import re

def get_book_index(book_name):
    """
    Maps book names to (index, version) tuple.
    Version: 0 for Old Testament, 1 for New Testament.
    """
    book_name = book_name.lower()
    
    # Old Testament (bibleVer=0)
    ot_books = {
        'genesis': 1, 'exodus': 2, 'leviticus': 3, 'numbers': 4, 'deuteronomy': 5,
        'joshua': 6, 'judges': 7, 'ruth': 8, '1 samuel': 9, '2 samuel': 10,
        '1 kings': 11, '2 kings': 12, '1 chronicles': 13, '2 chronicles': 14,
        'ezra': 15, 'nehemiah': 16, 'esther': 17, 'job': 18, 'psalms': 19,
        'proverbs': 20, 'ecclesiastes': 21, 'song of songs': 22, 'isaiah': 23,
        'jeremiah': 24, 'lamentations': 25, 'ezekiel': 26, 'daniel': 27,
        'hosea': 28, 'joel': 29, 'amos': 30, 'obadiah': 31, 'jonah': 32,
        'micah': 33, 'nahum': 34, 'habakkuk': 35, 'zephaniah': 36,
        'haggai': 37, 'zechariah': 38, 'malachi': 39
    }
    
    # New Testament (bibleVer=1)
    nt_books = {
        'matthew': 1, 'mark': 2, 'luke': 3, 'john': 4, 'acts': 5,
        'romans': 6, '1 corinthians': 7, '2 corinthians': 8, 'galatians': 9,
        'ephesians': 10, 'philippians': 11, 'colossians': 12,
        '1 thessalonians': 13, '2 thessalonians': 14, '1 timothy': 15,
        '2 timothy': 16, 'titus': 17, 'philemon': 18, 'hebrews': 19,
        'james': 20, '1 peter': 21, '2 peter': 22, '1 john': 23,
        '2 john': 24, '3 john': 25, 'jude': 26, 'revelation': 27
    }

    if book_name in ot_books:
        return ot_books[book_name], 0
    elif book_name in nt_books:
        return nt_books[book_name], 1
    
    return None, None

def fetch_verse(book, chapter, verse_spec):
    idx, ver = get_book_index(book)
    if idx is None:
        print(f"Error: Unknown book '{book}'")
        sys.exit(1)

    url = f"http://rv.or.kr/read_recovery.php?bibleVer={ver}&bibleSelOp={idx}&bibChapt={chapter}"
    
    try:
        with urllib.request.urlopen(url) as response:
             # Try to detect encoding or default to utf-8. The site is likely utf-8 or euc-kr.
             # Let's try utf-8 first.
             html_content = response.read().decode('utf-8')
    except urllib.error.URLError as e:
        print(f"Error fetching URL: {e}")
        sys.exit(1)
        
    # Parse verse spec
    target_verses = []
    if verse_spec:
        if '-' in verse_spec:
            try:
                start, end = map(int, verse_spec.split('-'))
                target_verses = list(range(start, end + 1))
            except ValueError:
                pass
        elif ',' in verse_spec:
            try:
                target_verses = [int(v) for v in verse_spec.split(',')]
            except ValueError:
                pass
        else:
            try:
                target_verses = [int(verse_spec)]
            except ValueError:
                pass
    
    # Regex based extraction
    # Structure: <div class="num" id="1">1</div> <div class="text">content</div>
    # or similar.
    # We will look for <div class="num" id="ID">ID</div>...<div class="text">CONTENT</div>
    # The content might span multiple lines or tags, but usually simple text.
    
    # This regex looks for the num div, capturing the ID, then non-greedy match until the text div starts, then captures the text div content.
    # Note: Regex parsing HTML is fragile, but for a known simple structure it works better than no parser.
    # Improved regex to be more robust for this specific site structure.
    
    # Pattern: <div class="num" id="(\d+)">\d+</div>\s*<div class="text">([^<]+)</div>
    pattern = re.compile(r'<div class="num" id="(\d+)">\d+</div>\s*<div class="text">(.*?)</div>', re.DOTALL)
    
    found_verses = pattern.findall(html_content)
    
    result_text = []
    
    for v_str, text_content in found_verses:
        try:
            v_num = int(v_str)
        except ValueError:
            continue
            
        if not target_verses or v_num in target_verses:
            # Clean up text content
            # Remove any internal tags if present (though regex above assumes none or non-greedy)
            # Unescape html entities if needed (standard library has html module)
            import html
            clean_text = html.unescape(text_content.strip())
            result_text.append(f"{v_num} {clean_text}")
    
    if not result_text:
        # Fallback debug: print first 500 chars if no match found, maybe structure changed
        # print("No verses found. Debug content snippet:", html_content[:500], file=sys.stderr)
        print("No verses found.")
    else:
        print("\n".join(result_text))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Korean Bible verses.")
    parser.add_argument("--book", required=True, help="Bible book name")
    parser.add_argument("--chapter", required=True, type=int, help="Chapter number")
    parser.add_argument("--verse", help="Verse number or range (e.g., 1, 1-5)")
    
    args = parser.parse_args()
    
    fetch_verse(args.book, args.chapter, args.verse)
