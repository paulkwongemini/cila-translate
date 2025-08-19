#!/usr/bin/env python3
"""
Test script for the translation web application
"""

def test_bible_scraper():
    """Test the Bible verse scraper"""
    try:
        from bible_verse_scraper import get_bible_verse, parse_verse_reference
        
        # Test parsing
        book_name, chapter, verse = parse_verse_reference("요한복음15장1절")
        print(f"✅ Parsing test: {book_name} {chapter}:{verse}")
        
        # Test verse retrieval
        verse_text = get_bible_verse("요한복음", 15, 1)
        print(f"✅ Verse retrieval: {verse_text[:50]}...")
        
        return True
    except Exception as e:
        print(f"❌ Bible scraper test failed: {e}")
        return False

def test_translation_files():
    """Test if translation files exist"""
    import os
    
    files_to_check = [
        'translate/TRANSLATE.md',
        'translate/WORDS.csv'
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ Found: {file_path}")
        else:
            print(f"❌ Missing: {file_path}")
            return False
    
    return True

def test_requirements():
    """Test if required packages can be imported"""
    packages = [
        ('requests', 'HTTP requests'),
        ('bs4', 'BeautifulSoup HTML parsing')
    ]
    
    for package, description in packages:
        try:
            __import__(package)
            print(f"✅ {description}: {package}")
        except ImportError:
            print(f"❌ Missing package: {package} ({description})")
            print(f"   Install with: pip install {package}")
            return False
    
    return True

def main():
    """Run all tests"""
    print("🧪 Testing Translation Web Application Setup\n")
    
    tests = [
        ("Required packages", test_requirements),
        ("Translation files", test_translation_files),
        ("Bible scraper", test_bible_scraper)
    ]
    
    all_passed = True
    
    for test_name, test_func in tests:
        print(f"\n📋 Testing {test_name}:")
        if not test_func():
            all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("🎉 All tests passed! Ready to run the web application.")
        print("\nTo start the application:")
        print("1. Get a free Google Gemini API key: https://makersuite.google.com/app/apikey")
        print("2. Run: pip install streamlit google-generativeai")
        print("3. Run: streamlit run streamlit_app.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")

if __name__ == "__main__":
    main()