#!/usr/bin/env python3
"""
스킬 자동 업데이트 스크립트
SKILL.md의 frontmatter에서 repo와 version을 읽어 업데이트 여부를 확인하고 처리합니다.

사용법:
    python3 check_update.py <skill-path>
    python3 check_update.py .claude/skills/md2pdf
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request


def get_skill_info(skill_path: str) -> dict:
    """SKILL.md에서 스킬 정보 추출"""
    skill_md_path = os.path.join(skill_path, 'SKILL.md')

    if not os.path.exists(skill_md_path):
        print(f"에러: SKILL.md를 찾을 수 없습니다: {skill_md_path}")
        sys.exit(1)

    with open(skill_md_path, 'r', encoding='utf-8') as f:
        content = f.read()

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
        sys.exit(1)

    if 'version' not in info:
        print("에러: SKILL.md에 version 필드가 없습니다.")
        sys.exit(1)

    if 'name' not in info:
        print("에러: SKILL.md에 name 필드가 없습니다.")
        sys.exit(1)

    return info


def get_remote_version(repo: str, skill_name: str) -> str | None:
    """GitHub에서 원격 버전 확인"""
    # .claude/skills/skill-name/SKILL.md 경로로 시도
    urls = [
        f"https://raw.githubusercontent.com/{repo}/master/.claude/skills/{skill_name}/SKILL.md",
        f"https://raw.githubusercontent.com/{repo}/main/.claude/skills/{skill_name}/SKILL.md",
        f"https://raw.githubusercontent.com/{repo}/master/SKILL.md",
        f"https://raw.githubusercontent.com/{repo}/main/SKILL.md",
    ]

    for url in urls:
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                content = response.read().decode('utf-8')
                version_match = re.search(r'^version:\s*(.+)$', content, re.MULTILINE)
                if version_match:
                    return version_match.group(1).strip()
        except Exception:
            continue

    return None


def compare_versions(local: str, remote: str) -> int:
    """버전 비교: local < remote면 -1, 같으면 0, local > remote면 1"""
    def parse_version(v: str) -> tuple:
        # "1.0.0" -> (1, 0, 0)
        parts = v.split('.')
        return tuple(int(p) for p in parts if p.isdigit())

    local_parts = parse_version(local)
    remote_parts = parse_version(remote)

    if local_parts < remote_parts:
        return -1
    elif local_parts > remote_parts:
        return 1
    return 0


def update_skill(repo: str, skill_name: str, skill_path: str):
    """스킬 업데이트 실행"""
    print(f"📥 업데이트 다운로드 중...")

    # 임시 디렉토리에 다운로드
    with tempfile.TemporaryDirectory() as temp_dir:
        archive_url = f"https://github.com/{repo}/archive/refs/heads/master.tar.gz"
        archive_path = os.path.join(temp_dir, "archive.tar.gz")

        # 다운로드
        try:
            urllib.request.urlretrieve(archive_url, archive_path)
        except Exception:
            # master 브랜치가 없으면 main 시도
            archive_url = f"https://github.com/{repo}/archive/refs/heads/main.tar.gz"
            try:
                urllib.request.urlretrieve(archive_url, archive_path)
            except Exception as e:
                print(f"에러: 다운로드 실패 - {e}")
                sys.exit(1)

        # 압축 해제
        subprocess.run(['tar', '-xzf', archive_path, '-C', temp_dir], check=True)

        # 압축 해제된 폴더 찾기
        repo_name = repo.split('/')[-1]
        extracted_dirs = [d for d in os.listdir(temp_dir) if d.startswith(repo_name)]
        if not extracted_dirs:
            print("에러: 압축 해제 실패")
            sys.exit(1)

        extracted_path = os.path.join(temp_dir, extracted_dirs[0])

        # 새 스킬 경로 찾기
        new_skill_path = os.path.join(extracted_path, '.claude', 'skills', skill_name)
        if not os.path.exists(new_skill_path):
            # 루트에 SKILL.md가 있는 경우
            new_skill_path = extracted_path

        # 기존 스킬 삭제 및 교체
        parent_dir = os.path.dirname(skill_path)
        if os.path.exists(skill_path):
            shutil.rmtree(skill_path)

        shutil.copytree(new_skill_path, skill_path)

    print(f"   ✓ 업데이트 완료")


def main():
    parser = argparse.ArgumentParser(
        description='스킬 업데이트를 확인하고 적용합니다.'
    )
    parser.add_argument(
        'skill_path',
        help='스킬 경로 (예: .claude/skills/md2pdf)'
    )
    parser.add_argument(
        '--auto', '-a',
        action='store_true',
        help='업데이트가 있으면 자동으로 적용'
    )
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='최신 버전일 때 출력 없음'
    )

    args = parser.parse_args()

    # 경로 정규화
    skill_path = os.path.abspath(args.skill_path)

    if not os.path.exists(skill_path):
        print(f"에러: 스킬 경로가 존재하지 않습니다: {skill_path}")
        sys.exit(1)

    # 스킬 정보 가져오기
    skill_info = get_skill_info(skill_path)
    skill_name = skill_info['name']
    repo = skill_info['repo']
    local_version = skill_info['version']

    # 원격 버전 확인
    remote_version = get_remote_version(repo, skill_name)

    if remote_version is None:
        print(f"⚠️  원격 버전을 확인할 수 없습니다: {repo}")
        sys.exit(1)

    # 버전 비교
    comparison = compare_versions(local_version, remote_version)

    if comparison == 0:
        if not args.quiet:
            print(f"✓ {skill_name} v{local_version} - 최신 버전입니다.")
        sys.exit(0)
    elif comparison > 0:
        print(f"⚠️  {skill_name} v{local_version} - 로컬이 원격(v{remote_version})보다 높습니다.")
        sys.exit(0)
    else:
        print(f"🔄 {skill_name} 업데이트 가능: v{local_version} → v{remote_version}")

        if args.auto:
            update_skill(repo, skill_name, skill_path)
            print(f"🔄 {skill_name} 업데이트 완료: v{local_version} → v{remote_version}")
        else:
            print(f"\n업데이트하려면 --auto 옵션을 사용하세요:")
            print(f"  python3 {__file__} {args.skill_path} --auto")

        sys.exit(0)


if __name__ == "__main__":
    main()
