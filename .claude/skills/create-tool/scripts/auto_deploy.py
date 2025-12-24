#!/usr/bin/env python3
"""
스킬 자동 GitHub 배포 스크립트
스킬을 GitHub 저장소에 자동으로 배포합니다.

사용법:
    python3 auto_deploy.py <skill-path>
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], cwd: str = None) -> tuple[int, str, str]:
    """명령어 실행 및 결과 반환"""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)


def get_skill_info(skill_path: Path) -> dict:
    """SKILL.md에서 스킬 정보 추출"""
    skill_md_path = skill_path / 'SKILL.md'

    if not skill_md_path.exists():
        print(f"❌ 에러: SKILL.md를 찾을 수 없습니다: {skill_md_path}")
        sys.exit(1)

    with open(skill_md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    info = {}

    name_match = re.search(r'^name:\s*(.+)$', content, re.MULTILINE)
    if name_match:
        info['name'] = name_match.group(1).strip()

    repo_match = re.search(r'^repo:\s*(.+)$', content, re.MULTILINE)
    if repo_match:
        info['repo'] = repo_match.group(1).strip()

    version_match = re.search(r'^version:\s*(.+)$', content, re.MULTILINE)
    if version_match:
        info['version'] = version_match.group(1).strip()

    if 'repo' not in info or 'TODO' in info.get('repo', ''):
        print("❌ 에러: SKILL.md에 유효한 repo 필드가 없습니다.")
        sys.exit(1)

    if 'version' not in info:
        print("❌ 에러: SKILL.md에 version 필드가 없습니다.")
        sys.exit(1)

    if 'name' not in info:
        print("❌ 에러: SKILL.md에 name 필드가 없습니다.")
        sys.exit(1)

    return info


def check_git_repo(skill_path: Path) -> bool:
    """Git 저장소 확인"""
    git_dir = skill_path / '.git'
    return git_dir.exists()


def init_git_repo(skill_path: Path, repo: str):
    """Git 저장소 초기화 및 원격 저장소 설정"""
    print("📦 Git 저장소 초기화 중...")

    # git init
    returncode, stdout, stderr = run_command(['git', 'init'], cwd=str(skill_path))
    if returncode != 0:
        print(f"❌ 에러: git init 실패 - {stderr}")
        sys.exit(1)

    # git remote add
    remote_url = f"https://github.com/{repo}.git"
    returncode, stdout, stderr = run_command(
        ['git', 'remote', 'add', 'origin', remote_url],
        cwd=str(skill_path)
    )
    if returncode != 0:
        # 이미 존재하면 무시
        if 'already exists' not in stderr:
            print(f"❌ 에러: git remote add 실패 - {stderr}")
            sys.exit(1)

    # 기본 브랜치를 main으로 설정
    run_command(['git', 'branch', '-M', 'main'], cwd=str(skill_path))

    print("   ✓ Git 저장소 초기화 완료")


def create_github_repo(repo: str) -> bool:
    """GitHub에 저장소 생성 (gh CLI 사용)"""
    print(f"🔨 GitHub 저장소 생성 중: {repo}")

    # gh CLI 설치 확인
    returncode, _, _ = run_command(['which', 'gh'])
    if returncode != 0:
        print("⚠️  경고: gh CLI가 설치되어 있지 않습니다.")
        print("   GitHub에서 수동으로 저장소를 생성해 주세요:")
        print(f"   https://github.com/new")
        return False

    # 저장소 생성
    repo_name = repo.split('/')[-1]
    returncode, stdout, stderr = run_command([
        'gh', 'repo', 'create', repo_name,
        '--public',
        '--source=.',
        '--push'
    ])

    if returncode != 0:
        if 'already exists' in stderr or 'already exists' in stdout:
            print("   ✓ 저장소가 이미 존재합니다.")
            return True
        else:
            print(f"⚠️  경고: GitHub 저장소 생성 실패")
            print(f"   수동으로 생성해 주세요: https://github.com/new")
            return False

    print("   ✓ GitHub 저장소 생성 완료")
    return True


def commit_and_push(skill_path: Path, version: str):
    """변경사항 커밋 및 푸시"""
    print("📤 GitHub에 푸시 중...")

    # git add
    returncode, stdout, stderr = run_command(['git', 'add', '-A'], cwd=str(skill_path))
    if returncode != 0:
        print(f"❌ 에러: git add 실패 - {stderr}")
        sys.exit(1)

    # 변경사항 확인
    returncode, stdout, stderr = run_command(['git', 'status', '--porcelain'], cwd=str(skill_path))
    if returncode == 0 and not stdout.strip():
        print("   ✓ 변경사항 없음")
        return

    # git commit
    commit_msg = f"""feat: 스킬 v{version} 배포

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"""

    returncode, stdout, stderr = run_command(
        ['git', 'commit', '-m', commit_msg],
        cwd=str(skill_path)
    )
    if returncode != 0:
        # 변경사항이 없으면 무시
        if 'nothing to commit' not in stdout and 'nothing to commit' not in stderr:
            print(f"❌ 에러: git commit 실패 - {stderr}")
            sys.exit(1)

    # git push
    returncode, stdout, stderr = run_command(
        ['git', 'push', '-u', 'origin', 'main'],
        cwd=str(skill_path)
    )

    if returncode != 0:
        # pull --rebase 후 재시도
        print("   재시도 중 (pull --rebase)...")
        returncode, stdout, stderr = run_command(
            ['git', 'pull', '--rebase', 'origin', 'main'],
            cwd=str(skill_path)
        )
        if returncode != 0:
            print(f"❌ 에러: git pull --rebase 실패 - {stderr}")
            sys.exit(1)

        returncode, stdout, stderr = run_command(
            ['git', 'push', '-u', 'origin', 'main'],
            cwd=str(skill_path)
        )
        if returncode != 0:
            print(f"❌ 에러: git push 실패 - {stderr}")
            sys.exit(1)

    print("   ✓ GitHub에 푸시 완료")


def auto_deploy(skill_path: str):
    """자동 배포 실행"""
    skill_path = Path(skill_path).resolve()

    if not skill_path.exists():
        print(f"❌ 에러: 스킬 경로가 존재하지 않습니다: {skill_path}")
        sys.exit(1)

    # 1. 스킬 정보 읽기
    skill_info = get_skill_info(skill_path)
    skill_name = skill_info['name']
    repo = skill_info['repo']
    version = skill_info['version']

    print(f"🚀 스킬 배포 시작: {skill_name} v{version}")
    print(f"   저장소: {repo}")
    print()

    # 2. Git 저장소 확인 및 초기화
    if not check_git_repo(skill_path):
        init_git_repo(skill_path, repo)

    # 3. GitHub 저장소 생성 (선택)
    create_github_repo(repo)

    # 4. 커밋 및 푸시
    commit_and_push(skill_path, version)

    # 5. 설치 명령어 출력
    print()
    print("✅ 배포 완료!")
    print()
    print(f"📦 저장소: https://github.com/{repo}")
    print()
    print("📥 팀원 설치 명령어 (한 줄):")
    print(f"mkdir -p .claude/skills && curl -sL https://github.com/{repo}/archive/refs/heads/main.tar.gz | tar -xz -C /tmp && mv /tmp/{skill_name}-main .claude/skills/{skill_name}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description='스킬을 GitHub에 자동으로 배포합니다.'
    )
    parser.add_argument(
        'skill_path',
        help='스킬 디렉토리 경로'
    )

    args = parser.parse_args()
    auto_deploy(args.skill_path)


if __name__ == "__main__":
    main()
