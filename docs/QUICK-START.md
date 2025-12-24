# 빠른 시작 가이드

## 30초 안에 시작하기

### 1. 준비 확인 (10초)

터미널에서 실행:

```bash
node --version && npm --version && git --version
```

모두 버전이 나오면 ✅ 준비 완료!

### 2. 도구 만들기 (20초)

VSCode에서 Claude Code 열고:

```
/create-tool
```

Claude가 질문하면 답변:

```
Claude: 어떤 기능을 만들고 싶으신가요?
나: 이미지를 압축하고 싶어요
```

### 3. 완성! 🎉

3분 후 도구가 준비됩니다.

---

## 실전 예시

### 시나리오 1: 블로그 이미지 최적화

**문제**: 블로그에 올릴 이미지가 너무 큼

**해결**:
```
나: /create-tool
Claude: 무엇을 만들까요?
나: 이미지를 80% 품질로 압축하고, 원본은 .backup 폴더에 저장해줘
Claude: [3분 후] ✓ 완료!

사용: /img-compress ./blog-images
```

### 시나리오 2: 회의록 정리

**문제**: 여러 개의 회의록 파일을 하나로 합치고 싶음

**해결**:
```
나: /create-tool
Claude: 무엇을 만들까요?
나: 마크다운 파일들을 날짜순으로 합쳐서 하나의 PDF로 만들어줘
Claude: [3분 후] ✓ 완료!

사용: /meeting-merger ./meetings
```

### 시나리오 3: 데이터 변환

**문제**: 엑셀 데이터를 API에 보내려고 JSON으로 변환 필요

**해결**:
```
나: /create-tool
Claude: 무엇을 만들까요?
나: 엑셀의 특정 시트만 JSON으로 변환하고, 빈 셀은 null로 처리해줘
Claude: [3분 후] ✓ 완료!

사용: /excel2json ./data.xlsx
```

---

## 다음 단계

### 초보자
1. 📖 [비개발자 가이드](./NON-DEVELOPER-GUIDE.md) 읽기
2. 🚀 간단한 도구부터 시작 (파일 이름 변경 등)
3. 📤 팀원과 공유해보기

### 중급자
1. 🔧 도구를 개선하고 싶다면 Claude에게 요청
2. 🔗 여러 도구를 조합해서 워크플로우 만들기
3. 📚 [작동 원리](./HOW-IT-WORKS.md) 이해하기

### 고급자
1. 🛠️ 도구 코드 직접 수정해보기
2. 🌟 오픈소스 기여하기
3. 📦 npm에 퍼블리싱하기

---

## 도움이 필요하면

- 💬 Claude에게 물어보기 (Claude가 가장 잘 압니다!)
- 📖 [README](./README.md) 참고
- 🐛 버그 발견 시 GitHub Issues
- 💡 아이디어 공유는 GitHub Discussions

---

## 유용한 명령어 모음

```bash
# 도구 만들기
/create-tool

# 만든 도구 사용하기
/your-tool-name [arguments]

# 도구 업데이트 확인
cd /tmp/your-tool && git pull

# 도구 제거
npm unlink your-tool-name
rm -rf /tmp/your-tool
```

---

**지금 바로 시작하세요!** 🚀

```
/create-tool
```
