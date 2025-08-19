import streamlit as st
import google.generativeai as genai
import os
import re
from bible_verse_scraper import get_bible_verse, parse_verse_reference
import csv

# Page configuration
st.set_page_config(
    page_title="교회 기도문 번역기 - Church Prayer Translation Service",
    page_icon="🙏",
    layout="wide"
)

# Load translation dictionary
@st.cache_data
def load_translation_dict():
    """Load the translation word dictionary"""
    word_dict = {}
    try:
        with open('translate/WORDS.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                word_dict[row['en'].lower()] = row['ko']
    except FileNotFoundError:
        st.warning("번역 사전 파일을 찾을 수 없습니다. (translate/WORDS.csv)")
    return word_dict

# Load translation instructions
@st.cache_data
def load_translation_instructions():
    """Load the translation instructions"""
    try:
        with open('translate/TRANSLATE.md', 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "번역 지침을 불러올 수 없습니다."

def get_bible_verse_korean(verse_ref):
    """Get Korean Bible verse using the scraper"""
    try:
        book_name, chapter, verse_num = parse_verse_reference(verse_ref)
        verse_text = get_bible_verse(book_name, chapter, verse_num)
        return verse_text
    except Exception as e:
        return f"성경구절 오류: {e}"

def find_bible_verses_in_text(text):
    """Find Bible verse references in English text"""
    # Pattern to match Bible references like "Rev. 19:7", "John 15:1-2, 6, 16"
    patterns = [
        r'([1-3]?\s*[A-Za-z]+\.?\s+\d+:\d+(?:-\d+)?(?:,\s*\d+)*)',
        r'\(([1-3]?\s*[A-Za-z]+\.?\s+\d+:\d+(?:-\d+)?(?:,\s*\d+)*)\)'
    ]
    
    verses = []
    for pattern in patterns:
        matches = re.findall(pattern, text)
        verses.extend(matches)
    
    return list(set(verses))  # Remove duplicates

def translate_bible_reference(en_ref):
    """Translate English Bible reference to Korean format"""
    # Simple mapping for common books
    book_mapping = {
        'rev': '계', 'revelation': '계시록',
        'john': '요', 'jn': '요',
        'matt': '마', 'matthew': '마태복음',
        'mark': '마가복음', 'luke': '누가복음',
        'acts': '행', 'rom': '롬', 'romans': '로마서',
        'cor': '고', '1 cor': '고전', '2 cor': '고후',
        'gal': '갈', 'eph': '엡', 'phil': '빌', 'col': '골',
        'thess': '살', '1 thess': '살전', '2 thess': '살후',
        'tim': '딤', '1 tim': '딤전', '2 tim': '딤후',
        'tit': '딛', 'philem': '몬', 'heb': '히',
        'jas': '약', 'james': '야고보서',
        'pet': '벧', '1 pet': '벧전', '2 pet': '벧후',
        '1 kings': '열왕기상', '1 kgs': '왕상'
    }
    
    en_ref_lower = en_ref.lower().strip()
    for eng, kor in book_mapping.items():
        if en_ref_lower.startswith(eng):
            return en_ref_lower.replace(eng, kor, 1)
    
    return en_ref

def setup_gemini_api():
    """Setup Google Gemini API"""
    api_key = st.session_state.get('gemini_api_key', '')
    if api_key:
        genai.configure(api_key=api_key)
        return True
    return False

def translate_with_gemini(text, instructions, word_dict):
    """Translate text using Google Gemini API"""
    if not setup_gemini_api():
        return "API 키가 설정되지 않았습니다."
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Create specialized dictionary context
        dict_context = "\n".join([f"- {en}: {ko}" for en, ko in word_dict.items()])
        
        prompt = f"""
당신은 교회 기도문과 신앙 서적을 전문적으로 번역하는 영한 번역 전문가입니다.

다음 번역 지침을 반드시 따르세요:
{instructions}

특별 용어 사전:
{dict_context}

다음 영문을 한국어로 번역해 주세요. 성경구절이 포함된 경우 한국복음서원 회복역 번역을 사용하세요:

{text}

번역 시 주의사항:
1. 성경구절은 정확한 회복역 번역을 사용하세요
2. 교회와 신앙 관련 전문용어는 제공된 사전을 참고하세요  
3. 겸손하고 진지한 어조를 유지하세요
4. 자연스러운 한국어 표현을 사용하세요
"""
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"번역 오류: {str(e)}"

# Main UI
st.title("🙏 교회 기도문 번역 서비스")
st.subtitle("Church Prayer Translation Service")

# API Key input
st.sidebar.title("🔑 API 설정")
api_key = st.sidebar.text_input(
    "Google Gemini API Key", 
    type="password",
    help="https://makersuite.google.com/app/apikey 에서 무료 API 키를 발급받으세요"
)

if api_key:
    st.session_state['gemini_api_key'] = api_key
    st.sidebar.success("✅ API 키가 설정되었습니다")
else:
    st.sidebar.warning("⚠️ API 키를 입력해주세요")

# Instructions display
st.sidebar.title("📋 번역 지침")
with st.sidebar.expander("번역 지침 보기"):
    instructions = load_translation_instructions()
    st.text(instructions[:500] + "..." if len(instructions) > 500 else instructions)

# Main translation interface
col1, col2 = st.columns(2)

with col1:
    st.header("📝 영문 원문")
    english_text = st.text_area(
        "번역할 영문을 입력하세요:",
        height=400,
        placeholder="영어 기도문이나 신앙 텍스트를 입력해주세요..."
    )

with col2:
    st.header("🇰🇷 한글 번역문")
    
    if st.button("🔄 번역하기", type="primary", disabled=not api_key):
        if english_text:
            with st.spinner("번역 중입니다..."):
                # Load resources
                word_dict = load_translation_dict()
                instructions = load_translation_instructions()
                
                # Find Bible verses in the text
                bible_verses = find_bible_verses_in_text(english_text)
                
                # Translate
                korean_text = translate_with_gemini(english_text, instructions, word_dict)
                
                st.text_area(
                    "번역 결과:",
                    value=korean_text,
                    height=400
                )
                
                # Show Bible verses found
                if bible_verses:
                    st.subheader("📖 발견된 성경구절")
                    for verse in bible_verses:
                        korean_ref = translate_bible_reference(verse)
                        st.write(f"- {verse} → {korean_ref}")
        else:
            st.warning("번역할 텍스트를 입력해주세요.")
    
    # Placeholder for results
    if 'korean_text' not in st.session_state:
        st.text_area(
            "번역 결과:",
            value="번역 결과가 여기에 표시됩니다...",
            height=400,
            disabled=True
        )

# Features section
st.markdown("---")
st.header("✨ 주요 기능")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📖 성경구절 자동 인식")
    st.write("영문 텍스트에서 성경구절을 자동으로 찾아 한국복음서원 회복역으로 정확히 번역합니다.")

with col2:
    st.subheader("📚 전문용어 사전")
    st.write("교회와 신앙 관련 전문용어들을 정확하고 일관되게 번역합니다.")

with col3:
    st.subheader("🤖 AI 번역 + 전문가 검토")
    st.write("Google Gemini AI와 전문 번역 지침을 결합하여 고품질 번역을 제공합니다.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
    <p>Church in Los Angeles, Hall 1</p>
    <p><small>Powered by Google Gemini API & Streamlit</small></p>
    </div>
    """,
    unsafe_allow_html=True
)