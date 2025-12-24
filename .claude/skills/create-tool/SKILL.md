---
name: create-tool
version: 1.1.1
repo: daht-mad/create-tool
description: |
  비개발자를 위한 AI 스킬 자동 생성기. 자연어 대화만으로 Claude Code 스킬을 만들고 GitHub에 배포하여 팀원들이 한 줄로 설치할 수 있게 합니다.
  이 스킬 실행 시 플랜모드로 진입하여 사용자와 대화하며 기획을 구체화합니다.
  다음과 같은 요청에 이 스킬을 사용하세요:
  - "/create-tool"
  - "새 스킬 만들어줘"
  - "도구 만들고 싶어"
  - "자동화 스킬 만들어줘"
  - "팀에서 쓸 스킬 만들어줘"
  - "스킬 생성"
allowed-tools: Bash(git:*), Bash(npm:*), Bash(mkdir:*), Bash(which:*), Bash(gh:*), Bash(python3:*), Bash(ls:*), Bash(tar:*), Bash(curl:*)
---

# create-tool

비개발자도 자연어 대화만으로 스킬을 만들고, GitHub에 배포하여 **팀원들이 한 줄 명령어로 설치**할 수 있게 합니다.

## 핵심 가치

```
1. 대화로 스킬 생성 → 2. GitHub 자동 배포 → 3. 팀원이 한 줄로 설치
```

## 워크플로우 개요

1. **대화** - 스킬 아이디어를 자연어로 설명
2. **생성** - SKILL.md, scripts, references 자동 생성
3. **검증** - quick_validate.py로 검증
4. **배포** - GitHub에 자동 푸시
5. **공유** - 한 줄 설치 명령어 제공 (GitHub Archive API 활용)

자세한 단계별 가이드: [WORKFLOW.md](references/WORKFLOW.md)

## 시작하기

대화로 시작:
```
안녕하세요! 어떤 스킬을 만들고 싶으세요?
편하게 설명해 주시면 제가 도와드릴게요.
```

## 스킬 구조

```
skill-name/
├── README.md          # 필수: GitHub 배포용 (사람용)
├── SKILL.md           # 필수: 스킬 정의 (AI용)
├── scripts/           # 선택: 실행 스크립트
├── references/        # 선택: 참조 문서
└── assets/            # 선택: 템플릿, 이미지 등
```

## 완료 시 출력

```
🎉 스킬 생성 완료!

📦 저장소: https://github.com/[사용자명]/[스킬이름]

📥 팀원 설치 명령어 (한 줄):
mkdir -p .claude/skills && curl -sL https://github.com/[사용자명]/[스킬이름]/archive/refs/heads/master.tar.gz | tar -xz -C /tmp && mv /tmp/[스킬이름]-master .claude/skills/[스킬이름]

🚀 사용: 스킬 트리거 조건에 맞는 요청을 하면 자동 실행됩니다.
```

## 스크립트

스킬 생성 시 사용할 스크립트:

| 스크립트 | 용도 |
| -------- | ---- |
| `scripts/init_skill.py` | 새 스킬 초기화 |
| `scripts/quick_validate.py` | 스킬 검증 |
| `scripts/check_update.py` | 스킬 업데이트 확인 |
| `scripts/contribute_fix.py` | 버그 수정 PR 제출 |

## 템플릿

스킬 작성 시 참고할 템플릿: [TEMPLATES.md](references/TEMPLATES.md)

## README 작성

GitHub 저장소 README 작성 가이드: [README-GUIDE.md](references/README-GUIDE.md)

## 버그 수정 기여

설치한 스킬에서 버그를 발견했다면, 원작자에게 PR을 보내 기여할 수 있습니다:

```bash
python3 .claude/skills/create-tool/scripts/contribute_fix.py [스킬경로] --message "버그 설명"
```

자세한 가이드: [WORKFLOW.md - 버그 수정 및 기여 가이드](references/WORKFLOW.md#버그-수정-및-기여-가이드)

### 스킬 수정 감지 시 자동 기여 제안

**중요**: 사용자가 설치한 스킬의 파일을 수정했다면, 수정 완료 후 다음과 같이 기여 여부를 물어보세요:

```
수정하신 내용을 원작자에게 PR로 보내시겠어요?
다른 사용자들도 이 수정사항을 받을 수 있습니다.

1. 예, PR 보내기
2. 아니요, 로컬에서만 사용
```

사용자가 "예"를 선택하면:

```bash
python3 .claude/skills/create-tool/scripts/contribute_fix.py [스킬경로] --message "[수정 내용 요약]"
```

## 출력 패턴

일관된 출력을 위한 패턴: [OUTPUT-PATTERNS.md](references/OUTPUT-PATTERNS.md)

## 자동 업데이트

각 스킬에 포함된 `scripts/check_update.py`를 사용하여 독립적으로 업데이트 확인:

```bash
python3 .claude/skills/[스킬이름]/scripts/check_update.py --auto --quiet
```

**중요**: 스킬 실행 전 업데이트 확인을 수행해야 합니다.
