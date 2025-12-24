#!/usr/bin/env python3
"""
스킬 버그 수정 기여 스크립트
설치한 스킬의 버그를 수정하고 원작자에게 PR을 제출합니다.

사용법:
    python3 contribute_fix.py <skill-path> --message "버그 설명"
"""

import argparse
import os
import re
import subprocess
import sys
import tempfile


def run_command(cmd: list[str], cwd: str = None, check: bool = True) -> subprocess.CompletedProcess:
    """명령어 실행"""
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"에러: {' '.join(cmd)}")
        print(result.stderr)
        sys.exit(1)
    return result


def get_skill_info(skill_path: str) -> dict:
    """SKILL.md에서 스킬 정보 추출"""
    skill_md_path = os.path.join(skill_path, 'SKILL.md')

    if not os.path.exists(skill_md_path):
        print(f"에러: SKILL.md를 찾을 수 없습니다: {skill_md_path}")
        sys.exit(1)

    with open(skill_md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # frontmatter에서 정보 추출
    info = {}

    # name 추출
    name_match = re.search(r'^name:\s*(.+)$', content, re.MULTILINE)
    if name_match:
        info['name'] = name_match.group(1).strip()

    # repo 추출
    repo_match = re.search(r'^repo:\s*(.+)$', content, re.MULTILINE)
    if repo_match:
        info['repo'] = repo_match.group(1).strip()

    # version 추출
    version_match = re.search(r'^version:\s*(.+)$', content, re.MULTILINE)
    if version_match:
        info['version'] = version_match.group(1).strip()

    if 'repo' not in info or 'TODO' in info.get('repo', ''):
        print("에러: SKILL.md에 유효한 repo 필드가 없습니다.")
        print("      원본 저장소 정보가 필요합니다. (예: repo: username/skill-name)")
        sys.exit(1)

    return info


def check_gh_cli():
    """GitHub CLI 설치 확인"""
    result = run_command(['which', 'gh'], check=False)
    if result.returncode != 0:
        print("에러: GitHub CLI(gh)가 설치되어 있지 않습니다.")
        print("      설치: https://cli.github.com/")
        sys.exit(1)

    # 로그인 상태 확인
    result = run_command(['gh', 'auth', 'status'], check=False)
    if result.returncode != 0:
        print("에러: GitHub에 로그인되어 있지 않습니다.")
        print("      실행: gh auth login")
        sys.exit(1)


def fork_and_clone(repo: str, temp_dir: str) -> str:
    """저장소 fork 및 clone"""
    print(f"📋 저장소 fork 중: {repo}")

    # fork (이미 있으면 무시)
    run_command(['gh', 'repo', 'fork', repo, '--clone=false'], check=False)

    # 내 계정명 가져오기
    result = run_command(['gh', 'api', 'user', '-q', '.login'])
    my_username = result.stdout.strip()

    # fork된 저장소 이름
    repo_name = repo.split('/')[-1]
    my_repo = f"{my_username}/{repo_name}"

    # clone
    clone_path = os.path.join(temp_dir, repo_name)
    print(f"📥 저장소 clone 중: {my_repo}")
    run_command(['gh', 'repo', 'clone', my_repo, clone_path])

    # upstream 추가
    run_command(['git', 'remote', 'add', 'upstream', f'https://github.com/{repo}.git'], cwd=clone_path, check=False)

    return clone_path


def copy_changes(skill_path: str, clone_path: str, skill_name: str):
    """수정된 파일들 복사"""
    print("📝 수정사항 복사 중...")

    # 스킬 폴더 내용을 clone된 저장소의 스킬 폴더로 복사
    target_skill_path = os.path.join(clone_path, skill_name)

    # 기존 스킬 폴더가 있으면 삭제
    if os.path.exists(target_skill_path):
        import shutil
        shutil.rmtree(target_skill_path)

    # 복사
    import shutil
    shutil.copytree(skill_path, target_skill_path)

    print(f"   ✓ {skill_path} -> {target_skill_path}")


def create_branch_and_commit(clone_path: str, message: str) -> str:
    """브랜치 생성 및 커밋"""
    # 브랜치명 생성 (안전한 문자만)
    safe_message = re.sub(r'[^a-zA-Z0-9가-힣-]', '-', message)[:30]
    branch_name = f"fix/{safe_message}"

    print(f"🌿 브랜치 생성: {branch_name}")
    run_command(['git', 'checkout', '-b', branch_name], cwd=clone_path)

    print("📦 변경사항 커밋 중...")
    run_command(['git', 'add', '.'], cwd=clone_path)
    run_command(['git', 'commit', '-m', f'fix: {message}'], cwd=clone_path)

    print("⬆️ 푸시 중...")
    run_command(['git', 'push', '-u', 'origin', branch_name], cwd=clone_path)

    return branch_name


def create_pr(clone_path: str, original_repo: str, branch_name: str, message: str):
    """PR 생성"""
    print("🔀 PR 생성 중...")

    pr_body = f"""## 문제
{message}

## 수정 내용
버그를 수정했습니다.

## 테스트
로컬에서 테스트 완료했습니다.
"""

    result = run_command([
        'gh', 'pr', 'create',
        '--repo', original_repo,
        '--title', f'fix: {message}',
        '--body', pr_body,
        '--head', branch_name
    ], cwd=clone_path)

    # PR URL 추출
    pr_url = result.stdout.strip()
    return pr_url


def main():
    parser = argparse.ArgumentParser(
        description='스킬 버그 수정을 원작자에게 PR로 제출합니다.'
    )
    parser.add_argument(
        'skill_path',
        help='수정한 스킬 경로 (예: .claude/skills/my-skill)'
    )
    parser.add_argument(
        '--message', '-m',
        required=True,
        help='버그 수정 설명 (예: "변환 오류 수정")'
    )

    args = parser.parse_args()

    # 경로 정규화
    skill_path = os.path.abspath(args.skill_path)

    if not os.path.exists(skill_path):
        print(f"에러: 스킬 경로가 존재하지 않습니다: {skill_path}")
        sys.exit(1)

    # GitHub CLI 확인
    check_gh_cli()

    # 스킬 정보 가져오기
    skill_info = get_skill_info(skill_path)
    skill_name = skill_info['name']
    original_repo = skill_info['repo']

    print(f"\n📍 스킬: {skill_name}")
    print(f"📍 원본 저장소: {original_repo}")
    print(f"📍 수정 내용: {args.message}\n")

    # 임시 디렉토리에서 작업
    with tempfile.TemporaryDirectory() as temp_dir:
        # fork 및 clone
        clone_path = fork_and_clone(original_repo, temp_dir)

        # 수정사항 복사
        copy_changes(skill_path, clone_path, skill_name)

        # 브랜치 생성 및 커밋
        branch_name = create_branch_and_commit(clone_path, args.message)

        # PR 생성
        pr_url = create_pr(clone_path, original_repo, branch_name, args.message)

    print(f"\n🎉 PR 생성 완료!")
    print(f"📎 PR URL: {pr_url}")
    print("\n원작자가 PR을 머지하면 다른 사용자들에게 업데이트가 전달됩니다.")


if __name__ == "__main__":
    main()
