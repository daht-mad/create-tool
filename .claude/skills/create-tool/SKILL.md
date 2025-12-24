---
name: create-tool
description: |
  비개발자를 위한 AI 도구 자동 생성기. 자연어 대화만으로 완전한 Claude Code 슬래시 커맨드 도구를 만듭니다.
  다음과 같은 요청에 이 스킬을 사용하세요:
  - "새 도구 만들어줘"
  - "CLI 도구 생성해줘"
  - "자동화 도구 만들고 싶어"
  - "슬래시 커맨드 만들어줘"
  - "/create-tool"
  - "도구 생성"
allowed-tools: Bash(git:*), Bash(npm:*), Bash(mkdir:*), Bash(which:*), Bash(gh:*), Bash(node:*), Bash(ls:*)
---

# create-tool

비개발자도 자연어 대화만으로 완전한 CLI 도구를 만들고 GitHub에 배포할 수 있습니다.

## 프로세스 개요

1. 대화로 요구사항 파악
2. 자동 코드 생성
3. 로컬 테스트
4. GitHub 배포
5. 설치 명령어 제공

## 워크플로우

자세한 단계별 가이드는 [WORKFLOW.md](references/WORKFLOW.md)를 참조하세요.

## 시작하기

대화로 시작합니다:
```
안녕하세요! 어떤 도구를 만들고 싶으세요?
편하게 설명해 주시면 제가 도와드릴게요.
```

사용자 아이디어를 듣고 자연스럽게 질문하며 요구사항을 파악합니다.

## 코드 템플릿

프로젝트 생성 시 사용할 템플릿은 [TEMPLATES.md](references/TEMPLATES.md)를 참조하세요.

## 네임스페이스 규칙

- npm 패키지명: `@[스코프]/[도구이름]` (예: @daht-mad/md2pdf)
- bin 명령어: `[스코프토큰]-[도구이름]` (예: dahtmad-md2pdf)
- Claude 커맨드: `/[도구이름]`

## 완료 시 제공 정보

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
