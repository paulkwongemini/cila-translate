# 🚀 배포 가이드 (Deployment Guide)

교회 기도문 번역 서비스를 웹에 배포하는 방법을 안내합니다.

## 📋 배포 전 준비사항

1. **Google Gemini API 키 발급**
   - [Google AI Studio](https://makersuite.google.com/app/apikey) 접속
   - 무료 API 키 발급 (월 15,000 요청 제한)
   - API 키를 안전하게 보관

2. **GitHub 저장소 생성**
   - 프로젝트를 GitHub에 업로드
   - public 또는 private 저장소로 설정

## 🌟 추천: Streamlit Cloud 배포 (무료)

### 1단계: 프로젝트 준비
```bash
# GitHub에 코드 푸시
git add .
git commit -m "Add translation web app"
git push origin main
```

### 2단계: Streamlit Cloud 배포
1. [Streamlit Cloud](https://share.streamlit.io/) 접속
2. GitHub 계정으로 로그인
3. "New app" 클릭
4. GitHub 저장소 선택
5. 메인 파일: `streamlit_app.py`
6. "Deploy" 클릭

### 3단계: 환경변수 설정 (선택)
- Advanced settings에서 환경변수 설정 가능
- `GEMINI_API_KEY=your_api_key_here`

## 🛠 기타 배포 옵션

### Railway (무료 티어)
```bash
# Railway CLI 설치
npm install -g @railway/cli

# 배포
railway login
railway init
railway up
```

### Render (무료 티어)
1. [Render](https://render.com) 접속
2. GitHub 저장소 연결
3. Web Service 생성
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `streamlit run streamlit_app.py --server.port $PORT`

### Heroku
```bash
# Procfile 생성
echo "web: streamlit run streamlit_app.py --server.port \$PORT --server.address 0.0.0.0" > Procfile

# 배포
git add Procfile
git commit -m "Add Procfile"
git push heroku main
```

## 🔧 배포 후 설정

### 도메인 설정
- 대부분의 플랫폼에서 커스텀 도메인 설정 가능
- 예: `prayer-translator.yourdomain.com`

### SSL 인증서
- 모든 추천 플랫폼에서 자동 SSL 제공

### 환경변수 설정
각 플랫폼별 환경변수 설정:
- **Streamlit Cloud**: Settings → Secrets
- **Railway**: Variables 탭
- **Render**: Environment 탭
- **Heroku**: Config Vars

## 📊 사용량 모니터링

### Google Gemini API 사용량 확인
1. [Google Cloud Console](https://console.cloud.google.com/)
2. APIs & Services → Credentials
3. API 사용량 통계 확인

### 월간 사용량 제한
- 무료 티어: 15,000 요청/월
- 유료 전환 시 더 높은 제한

## 🔒 보안 고려사항

### API 키 보안
```bash
# 환경변수로 설정
export GEMINI_API_KEY="your_api_key"
```

### 사용량 제한
- 필요시 API 호출 빈도 제한 구현
- 사용자별 일일 사용량 제한

## 📈 성능 최적화

### 캐싱 활용
```python
@st.cache_data(ttl=3600)  # 1시간 캐싱
def cached_translation(text):
    return translate_text(text)
```

### 로딩 시간 개선
- 자주 사용되는 번역 결과 캐싱
- 성경구절 사전 로딩 최적화

## 🎯 사용자 피드백 수집

### 분석 도구 연동
- Google Analytics 추가
- 사용량 통계 수집

### 피드백 기능
- 번역 품질 평가 기능
- 개선 요청 수집

## 📞 문제 해결

### 자주 발생하는 문제들

1. **API 키 오류**
   - 환경변수가 올바르게 설정되었는지 확인
   - API 키 유효성 검사

2. **메모리 부족**
   - 배포 플랫폼의 메모리 제한 확인
   - 불필요한 패키지 제거

3. **성능 저하**
   - 캐싱 구현
   - API 호출 최적화

### 로그 확인
```bash
# Streamlit 로그 확인
streamlit logs

# Railway 로그 확인  
railway logs

# Heroku 로그 확인
heroku logs --tail
```

## 🚀 고급 배포 옵션

### Docker 컨테이너화
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Kubernetes 배포
- 대규모 사용자를 위한 확장성
- 로드 밸런싱 및 고가용성

이제 웹에서 누구나 사용할 수 있는 번역 서비스가 준비되었습니다! 🎉