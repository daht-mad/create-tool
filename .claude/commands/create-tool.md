# /create-tool - 비개발자를 위한 AI 도구 자동 생성기

자연어 대화만으로 완전한 Claude Code 슬래시 커맨드 도구를 만듭니다. 코딩 불필요!

## 이 명령어가 하는 일

원하는 도구를 설명 → Claude가 모든 것을 자동 생성 → 바로 사용 및 공유 가능

## 사용법

```
/create-tool
```

입력 후 Claude와 대화하면 됩니다.

## 프로세스 개요

이 명령어는 다음 단계를 안내합니다:

1. **대화** - 도구 아이디어 설명
2. **자동 생성** - Claude가 모든 코드 작성
3. **테스트** - Claude가 로컬에서 테스트
4. **GitHub 배포** - Claude가 GitHub에 푸시
5. **공유 준비** - 설치 명령어 제공

## 단계별 워크플로우

### Phase 1: 자연스러운 대화로 요구사항 파악

**중요: 선택지나 양식을 바로 보여주지 말고, 친근한 대화로 시작하세요.**

시작 멘트 예시:
```
안녕하세요! 어떤 도구를 만들고 싶으세요?
편하게 설명해 주시면 제가 도와드릴게요.
```

사용자가 아이디어를 말하면, 자연스럽게 후속 질문을 합니다:
- 대화 흐름에 맞춰 하나씩 질문 (한 번에 여러 개 X)
- 사용자 답변에 맞춰 유연하게 진행
- 필요한 정보: 주요 기능, 입력 데이터, 출력 형태, 특별 요구사항

**예시 대화:**
```
사용자: 엑셀 파일을 JSON으로 바꾸고 싶어요
Claude: 아, 엑셀을 JSON으로 변환하는 도구군요!
        혹시 여러 시트가 있는 엑셀도 처리해야 하나요?
사용자: 네, 시트별로 따로 저장했으면 좋겠어요
Claude: 좋아요. 그럼 출력 파일명은 어떻게 할까요?
        시트 이름을 파일명으로 쓸까요?
```

요구사항이 충분히 파악되면:
1. 지금까지 이해한 내용을 요약해서 확인
2. **플랜 모드로 진입하여** 구체적인 구현 계획 작성
3. 사용자 승인 후 실제 구현 시작

**플랜 모드 진입 시점:**
- 도구가 무엇을 하는지 명확해졌을 때
- 입력/출력이 정해졌을 때
- 특별한 요구사항이 파악되었을 때

플랜에 포함할 내용:
- 도구 이름 제안 (예: `excel-to-json`, `img-resize`)
- 주요 기능 목록
- 필요한 npm 패키지
- 파일 구조
- 구현 순서

### Phase 2: 저장 위치 확인

**중요: 프로젝트를 생성하기 전에 저장 위치를 사용자에게 확인합니다.**

질문 예시:
```
도구를 어디에 저장할까요?
현재 위치: /Users/username/Documents

예시:
- /Users/username/Documents/DEV/create-tool 폴더 하위에 저장해줘
- 현재 폴더에 저장해줘
- ~/Projects 에 저장해줘
```

사용자가 위치를 지정하면:
1. 해당 경로가 존재하는지 확인
2. 존재하지 않으면 생성할지 물어봄
3. 절대 경로로 변환하여 사용

### Phase 3: 프로젝트 설정

저장 위치가 확정되면 자동으로 실행:

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

# 설정 파일 생성
```

다음 파일들을 생성:
- `tsconfig.json` - TypeScript 설정
- `.gitignore` - Git 제외 패턴
- `package.json` - bin 필드와 스크립트 업데이트

### Phase 4: 코드 생성

사용자 요구사항에 맞춰 생성:

**1. 메인 로직 (`src/[도구이름].ts`)**
```typescript
// 템플릿 구조:
- 파일/디렉토리 검색 함수
- 메인 처리 로직
- CLI 인자 파싱
- 에러 처리
- 진행 상황 표시
- main() 함수 export
```

**2. CLI 진입점 (`bin/[도구이름].js`)**
```javascript
#!/usr/bin/env node
require('../dist/[도구이름]').main(process.argv.slice(2));
```

**3. Claude 커맨드 파일 (`.claude/commands/[도구이름].md`)**

다음 템플릿 구조를 따릅니다:

```markdown
# /[도구이름] - [간단한 설명]

## ⚠️ 중요: 실행 전 반드시 수행할 단계

**[도구이름] 실행 전에 반드시 아래 단계를 순서대로 수행하세요:**

### Step 1: 설치 여부 확인
```bash
which [도구이름]
```

### Step 2-A: 이미 설치된 경우 → 도구 + 커맨드 파일 업데이트 (필수!)

**반드시 GitHub에서 최신 버전인지 확인하고, 도구와 커맨드 파일 모두 업데이트하세요:**

```bash
TOOL_PATH=$(dirname $(dirname $(which [도구이름]))) && cd $TOOL_PATH && git fetch origin && LOCAL=$(git rev-parse HEAD) && REMOTE=$(git rev-parse origin/master) && if [ "$LOCAL" != "$REMOTE" ]; then echo "🔄 새 버전 발견, 업데이트 중..." && git pull origin master && npm install && npm run build && cp .claude/commands/[도구이름].md $OLDPWD/.claude/commands/[도구이름].md && echo "✅ 도구 및 커맨드 파일 업데이트 완료!"; else echo "✅ 이미 최신 버전입니다."; fi
```

### Step 2-B: 설치되지 않은 경우 → 자동 설치
```bash
git clone https://github.com/[사용자명]/[도구이름].git /tmp/[도구이름] && cd /tmp/[도구이름] && npm install && npm run build && npm link
```

### Step 3: 도구 실행
```bash
[도구이름] [인자들]
```

## 사용법
/[도구이름] [인자들]

## 실행 단계

사용자가 `/[도구이름] [인자들]`을 실행하면:

1. 설치 확인 → 없으면 자동 설치, 있으면 업데이트 확인 (도구 + 커맨드 파일 모두)
2. 인자 검증
3. 입력 파일 검색 (해당되는 경우)
4. 실행: `[도구이름] [인자들]`
5. 결과 표시

## 에러 처리

- 파일 없음: 명확한 에러 표시
- 잘못된 입력: 올바른 형식 제안
- 설치 실패: Node.js/npm 확인 안내
- 업데이트 실패: 수동 업데이트 방법 안내
```

**4. 문서 (`README.md`)**

```markdown
# [도구이름]

[기능 설명]

## 설치 (한 줄 명령어)

```bash
mkdir -p .claude/commands && curl -o .claude/commands/[도구이름].md https://raw.githubusercontent.com/[사용자명]/[도구이름]/master/.claude/commands/[도구이름].md
```

## 사용법

Claude Code로:
```
/[도구이름] [인자들]
```

CLI로:
```bash
[도구이름] [인자들]
```

## 기능

- [기능 1]
- [기능 2]
- [기능 3]

## 예시

[입력/출력 예시 표시]

## 작동 원리

이 도구는 Claude Code의 슬래시 커맨드 시스템을 사용하여 쉽게 배포됩니다.

## 라이선스

MIT
```

### Phase 5: 빌드 및 테스트

자동으로 실행:

```bash
# 빌드
npm run build

# 로컬 테스트를 위한 링크
npm link

# 테스트 실행
[도구이름] [테스트-인자]
```

확인사항:
- 빌드 성공
- 명령어가 전역적으로 사용 가능
- 출력이 올바름

### Phase 6: Git 및 GitHub

**사용자에게 질문**: "GitHub 사용자명이 무엇인가요?"

그 후 실행:

```bash
# git 초기화
git init
git add .
git commit -m "Initial commit: [도구 설명]"

# GitHub 저장소 생성 (gh CLI가 있으면)
gh repo create [도구이름] --public --source=. --remote=origin --push

# 또는 수동 방법 안내
```

GitHub CLI가 없으면 다음 안내 표시:

```
1. https://github.com/new 접속
2. 저장소 이름 입력: [도구이름]
3. 다음 명령어 실행:
   git remote add origin https://github.com/[사용자명]/[도구이름].git
   git branch -M master
   git push -u origin master
```

### Phase 7: 완료 요약

사용자에게 표시:

```
🎉 도구 생성 완료!

📦 저장소: https://github.com/[사용자명]/[도구이름]

📥 설치 명령어:
mkdir -p .claude/commands && curl -o .claude/commands/[도구이름].md https://raw.githubusercontent.com/[사용자명]/[도구이름]/master/.claude/commands/[도구이름].md

🚀 사용법:
/[도구이름] [인자들]

✅ 다음 단계:
1. 테스트: /[도구이름] [예시]
2. 팀에 설치 명령어 공유
3. GitHub 저장소에 스타 추가
4. 이슈 리포트: https://github.com/[사용자명]/[도구이름]/issues

또 다른 도구를 만들고 싶으신가요? /create-tool을 다시 실행하세요!
```

## 코드 템플릿

### TypeScript 기본 템플릿

```typescript
#!/usr/bin/env node
import * as fs from 'fs';
import * as path from 'path';

interface ToolOptions {
  // 요구사항에 따라 정의
}

async function findTargetFiles(
  startPath: string,
  extensions: string[]
): Promise<string[]> {
  const results: string[] = [];
  const items = fs.readdirSync(startPath, { withFileTypes: true });

  for (const item of items) {
    const fullPath = path.join(startPath, item.name);
    if (item.isDirectory()) {
      results.push(...await findTargetFiles(fullPath, extensions));
    } else if (item.isFile()) {
      const ext = path.extname(item.name);
      if (extensions.includes(ext)) {
        results.push(fullPath);
      }
    }
  }

  return results;
}

async function processFile(
  filePath: string,
  options: ToolOptions
): Promise<void> {
  // 메인 처리 로직
  console.log(`처리 중: ${filePath}`);
}

export async function main(args: string[]): Promise<void> {
  if (args.length === 0) {
    console.log('사용법: [도구이름] [인자들]');
    process.exit(1);
  }

  const targetPath = args[0];

  if (!fs.existsSync(targetPath)) {
    console.error(`에러: 경로를 찾을 수 없습니다: ${targetPath}`);
    process.exit(1);
  }

  // 메인 실행 로직
  console.log('시작 중...');

  try {
    // 파일 처리
    console.log('✓ 완료!');
  } catch (error) {
    console.error('에러:', error.message);
    process.exit(1);
  }
}

// CLI 진입점
if (require.main === module) {
  main(process.argv.slice(2));
}
```

### package.json 템플릿

```json
{
  "name": "[도구이름]",
  "version": "1.0.0",
  "description": "[도구 설명]",
  "main": "dist/[도구이름].js",
  "bin": {
    "[도구이름]": "./bin/[도구이름].js"
  },
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch",
    "prepublish": "npm run build"
  },
  "keywords": ["claude-code", "automation"],
  "author": "[작성자 이름]",
  "license": "MIT",
  "devDependencies": {
    "@types/node": "^20.0.0",
    "typescript": "^5.0.0"
  },
  "dependencies": {
    // 요구사항에 따라 추가
  }
}
```

### tsconfig.json 템플릿

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### .gitignore 템플릿

```
node_modules/
dist/
*.log
.DS_Store
*.backup
.env
.vscode/
```

## 일반적인 도구 패턴

### 패턴 1: 파일 변환기
- 입력: A 타입의 파일들
- 출력: B 타입의 파일들
- 예시: markdown → pdf, csv → json

### 패턴 2: 파일 처리기
- 입력: 파일들
- 출력: 수정된 파일 또는 리포트
- 예시: 이미지 최적화, 코드 포맷터

### 패턴 3: 데이터 집계기
- 입력: 여러 파일/소스
- 출력: 하나로 합쳐진 파일
- 예시: 로그 집계기, 리포트 생성기

### 패턴 4: 코드 생성기
- 입력: 설정 또는 스펙
- 출력: 코드 파일들
- 예시: API 클라이언트 생성기, 보일러플레이트 생성기

## 의존성 추천

도구 타입에 따라 제안:

**PDF**: `puppeteer`, `pdf-lib`
**이미지**: `sharp`, `jimp`
**Excel/CSV**: `xlsx`, `csv-parser`
**Markdown**: `marked`, `markdown-it`
**HTML**: `cheerio`, `jsdom`
**HTTP**: `axios`, `node-fetch`
**CLI**: `commander`, `inquirer`, `chalk`

## 에러 방지

배포 전 확인사항:

- ✅ 모든 필요한 파일이 존재
- ✅ package.json에 올바른 bin 필드
- ✅ bin 파일에 shebang (#!/usr/bin/env node)
- ✅ TypeScript가 에러 없이 컴파일
- ✅ .gitignore에 node_modules와 dist 포함
- ✅ README에 올바른 GitHub 사용자명
- ✅ Claude 커맨드 파일에 올바른 저장소 URL

## 문제 해결 가이드

모든 도구의 README에 포함:

**"command not found"**
→ Node.js 설치 확인: `node --version`

**"Permission denied"**
→ 실행: `sudo npm link`

**"Module not found"**
→ 도구 디렉토리에서 실행: `npm install`

**"Build failed"**
→ Node.js 버전 확인 (18+ 필요)

## 성공 기준

도구가 완성된 것으로 간주되는 조건:
1. 에러 없이 빌드
2. 테스트 입력으로 성공적으로 실행
3. GitHub 저장소가 생성되고 푸시됨
4. README에 작동하는 설치 명령어
5. 사용자가 한 줄 curl 명령어로 설치 가능
6. Claude Code 슬래시 커맨드로 작동

## 대화 예시

**예시 1: 이미지 압축기**

```
사용자: /create-tool
Claude: 이 도구가 무엇을 해야 하나요?
사용자: 이미지를 압축해서 파일 크기를 줄이고 싶어요
Claude: 좋습니다! 어떤 형식을 지원할까요? (PNG, JPG, WebP 등)
사용자: 전부 다요
Claude: 원본 파일을 백업으로 보관할까요?
사용자: 네
Claude: 완벽합니다! "img-compress" 도구를 만들겠습니다...
[자동 생성 프로세스]
Claude: ✓ 완료! 설치: [curl 명령어]
```

**예시 2: CSV를 마크다운 테이블로**

```
사용자: /create-tool
Claude: 이 도구가 무엇을 해야 하나요?
사용자: CSV 파일을 마크다운 테이블로 변환하고 싶어요
Claude: 큰 파일도 처리해야 하나요?
사용자: 네, 그리고 정렬 옵션도 추가해주세요
Claude: 알겠습니다! "csv-to-md" 도구를 만들겠습니다...
[자동 생성 프로세스]
Claude: ✓ 완료! 사용해보세요: /csv-to-md data.csv
```

## Claude를 위한 참고사항

이 명령어를 실행할 때:

1. **대화식으로 진행** - 자연스럽게 안내
2. **명확히 질문** - 추측하지 말 것
3. **진행 상황 표시** - 각 단계마다 업데이트
4. **에러를 우아하게 처리** - 문제를 설명
5. **철저히 테스트** - 깨진 도구 배포 금지
6. **예시 제공** - 도구 사용법 표시
7. **URL 재확인** - GitHub 링크가 정확한지 확인

## 출력 형식

항상 제공:
- 명확한 진행 상황 업데이트
- 실패 시 에러 메시지
- 모든 명령어가 포함된 최종 요약
- 사용자를 위한 다음 단계

기술적인 프로세스가 아닌 안내 마법사처럼 느껴지게 하세요!

## 한국어 응답

- 모든 대화는 한국어로 진행
- 에러 메시지도 한국어로 표시
- 진행 상황도 한국어로 업데이트
- 최종 요약도 한국어로 제공
