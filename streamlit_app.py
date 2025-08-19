import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import os
import re
from bible_verse_scraper import get_bible_verse, parse_verse_reference
import csv

# Load environment variables from .env file (for local development)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not available, use environment variables directly

# Page configuration
st.set_page_config(
    page_title="기도문 번역",
    page_icon="🙏",
    layout="centered"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main .block-container {
        max-width: 800px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    .stButton > button {
        background-color: #1e3a8a !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 2rem !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        width: auto !important;
        margin: 1rem auto !important;
        display: block !important;
    }
    
    .stButton > button:hover {
        background-color: #1e40af !important;
        color: white !important;
    }
    
    .stTextArea > div > div > textarea {
        font-family: 'Courier New', monospace !important;
        font-size: 14px !important;
        line-height: 1.6 !important;
    }
    
    /* Center spinner */
    .stSpinner {
        text-align: center !important;
        margin: 2rem 0 !important;
    }
    
    /* Style markdown output */
    .main .block-container h4 {
        color: #1f2937 !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Load translation dictionary
@st.cache_data(ttl=300)  # Cache for 5 minutes, then reload
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
@st.cache_data(ttl=300)  # Cache for 5 minutes, then reload
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
    """Translate English Bible reference to Korean format for bible scraper"""
    # Enhanced mapping for bible scraper compatibility
    book_mapping = {
        # New Testament
        'rev.': '계시록', 'revelation': '계시록', 'rev': '계시록',
        'john': '요한복음', 'jn': '요한복음', 'joh': '요한복음',
        'matt.': '마태복음', 'matthew': '마태복음', 'mt': '마태복음',
        'mark': '마가복음', 'mk': '마가복음',
        'luke': '누가복음', 'lk': '누가복음', 'luk': '누가복음',
        'acts': '사도행전', 'act': '사도행전',
        'rom.': '로마서', 'romans': '로마서', 'rom': '로마서',
        '1 cor.': '고린도전서', '1 cor': '고린도전서', '1 corinthians': '고린도전서',
        '2 cor.': '고린도후서', '2 cor': '고린도후서', '2 corinthians': '고린도후서',
        'gal.': '갈라디아서', 'galatians': '갈라디아서', 'gal': '갈라디아서',
        'eph.': '에베소서', 'ephesians': '에베소서', 'eph': '에베소서',
        'phil.': '빌립보서', 'philippians': '빌립보서', 'phil': '빌립보서',
        'col.': '골로새서', 'colossians': '골로새서', 'col': '골로새서',
        '1 thess.': '데살로니가전서', '1 thess': '데살로니가전서', '1 thessalonians': '데살로니가전서',
        '2 thess.': '데살로니가후서', '2 thess': '데살로니가후서', '2 thessalonians': '데살로니가후서',
        '1 tim.': '디모데전서', '1 tim': '디모데전서', '1 timothy': '디모데전서',
        '2 tim.': '디모데후서', '2 tim': '디모데후서', '2 timothy': '디모데후서',
        'tit.': '디도서', 'titus': '디도서', 'tit': '디도서',
        'philem.': '빌레몬서', 'philemon': '빌레몬서', 'philem': '빌레몬서',
        'heb.': '히브리서', 'hebrews': '히브리서', 'heb': '히브리서',
        'jas.': '야고보서', 'james': '야고보서', 'jas': '야고보서',
        '1 pet.': '베드로전서', '1 pet': '베드로전서', '1 peter': '베드로전서',
        '2 pet.': '베드로후서', '2 pet': '베드로후서', '2 peter': '베드로후서',
        '1 jn': '요한일서', '1 john': '요한일서',
        '2 jn': '요한이서', '2 john': '요한이서',
        '3 jn': '요한삼서', '3 john': '요한삼서',
        'jude': '유다서',
        
        # Old Testament (common ones)
        'gen.': '창세기', 'genesis': '창세기', 'gen': '창세기',
        'exod.': '출애굽기', 'exodus': '출애굽기', 'exod': '출애굽기',
        'ps.': '시편', 'psalm': '시편', 'psalms': '시편', 'psa': '시편',
        '1 kings': '열왕기상', '1 kgs': '열왕기상',
        '2 kings': '열왕기하', '2 kgs': '열왕기하',
        'isa.': '이사야', 'isaiah': '이사야', 'isa': '이사야',
        'jer.': '예레미야', 'jeremiah': '예레미야', 'jer': '예레미야'
    }
    
    en_ref_lower = en_ref.lower().strip()
    
    # Find the best match (longest match first to avoid partial matches)
    best_match = ""
    best_replacement = ""
    
    for eng, kor in sorted(book_mapping.items(), key=len, reverse=True):
        if en_ref_lower.startswith(eng):
            if len(eng) > len(best_match):
                best_match = eng
                best_replacement = kor
    
    if best_match:
        # Replace and format for bible scraper
        verse_part = en_ref_lower[len(best_match):].strip()
        # Convert "3:16" to "3장16절" format
        verse_part = verse_part.replace(':', '장').replace(' ', '') + '절'
        return f"{best_replacement}{verse_part}"
    
    return en_ref

def setup_gemini_api():
    """Setup Google Gemini API"""
    # Try to get API key from environment variable first
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        genai.configure(api_key=api_key)
        return True
    return False

def check_password():
    """Check if password is correct"""
    correct_password = os.getenv('APP_PASSWORD', 'default_password')
    
    if 'password_correct' not in st.session_state:
        st.session_state.password_correct = False
    
    if not st.session_state.password_correct:
        st.title("🔒 교회 기도문 번역 서비스 - 접근 제한")
        st.write("이 서비스는 승인된 사용자만 이용할 수 있습니다.")
        
        password = st.text_input("비밀번호를 입력하세요:", type="password", key="password_input")
        
        if st.button("로그인"):
            if password == correct_password:
                st.session_state.password_correct = True
                st.rerun()
            else:
                st.error("비밀번호가 올바르지 않습니다.")
        
        st.markdown("---")
        st.markdown("*관리자에게 문의하여 비밀번호를 받으세요.*")
        return False
    
    return True

def enhance_text_with_bible_verses(text):
    """Find and enhance English text with Korean Bible verses"""
    # Find Bible verses in the text
    bible_verses = find_bible_verses_in_text(text)
    
    enhanced_info = []
    if bible_verses:
        enhanced_info.append("발견된 성경구절과 한국복음서원 회복역 번역:")
        for verse in bible_verses:
            korean_ref = translate_bible_reference(verse)
            korean_verse = get_bible_verse_korean(korean_ref)
            if not korean_verse.startswith("성경구절 오류") and not korean_verse.startswith("오류"):
                enhanced_info.append(f"- {verse} → {korean_ref}: {korean_verse}")
    
    return enhanced_info

def translate_with_gemini(text, instructions, word_dict):
    """Translate text using Google Gemini API with Bible verse integration"""
    if not setup_gemini_api():
        return "API 키가 설정되지 않았습니다. 관리자에게 문의하세요."
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Find and get Korean Bible verses
        bible_verse_info = enhance_text_with_bible_verses(text)
        bible_context = "\n".join(bible_verse_info) if bible_verse_info else ""
        
        # Create specialized dictionary context
        dict_context = "\n".join([f"- {en}: {ko}" for en, ko in word_dict.items()])
        
        prompt = f"""
당신은 교회 기도문과 신앙 서적을 전문적으로 번역하는 영한 번역 전문가입니다.

다음 번역 지침을 반드시 따르세요:
{instructions}

특별 용어 사전:
{dict_context}

성경구절 참고 정보 (한국복음서원 회복역):
{bible_context}

다음 영문을 한국어로 번역해 주세요:

{text}

번역 시 주의사항:
1. 위에 제공된 한국복음서원 회복역 성경구절을 정확히 사용하세요
2. 교회와 신앙 관련 전문용어는 제공된 사전을 참고하세요  
3. 겸손하고 진지한 어조를 유지하세요
4. 자연스러운 한국어 표현을 사용하세요
5. 성경구절 번역은 절대 추측하지 말고 위 정보를 정확히 활용하세요
"""
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"번역 오류: {str(e)}"

# Check password first
if not check_password():
    st.stop()

# Check API configuration
if not setup_gemini_api():
    st.error("⚠️ API 설정에 문제가 있습니다. 관리자에게 문의하세요.")
    st.stop()

# Main UI
st.title("🙏 기도문 번역")

# Initialize session state
if 'translation_state' not in st.session_state:
    st.session_state.translation_state = 'input'  # 'input', 'processing', 'result'
if 'korean_result' not in st.session_state:
    st.session_state.korean_result = ""

# Input state - show input form
if st.session_state.translation_state == 'input':
    st.markdown("#### 📝 번역할 기도문을 입력하세요 - Markdown / HTML")
    
    english_text = st.text_area(
        "",
        height=300,
        placeholder="",
        label_visibility="collapsed"
    )
    
    if st.button("번역"):
        if english_text.strip():
            st.session_state.english_input = english_text
            st.session_state.translation_state = 'processing'
            st.rerun()
        else:
            st.warning("번역할 텍스트를 입력해주세요.")

# Processing state - show only spinner, hide everything else
elif st.session_state.translation_state == 'processing':
    # Empty container to push spinner to center
    st.empty()
    
    with st.spinner("번역 중입니다..."):
        # Load resources
        word_dict = load_translation_dict()
        instructions = load_translation_instructions()
        
        # Translate
        korean_text = translate_with_gemini(
            st.session_state.english_input, 
            instructions, 
            word_dict
        )
        
        st.session_state.korean_result = korean_text
        st.session_state.translation_state = 'result'
        st.rerun()

# Result state - show translation result
elif st.session_state.translation_state == 'result':
    st.markdown("#### 🇰🇷 한글 번역 결과:")
    
    st.markdown(st.session_state.korean_result)
    
    # Add some space before button
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Copy button with JavaScript functionality
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("📋 복사하기", use_container_width=True):
            # Create JavaScript to copy to clipboard and show browser confirm
            import json
            copy_text = json.dumps(st.session_state.korean_result)
            components.html(f"""
                <div>
                    <button id="copyBtn" style="
                        background-color: #1e3a8a;
                        color: white;
                        border: none;
                        border-radius: 8px;
                        padding: 8px 16px;
                        font-weight: 600;
                        font-size: 16px;
                        cursor: pointer;
                        width: 100%;
                        margin: 10px 0;
                    ">📋 텍스트 복사</button>
                    <script>
                        const textToCopy = {copy_text};
                        document.getElementById('copyBtn').addEventListener('click', function() {{
                            // Use the more reliable textarea method
                            const textArea = document.createElement('textarea');
                            textArea.value = textToCopy;
                            textArea.style.position = 'fixed';
                            textArea.style.left = '-999999px';
                            textArea.style.top = '-999999px';
                            document.body.appendChild(textArea);
                            textArea.focus();
                            textArea.select();
                            
                            try {{
                                const successful = document.execCommand('copy');
                                if (successful) {{
                                    alert('복사가 완료되었습니다. 기도문 준비 문서에 "Edit - Paste from Markdown"을 사용해 붙여 넣어주세요.');
                                }} else {{
                                    alert('복사에 실패했습니다.');
                                }}
                            }} catch (err) {{
                                alert('복사에 실패했습니다.');
                            }}
                            
                            document.body.removeChild(textArea);
                        }});
                    </script>
                </div>
            """, height=80)
    
