내가 번역을 명령하면 [translate/TRANSLATE.md]를 수행해
내가 변환을 명령하면 [parse/PARSE.md]를 수행해

# 파일 인코딩 처리
한글이 포함된 파일을 생성할 때는 반드시 UTF-8 인코딩을 사용해야 해.
Write tool을 사용하면 인코딩 문제가 발생할 수 있으니, 한글이 포함된 파일을 생성할 때는 Python 스크립트를 사용하여 명시적으로 UTF-8 인코딩으로 작성해야 해.

예시:
```python
with open('output.md', 'w', encoding='utf-8') as f:
    f.write(content)
```