# 스킬 배포 커맨드

스킬을 GitHub 레포지토리에 배포합니다.

## 사용법

- `/deploy` - 현재 스킬 배포

## 입력

$ARGUMENTS

## 실행 방법

1. **변경사항 확인**:
   - `git status --porcelain`으로 변경사항 확인
   - 변경사항이 없으면 "✓ 변경사항 없음" 출력 후 종료

2. **버전 업데이트**:
   - 변경된 파일 중 `SKILL.md` 또는 `scripts/` 내 파일이 있으면 SKILL.md의 patch 버전 +1 (예: 1.0.2 → 1.0.3)
   - README.md만 변경된 경우 버전 유지

3. **Git 배포**:
   - `git add -A`
   - 변경된 파일 기반으로 커밋 메시지 생성
   - `git commit` (표준 커밋 메시지 형식 사용)
   - `git push` (실패 시 `git pull --rebase` 후 재시도)

## 커밋 메시지 형식

```
update: 변경된파일1, 변경된파일2

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

## 출력 예시

```
🚀 배포 시작

📦 버전 업데이트: 1.0.2 → 1.0.3
✓ 배포 완료
```
