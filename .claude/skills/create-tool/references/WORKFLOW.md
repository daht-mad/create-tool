# 워크플로우 가이드

## Phase 1: 대화로 요구사항 파악

선택지나 양식을 바로 보여주지 말고, 친근한 대화로 시작하세요.

### 질문 방식
- 대화 흐름에 맞춰 하나씩 질문 (한 번에 여러 개 X)
- 사용자 답변에 맞춰 유연하게 진행
- 필요한 정보: 주요 기능, 입력 데이터, 출력 형태, 특별 요구사항

### 예시 대화
```
사용자: 엑셀 파일을 JSON으로 바꾸고 싶어요
Claude: 아, 엑셀을 JSON으로 변환하는 도구군요!
        혹시 여러 시트가 있는 엑셀도 처리해야 하나요?
사용자: 네, 시트별로 따로 저장했으면 좋겠어요
Claude: 좋아요. 그럼 출력 파일명은 어떻게 할까요?
```

요구사항이 충분히 파악되면 플랜 모드로 진입합니다.

## Phase 2: 저장 위치 확인

프로젝트를 생성하기 전에 저장 위치를 확인합니다:
```
도구를 어디에 저장할까요?
현재 위치: /Users/username/Documents

예시:
- /Users/username/Documents/DEV/create-tool 폴더 하위에 저장해줘
- 현재 폴더에 저장해줘
```

## Phase 3: 프로젝트 설정

```bash
# 지정된 위치로 이동
cd [저장위치]

# 프로젝트 구조 생성
mkdir -p [도구이름]/{src,bin,.claude/commands}
cd [도구이름]

# npm 초기화
npm init -y

# 의존성 설치
npm install -D typescript @types/node
npm install [필요한-패키지들]
```

### 프로젝트 구조 판단

**단순 구조 (bin만 사용) - 기본값**
- 소스 파일 3개 이하
- CLI 전용 도구
- 구조: `src/*.ts` → 빌드 → `bin/*.js`

**분리 구조 (dist + bin)**
- 소스 파일 4개 이상
- 라이브러리 + CLI 모두 제공
- 구조: `src/*.ts` → `dist/*.js`, `bin/cli.js`는 dist를 불러옴

### 네임스페이스 규칙

| 변수 | 예시 | 설명 |
|------|------|------|
| `[스코프]` | daht-mad | npm 스코프 |
| `[스코프토큰]` | dahtmad | 스코프에서 하이픈 제거 |
| `[도구이름]` | md2pdf | 도구 이름 |
| `[bin명령어]` | dahtmad-md2pdf | 실제 CLI 명령어 |

## Phase 4: 코드 생성

생성할 파일:
1. `src/[도구이름].ts` - 메인 로직
2. `.claude/commands/[도구이름].md` - Claude 커맨드
3. `README.md` - 문서

## Phase 5: 빌드 및 테스트

```bash
npm run build
npm link
[스코프토큰]-[도구이름] [테스트-인자]
```

## Phase 6: Git 및 GitHub

```bash
git init
git add .
git commit -m "Initial commit: [도구 설명]"
gh repo create [도구이름] --public --source=. --remote=origin --push
```

GitHub CLI가 없으면 수동 방법 안내:
1. https://github.com/new 접속
2. 저장소 이름 입력
3. git remote add origin 후 push

## Phase 7: 완료 요약

```
🎉 도구 생성 완료!

📦 npm 패키지: @[스코프]/[도구이름]
📦 저장소: https://github.com/[사용자명]/[도구이름]

📥 설치 명령어:
mkdir -p .claude/commands && curl -o .claude/commands/[도구이름].md \
  https://raw.githubusercontent.com/[사용자명]/[도구이름]/master/.claude/commands/[도구이름].md

🚀 사용법:
- Claude Code: /[도구이름] [인자들]
- 터미널: [스코프토큰]-[도구이름] [인자들]
```

## 실행 환경별 설정 파일

### Claude Code
- 위치: `.claude/commands/[도구이름].md`

### Antigravity
- 위치: `.agent/rules/[도구이름].md`
- YAML frontmatter 필요:
```yaml
---
trigger: glob
glob: "**/*"
---
```
