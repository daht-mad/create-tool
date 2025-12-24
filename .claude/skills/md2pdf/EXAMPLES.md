# 사용 예시

## 기본 변환

```bash
dahtmad-md2pdf README.md
# 출력: README.pdf (같은 디렉토리에 생성)
```

## 여러 파일 변환

```bash
dahtmad-md2pdf docs/guide.md
dahtmad-md2pdf CHANGELOG.md
```

## Mermaid 다이어그램 포함 문서

Mermaid 코드 블록이 있는 마크다운도 자동으로 이미지로 변환됩니다.

```markdown
# 예시 문서

## 플로우차트

\`\`\`mermaid
graph LR
    A[시작] --> B[처리]
    B --> C[완료]
\`\`\`
```

위와 같은 마크다운을 PDF로 변환하면 다이어그램이 이미지로 렌더링됩니다.

## 코드 하이라이팅

코드 블록은 언어에 맞게 구문 강조가 적용됩니다.

```markdown
\`\`\`javascript
function hello() {
  console.log('Hello, World!');
}
\`\`\`
```

## 한글 문서

한글 폰트가 기본 지원되어 별도 설정 없이 한글 문서를 PDF로 변환할 수 있습니다.
