# create-tool

비개발자도 자연어 대화만으로 AI 스킬을 만들고, GitHub에 배포하여 팀원들이 한 줄 명령어로 설치할 수 있게 합니다.

## 핵심 가치

```
1. 대화로 스킬 생성 → 2. GitHub 자동 배포 → 3. 팀원이 한 줄로 설치
```

## 설치

```bash
mkdir -p .claude/skills .claude/commands && curl -sL https://github.com/daht-mad/create-tool/archive/refs/heads/master.tar.gz | tar -xz -C /tmp && cp -r /tmp/create-tool-master/.claude/skills/create-tool .claude/skills/ && cp /tmp/create-tool-master/.claude/commands/deploy.md .claude/commands/ 2>/dev/null || true && rm -rf /tmp/create-tool-master
```

Claude Code를 재시작하면 `/create-tool` 커맨드를 사용할 수 있습니다.

## 사용법

Claude Code에서:

```
/create-tool
```

또는:

```
새 스킬 만들어줘
```

대화형으로 스킬을 만들고 GitHub에 배포까지 자동으로 진행됩니다.

## 기능

- **대화형 스킬 생성**: 자연어로 아이디어 설명 → 자동 생성
- **표준 구조**: SKILL.md, scripts, references, assets 자동 생성
- **자동 업데이트**: check_update.py 포함 (사용자가 자동 업데이트 받음)
- **배포 커맨드**: /deploy로 버전 관리 + GitHub 푸시 자동화
- **한 줄 설치**: GitHub Archive API 활용한 설치 명령어 제공

## 생성되는 스킬 구조

```
my-skill/
├── README.md              # GitHub 배포용
├── SKILL.md               # 스킬 정의 (AI용)
├── scripts/
│   ├── check_update.py   # 자동 업데이트
│   └── example.py        # 예시 스크립트
├── references/
│   └── example.md        # 참조 문서
├── assets/
│   └── README.md         # 에셋 설명
└── .claude/
    └── commands/
        └── deploy.md     # 배포 커맨드
```

## 워크플로우

1. **스킬 생성**: `/create-tool` 실행
2. **개발**: SKILL.md, scripts 수정
3. **배포**: `/deploy` - 자동 버전 업데이트 + GitHub 푸시
4. **공유**: 팀원에게 한 줄 설치 명령어 전달

## 필요 환경

- Python 3.8+
- Git
- GitHub CLI (gh) - PR 제출 시 필요

---

Last updated: 2025-12-24
