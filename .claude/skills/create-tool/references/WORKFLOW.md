# 워크플로우 가이드

## Phase 1: 대화로 요구사항 파악 (플랜모드 진입)

선택지나 양식을 바로 보여주지 말고, 친근한 대화로 시작하세요.
**이 단계에서 플랜모드로 진입하여 사용자와 대화하며 기획을 구체화합니다.**

### 필수 수집 정보

대화를 통해 다음 정보를 수집합니다:

| 항목 | 설명 | 기본값 |
| ---- | ---- | ------ |
| **스킬 기능** | 무엇을 하는 스킬인지 | - |
| **트리거 조건** | 어떤 요청에 반응할지 | - |
| **저장소 위치** | 스킬을 어디에 저장할지 | 현재 프로젝트의 `.claude/skills/` |
| **GitHub 계정명** | 배포할 GitHub 사용자명 | - |
| **스크립트 필요 여부** | 실행 스크립트가 필요한지 | 필요 시 |

### 질문 방식
- 대화 흐름에 맞춰 하나씩 질문 (한 번에 여러 개 X)
- 사용자 답변에 맞춰 유연하게 진행
- 기본값이 있는 항목은 사용자가 원하면 그대로 사용

### 예시 대화

```text
Claude: 어떤 스킬을 만들고 싶으세요?
사용자: PDF를 엑셀로 변환하는 스킬이요

Claude: PDF를 엑셀로 변환하는 스킬이군요!
        어떤 상황에서 이 스킬이 작동하면 좋을까요?
사용자: "PDF를 엑셀로", "표 추출해줘" 같은 요청이요

Claude: 좋아요! 스킬을 저장할 위치는 어디로 할까요?
        (기본: 현재 프로젝트의 .claude/skills/)
사용자: 기본으로 해줘

Claude: GitHub에 배포할 때 사용할 계정명이 뭔가요?
사용자: daht-mad

Claude: 마지막으로, 변환 스크립트도 포함할까요?
사용자: 네, Python으로요

Claude: 알겠습니다! 정리하면:
        - 스킬명: pdf2excel
        - 기능: PDF 표를 Excel로 변환
        - 트리거: "PDF를 엑셀로", "표 추출해줘"
        - 저장 위치: .claude/skills/
        - GitHub: daht-mad/pdf2excel
        - 스크립트: Python

        이대로 진행할까요?
```

요구사항이 충분히 파악되면 다음 Phase로 진행합니다.

## Phase 2: 저장 위치 확인

스킬을 생성하기 전에 저장 위치를 확인합니다:
```
스킬을 어디에 저장할까요?
현재 위치: /Users/username/Documents

예시:
- .claude/skills 폴더에 저장해줘
- ~/my-skills 에 저장해줘
```

## Phase 3: 스킬 초기화

init_skill.py를 사용하여 기본 구조 생성:

```bash
python3 scripts/init_skill.py [스킬이름] --path [저장위치]
```

생성되는 구조:
```
skill-name/
├── SKILL.md           # 스킬 정의 (필수)
├── scripts/           # 실행 스크립트
│   └── example.py
├── references/        # 참조 문서
│   └── example.md
└── assets/            # 템플릿, 이미지 등
    └── README.md
```

## Phase 4: SKILL.md 작성

### Frontmatter (필수)

```yaml
---
name: skill-name
version: 1.0.0
repo: username/skill-name
description: |
  스킬 설명. 다음과 같은 요청에 이 스킬을 사용하세요:
  - "트리거 예시 1"
  - "트리거 예시 2"
---
```

**버전 필드 설명:**

- `version`: 시맨틱 버전 (예: 1.0.0, 1.0.1)
- `repo`: GitHub 저장소 경로 (예: daht-mad/md2pdf)

이 필드들은 자동 업데이트 기능을 위해 필요합니다.

### 본문 구성

- 스킬 개요
- 사용 방법
- 스크립트/참조 파일 링크

## Phase 5: 리소스 작성

필요에 따라 작성:

| 디렉토리 | 용도 | 예시 |
| -------- | ---- | ---- |
| scripts/ | 실행 스크립트 | convert.py, process.sh |
| references/ | 참조 문서 | api-docs.md, schema.md |
| assets/ | 출력용 파일 | template.html, logo.png |

## Phase 6: 검증

quick_validate.py로 스킬 검증:

```bash
python3 scripts/quick_validate.py [스킬경로]
```

검증 항목:
- SKILL.md 존재 여부
- frontmatter 필수 필드 (name, description)
- TODO 플레이스홀더 제거 여부
- 참조 파일 존재 여부

## Phase 7: 패키징

package_skill.py로 배포 파일 생성:

```bash
python3 scripts/package_skill.py [스킬경로] [출력경로]
```

생성 파일:

- `[스킬이름].skill` - zip 형태
- `[스킬이름].tar.gz` - tar.gz 형태

### 업데이트 배포 시

스킬을 업데이트하여 재배포할 때는 반드시 SKILL.md의 `version`을 올려야 합니다:

```yaml
version: 1.0.0  →  version: 1.0.1
```

버전을 올리지 않으면 기존 사용자에게 업데이트가 전달되지 않습니다.

## Phase 8: Git 및 GitHub 배포

```bash
git init
git add .
git commit -m "feat: [스킬이름] 스킬 추가"
gh repo create [스킬이름] --public --source=. --remote=origin --push
```

GitHub CLI가 없으면 수동 방법 안내:

1. https://github.com/new 접속
2. 저장소 이름 입력
3. git remote add origin 후 push

### 저장소 생성 후 repo 필드 업데이트

GitHub 저장소 생성 후, `gh repo view --json owner,name`으로 정확한 저장소 경로를 확인하고 SKILL.md의 `repo` 필드를 업데이트합니다:

```bash
# 저장소 정보 확인
gh repo view --json owner,name

# SKILL.md의 repo 필드 업데이트
repo: [owner]/[name]
```

그 후 다시 패키징하고 push합니다:

```bash
# 재패키징
python3 scripts/package_skill.py [스킬경로] [출력경로]

# 변경사항 커밋 및 push
git add .
git commit -m "fix: repo 필드 업데이트"
git push
```

## Phase 9: 완료 요약

```
🎉 스킬 생성 완료!

📦 저장소: https://github.com/[사용자명]/[스킬이름]

📥 팀원 설치 명령어 (한 줄):
curl -L https://github.com/[사용자명]/[스킬이름]/raw/master/[스킬이름].tar.gz | tar -xz -C .claude/skills/

🚀 사용: 스킬 트리거 조건에 맞는 요청을 하면 자동 실행됩니다.
```

---

## 버그 수정 및 기여 가이드

설치한 스킬에서 버그를 발견하고 수정했다면, 원작자에게 PR을 보내 기여할 수 있습니다.

### 기여 워크플로우

1. **버그 수정**: `.claude/skills/[스킬이름]/` 폴더에서 직접 수정

2. **PR 제출 준비**:

   ```bash
   # 원본 저장소 fork (GitHub에서)
   # fork한 저장소 clone
   git clone https://github.com/[내계정]/[스킬이름].git
   cd [스킬이름]

   # 수정한 파일들 복사
   cp -r ~/.claude/skills/[스킬이름]/* .

   # 브랜치 생성 및 커밋
   git checkout -b fix/버그설명
   git add .
   git commit -m "fix: 버그 설명"
   git push origin fix/버그설명
   ```

3. **PR 생성**:

   ```bash
   gh pr create --title "fix: 버그 설명" --body "## 문제
   [버그 설명]

   ## 수정 내용
   [수정한 내용]

   ## 테스트
   [테스트 방법]"
   ```

### 자동화 스크립트 사용

contribute_fix.py 스크립트로 간편하게 PR을 제출할 수 있습니다:

```bash
python3 .claude/skills/create-tool/scripts/contribute_fix.py [스킬경로] --message "버그 설명"
```

스크립트가 자동으로:

- 원본 저장소 fork
- 수정사항 커밋
- PR 생성

### PR 머지 후

원작자가 PR을 머지하면:

1. 원작자가 버전 업데이트 후 재배포
2. 다른 사용자들이 자동 업데이트로 수정사항 받음
