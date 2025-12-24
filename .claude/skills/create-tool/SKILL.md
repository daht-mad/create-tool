---
name: create-tool
description: |
  비개발자를 위한 AI 도구 자동 생성기. 자연어 대화만으로 CLI 도구를 만들고 GitHub에 배포하여 팀원들이 한 줄로 설치할 수 있게 합니다.
  다음과 같은 요청에 이 스킬을 사용하세요:
  - "새 도구 만들어줘"
  - "CLI 도구 생성해줘"
  - "자동화 도구 만들고 싶어"
  - "슬래시 커맨드 만들어줘"
  - "/create-tool"
  - "도구 생성"
  - "팀에서 쓸 도구 만들어줘"
allowed-tools: Bash(git:*), Bash(npm:*), Bash(mkdir:*), Bash(which:*), Bash(gh:*), Bash(node:*), Bash(ls:*)
---

# create-tool

비개발자도 자연어 대화만으로 CLI 도구를 만들고, GitHub에 배포하여 **팀원들이 한 줄 명령어로 설치**할 수 있게 합니다.

## 핵심 가치

```
1. 대화로 도구 생성 → 2. GitHub 자동 배포 → 3. 팀원이 한 줄로 설치
```

## 워크플로우 개요

1. **대화** - 도구 아이디어를 자연어로 설명
2. **생성** - 코드, 문서 자동 생성
3. **테스트** - 로컬에서 동작 확인
4. **배포** - GitHub에 자동 푸시
5. **공유** - 한 줄 설치 명령어 제공

자세한 단계별 가이드: [WORKFLOW.md](references/WORKFLOW.md)

## 시작하기

대화로 시작:
```
안녕하세요! 어떤 도구를 만들고 싶으세요?
편하게 설명해 주시면 제가 도와드릴게요.
```

## 네임스페이스 규칙

| 항목 | 형식 | 예시 |
|------|------|------|
| npm 패키지 | `@[스코프]/[도구이름]` | @daht-mad/md2pdf |
| CLI 명령어 | `[스코프토큰]-[도구이름]` | dahtmad-md2pdf |
| 슬래시 커맨드 | `/[도구이름]` | /md2pdf |

## 완료 시 출력

```
🎉 도구 생성 완료!

📦 저장소: https://github.com/[사용자명]/[도구이름]

📥 팀원 설치 명령어 (한 줄):
mkdir -p .claude/commands && curl -o .claude/commands/[도구이름].md \
  https://raw.githubusercontent.com/[사용자명]/[도구이름]/master/.claude/commands/[도구이름].md

🚀 사용법:
- Claude Code: /[도구이름] [인자들]
- 터미널: [스코프토큰]-[도구이름] [인자들]
```

## 템플릿

코드 및 설정 파일 템플릿: [TEMPLATES.md](references/TEMPLATES.md)

## 출력 패턴

일관된 출력을 위한 패턴: [OUTPUT-PATTERNS.md](references/OUTPUT-PATTERNS.md)
