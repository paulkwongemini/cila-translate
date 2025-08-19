#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import sys
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 성경책 이름을 (버전, 인덱스) 튜플로 매핑
BIBLE_BOOKS = {
    # 구약 성경 (bibleVer=0)
    "창세기": (0, 1), "창": (0, 1),
    "출애굽기": (0, 2), "출": (0, 2),
    "레위기": (0, 3), "레": (0, 3),
    "민수기": (0, 4), "민": (0, 4),
    "신명기": (0, 5), "신": (0, 5),
    "여호수아": (0, 6), "수": (0, 6),
    "사사기": (0, 7), "삿": (0, 7),
    "룻기": (0, 8), "룻": (0, 8),
    "사무엘상": (0, 9), "삼상": (0, 9),
    "사무엘하": (0, 10), "삼하": (0, 10),
    "열왕기상": (0, 11), "왕상": (0, 11),
    "열왕기하": (0, 12), "왕하": (0, 12),
    "역대상": (0, 13), "대상": (0, 13),
    "역대하": (0, 14), "대하": (0, 14),
    "에스라": (0, 15), "스": (0, 15),
    "느헤미야": (0, 16), "느": (0, 16),
    "에스더": (0, 17), "더": (0, 17),
    "욥기": (0, 18), "욥": (0, 18),
    "시편": (0, 19), "시": (0, 19),
    "잠언": (0, 20), "잠": (0, 20),
    "전도서": (0, 21), "전": (0, 21),
    "아가": (0, 22), "아": (0, 22),
    "이사야": (0, 23), "사": (0, 23),
    "예레미야": (0, 24), "렘": (0, 24),
    "예레미야애가": (0, 25), "애": (0, 25),
    "에스겔": (0, 26), "겔": (0, 26),
    "다니엘": (0, 27), "단": (0, 27),
    "호세아": (0, 28), "호": (0, 28),
    "요엘": (0, 29), "욜": (0, 29),
    "아모스": (0, 30), "암": (0, 30),
    "오바댜": (0, 31), "옵": (0, 31),
    "요나": (0, 32), "욘": (0, 32),
    "미가": (0, 33), "미": (0, 33),
    "나훔": (0, 34), "나": (0, 34),
    "하박국": (0, 35), "합": (0, 35),
    "스바냐": (0, 36), "습": (0, 36),
    "학개": (0, 37), "학": (0, 37),
    "스가랴": (0, 38), "슥": (0, 38),
    "말라기": (0, 39), "말": (0, 39),
    
    # 신약 성경 (bibleVer=1)
    "마태복음": (1, 1), "마태": (1, 1), "마": (1, 1),
    "마가복음": (1, 2), "마가": (1, 2),
    "누가복음": (1, 3), "누가": (1, 3),
    "요한복음": (1, 4), "요한": (1, 4),
    "사도행전": (1, 5), "행전": (1, 5), "행": (1, 5),
    "로마서": (1, 6), "로마": (1, 6), "롬": (1, 6),
    "고린도전서": (1, 7), "고전": (1, 7),
    "고린도후서": (1, 8), "고후": (1, 8),
    "갈라디아서": (1, 9), "갈라디아": (1, 9), "갈": (1, 9),
    "에베소서": (1, 10), "에베소": (1, 10), "에베": (1, 10), "엡": (1, 10),
    "빌립보서": (1, 11), "빌립보": (1, 11), "빌": (1, 11),
    "골로새서": (1, 12), "골로새": (1, 12), "골": (1, 12),
    "데살로니가전서": (1, 13), "살전": (1, 13),
    "데살로니가후서": (1, 14), "살후": (1, 14),
    "디모데전서": (1, 15), "딤전": (1, 15),
    "디모데후서": (1, 16), "딤후": (1, 16),
    "디도서": (1, 17), "디도": (1, 17), "딛": (1, 17),
    "빌레몬서": (1, 18), "빌레몬": (1, 18), "몬": (1, 18),
    "히브리서": (1, 19), "히브리": (1, 19), "히": (1, 19),
    "야고보서": (1, 20), "야고보": (1, 20), "약": (1, 20),
    "베드로전서": (1, 21), "벧전": (1, 21),
    "베드로후서": (1, 22), "벧후": (1, 22),
    "요한일서": (1, 23), "요일": (1, 23),
    "요한이서": (1, 24), "요이": (1, 24),
    "요한삼서": (1, 25), "요삼": (1, 25),
    "유다서": (1, 26), "유다": (1, 26), "유": (1, 26),
    "요한계시록": (1, 27), "계시록": (1, 27), "계": (1, 27),
}

def parse_verse_reference(verse_ref):
    """
    '빌립보서3장11절' 형태의 문자열을 파싱하여 (책이름, 장, 절)을 반환
    """
    # 정규식으로 책이름, 장, 절 추출
    patterns = [
        r'(.+?)(\d+)장(\d+)절',  # 빌립보서3장11절
        r'(.+?)(\d+)편(\d+)절',  # 시편23편1절
        r'(.+?)\s*(\d+):(\d+)', # 빌립보서 3:11
        r'(.+?)\s+(\d+)\s+(\d+)', # 빌립보서 3 11
    ]
    
    for pattern in patterns:
        match = re.match(pattern, verse_ref.strip())
        if match:
            book_name = match.group(1).strip()
            chapter = int(match.group(2))
            verse = int(match.group(3))
            return book_name, chapter, verse
    
    raise ValueError(f"구절 형식을 인식할 수 없습니다: {verse_ref}")

def get_book_info(book_name):
    """책 이름을 (버전, 인덱스) 튜플로 변환"""
    if book_name in BIBLE_BOOKS:
        return BIBLE_BOOKS[book_name]
    
    # 부분 매칭 시도
    for key, value in BIBLE_BOOKS.items():
        if book_name in key or key in book_name:
            return value
    
    raise ValueError(f"성경책을 찾을 수 없습니다: {book_name}")

def get_bible_verse(book_name, chapter, verse_num):
    """
    한국복음서원 회복역에서 성경 구절을 가져옴
    """
    try:
        # 책 정보 찾기 (버전, 인덱스)
        bible_ver, book_index = get_book_info(book_name)
        
        # URL 구성 (구약=0, 신약=1)
        url = f"http://rv.or.kr/read_recovery.php?bibleVer={bible_ver}&bibVerse=&bibOutline=&bibleSelOp={book_index}&bibChapt={chapter}"
        
        # 웹페이지 가져오기
        response = requests.get(url, verify=False, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            raise Exception(f"웹페이지를 가져올 수 없습니다. Status: {response.status_code}")
        
        # HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 해당 절 찾기
        verse_div = soup.find('div', {'class': 'num', 'id': str(verse_num)})
        if not verse_div:
            raise Exception(f"{verse_num}절을 찾을 수 없습니다.")
        
        # 절 텍스트 찾기 (다음 형제 요소에서)
        parent_verse = verse_div.find_parent('div', class_='verse')
        if parent_verse:
            text_div = parent_verse.find('div', class_='text')
            if text_div:
                return text_div.get_text(strip=True)
        
        raise Exception(f"{verse_num}절의 텍스트를 찾을 수 없습니다.")
        
    except Exception as e:
        return f"오류: {e}"

def main():
    """메인 함수"""
    if len(sys.argv) != 2:
        print("사용법: python bible_verse_scraper.py '빌립보서3장11절'")
        print("예시: python bible_verse_scraper.py '빌립보서3장11절'")
        print("      python bible_verse_scraper.py '로마서8장28절'")
        sys.exit(1)
    
    verse_reference = sys.argv[1]
    
    try:
        # 구절 참조 파싱
        book_name, chapter, verse_num = parse_verse_reference(verse_reference)
        
        # 성경 구절 가져오기
        verse_text = get_bible_verse(book_name, chapter, verse_num)
        
        # 결과 출력
        print(verse_text)
        
    except Exception as e:
        print(f"오류: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()