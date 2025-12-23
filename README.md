# Claude Code 도구 자동 생성 시스템

**비개발자도 AI와 대화만으로 자동화 도구를 만들고 배포할 수 있는 혁신적인 시스템**

## 핵심 개념

이 시스템은 **Claude Code의 슬래시 커맨드 기능**을 활용하여:
1. 비개발자가 **자연어로** 기능을 설명
2. Claude가 **자동으로 코드 생성, 테스트, 배포**
3. 결과물을 **한 줄 명령어로 공유** 가능

## 빠른 시작

### 설치 (한 줄 명령어)

**Claude Code용:**

```bash
mkdir -p .claude/commands && curl -o .claude/commands/create-tool.md https://raw.githubusercontent.com/daht-mad/create-tool/master/.claude/commands/create-tool.md
```

**Antigravity (Google AI IDE)용:**

```bash
mkdir -p .agent/rules && curl -o .agent/rules/create-tool.md https://raw.githubusercontent.com/daht-mad/create-tool/master/.agent/rules/create-tool.md
```

설치 후 `/create-tool`로 바로 사용 가능합니다.

### 비개발자라면

👉 [비개발자 가이드](./NON-DEVELOPER-GUIDE.md)를 읽어보세요!

간단히 말하면:

```
1. 위 설치 명령어 실행
2. /create-tool 입력
3. Claude와 대화하며 원하는 기능 설명
4. 완성된 도구를 팀과 공유!
```

### 개발자라면

👉 [작동 원리 문서](./HOW-IT-WORKS.md)를 읽어보세요!

시스템 아키텍처와 기술적 세부사항을 확인할 수 있습니다.

## 시스템 구성

```
이 저장소
├── .claude/
│   └── commands/
│       └── create-tool.md        ⭐ Claude Code용 커맨드
├── .agent/
│   └── rules/
│       └── create-tool.md        ⭐ Antigravity용 규칙
├── md2pdf/                       📁 예시 도구 (마크다운 → PDF)
├── pdf2excel/                    📁 예시 도구 (PDF 표 → Excel)
├── org-matcher/                  📁 예시 도구 (조직명 유사도 매칭)
├── sheets-wrapper/               📁 예시 도구 (Google Sheets API 래퍼)
├── log-update/                   📁 예시 도구 (대화 내역 문서화)
├── HOW-IT-WORKS.md              📖 기술 문서 (개발자용)
├── NON-DEVELOPER-GUIDE.md       📖 사용 가이드 (비개발자용)
└── README.md                    📖 이 파일
```

## 주요 특징

### ✨ 코딩 없이 도구 제작
- 자연어 대화만으로 도구 생성
- TypeScript, npm, Git 등 몰라도 됨
- Claude가 모든 기술적 작업 자동 처리

### 🔀 멀티 IDE 지원
- **Claude Code**: `.claude/commands/` 디렉토리 사용
- **Antigravity (Google AI IDE)**: `.agent/rules/` 디렉토리 사용
- 두 환경 모두 자동 설정 파일 생성

### 💬 맥락 확인 (Step 0)
- 사용자가 인자 없이 커맨드 실행 시 필요한 정보 질문
- 모호한 요청에 대해 명확화 후 실행
- 에이전트가 먼저 맥락을 파악하여 정확한 작업 수행

### 🚀 원클릭 배포
- GitHub 저장소 자동 생성
- curl 명령어 하나로 설치 가능
- 팀 공유 즉시 가능

### 🔧 자동 업데이트
- 도구 개선 시 자동 재배포
- 사용자는 다음 실행 시 자동 업데이트
- 버전 관리 자동화

### 🎯 실용적인 도구
- 파일 변환 (PDF, 이미지, CSV 등)
- 데이터 처리 (압축, 분석, 정리)
- 자동화 (배포, 백업, 리포트)

## 사용 예시

### 예시 1: 이미지 압축 도구 만들기

```
나: /create-tool
Claude: 어떤 기능을 만들고 싶으신가요?
나: 이미지를 압축해서 파일 크기를 줄이고 싶어요

[3분 후]

Claude: ✓ img-compress 도구 생성 완료!

설치:
curl -o .claude/commands/img-compress.md https://raw.githubusercontent.com/username/img-compress/master/.claude/commands/img-compress.md

사용:
/img-compress ./photos
```

### 예시 2: 엑셀 → JSON 변환기

```
나: /create-tool
Claude: 어떤 기능을 만들고 싶으신가요?
나: 엑셀 파일에서 특정 열만 JSON으로 추출하고 싶어요

[3분 후]

Claude: ✓ excel-to-json 도구 생성 완료!

사용:
/excel-to-json ./data.xlsx
```

## 만들 수 있는 도구 아이디어

### 📄 문서 처리
- Markdown → PDF
- PDF → 이미지
- CSV → HTML 테이블
- JSON → Excel

### 🖼️ 이미지 처리
- 일괄 압축
- 리사이즈
- 포맷 변환
- 워터마크 추가

### 📊 데이터 분석
- 로그 파일 분석
- CSV 데이터 통계
- Git 커밋 통계
- 코드 복잡도 분석

### 🤖 자동화
- 배포 자동화
- 백업 자동화
- 리포트 생성
- 알림 발송

## 시스템 작동 방식 (간단 버전)

```
1. 사용자: "/create-tool" 입력
   ↓
2. Claude: 필요한 정보 질문
   ↓
3. 사용자: 자연어로 답변
   ↓
4. Claude:
   - 프로젝트 구조 생성
   - TypeScript 코드 작성
   - 테스트 실행
   - GitHub 저장소 생성
   - 문서 자동 생성
   ↓
5. 완성! 🎉
   - 설치 명령어 제공
   - 즉시 사용 가능
   - 팀과 공유 가능
```

자세한 내용은 [HOW-IT-WORKS.md](./HOW-IT-WORKS.md) 참고

## 필요 환경

### 최소 요구사항
- **VSCode** (최신 버전)
- **Claude Code** 확장 프로그램
- **Node.js** 18.0.0 이상
- **Git** 2.0.0 이상
- **GitHub 계정**

### 선택 사항
- **GitHub CLI** (gh) - 자동 배포에 편리
- **npm 계정** - npm 퍼블리싱 시 필요

### 설치 확인

```bash
node --version   # v18.0.0+
npm --version    # 9.0.0+
git --version    # 2.0.0+
gh --version     # (선택사항)
```

## 예시 도구: md2pdf

이 저장소에는 실제로 작동하는 예시 도구가 포함되어 있습니다:

**[md2pdf](./md2pdf/)** - Markdown을 PDF로 변환

### 설치
```bash
mkdir -p .claude/commands && curl -o .claude/commands/md2pdf.md https://raw.githubusercontent.com/daht-mad/md2pdf/master/.claude/commands/md2pdf.md
```

### 사용
```
/md2pdf README.md
```

### 특징
- 한글 폰트 지원
- 재귀적 파일 검색
- 중복 파일 선택 UI
- 자동 설치

이 도구를 참고해서 새로운 도구를 만들 수 있습니다!

## 프로젝트 구조 상세

### 생성되는 도구의 표준 구조

```
your-tool/
├── .claude/
│   └── commands/
│       └── your-tool.md       # Claude 슬래시 커맨드 정의
│
├── src/
│   └── your-tool.ts           # 메인 로직 (TypeScript)
│
├── bin/
│   └── your-tool.js           # CLI 진입점
│
├── dist/                      # 빌드 결과물 (자동 생성)
│
├── package.json               # npm 패키지 설정
├── tsconfig.json              # TypeScript 설정
├── .gitignore                 # Git 제외 파일
├── README.md                  # 사용자 문서
├── LICENSE                    # MIT 라이선스
└── HOW-IT-WORKS.md           # 기술 문서 (선택)
```

### 핵심 파일: .claude/commands/your-tool.md

이 파일이 **가장 중요**합니다!

```markdown
# /your-tool - 도구 설명

## Installation Check & Auto-Install
1. which your-tool로 확인
2. 없으면 자동 설치:
   - git clone
   - npm install
   - npm build
   - npm link

## Execution Steps
1. 입력 검증
2. 파일 검색
3. 처리 실행
4. 결과 리포트
```

Claude가 이 파일을 읽고 **자동으로 실행**합니다!

## 기술 스택

### 자동 생성되는 도구
- **언어**: TypeScript
- **런타임**: Node.js
- **패키지 관리**: npm
- **버전 관리**: Git
- **호스팅**: GitHub

### 라이브러리 (도구 기능에 따라 자동 선택)
- **PDF**: puppeteer, pdf-lib
- **이미지**: sharp, jimp
- **Excel**: xlsx
- **CSV**: csv-parser
- **Markdown**: marked
- **CLI**: commander, chalk

## 장점

### 사용자 관점
- ✅ 비개발자도 사용 가능
- ✅ 자연어로 소통
- ✅ 즉시 사용 가능
- ✅ 팀 공유 쉬움

### 개발자 관점
- ✅ 코드 작성 자동화
- ✅ 테스트 자동화
- ✅ 배포 자동화
- ✅ 문서 자동 생성

### 조직 관점
- ✅ 생산성 향상
- ✅ 지식 공유 촉진
- ✅ 반복 작업 자동화
- ✅ 유지보수 비용 절감

## 제한사항

- Claude Code 구독 필요 (유료)
- Node.js 기반 도구만 생성 가능
- GitHub public 저장소 권장
- 복잡한 GUI는 지원 안 됨 (CLI 도구만)

## 로드맵

### 현재 버전 (v1.0)
- ✅ 기본 CLI 도구 생성
- ✅ TypeScript 지원
- ✅ GitHub 자동 배포
- ✅ 문서 자동 생성

### 향후 계획
- [ ] Python 도구 지원
- [ ] GUI 래퍼 자동 생성
- [ ] npm 자동 퍼블리싱
- [ ] CI/CD 파이프라인 통합
- [ ] 도구 마켓플레이스
- [ ] 버전 관리 자동화

## 기여하기

이 시스템을 개선하고 싶으시다면:

1. 이 저장소 Fork
2. 기능 브랜치 생성 (`git checkout -b feature/amazing`)
3. 변경사항 커밋 (`git commit -m 'Add amazing feature'`)
4. 브랜치에 Push (`git push origin feature/amazing`)
5. Pull Request 생성

### 기여 아이디어
- 새로운 도구 템플릿 추가
- 에러 처리 개선
- 문서 번역 (영어, 일본어 등)
- 예시 도구 추가

## 문제 해결

### 일반적인 문제

**Q: "command not found" 에러**
```bash
# Node.js 설치 확인
node --version

# 없다면 설치
# macOS: brew install node
# Windows: https://nodejs.org 에서 다운로드
```

**Q: GitHub 저장소 생성 실패**
```bash
# GitHub CLI 설치 (선택사항)
# macOS: brew install gh
# Windows: winget install GitHub.cli

# 또는 수동으로 https://github.com/new 에서 생성
```

**Q: npm link 권한 에러**
```bash
sudo npm link
```

**Q: 빌드 에러**
```bash
# node_modules 삭제 후 재설치
rm -rf node_modules package-lock.json
npm install
npm run build
```

## 라이선스

MIT License - 자유롭게 사용, 수정, 배포 가능

## 제작자

이 시스템은 **Claude Code의 슬래시 커맨드 기능**을 최대한 활용하여 만들어졌습니다.

### 연락처
- GitHub Issues: 버그 리포트
- GitHub Discussions: 아이디어 공유, 질문
- Pull Requests: 기여 환영!

## 관련 링크

- [Claude Code 공식 문서](https://claude.com/claude-code)
- [Node.js 공식 사이트](https://nodejs.org)
- [GitHub CLI](https://cli.github.com)
- [TypeScript 문서](https://www.typescriptlang.org)

## 감사의 말

- **Anthropic**: Claude Code 플랫폼 제공
- **오픈소스 커뮤니티**: 수많은 npm 패키지
- **모든 사용자**: 피드백과 기여

---

## 시작하기

준비되셨나요?

```
/create-tool
```

입력하고 Claude와 대화를 시작하세요! 🚀

**당신의 첫 도구를 만들어보세요!**

---

<div align="center">

**Made with ❤️ using Claude Code**

[시작하기](./NON-DEVELOPER-GUIDE.md) | [기술 문서](./HOW-IT-WORKS.md) | [예시 도구](./md2pdf/)

</div>
