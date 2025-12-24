# 비개발자를 위한 Claude Code 도구 만들기 가이드

## 개요

**코딩 없이** Claude Code와 대화만으로 자동화 도구를 만들고 배포할 수 있습니다!

## 필요한 것

1. **VSCode** - 코드 에디터
2. **Claude Code** - VSCode 확장 프로그램
3. **Node.js** - JavaScript 실행 환경 ([설치 링크](https://nodejs.org))
4. **Git** - 버전 관리 도구 ([설치 링크](https://git-scm.com))
5. **GitHub 계정** - 코드 저장소 ([가입 링크](https://github.com))

## 설치 확인

터미널에서 다음 명령어를 실행해보세요:

```bash
node --version   # v18.0.0 이상이어야 함
npm --version    # 9.0.0 이상이어야 함
git --version    # 2.0.0 이상이어야 함
```

모두 버전이 나오면 준비 완료!

## 사용법

### 1단계: `/create-tool` 명령어 실행

VSCode에서 Claude Code 패널을 열고:

```
/create-tool
```

입력 후 엔터!

### 2단계: Claude와 대화하기

Claude가 질문을 하면 자연스럽게 답변하세요.

**예시 대화:**

```
Claude: 어떤 기능을 만들고 싶으신가요?

나: 엑셀 파일에서 특정 열만 추출해서 JSON으로 저장하고 싶어요

Claude: 좋습니다! 몇 가지 질문이 있습니다:
1. 어떤 열을 추출하시나요? (예: 이름, 이메일 등)
2. JSON 파일 이름은 어떻게 할까요?
3. 여러 엑셀 파일을 한 번에 처리할 수 있어야 하나요?

나:
1. 사용자가 선택할 수 있게 해주세요
2. 원본 파일명_output.json으로 해주세요
3. 네, 폴더 안의 모든 엑셀 파일을 처리했으면 좋겠어요

Claude: 완벽합니다! "excel-to-json" 도구를 만들겠습니다.
진행할까요? (yes/no)

나: yes

Claude:
✓ 프로젝트 구조 생성 중...
✓ 필요한 패키지 설치 중...
✓ 코드 작성 중...
✓ 테스트 중...
✓ GitHub 저장소 생성 준비...

GitHub 사용자명을 알려주세요:

나: myusername

Claude:
✓ Git 저장소 초기화 완료
✓ GitHub 저장소 생성 완료
✓ 코드 푸시 완료

🎉 도구 생성 완료!

📦 저장소: https://github.com/myusername/excel-to-json

📥 설치 명령어:
mkdir -p .claude/commands && curl -o .claude/commands/excel-to-json.md https://raw.githubusercontent.com/myusername/excel-to-json/master/.claude/commands/excel-to-json.md

🚀 사용법:
/excel-to-json ./data

바로 테스트해볼까요?
```

### 3단계: 완료!

이제 다음과 같이 사용할 수 있습니다:

```
/excel-to-json ./my-data-folder
```

## 실제 사용 예시

### 예시 1: 이미지 압축 도구

**대화:**
```
나: /create-tool
Claude: 어떤 기능을 만들고 싶으신가요?
나: 이미지를 압축해서 용량을 줄이고 싶어요
Claude: PNG, JPG, WebP 모두 지원할까요?
나: 네
Claude: 원본 파일은 백업할까요?
나: 네, 백업해주세요
```

**결과:**
- 도구 이름: `img-compress`
- 사용법: `/img-compress ./images`
- 기능: 이미지 압축 + 원본 백업 + 통계 리포트

### 예시 2: 로그 파일 분석기

**대화:**
```
나: /create-tool
Claude: 어떤 기능을 만들고 싶으신가요?
나: 로그 파일에서 에러만 추출해서 보기 쉽게 정리하고 싶어요
Claude: 어떤 형식의 로그 파일인가요?
나: .log 파일이고 각 줄이 [타임스탬프] [레벨] 메시지 형식이에요
Claude: 출력 형식은 어떻게 할까요?
나: HTML 리포트로 만들어주세요. 시간별로 그래프도 있으면 좋겠어요
```

**결과:**
- 도구 이름: `log-analyzer`
- 사용법: `/log-analyzer ./logs`
- 기능: 에러 추출 + HTML 리포트 + 시간별 그래프

### 예시 3: 마크다운 목차 생성기

**대화:**
```
나: /create-tool
Claude: 어떤 기능을 만들고 싶으신가요?
나: 마크다운 파일에 자동으로 목차를 추가하고 싶어요
Claude: 목차는 어디에 추가할까요?
나: 파일 맨 위에 추가해주세요
Claude: 원본 파일을 수정할까요, 아니면 새 파일로 저장할까요?
나: 원본을 수정해주세요
```

**결과:**
- 도구 이름: `md-toc`
- 사용법: `/md-toc README.md`
- 기능: 자동 목차 생성 + 원본 업데이트

## 팁과 요령

### 1. 명확하게 설명하기

❌ 나쁜 예: "파일 처리하는 거 만들어줘"
✅ 좋은 예: "엑셀 파일에서 이메일 주소만 추출해서 텍스트 파일로 저장하고 싶어요"

### 2. 구체적인 예시 제공

예시를 들어주면 Claude가 더 정확하게 이해합니다:

```
나: CSV 파일을 HTML 테이블로 변환하고 싶어요

Claude: 어떤 스타일을 원하시나요?

나: 이런 느낌이요:
- 헤더는 파란색 배경
- 행마다 번갈아가며 회색 배경
- 마우스 올리면 노란색으로 강조
- 정렬 가능하게
```

### 3. 단계별로 확인

한 번에 모든 기능을 요구하지 말고, 기본 기능부터 시작:

```
1차: CSV를 HTML로 변환
2차: 스타일 추가
3차: 정렬 기능 추가
4차: 검색 기능 추가
```

### 4. 에러 처리 고려

예상되는 문제를 미리 말해주세요:

```
나: 그런데 파일이 너무 크면 어떻게 되나요?
나: 같은 이름의 파일이 있으면 덮어쓸까요?
나: 인터넷 연결이 끊기면요?
```

## 만들 수 있는 도구 아이디어

### 파일 변환
- PDF → 이미지
- 동영상 → GIF
- CSV → Excel
- JSON → YAML

### 데이터 처리
- 이미지 일괄 리사이즈
- 파일 이름 일괄 변경
- 중복 파일 찾기
- 텍스트 대량 치환

### 분석 및 리포트
- 코드 복잡도 분석
- 웹사이트 스크린샷
- 테스트 커버리지 리포트
- Git 커밋 통계

### 자동화
- 정기 백업
- 배포 자동화
- 알림 발송
- 데이터 동기화

## 문제 해결

### "command not found" 에러

**원인**: Node.js가 설치되지 않았거나 경로 문제

**해결**:
```bash
# Node.js 설치 확인
node --version

# 없다면 https://nodejs.org 에서 설치
```

### GitHub 저장소 생성 실패

**원인**: GitHub CLI(`gh`)가 설치되지 않음

**해결**: Claude가 수동 방법을 안내해줍니다:
1. https://github.com/new 접속
2. 저장소 이름 입력
3. Public으로 생성
4. Claude가 알려준 명령어 실행

### 빌드 에러

**원인**: npm 패키지 설치 중 문제 발생

**해결**: Claude가 자동으로 재시도하거나 대안을 제시합니다

### 권한 에러

**원인**: npm link 시 관리자 권한 필요

**해결**:
```bash
sudo npm link
```

## 도구 공유하기

### 팀원에게 공유

생성된 설치 명령어를 복사해서 전달:

```bash
mkdir -p .claude/commands && curl -o .claude/commands/your-tool.md https://raw.githubusercontent.com/username/your-tool/master/.claude/commands/your-tool.md
```

팀원은 이 한 줄만 실행하면 끝!

### 사용법 문서 공유

Claude가 자동으로 생성한 README.md를 GitHub에서 확인 가능:

```
https://github.com/username/your-tool
```

### 업데이트 배포

도구를 개선하고 싶다면:

1. Claude에게 요청: "excel-to-json 도구에 필터 기능을 추가하고 싶어요"
2. Claude가 코드 수정
3. GitHub에 자동 푸시
4. 사용자들은 다음 실행 시 자동 업데이트!

## 고급 기능

### 여러 도구 조합

만든 도구들을 조합해서 사용:

```
/img-compress ./raw-images
/img-resize ./raw-images
/upload-to-s3 ./raw-images
```

### 자동화 스크립트

여러 도구를 한 번에 실행:

```bash
#!/bin/bash
img-compress ./images
csv-to-json ./data.csv
generate-report ./output
```

### 커스터마이징

Claude에게 요청:

```
나: excel-to-json 도구를 수정하고 싶어요
Claude: 어떤 기능을 추가하시겠어요?
나: 날짜 형식을 자동으로 변환했으면 좋겠어요
```

## 실전 프로젝트 예시

### 프로젝트: 블로그 관리 도구

**1단계: 이미지 최적화**
```
/create-tool
→ img-optimize 생성
→ 블로그 이미지 자동 압축
```

**2단계: 마크다운 검증**
```
/create-tool
→ md-lint 생성
→ 맞춤법, 링크 확인
```

**3단계: 배포 자동화**
```
/create-tool
→ blog-deploy 생성
→ 빌드 + 배포 자동화
```

**최종 워크플로우:**
```
/img-optimize ./posts/images
/md-lint ./posts
/blog-deploy
```

### 프로젝트: 데이터 분석 파이프라인

**1단계: 데이터 수집**
```
/create-tool
→ csv-merger 생성
→ 여러 CSV 파일 합치기
```

**2단계: 데이터 정제**
```
/create-tool
→ data-cleaner 생성
→ 중복 제거, 결측치 처리
```

**3단계: 리포트 생성**
```
/create-tool
→ data-report 생성
→ 통계 + 차트 HTML 리포트
```

## FAQ

**Q: 정말 코딩을 하나도 몰라도 되나요?**
A: 네! Claude와 자연스럽게 대화만 하면 됩니다.

**Q: 만든 도구를 수정할 수 있나요?**
A: 네! Claude에게 "이 기능을 추가해줘" 요청하면 됩니다.

**Q: 무료인가요?**
A: Claude Code는 유료이지만, 만든 도구는 영구적으로 무료로 사용 가능합니다.

**Q: 다른 사람이 만든 도구를 사용할 수 있나요?**
A: 네! curl 명령어로 설치하면 바로 사용 가능합니다.

**Q: 상업적으로 사용 가능한가요?**
A: 네! MIT 라이선스로 자유롭게 사용 가능합니다.

**Q: Windows에서도 되나요?**
A: 네! Windows, Mac, Linux 모두 지원합니다.

## 다음 단계

1. **첫 도구 만들기**: 간단한 것부터 시작 (파일 이름 변경 등)
2. **팀에 공유**: 유용하면 동료들과 공유
3. **피드백 수집**: 사용자 의견 반영해서 개선
4. **도구 모음 구축**: 여러 도구를 조합해서 워크플로우 자동화

## 커뮤니티

- GitHub Issues: 버그 리포트, 기능 요청
- GitHub Discussions: 아이디어 공유, 질문
- README 업데이트: 사용 예시 추가

## 결론

**이제 여러분도 도구 제작자입니다!**

복잡한 코딩 없이, Claude와 대화만으로:
- 반복 작업 자동화
- 팀 생산성 향상
- 맞춤형 도구 제작
- 오픈소스 기여

시작해볼까요? `/create-tool` 🚀
