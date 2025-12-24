#!/usr/bin/env python3
"""
SKILL.md 버전 자동 증가 스크립트
변경된 파일을 분석하여 자동으로 patch 버전을 증가시킵니다.

사용법:
    python3 auto_version_bump.py <skill-path>
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


def get_changed_files(skill_path: Path) -> list[str]:
    """변경된 파일 목록 가져오기"""
    returncode, stdout, stderr = run_command(
        ['git', 'status', '--porcelain'],
        cwd=str(skill_path)
    )

    if returncode != 0:
        print(f"❌ 에러: git status 실패 - {stderr}")
        sys.exit(1)

    changed_files = []
    for line in stdout.strip().split('\n'):
        if not line:
            continue
        # 파일명 추출 (앞의 상태 코드 제거)
        file_path = line[3:].strip()
        changed_files.append(file_path)

    return changed_files


def should_bump_version(changed_files: list[str]) -> bool:
    """버전 업데이트가 필요한지 판단"""
    for file_path in changed_files:
        # SKILL.md 변경 (경로 포함 가능)
        if file_path.endswith('SKILL.md') or file_path == 'SKILL.md':
            return True
        # scripts/ 내 파일 변경 (경로 포함 가능)
        if 'scripts/' in file_path:
            return True
        # references/ 내 파일 변경 (경로 포함 가능)
        if 'references/' in file_path:
            return True

    return False


def get_current_version(skill_path: Path) -> str:
    """SKILL.md에서 현재 버전 읽기"""
    skill_md_path = skill_path / 'SKILL.md'

    if not skill_md_path.exists():
        print(f"❌ 에러: SKILL.md를 찾을 수 없습니다: {skill_md_path}")
        sys.exit(1)

    with open(skill_md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    version_match = re.search(r'^version:\s*(.+)$', content, re.MULTILINE)
    if not version_match:
        print("❌ 에러: SKILL.md에 version 필드가 없습니다.")
        sys.exit(1)

    return version_match.group(1).strip()


def bump_patch_version(version: str) -> str:
    """patch 버전 증가 (1.0.2 → 1.0.3)"""
    parts = version.split('.')
    if len(parts) != 3:
        print(f"❌ 에러: 잘못된 버전 형식: {version}")
        sys.exit(1)

    major, minor, patch = parts
    new_patch = int(patch) + 1
    return f"{major}.{minor}.{new_patch}"


def update_version_in_skill_md(skill_path: Path, old_version: str, new_version: str):
    """SKILL.md의 버전 업데이트"""
    skill_md_path = skill_path / 'SKILL.md'

    with open(skill_md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # version 필드 교체
    updated_content = re.sub(
        r'^version:\s*.+$',
        f'version: {new_version}',
        content,
        flags=re.MULTILINE
    )

    with open(skill_md_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print(f"   ✓ 버전 업데이트: {old_version} → {new_version}")


def auto_version_bump(skill_path: str):
    """자동 버전 증가 실행"""
    skill_path = Path(skill_path).resolve()

    if not skill_path.exists():
        print(f"❌ 에러: 스킬 경로가 존재하지 않습니다: {skill_path}")
        sys.exit(1)

    # 1. 변경된 파일 확인
    changed_files = get_changed_files(skill_path)

    if not changed_files:
        print("   변경사항 없음 - 버전 유지")
        return

    # 2. 버전 업데이트 필요 여부 판단
    if not should_bump_version(changed_files):
        print("   버전 업데이트 불필요 (README.md 등 문서만 변경)")
        return

    # 3. 현재 버전 읽기
    current_version = get_current_version(skill_path)

    # 4. 새 버전 계산
    new_version = bump_patch_version(current_version)

    # 5. SKILL.md 업데이트
    update_version_in_skill_md(skill_path, current_version, new_version)

    # 6. git add SKILL.md
    returncode, stdout, stderr = run_command(
        ['git', 'add', 'SKILL.md'],
        cwd=str(skill_path)
    )

    if returncode != 0:
        print(f"❌ 에러: git add 실패 - {stderr}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='SKILL.md 버전을 자동으로 증가시킵니다.'
    )
    parser.add_argument(
        'skill_path',
        help='스킬 디렉토리 경로'
    )

    args = parser.parse_args()
    auto_version_bump(args.skill_path)


if __name__ == "__main__":
    main()
