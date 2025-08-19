# 🙏 교회 기도문 번역 서비스

Church Prayer Translation Service - 교회 기도문과 신앙 서적을 위한 전문 영한 번역 웹 애플리케이션

## ✨ 주요 기능

- **🤖 AI 번역**: Google Gemini API를 사용한 고품질 번역
- **📖 성경구절 자동 처리**: 한국복음서원 회복역 성경구절 자동 인식 및 번역
- **📚 전문용어 사전**: 교회/신앙 관련 전문용어 정확한 번역
- **🎨 직관적인 UI**: 사용하기 쉬운 웹 인터페이스
- **🆓 무료 사용**: Google Gemini 무료 API 티어 활용

## 🚀 빠른 시작

### 1. 프로젝트 클론 및 설치

```bash
# 가상환경 생성 (선택사항)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. Google Gemini API 키 발급

1. [Google AI Studio](https://makersuite.google.com/app/apikey)에서 무료 API 키 발급
2. 월 15,000 요청까지 무료 사용 가능

### 3. 애플리케이션 실행

```bash
streamlit run streamlit_app.py
```

브라우저에서 `http://localhost:8501`로 접속

### 4. 사용 방법

1. 사이드바에 Google Gemini API 키 입력
2. 왼쪽에 영문 기도문/텍스트 입력
3. "번역하기" 버튼 클릭
4. 오른쪽에서 번역 결과 확인

## 📁 프로젝트 구조

```
cila/
├── streamlit_app.py              # 메인 웹 애플리케이션
├── bible_verse_scraper.py        # 성경구절 스크래핑
├── requirements.txt              # Python 의존성
├── translate/
│   ├── TRANSLATE.md              # 번역 지침
│   ├── WORDS.csv                 # 전문용어 사전
│   ├── en                        # 영문 원본
│   └── output.md                 # 번역 결과
└── README.md                     # 이 파일
```

## 🌐 배포 옵션

### Streamlit Cloud (추천)

1. GitHub에 프로젝트 푸시
2. [Streamlit Cloud](https://streamlit.io/cloud)에서 배포
3. 무료 호스팅 가능

### 기타 플랫폼

- **Railway**: `railway login && railway deploy`
- **Render**: GitHub 연결 후 자동 배포
- **Heroku**: `git push heroku main`

## 🔧 설정

### 환경변수

```bash
# .env 파일 (선택사항)
GEMINI_API_KEY=your_api_key_here
```

### 번역 사전 수정

`translate/WORDS.csv` 파일을 수정하여 전문용어 추가:

```csv
en,ko
constitute,조성
redeem the time,시간을 구속하다
general subject,전체 주제
```

## 🤝 기여하기

1. 이슈 리포트: 버그나 개선사항 제안
2. 번역 품질 향상: 전문용어 사전 업데이트
3. 기능 추가: 새로운 기능 개발

## 📄 라이선스

이 프로젝트는 교회 사역을 위한 목적으로 개발되었습니다.

## 🆘 문제 해결

### 자주 묻는 질문

**Q: API 키 오류가 발생합니다**
A: Google AI Studio에서 발급받은 API 키가 올바른지 확인하세요.

**Q: 성경구절이 정확히 번역되지 않습니다**
A: bible_verse_scraper.py의 BIBLE_BOOKS 매핑을 확인하세요.

**Q: 번역 품질을 개선하고 싶습니다**
A: translate/WORDS.csv와 translate/TRANSLATE.md를 수정하세요.

## 📞 지원

기술적 문제나 질문이 있으시면 이슈를 생성해 주세요.