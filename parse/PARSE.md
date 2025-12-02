### 목적
- Markdown 파일을 HTML 포맷으로 변환합니다.

### 변환 규칙
- **HTML 스켈레톤 미생성**: `<!doctype html>`, `<html>`, `<body>` 등의 HTML 기본 포맷은 생성하지 않습니다. 입력 본문만 규칙에 따라 HTML 조각(fragment)으로 변환합니다.
- **상단 제목 무시**: 첫 번째 비어있지 않은 줄이 `#`로 시작하고 `주간 기도문`을 포함하면, 해당 줄은 HTML에 포함하지 않습니다.
- **제목**: `#`로 시작하는 줄은 모두 `<h3>`로 변환합니다. (개수 무관, 굵게 표기 `**`는 제거)
- **목록**: `* `로 시작하는 줄들은 연속 구간을 하나의 `<ul>`로 감싸고 각 줄을 `<li>`로 변환합니다.
- **문단**: 그 외 비어있지 않은 줄은 `<p>`로 감싸서 문단으로 변환합니다. 빈 줄은 구분 용도로만 사용하고 HTML 출력하지 않습니다.
- 영문과 한글이 번갈아 가며 나오는 파일이라면, 결과물에서 영어는 제외합니다.

### 변환 대상
parse 폴더 내에, 혹은 root directory 에서 [🙏 기도문 준비 📋.md] 라는 이름의 파일을 찾습니다.
만일 파일이 여러개인 경우라면 나에게 어떤 파일을 변환해야 할지 물어봅니다.

### 결과물 위치
root_directory에 [PARSED_OUTPUT.html] 라는 파일을 생성, 혹은 덮어쓰기

### 마무리 작업
변환을 마치면, 변환된 작업물 전체를 <div class="korean-section"> 태그로 감싸고, 가장 상단에 아래와 같은 코드를 붙입니다:
```
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nanum+Myeongjo&display=swap" rel="stylesheet">
<style>
.korean-section { 
  h3, p, li { font-family: "Nanum Myeongjo", serif !important; } 
  h3:not(:first-child) { margin-top: 72px; }
  table {
    th, td { padding: 8px; }
  }
}
</style>
```
위에 붙인 이 코드와 작업물 사이에 new line을 추가하지 않도록 합니다.