# README 생성 가이드

스킬의 GitHub 저장소에 포함될 README.md 작성 지침입니다.

## 필수 섹션

README는 간결하게 다음 내용만 포함합니다:

### 1. 스킬 이름 및 한 줄 설명

```markdown
# 스킬-이름

한 줄로 스킬이 하는 일을 설명합니다.
```

### 2. 기능 (Features)

주요 기능을 3-5개 이내로 간단히 나열합니다.

```markdown
## 기능

- 기능 1
- 기능 2
- 기능 3
```

### 3. 설치 방법

GitHub Archive API를 활용한 설치 명령어를 제공합니다. (저장소에 tar.gz 파일 불필요)

```markdown
## 설치

\`\`\`bash
mkdir -p .claude/skills && curl -L https://github.com/[사용자명]/[스킬이름]/archive/refs/heads/master.tar.gz | tar -xz -C /tmp && mv /tmp/[스킬이름]-master .claude/skills/[스킬이름]
\`\`\`
```

### 4. 필요 환경 (선택)

스킬 실행에 필요한 외부 도구나 설정이 있다면 명시합니다.

```markdown
## 필요 환경

- Python 3.8+
- `pip install pandas`
```

### 5. 기여자 (선택)

PR을 통해 기여한 사람이 있다면 명시합니다.

```markdown
## 기여자

- [@username](https://github.com/username) - 버그 수정
```

### 6. 업데이트 날짜

마지막 업데이트 날짜를 표시합니다.

```markdown
---

Last updated: 2024-12-24
```

## 전체 템플릿

```markdown
# 스킬-이름

한 줄 설명.

## 기능

- 기능 1
- 기능 2
- 기능 3

## 설치

\`\`\`bash
mkdir -p .claude/skills && curl -L https://github.com/[사용자명]/[스킬이름]/archive/refs/heads/master.tar.gz | tar -xz -C /tmp && mv /tmp/[스킬이름]-master .claude/skills/[스킬이름]
\`\`\`

## 필요 환경

- 필요한 도구/라이브러리 (없으면 이 섹션 생략)

## 기여자

- [@contributor](https://github.com/contributor) - 기여 내용 (없으면 이 섹션 생략)

---

Last updated: YYYY-MM-DD
```

## 주의사항

- 과도한 설명 금지: 사용법, 예시, 상세 문서는 SKILL.md나 references/ 에 포함
- 배지(badge) 남용 금지: 필요시 버전 배지 하나 정도만 사용
- 스크린샷/GIF: 시각적 도구인 경우에만 포함
