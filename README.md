# create-tool

비개발자도 AI 대화만으로 Claude Code 스킬을 만들고 배포합니다.

## 기능

- 자연어 대화로 스킬 생성
- GitHub 자동 배포
- 한 줄 설치 명령어 제공

## 설치

```bash
mkdir -p .claude/skills && curl -L https://github.com/daht-mad/create-tool/archive/refs/heads/master.tar.gz | tar -xz -C /tmp && mv /tmp/create-tool-master .claude/skills/create-tool
```

## 필요 환경

- Git 2.0.0+
- GitHub CLI (`gh`)

---

Last updated: 2024-12-24
