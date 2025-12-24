# Commands vs Skills 비교 분석

## 목적

> **"비개발자가 AI 도구를 쉽게 만들고, 다른 비개발자도 쉽게 사용"**

이 문서는 위 목적을 달성하기 위해 Claude Code의 두 가지 확장 방식을 비교합니다.

---

## 공식 문서 출처

- **Commands**: https://code.claude.com/docs/en/slash-commands
- **Skills**: https://code.claude.com/docs/en/skills

> **주의**: 이 문서는 **Claude Code**의 Commands/Skills를 다룹니다.
> Claude API의 "Agent Skills"(platform.claude.com)와는 다른 개념입니다.

---

## 핵심 차이점 요약

| 구분 | Commands | Skills |
|------|----------|--------|
| **호출 방식** | 명시적 (`/명령어`) | 자동 (Claude가 판단) |
| **구조** | 단일 `.md` 파일 | `SKILL.md` + 지원 파일들 (디렉토리) |
| **Bash 실행** | ✅ 가능 | ✅ 가능 (allowed-tools 설정) |
| **외부 프로그램** | ✅ 가능 | ✅ 가능 |
| **네트워크** | ✅ 가능 | ✅ 가능 |
| **실행 환경** | 로컬 머신 | 로컬 머신 |

**두 방식 모두 로컬에서 실행되므로, 기술적 제한은 동일합니다.**

---

## 예시 도구 3가지

| 도구 | 기능 | 필요한 외부 프로그램 |
|------|------|---------------------|
| **md2pdf** | 마크다운 → PDF 변환 | puppeteer, mermaid-cli |
| **video-trim** | 영상 자르기/편집 | ffmpeg |
| **img-optimize** | 이미지 압축/리사이즈 | sharp, imagemagick |

---

## 1. 호출 방식 비교

### Commands (명시적 호출)

```
사용자: /md2pdf README.md
Claude: (커맨드 실행) PDF 생성 완료!
```

```
사용자: /video-trim input.mp4 00:30 01:00
Claude: (ffmpeg 실행) 영상 자르기 완료!
```

```
사용자: /img-optimize ./images/
Claude: (sharp 실행) 12개 이미지 압축 완료!
```

**인자 없이 호출 시 (대화형):**

```
사용자: /video-trim
Claude: 어떤 영상 파일을 자를까요?
사용자: input.mp4
Claude: 시작 시간을 알려주세요 (예: 00:30)
사용자: 00:30
Claude: 끝 시간을 알려주세요 (예: 01:00)
사용자: 01:00
Claude: (ffmpeg 실행) 영상 자르기 완료!
```

→ **슬래시 명령 후 필요한 인자는 대화 형식으로 수집 가능**

### Skills (자동 감지)

```
사용자: "README를 PDF로 만들어줘"
Claude: (md2pdf Skill 자동 감지 → 실행) PDF 생성 완료!
```

```
사용자: "이 영상 30초부터 1분까지 잘라줘"
Claude: (video-trim Skill 자동 감지) "어떤 파일인가요?"
사용자: input.mp4
Claude: (ffmpeg 실행) 영상 자르기 완료!
```

```
사용자: "images 폴더 이미지들 용량 줄여줘"
Claude: (img-optimize Skill 자동 감지 → 실행) 12개 이미지 압축 완료!
```

---

## 2. 파일 구조 비교

### Commands

```
.claude/commands/
└── md2pdf.md          # 단일 파일
```

**md2pdf.md 예시:**
```markdown
---
allowed-tools: Bash(dahtmad-md2pdf:*), Bash(git:*), Bash(npm:*)
---

# /md2pdf - 마크다운을 PDF로 변환

## 실행 단계
1. 설치 확인: `which dahtmad-md2pdf`
2. 없으면 자동 설치
3. 실행: `dahtmad-md2pdf <파일>`
```

### Skills

```
.claude/skills/
└── md2pdf/
    ├── SKILL.md       # 필수: 메인 파일
    ├── INSTALL.md     # 선택: 설치 가이드
    └── EXAMPLES.md    # 선택: 사용 예시
```

**SKILL.md 예시:**

```markdown
---
name: md2pdf
description: 마크다운 파일을 PDF로 변환합니다. 사용자가 PDF 변환, 문서 출력을 요청할 때 사용하세요.
allowed-tools: Bash(dahtmad-md2pdf:*), Bash(git:*), Bash(npm:*)
---

# md2pdf

마크다운을 PDF로 변환하는 도구입니다.

## 설치 확인
[INSTALL.md](INSTALL.md) 참조

## 사용법
`dahtmad-md2pdf <파일경로>`
```

---

## 3. 실제 파일 내용 비교 (md2pdf 예시)

### Commands 방식: `.claude/commands/md2pdf.md`

**단일 파일로 모든 내용 포함:**

```markdown
---
allowed-tools: Bash(dahtmad-md2pdf:*), Bash(git:*), Bash(npm:*), Bash(which:*), Bash(cd:*)
---

# /md2pdf - 마크다운을 PDF로 변환

마크다운 파일을 고품질 PDF로 변환합니다.

## 실행 단계

### Step 1: 설치 확인
\`\`\`bash
which dahtmad-md2pdf
\`\`\`

### Step 2: 설치되어 있지 않으면 자동 설치
\`\`\`bash
git clone https://github.com/daht-mad/md2pdf.git /tmp/dahtmad-md2pdf
cd /tmp/dahtmad-md2pdf && npm install && npm link
\`\`\`

### Step 3: 변환 실행
\`\`\`bash
dahtmad-md2pdf $ARGUMENTS
\`\`\`

## 사용법
/md2pdf <파일경로>

## 예시
/md2pdf README.md
```

**특징:**
- `$ARGUMENTS`: 슬래시 명령 뒤에 입력한 인자가 자동으로 대입됨
- 파일 1개로 완결
- `/md2pdf README.md` 형태로 호출

---

### Skills 방식: `.claude/skills/md2pdf/SKILL.md`

**YAML frontmatter에 description 필수:**

```markdown
---
name: md2pdf
description: |
  마크다운 파일을 PDF로 변환합니다.
  다음과 같은 요청에 이 스킬을 사용하세요:
  - "PDF로 변환해줘"
  - "마크다운을 PDF로"
  - "문서 출력해줘"
  - "PDF 만들어줘"
  - "PDF로 내보내기"
allowed-tools: Bash(dahtmad-md2pdf:*), Bash(git:*), Bash(npm:*), Bash(which:*), Bash(cd:*)
---

# md2pdf

마크다운 파일을 고품질 PDF로 변환하는 도구입니다.

## 실행 전 확인사항

### Step 1: 설치 확인
\`\`\`bash
which dahtmad-md2pdf
\`\`\`

### Step 2: 설치되어 있지 않으면 자동 설치
\`\`\`bash
git clone https://github.com/daht-mad/md2pdf.git /tmp/dahtmad-md2pdf
cd /tmp/dahtmad-md2pdf && npm install && npm link
\`\`\`

## 사용법
\`\`\`bash
dahtmad-md2pdf <마크다운_파일_경로>
\`\`\`

## 주요 기능
- Mermaid 다이어그램 자동 렌더링
- 한글 폰트 지원
- GitHub Flavored Markdown 지원
```

**특징:**
- `name`: 스킬 식별자 (필수)
- `description`: Claude가 언제 이 스킬을 사용할지 판단하는 핵심 (필수)
- `$ARGUMENTS` 없음: 자연어에서 파일 경로를 파싱해야 함
- "README를 PDF로 만들어줘" 형태로 호출

---

### 핵심 차이점 요약

| 항목 | Commands | Skills |
|------|----------|--------|
| **필수 frontmatter** | `allowed-tools` | `name`, `description`, `allowed-tools` |
| **인자 처리** | `$ARGUMENTS`로 자동 대입 | Claude가 자연어에서 추출 |
| **호출 트리거** | `/명령어` 입력 시 | `description`과 일치하는 자연어 |
| **파일 구조** | 단일 `.md` 파일 | `SKILL.md` 필수 (디렉토리) |

---

## 4. 배포/공유 비교

### Commands

**설치 명령어 (한 줄):**
```bash
mkdir -p .claude/commands && curl -o .claude/commands/md2pdf.md https://raw.githubusercontent.com/daht-mad/md2pdf/master/.claude/commands/md2pdf.md
```

**장점:**
- 파일 1개만 다운로드
- 간단한 curl 명령어

### Skills

**설치 명령어 (여러 줄 또는 스크립트):**
```bash
mkdir -p .claude/skills/md2pdf
curl -o .claude/skills/md2pdf/SKILL.md https://raw.githubusercontent.com/.../SKILL.md
curl -o .claude/skills/md2pdf/INSTALL.md https://raw.githubusercontent.com/.../INSTALL.md
```

또는 zip 다운로드 후 압축 해제:
```bash
curl -L https://github.com/.../archive/master.zip -o /tmp/skill.zip
unzip /tmp/skill.zip -d .claude/skills/
```

**단점:**
- 디렉토리 구조 필요
- 여러 파일 다운로드 또는 압축 해제

---

## 4. 장단점 상세 비교

### Commands 장점

| 장점 | 설명 |
|------|------|
| **단순한 구조** | 파일 1개로 완결 |
| **배포 간편** | curl 한 줄로 설치 |
| **예측 가능** | `/명령어` 입력 시 항상 실행 |
| **인자 전달 명확** | `/video-trim input.mp4 00:30 01:00` |
| **버전 관리 쉬움** | 파일 1개만 업데이트 |

### Commands 단점

| 단점 | 설명 |
|------|------|
| **명령어 암기** | 사용자가 `/md2pdf` 등을 알아야 함 |
| **발견성 낮음** | `/help`로 확인해야 함 |
| **단일 파일 제약** | 복잡한 문서 분리 어려움 |

### Skills 장점

| 장점 | 설명 |
|------|------|
| **자연어 호출** | "PDF로 변환해줘"로 실행 가능 |
| **자동 발견** | Claude가 맥락에 맞는 Skill 선택 |
| **문서 분리** | 여러 파일로 체계적 구성 가능 |
| **확장성** | 복잡한 워크플로우 지원 |

### Skills 단점

| 단점 | 설명 |
|------|------|
| **배포 복잡** | 디렉토리 구조 필요 |
| **불확실성** | Claude가 Skill 선택 안 할 수도 있음 |
| **description 의존** | 설명이 부정확하면 감지 실패 |
| **인자 파싱** | 자연어에서 인자 추출 필요 |

---

## 5. 사용자 경험 시나리오

### 시나리오 1: 첫 사용자가 도구 사용

**Commands:**
```
사용자: (README를 보고) /md2pdf 입력해야 하는구나
사용자: /md2pdf README.md
Claude: PDF 생성 완료!
```
→ 명령어를 알아야 하지만, 알면 확실히 동작

**Skills:**
```
사용자: README를 PDF로 만들어줘
Claude: (Skill 자동 감지) PDF 생성 완료!
```
→ 명령어 몰라도 됨, 하지만 Skill이 감지 안 될 수도 있음

### 시나리오 2: 복잡한 인자 전달

**Commands:**
```
사용자: /video-trim input.mp4 00:30 01:00 --output cut.mp4
Claude: (명확한 인자) 영상 자르기 완료!
```

**Skills:**
```
사용자: input.mp4를 30초부터 1분까지 자르고 cut.mp4로 저장해
Claude: (자연어 파싱) 영상 자르기 완료!
```
→ 파싱 실패 가능성 있음

### 시나리오 3: 도구 목록 확인

**Commands:**
```
사용자: /help
Claude: 사용 가능한 명령어:
  /md2pdf - 마크다운을 PDF로 변환
  /video-trim - 영상 자르기
  /img-optimize - 이미지 압축
```

**Skills:**
```
사용자: 어떤 도구들을 쓸 수 있어?
Claude: (Skills 목록 나열) md2pdf, video-trim, img-optimize...
```
→ 둘 다 가능하지만 Commands가 더 명시적

---

## 6. 기술적 비교

### 외부 프로그램 실행

**Commands:**
```markdown
---
allowed-tools: Bash(ffmpeg:*), Bash(npm:*)
---
```

**Skills:**
```markdown
---
name: video-trim
description: 영상을 자릅니다
allowed-tools: Bash(ffmpeg:*), Bash(npm:*)
---
```

**결론: 동일하게 가능**

### 자동 설치/업데이트

**Commands:**
```markdown
## 실행 전 단계

### Step 1: 설치 확인
\`\`\`bash
which dahtmad-md2pdf
\`\`\`

### Step 2: 없으면 설치
\`\`\`bash
git clone ... && npm install && npm link
\`\`\`
```

**Skills:**
```markdown
## 설치 확인

도구가 설치되어 있는지 확인하고, 없으면 자동 설치합니다.

[INSTALL.md](INSTALL.md) 참조
```

**결론: 동일하게 가능** (로컬 실행이므로 git, npm 모두 사용 가능)

---

## 7. 선택 가이드

### Commands를 선택해야 할 때

- ✅ **배포를 최대한 간단하게** 하고 싶을 때
- ✅ **명확한 인자 전달**이 필요할 때 (파일 경로, 시간 등)
- ✅ **항상 동일한 동작**을 보장하고 싶을 때
- ✅ **비개발자에게 명령어 하나만** 알려주면 되는 상황

### Skills를 선택해야 할 때

- ✅ **자연어로 호출**하고 싶을 때
- ✅ **복잡한 워크플로우**를 여러 문서로 구성할 때
- ✅ Claude가 **맥락에 따라 자동 선택**하길 원할 때
- ✅ **발견성**이 중요할 때 (사용자가 명령어를 몰라도 됨)

---

## 8. 결론

### 기술적으로는 동등

| 기능 | Commands | Skills |
|------|----------|--------|
| 외부 프로그램 실행 | ✅ | ✅ |
| 자동 설치/업데이트 | ✅ | ✅ |
| 네트워크 접근 | ✅ | ✅ |
| 파일 시스템 접근 | ✅ | ✅ |

### 차이는 "사용자 경험"

| 측면 | Commands | Skills |
|------|----------|--------|
| **호출 방식** | 명시적 `/명령어` | 자연어 |
| **배포 난이도** | 쉬움 (파일 1개) | 보통 (디렉토리) |
| **예측 가능성** | 높음 | 보통 |
| **발견성** | 낮음 | 높음 |

### create-tool에서의 선택

현재 create-tool은 **Commands 방식**을 사용합니다.

**이유:**
1. **배포 간편**: 파일 1개로 완결
2. **명확한 인자 전달**: `/md2pdf README.md`
3. **예측 가능**: 명령어 입력 시 항상 실행
4. **비개발자 안내 용이**: "터미널에 `/md2pdf` 입력하세요"

**향후 고려사항:**
- Skills 방식도 지원하여 사용자 선택권 제공 가능
- 하이브리드 접근: Commands로 배포, Skills로 자동 발견

---

## 9. 다른 AI 도구에서 사용하기

Claude Code의 Commands/Skills와 동일한 방식으로 다른 AI 코딩 도구에서도 커스텀 명령을 만들고 배포할 수 있습니다.

### 도구별 비교

| AI 도구 | 커스텀 명령 방식 | 설정 위치 | 문서 |
|---------|-----------------|-----------|------|
| **Claude Code** | `.claude/commands/*.md` | 프로젝트 루트 | [공식 문서](https://docs.anthropic.com/en/docs/claude-code/slash-commands) |
| **Cursor** | `.cursor/rules/*.md` 또는 `.cursorrules` | 프로젝트 루트 | [Cursor Rules](https://docs.cursor.com/context/rules-for-ai) |
| **Windsurf** | `.windsurfrules` | 프로젝트 루트 | [Windsurf Rules](https://docs.windsurf.com/windsurf/memories#memories-and-rules) |
| **GitHub Copilot** | `.github/copilot-instructions.md` | 프로젝트 루트 | [Copilot Instructions](https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot) |
| **Trae** | `.trae/rules/*.md` | 프로젝트 루트 | [Trae Rules](https://docs.trae.ai/ide/customize-ai-with-rules) |

### Cursor에서 사용하기

**1. Rules 파일 생성:**

```
.cursor/rules/
└── md2pdf.md
```

**md2pdf.md 예시:**

```markdown
# md2pdf 규칙

사용자가 "PDF로 변환", "마크다운을 PDF로" 등을 요청하면:

1. dahtmad-md2pdf 설치 확인: `which dahtmad-md2pdf`
2. 없으면 설치:
   ```bash
   git clone https://github.com/daht-mad/md2pdf.git /tmp/md2pdf
   cd /tmp/md2pdf && npm install && npm link
   ```
3. 실행: `dahtmad-md2pdf <파일경로>`
```

**2. 또는 .cursorrules 파일 (프로젝트 전역):**

```markdown
# 프로젝트 규칙

## PDF 변환
마크다운 파일을 PDF로 변환할 때는 dahtmad-md2pdf를 사용하세요.
설치: npm install -g dahtmad-md2pdf
실행: dahtmad-md2pdf <파일>
```

**3. 배포:**

```bash
# 단일 파일 배포
mkdir -p .cursor/rules && curl -o .cursor/rules/md2pdf.md https://raw.githubusercontent.com/daht-mad/md2pdf/master/.cursor/rules/md2pdf.md
```

### Windsurf에서 사용하기

**1. .windsurfrules 파일 생성:**

```markdown
# Windsurf Rules

## md2pdf - 마크다운을 PDF로 변환

사용자가 PDF 변환을 요청하면:

1. 설치 확인: `which dahtmad-md2pdf`
2. 없으면: `npm install -g dahtmad-md2pdf`
3. 실행: `dahtmad-md2pdf <파일>`
```

**2. 배포:**

```bash
curl -o .windsurfrules https://raw.githubusercontent.com/daht-mad/md2pdf/master/.windsurfrules
```

### GitHub Copilot에서 사용하기

**1. .github/copilot-instructions.md 생성:**

```markdown
# Copilot Instructions

## PDF 변환 도구

마크다운을 PDF로 변환할 때:
- 도구: dahtmad-md2pdf
- 설치: `npm install -g dahtmad-md2pdf`
- 사용: `dahtmad-md2pdf <파일경로>`
```

**2. 배포:**

```bash
mkdir -p .github && curl -o .github/copilot-instructions.md https://raw.githubusercontent.com/daht-mad/md2pdf/master/.github/copilot-instructions.md
```

### Trae에서 사용하기

**1. .trae/rules/ 디렉토리에 규칙 파일 생성:**

```
.trae/rules/
└── md2pdf.md
```

**md2pdf.md 예시:**

```markdown
# md2pdf

마크다운 파일을 PDF로 변환하는 도구입니다.

## 사용 조건
- 사용자가 "PDF 변환", "마크다운을 PDF로" 등을 요청할 때

## 실행 방법
1. 설치 확인: `which dahtmad-md2pdf`
2. 설치: `npm install -g dahtmad-md2pdf`
3. 실행: `dahtmad-md2pdf <파일경로>`
```

**2. 배포:**

```bash
mkdir -p .trae/rules && curl -o .trae/rules/md2pdf.md https://raw.githubusercontent.com/daht-mad/md2pdf/master/.trae/rules/md2pdf.md
```

### 멀티 플랫폼 배포 전략

하나의 도구를 여러 AI 코딩 도구에서 사용할 수 있도록 배포하려면:

**저장소 구조:**

```
my-tool/
├── .claude/commands/my-tool.md    # Claude Code용
├── .cursor/rules/my-tool.md       # Cursor용
├── .trae/rules/my-tool.md         # Trae용
├── .windsurfrules                 # Windsurf용
├── .github/copilot-instructions.md # GitHub Copilot용
├── install.sh                     # 통합 설치 스크립트
└── README.md
```

**통합 설치 스크립트 (install.sh):**

```bash
#!/bin/bash

# 사용할 AI 도구 감지 및 설치
REPO_URL="https://raw.githubusercontent.com/user/my-tool/master"

# Claude Code
if [ -d ".claude" ] || command -v claude &> /dev/null; then
  mkdir -p .claude/commands
  curl -o .claude/commands/my-tool.md "$REPO_URL/.claude/commands/my-tool.md"
  echo "✅ Claude Code 설치 완료"
fi

# Cursor
if [ -d ".cursor" ]; then
  mkdir -p .cursor/rules
  curl -o .cursor/rules/my-tool.md "$REPO_URL/.cursor/rules/my-tool.md"
  echo "✅ Cursor 설치 완료"
fi

# Windsurf
if [ -f ".windsurfrules" ] || [ -d ".windsurf" ]; then
  curl -o .windsurfrules "$REPO_URL/.windsurfrules"
  echo "✅ Windsurf 설치 완료"
fi

# Trae
if [ -d ".trae" ]; then
  mkdir -p .trae/rules
  curl -o .trae/rules/my-tool.md "$REPO_URL/.trae/rules/my-tool.md"
  echo "✅ Trae 설치 완료"
fi

# GitHub Copilot
if [ -d ".github" ]; then
  curl -o .github/copilot-instructions.md "$REPO_URL/.github/copilot-instructions.md"
  echo "✅ GitHub Copilot 설치 완료"
fi
```

### 핵심 차이점

| 특성 | Claude Code | Cursor | Windsurf | Copilot | Trae |
|------|-------------|--------|----------|---------|------|
| **슬래시 명령** | ✅ `/명령어` | ❌ | ❌ | ❌ | ❌ |
| **자동 감지** | Skills로 가능 | Rules로 가능 | Rules로 가능 | ✅ | Rules로 가능 |
| **allowed-tools** | ✅ 지원 | ❌ | ❌ | ❌ | ❌ |
| **디렉토리 구조** | 지원 | 지원 | 단일 파일 | 단일 파일 | 지원 |

**참고:**
- Claude Code만 `/명령어` 형태의 명시적 슬래시 커맨드를 지원
- 다른 도구들은 "규칙(Rules)" 또는 "지침(Instructions)" 형태로 AI 동작을 커스터마이징
- 다른 도구에서는 자연어로 요청하면 규칙에 따라 동작

---

## 부록: 공식 문서 인용

### Commands (Slash Commands)

> "Slash commands are reusable prompt templates that expand when you type them."
>
> "Use the `allowed-tools` frontmatter field to specify which tools the command can use."
>
> — https://code.claude.com/docs/en/slash-commands

### Skills

> "Skills are markdown files (SKILL.md) with YAML frontmatter that Claude automatically discovers and uses when relevant."
>
> "Use the `allowed-tools` frontmatter field to limit which tools Claude can use when a Skill is active."
>
> — https://code.claude.com/docs/en/skills
