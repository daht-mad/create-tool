# Claude Code 도구 자동 생성 시스템

**비개발자도 AI와 대화만으로 자동화 도구를 만들고 배포할 수 있는 시스템**

Claude Code의 슬래시 커맨드 기능을 활용하여:
- 자연어로 원하는 기능을 설명하면 Claude가 코드 생성, 테스트, 배포까지 자동 처리
- 만들어진 도구는 curl 한 줄로 누구나 설치 가능
- Git, npm, 터미널 명령어를 몰라도 사용 가능

---

## 핵심 가치

### 1. 비개발자도 누구나 만들어서 딸깍 배포

```
나: /create-tool
Claude: 어떤 기능을 만들고 싶으신가요?
나: 이미지를 압축해서 파일 크기를 줄이고 싶어요

[3분 후]

Claude: ✅ img-compress 도구 생성 완료!
설치 명령어: curl -o .claude/commands/img-compress.md ...
```

### 2. 비개발자도 누구나 필요한 것 딸깍 설치

```bash
# 설치 (복사-붙여넣기 한 번)
mkdir -p .claude/commands && curl -o .claude/commands/md2pdf.md https://raw.githubusercontent.com/daht-mad/md2pdf/master/.claude/commands/md2pdf.md

# 사용
/md2pdf README.md
```

---

## 빠른 시작

### 설치

**Claude Code용:**
```bash
mkdir -p .claude/commands && curl -o .claude/commands/create-tool.md https://raw.githubusercontent.com/daht-mad/create-tool/master/.claude/commands/create-tool.md
```

**Antigravity (Google AI IDE)용:**
```bash
mkdir -p .agent/rules && curl -o .agent/rules/create-tool.md https://raw.githubusercontent.com/daht-mad/create-tool/master/.agent/rules/create-tool.md
```

### 사용

```
/create-tool
```

Claude와 대화하며 원하는 기능을 설명하면 끝!

---

## 작동 원리

### 전체 흐름

```
1. 도구 제작자 (개발자 또는 비개발자 + Claude)
   ↓
2. GitHub에 업로드
   ↓
3. 사용자가 명령어 설명서 다운로드 (curl 한 줄)
   ↓
4. Claude Code가 설명서를 읽고 자동 실행
   ↓
5. 실제 도구가 작동
```

### 핵심 개념: `.claude/commands/*.md`

이 파일은 **Claude Code에게 주는 각본**입니다:

```
"사용자가 /md2pdf를 입력하면:
1. 먼저 설치됐는지 확인해
2. 안 됐으면 GitHub에서 클론해서 설치해
3. 파일 찾아서
4. md2pdf 명령어 실행해
5. 결과 알려줘"
```

Claude가 이 파일을 읽고 **자동으로 실행**합니다.

### 맥락 확인 (Step 0)

모든 커맨드는 필요한 정보가 없으면 먼저 질문합니다:

```
사용자: /create-tool
Claude: 어떤 기능을 만들고 싶으신가요?
        예: 이미지 압축, 파일 변환, 데이터 처리 등
```

---

## 시스템 구성

```
create-tool/
├── .claude/commands/
│   ├── create-tool.md        ⭐ 도구 자동 생성 커맨드
│   └── deploy-all.md         ⭐ 일괄 배포 커맨드
├── .agent/rules/
│   └── create-tool.md        ⭐ Antigravity용 규칙
├── md2pdf/                   📁 마크다운 → PDF
├── pdf2excel/                📁 PDF 표 → Excel
├── org-matcher/              📁 조직명 유사도 매칭
├── sheets-wrapper/           📁 Google Sheets API 래퍼
├── log-update/               📁 대화 내역 문서화
└── docs/                     📖 문서
```

---

## 예시 도구

| 도구 | 설명 | 설치 |
|------|------|------|
| **md2pdf** | 마크다운 → PDF | `curl -o .claude/commands/md2pdf.md https://raw.githubusercontent.com/daht-mad/md2pdf/master/.claude/commands/md2pdf.md` |
| **pdf2excel** | PDF 표 → Excel | `curl -o .claude/commands/pdf2excel.md https://raw.githubusercontent.com/daht-mad/pdf2excel/master/.claude/commands/pdf2excel.md` |
| **org-matcher** | 조직명 매칭 | `curl -o .claude/commands/org-matcher.md https://raw.githubusercontent.com/daht-mad/org-matcher/master/.claude/commands/org-matcher.md` |
| **sheets-wrapper** | Google Sheets | `curl -o .claude/commands/sheets-wrapper.md https://raw.githubusercontent.com/daht-mad/sheets-wrapper/master/.claude/commands/sheets-wrapper.md` |
| **log-update** | 대화 문서화 | `curl -o .claude/commands/log-update.md https://raw.githubusercontent.com/daht-mad/log-update/master/.claude/commands/log-update.md` |

---

## 관리 커맨드

### /create-tool - 새 도구 생성

```
/create-tool
```

Claude가 질문하고 사용자가 답하면:
1. 프로젝트 구조 생성
2. TypeScript 코드 작성
3. 테스트 실행
4. GitHub 저장소 생성
5. 문서 자동 생성

### /deploy-all - 일괄 배포

```
/deploy-all "커밋 메시지"
```

모든 하위 도구와 create-tool을 한 번에 커밋/푸시합니다.

---

## 멀티 IDE 지원

| AI IDE | 설정 위치 | 파일 형식 |
|--------|----------|----------|
| **Claude Code** | `.claude/commands/` | `.md` |
| **Antigravity (Google)** | `.agent/rules/` | `.md` |
| **Cursor** | `.cursor/rules/` | `.mdc` |
| **Windsurf** | `.windsurf/rules/` | `.md` |
| **GitHub Copilot** | `.github/` | `.md` |

---

## 왜 혁신적인가?

### 기존 방식 (개발자만 가능)

```bash
git clone https://github.com/daht-mad/md2pdf.git
cd md2pdf
npm install
npm run build
npm link
md2pdf README.md
```

### 새로운 방식 (비개발자도 가능)

```bash
# 설치
curl -o .claude/commands/md2pdf.md https://raw.githubusercontent.com/daht-mad/md2pdf/master/.claude/commands/md2pdf.md

# 사용
/md2pdf README.md
```

**차이점:**
- Git, npm, 터미널 명령어 몰라도 됨
- Claude가 모든 복잡한 작업을 대신 처리
- 에러 처리도 Claude가 알아서 해결

---

## 메타포: Claude Code용 앱스토어

| 요소 | 역할 |
|------|------|
| **앱스토어** | GitHub 저장소 |
| **앱** | CLI 도구 (md2pdf, pdf2excel 등) |
| **앱 설치 링크** | `.claude/commands/*.md` |
| **앱 실행** | `/도구명` 슬래시 커맨드 |
| **앱 생성** | `/create-tool` |
| **일괄 배포** | `/deploy-all` |

---

## 필요 환경

- **VSCode** + **Claude Code** 확장 프로그램
- **Node.js** 18.0.0 이상
- **Git** 2.0.0 이상
- **GitHub 계정**

```bash
# 확인
node --version   # v18.0.0+
git --version    # 2.0.0+
```

---

## 문제 해결

**"command not found" 에러**
```bash
# Node.js 설치 확인
node --version
# 없다면: brew install node (macOS)
```

**GitHub 저장소 생성 실패**
```bash
# GitHub CLI 설치 (선택)
brew install gh
# 또는 https://github.com/new 에서 수동 생성
```

**npm link 권한 에러**
```bash
sudo npm link
```

---

## 관련 문서

- [비개발자 가이드](./NON-DEVELOPER-GUIDE.md)
- [자주 묻는 질문](./faq.md)

---

## 라이선스

MIT License

---

<div align="center">

**Made with Claude Code**

</div>
