내가 "번역해 줘"라고 명령하면:
- **에이전트 역할**: 에이전트는 `skills/translator/SKILL.md`의 지침을 따릅니다.
- **프로세스**: 
  1. `inputs/raw.html`을 읽고 성경 구절을 식별합니다.
  2. `curl` 등을 사용하여 `rv.or.kr`에서 정확한 성경 구절을 가져옵니다.
  3. `skills/translator/SKILL.md`의 번역 지침과 `skills/translator/resources/WORDS.csv`를 참고하여 직접 번역하고 `workspace/translated.md`에 저장합니다.

내가 "변환해 줘"라고 명령하면:
- **에이전트 역할**: 에이전트는 `skills/parser/SKILL.md`의 지침을 따릅니다.
- **프로세스**: `workspace/translated.md` 파일을 읽고, `skills/parser/SKILL.md`에 정의된 규칙에 따라 변환하여 `outputs/final.html`에 저장합니다.
