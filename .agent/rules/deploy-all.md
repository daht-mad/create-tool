---
trigger: glob
glob: "**/*"
---

# deploy-all - 모든 하위 도구 및 create-tool 일괄 커밋/푸시

create-tool의 모든 하위 도구(서브모듈)를 각각의 GitHub 저장소에 커밋/푸시하고, 최종적으로 create-tool도 커밋/푸시합니다.

## 맥락 확인 (Step 0)

**중요: 도구 실행 전에 필요한 정보가 충분한지 먼저 확인하세요.**

사용자가 `/deploy-all`만 입력한 경우:
1. "어떤 변경사항을 커밋할까요? 커밋 메시지를 알려주세요."
2. "예: `/deploy-all feat: 새 기능 추가` 또는 `/deploy-all fix: 버그 수정`"

**커밋 메시지가 제공된 경우에만** 아래 실행 단계로 진행합니다.

## 실행 단계

### Step 1: 변경사항 확인

먼저 각 하위 도구의 변경사항을 확인합니다.

```bash
cd /Users/dahye.dyan/Documents/DEV/create-tool

echo "=== 하위 도구 변경사항 확인 ==="
for dir in log-update md2pdf org-matcher pdf2excel sheets-wrapper; do
  if [ -d "$dir" ]; then
    echo ""
    echo "📁 $dir:"
    cd "$dir"
    git status --short
    cd ..
  fi
done

echo ""
echo "=== create-tool 변경사항 확인 ==="
git status --short
```

### Step 2: 하위 도구 커밋 및 푸시

변경사항이 있는 각 하위 도구를 개별적으로 커밋하고 푸시합니다.

**각 하위 도구에 대해 순서대로 실행:**

```bash
# log-update
cd /Users/dahye.dyan/Documents/DEV/create-tool/log-update
git add -A
git commit -m "[커밋메시지]

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
git push origin master
```

```bash
# md2pdf
cd /Users/dahye.dyan/Documents/DEV/create-tool/md2pdf
git add -A
git commit -m "[커밋메시지]

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
git push origin master
```

```bash
# org-matcher
cd /Users/dahye.dyan/Documents/DEV/create-tool/org-matcher
git add -A
git commit -m "[커밋메시지]

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
git push origin master
```

```bash
# pdf2excel
cd /Users/dahye.dyan/Documents/DEV/create-tool/pdf2excel
git add -A
git commit -m "[커밋메시지]

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
git push origin master
```

```bash
# sheets-wrapper
cd /Users/dahye.dyan/Documents/DEV/create-tool/sheets-wrapper
git add -A
git commit -m "[커밋메시지]

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
git push origin master
```

### Step 3: create-tool 최종 커밋 및 푸시

```bash
cd /Users/dahye.dyan/Documents/DEV/create-tool
git add README.md log-update md2pdf org-matcher pdf2excel sheets-wrapper .claude .agent
git commit -m "[커밋메시지]

- 하위 도구 서브모듈 업데이트

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
git push origin master
```

### Step 4: 결과 요약

```
✅ 배포 완료!

📦 업데이트된 저장소:
- https://github.com/daht-mad/log-update
- https://github.com/daht-mad/md2pdf
- https://github.com/daht-mad/org-matcher
- https://github.com/daht-mad/pdf2excel
- https://github.com/daht-mad/sheets-wrapper
- https://github.com/daht-mad/create-tool

커밋 메시지: [커밋메시지]
```

## 에러 처리

- **"nothing to commit"**: 해당 도구에 변경사항이 없음 (정상)
- **"rejected"**: 먼저 `git pull`로 원격 변경사항 가져오기
- **"permission denied"**: GitHub 인증 확인 필요

## 예시

```
/deploy-all feat: 맥락 확인 기능 추가
/deploy-all fix: 버그 수정 및 문서 업데이트
/deploy-all docs: README 업데이트
```
