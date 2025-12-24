# 코드 템플릿

## TypeScript 기본 템플릿

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

  console.log('시작 중...');

  try {
    // 파일 처리 로직
    console.log('✓ 완료!');
  } catch (error) {
    console.error('에러:', error.message);
    process.exit(1);
  }
}

if (require.main === module) {
  main(process.argv.slice(2));
}
```

## package.json 템플릿

```json
{
  "name": "@[스코프]/[도구이름]",
  "version": "1.0.0",
  "description": "[도구 설명]",
  "type": "module",
  "main": "bin/[도구이름].js",
  "bin": {
    "[스코프토큰]-[도구이름]": "./bin/[도구이름].js"
  },
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch",
    "prepublishOnly": "npm run build"
  },
  "keywords": ["claude-code", "automation"],
  "author": "[작성자 이름]",
  "license": "MIT",
  "engines": {
    "node": ">=18.0.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "typescript": "^5.0.0"
  }
}
```

## tsconfig.json 템플릿

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ES2022",
    "lib": ["ES2022"],
    "moduleResolution": "node",
    "outDir": "./bin",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "bin"]
}
```

## .gitignore 템플릿

```gitignore
node_modules/
bin/
*.log
.DS_Store
*.backup
.env
.vscode/
```

## Claude 커맨드 파일 템플릿

```markdown
# /[도구이름] - [간단한 설명]

## ⚠️ 중요: 실행 전 반드시 수행할 단계

### Step 1: 설치 여부 확인
\`\`\`bash
which [스코프토큰]-[도구이름]
\`\`\`

### Step 2-A: 이미 설치된 경우 → 업데이트 확인
\`\`\`bash
TOOL_PATH=$(dirname $(dirname $(which [스코프토큰]-[도구이름]))) && cd $TOOL_PATH && git fetch origin && LOCAL=$(git rev-parse HEAD) && REMOTE=$(git rev-parse origin/master) && if [ "$LOCAL" != "$REMOTE" ]; then echo "🔄 새 버전 발견, 업데이트 중..." && git pull origin master && npm install && npm run build && echo "✅ 업데이트 완료!"; else echo "✅ 이미 최신 버전입니다."; fi
\`\`\`

### Step 2-B: 설치되지 않은 경우 → 자동 설치
\`\`\`bash
git clone https://github.com/[사용자명]/[도구이름].git /tmp/[도구이름] && cd /tmp/[도구이름] && npm install && npm run build && npm link
\`\`\`

### Step 3: 도구 실행
\`\`\`bash
[스코프토큰]-[도구이름] [인자들]
\`\`\`

## 사용법
/[도구이름] [인자들]

## 맥락 확인 (Step 0)

사용자가 `/[도구이름]`만 입력하거나 인자가 부족한 경우:
1. 필요한 정보를 친절하게 질문
2. 예시를 보여주며 안내
3. 답변 후 실행 진행

## 에러 처리

- 파일 없음: 명확한 에러 표시
- 잘못된 입력: 올바른 형식 제안
- 설치 실패: Node.js/npm 확인 안내
```

## README.md 템플릿

```markdown
# [도구이름]

[기능 설명]

## 설치 (한 줄 명령어)

\`\`\`bash
mkdir -p .claude/commands && curl -o .claude/commands/[도구이름].md https://raw.githubusercontent.com/[사용자명]/[도구이름]/master/.claude/commands/[도구이름].md
\`\`\`

## 사용법

Claude Code로:
\`\`\`
/[도구이름] [인자들]
\`\`\`

CLI로 (터미널에서 직접):
\`\`\`bash
[스코프토큰]-[도구이름] [인자들]
\`\`\`

## 기능

- [기능 1]
- [기능 2]

## 라이선스

MIT
```

## 일반적인 도구 패턴

### 패턴 1: 파일 변환기
- 입력: A 타입 파일들
- 출력: B 타입 파일들
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
- 예시: API 클라이언트 생성기

## 의존성 추천

| 도구 타입 | 추천 패키지 |
|-----------|------------|
| PDF | puppeteer, pdf-lib |
| 이미지 | sharp, jimp |
| Excel/CSV | xlsx, csv-parser |
| Markdown | marked, markdown-it |
| HTML | cheerio, jsdom |
| HTTP | axios, node-fetch |
| CLI | commander, inquirer, chalk |
