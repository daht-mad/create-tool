# create-tool

비개발자도 AI와 대화만으로 Claude Code 스킬을 만들고 배포할 수 있는 도구

---

## 핵심 가치

```
1. 대화로 스킬 생성 → 2. GitHub 자동 배포 → 3. 팀원이 한 줄로 설치
```

### 1. 대화만으로 스킬 생성

```
나: 새 스킬 만들어줘
Claude: 어떤 스킬을 만들고 싶으세요?
나: 마크다운을 PDF로 변환하고 싶어

[3분 후]

Claude: ✅ md2pdf 스킬 생성 완료!
📥 팀원 설치 명령어:
curl -L https://github.com/username/md2pdf/raw/master/md2pdf.tar.gz | tar -xz -C .claude/skills/
```

### 2. 한 줄로 설치

```bash
# 설치
mkdir -p .claude/skills && curl -L https://github.com/daht-mad/md2pdf/raw/master/md2pdf.tar.gz | tar -xz -C .claude/skills/

# 사용 - 자연어로 요청하면 자동 실행
"README.md를 PDF로 변환해줘"
```

---

## 설치

```bash
mkdir -p .claude/skills && curl -L https://github.com/daht-mad/create-tool/raw/master/create-tool.tar.gz | tar -xz -C .claude/skills/
```

## 사용

스킬 생성을 원하면 자연어로 요청:

```
"새 스킬 만들어줘"
"도구 만들고 싶어"
"팀에서 쓸 스킬 만들어줘"
```

---

## 작동 원리

### 스킬 구조

```
.claude/skills/skill-name/
├── SKILL.md           # 스킬 정의 (필수)
├── scripts/           # 실행 스크립트
├── references/        # 참조 문서
└── assets/            # 템플릿, 이미지 등
```

### 워크플로우

1. **대화** - 스킬 아이디어를 자연어로 설명
2. **생성** - SKILL.md, scripts, references 자동 생성
3. **검증** - 스킬 구조 검증
4. **패키징** - .tar.gz 생성
5. **배포** - GitHub에 자동 푸시
6. **공유** - 한 줄 설치 명령어 제공

### 자동 업데이트

스킬 실행 시 자동으로 최신 버전 확인 및 업데이트:

```
🔄 새 버전 발견: 1.0.0 → 1.0.1
📦 업데이트 중...
✅ 업데이트 완료!
```

버전 관리를 위해 SKILL.md에 다음 필드가 필요합니다:

```yaml
version: 1.0.0
repo: username/skill-name
```

---

## 예시 스킬

| 스킬 | 설명 | 설치 |
|------|------|------|
| **md2pdf** | 마크다운 → PDF | `curl -L https://github.com/daht-mad/md2pdf/raw/master/md2pdf.tar.gz \| tar -xz -C .claude/skills/` |
| **pdf2excel** | PDF 표 → Excel | `curl -L https://github.com/daht-mad/pdf2excel/raw/master/pdf2excel.tar.gz \| tar -xz -C .claude/skills/` |
| **org-matcher** | 조직명 매칭 | `curl -L https://github.com/daht-mad/org-matcher/raw/master/org-matcher.tar.gz \| tar -xz -C .claude/skills/` |
| **sheets-wrapper** | Google Sheets | `curl -L https://github.com/daht-mad/sheets-wrapper/raw/master/sheets-wrapper.tar.gz \| tar -xz -C .claude/skills/` |
| **log-update** | 대화 문서화 | `curl -L https://github.com/daht-mad/log-update/raw/master/log-update.tar.gz \| tar -xz -C .claude/skills/` |

---

## 필요 환경

- **VSCode** + **Claude Code** 확장 프로그램
- **Node.js** 18.0.0 이상 (스크립트 실행용)
- **Git** 2.0.0 이상
- **GitHub 계정** + **GitHub CLI** (배포용)

```bash
# 확인
node --version   # v18.0.0+
git --version    # 2.0.0+
gh --version     # 선택사항
```

---

## 라이선스

MIT License

---

<div align="center">

**Made with Claude Code**

</div>
