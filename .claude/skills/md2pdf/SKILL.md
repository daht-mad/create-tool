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
  - "이 문서 PDF로"
allowed-tools: Bash(dahtmad-md2pdf:*), Bash(git:*), Bash(npm:*), Bash(which:*), Bash(cd:*)
---

# md2pdf

마크다운 파일을 고품질 PDF로 변환하는 도구입니다.

## 설치 확인

도구 실행 전 반드시 설치 여부를 확인하세요.
설치되어 있지 않으면 [INSTALL.md](INSTALL.md)를 참조하여 자동 설치합니다.

## 사용법

```bash
dahtmad-md2pdf <마크다운_파일_경로>
```

자세한 사용 예시는 [EXAMPLES.md](EXAMPLES.md)를 참조하세요.

## 주요 기능

- Mermaid 다이어그램 자동 렌더링
- 한글 폰트 지원
- GitHub Flavored Markdown 지원
- 코드 하이라이팅
