#!/usr/bin/env python3
"""
스킬 초기화 스크립트
새 스킬 디렉토리와 기본 파일들을 생성합니다.

사용법:
    python3 init_skill.py <skill-name> --path <output-directory>
"""

import argparse
import os
import sys


def create_skill_md(skill_name: str) -> str:
    """SKILL.md 템플릿 생성"""
    return f'''---
name: {skill_name}
version: 1.0.0
repo: TODO/username/{skill_name}
description: |
  TODO: 이 스킬이 무엇을 하는지 설명하세요.
  다음과 같은 요청에 이 스킬을 사용하세요:
  - "TODO: 트리거 예시 1"
  - "TODO: 트리거 예시 2"
---

# {skill_name}

TODO: 스킬 설명을 작성하세요.

## 사용법

TODO: 기본 사용법을 작성하세요.

## 주요 기능

- TODO: 기능 1
- TODO: 기능 2
'''


def create_example_script() -> str:
    """예시 스크립트 생성"""
    return '''#!/usr/bin/env python3
"""
예시 스크립트
TODO: 필요에 따라 수정하거나 삭제하세요.
"""

import sys


def main():
    print("Hello from example script!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''


def create_example_reference() -> str:
    """예시 참조 문서 생성"""
    return '''# 참조 문서

TODO: 필요에 따라 수정하거나 삭제하세요.

## 섹션 1

상세 내용...

## 섹션 2

상세 내용...
'''


def create_example_asset() -> str:
    """예시 에셋 파일 생성"""
    return '''# 에셋 README

이 디렉토리에는 출력에 사용되는 에셋 파일들이 저장됩니다.
예: 템플릿, 이미지, 폰트 등

TODO: 필요한 에셋을 추가하고 이 파일은 삭제하세요.
'''


def create_check_update_script() -> str:
    """check_update.py 스크립트 생성 (자동 업데이트용)"""
    return '''#!/usr/bin/env python3
"""
스킬 자동 업데이트 스크립트
SKILL.md의 frontmatter에서 repo와 version을 읽어 업데이트 여부를 확인하고 처리합니다.

사용법:
    python3 check_update.py [--auto] [--quiet]
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request


def get_skill_path() -> str:
    """현재 스크립트 기준 스킬 경로 반환"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_skill_info(skill_path: str) -> dict:
    """SKILL.md에서 스킬 정보 추출"""
    skill_md_path = os.path.join(skill_path, 'SKILL.md')

    if not os.path.exists(skill_md_path):
        print(f"에러: SKILL.md를 찾을 수 없습니다: {skill_md_path}")
        sys.exit(1)

    with open(skill_md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    info = {}

    name_match = re.search(r'^name:\\s*(.+)$', content, re.MULTILINE)
    if name_match:
        info['name'] = name_match.group(1).strip()

    repo_match = re.search(r'^repo:\\s*(.+)$', content, re.MULTILINE)
    if repo_match:
        info['repo'] = repo_match.group(1).strip()

    version_match = re.search(r'^version:\\s*(.+)$', content, re.MULTILINE)
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
    urls = [
        f"https://raw.githubusercontent.com/{repo}/master/SKILL.md",
        f"https://raw.githubusercontent.com/{repo}/main/SKILL.md",
    ]

    for url in urls:
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                content = response.read().decode('utf-8')
                version_match = re.search(r'^version:\\s*(.+)$', content, re.MULTILINE)
                if version_match:
                    return version_match.group(1).strip()
        except Exception:
            continue

    return None


def compare_versions(local: str, remote: str) -> int:
    """버전 비교: local < remote면 -1, 같으면 0, local > remote면 1"""
    def parse_version(v: str) -> tuple:
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

    with tempfile.TemporaryDirectory() as temp_dir:
        archive_url = f"https://github.com/{repo}/archive/refs/heads/master.tar.gz"
        archive_path = os.path.join(temp_dir, "archive.tar.gz")

        try:
            urllib.request.urlretrieve(archive_url, archive_path)
        except Exception:
            archive_url = f"https://github.com/{repo}/archive/refs/heads/main.tar.gz"
            try:
                urllib.request.urlretrieve(archive_url, archive_path)
            except Exception as e:
                print(f"에러: 다운로드 실패 - {e}")
                sys.exit(1)

        subprocess.run(['tar', '-xzf', archive_path, '-C', temp_dir], check=True)

        repo_name = repo.split('/')[-1]
        extracted_dirs = [d for d in os.listdir(temp_dir) if d.startswith(repo_name)]
        if not extracted_dirs:
            print("에러: 압축 해제 실패")
            sys.exit(1)

        extracted_path = os.path.join(temp_dir, extracted_dirs[0])

        if os.path.exists(skill_path):
            shutil.rmtree(skill_path)

        shutil.copytree(extracted_path, skill_path)

    print(f"   ✓ 업데이트 완료")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='스킬 업데이트를 확인하고 적용합니다.')
    parser.add_argument('--auto', '-a', action='store_true', help='업데이트가 있으면 자동으로 적용')
    parser.add_argument('--quiet', '-q', action='store_true', help='최신 버전일 때 출력 없음')

    args = parser.parse_args()

    skill_path = get_skill_path()
    skill_info = get_skill_info(skill_path)
    skill_name = skill_info['name']
    repo = skill_info['repo']
    local_version = skill_info['version']

    remote_version = get_remote_version(repo, skill_name)

    if remote_version is None:
        if not args.quiet:
            print(f"⚠️  원격 버전을 확인할 수 없습니다: {repo}")
        sys.exit(0)

    comparison = compare_versions(local_version, remote_version)

    if comparison == 0:
        if not args.quiet:
            print(f"✓ {skill_name} v{local_version} - 최신 버전입니다.")
        sys.exit(0)
    elif comparison > 0:
        if not args.quiet:
            print(f"⚠️  {skill_name} v{local_version} - 로컬이 원격(v{remote_version})보다 높습니다.")
        sys.exit(0)
    else:
        print(f"🔄 {skill_name} 업데이트 가능: v{local_version} → v{remote_version}")

        if args.auto:
            update_skill(repo, skill_name, skill_path)
            print(f"🔄 {skill_name} 업데이트 완료: v{local_version} → v{remote_version}")
        else:
            print(f"\\n업데이트하려면 --auto 옵션을 사용하세요:")
            print(f"  python3 scripts/check_update.py --auto")

        sys.exit(0)


if __name__ == "__main__":
    main()
'''


def create_readme(skill_name: str) -> str:
    """README.md 템플릿 생성 (GitHub 배포용)"""
    return f'''# {skill_name}

TODO: 스킬에 대한 한 줄 설명을 작성하세요.

## 기능

- TODO: 기능 1
- TODO: 기능 2
- TODO: 기능 3

## 설치

```bash
mkdir -p .claude/skills && curl -L https://github.com/TODO_USERNAME/{skill_name}/archive/refs/heads/master.tar.gz | tar -xz -C /tmp && mv /tmp/{skill_name}-master .claude/skills/{skill_name}
```

## 필요 환경

- TODO: 필요한 도구/라이브러리 (없으면 이 섹션 삭제)

---

Last updated: TODO_DATE
'''


def init_skill(skill_name: str, output_path: str) -> None:
    """스킬 디렉토리 구조 초기화"""

    # 스킬 디렉토리 경로
    skill_dir = os.path.join(output_path, skill_name)

    # 디렉토리 생성
    directories = [
        skill_dir,
        os.path.join(skill_dir, 'scripts'),
        os.path.join(skill_dir, 'references'),
        os.path.join(skill_dir, 'assets'),
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ 디렉토리 생성: {directory}")

    # SKILL.md 생성
    skill_md_path = os.path.join(skill_dir, 'SKILL.md')
    with open(skill_md_path, 'w', encoding='utf-8') as f:
        f.write(create_skill_md(skill_name))
    print(f"✓ 파일 생성: {skill_md_path}")

    # 예시 스크립트 생성
    script_path = os.path.join(skill_dir, 'scripts', 'example.py')
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(create_example_script())
    os.chmod(script_path, 0o755)
    print(f"✓ 파일 생성: {script_path}")

    # check_update.py 생성 (자동 업데이트용)
    check_update_path = os.path.join(skill_dir, 'scripts', 'check_update.py')
    with open(check_update_path, 'w', encoding='utf-8') as f:
        f.write(create_check_update_script())
    os.chmod(check_update_path, 0o755)
    print(f"✓ 파일 생성: {check_update_path}")

    # 예시 참조 문서 생성
    reference_path = os.path.join(skill_dir, 'references', 'example.md')
    with open(reference_path, 'w', encoding='utf-8') as f:
        f.write(create_example_reference())
    print(f"✓ 파일 생성: {reference_path}")

    # 예시 에셋 README 생성
    asset_readme_path = os.path.join(skill_dir, 'assets', 'README.md')
    with open(asset_readme_path, 'w', encoding='utf-8') as f:
        f.write(create_example_asset())
    print(f"✓ 파일 생성: {asset_readme_path}")

    # README.md 생성 (GitHub 배포용)
    readme_path = os.path.join(skill_dir, 'README.md')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(create_readme(skill_name))
    print(f"✓ 파일 생성: {readme_path}")

    print(f"\n🎉 스킬 '{skill_name}' 초기화 완료!")
    print(f"   위치: {skill_dir}")
    print("\n다음 단계:")
    print("1. SKILL.md를 편집하여 스킬 설명 작성")
    print("2. README.md의 TODO_USERNAME과 TODO_DATE 수정")
    print("3. 필요한 scripts/, references/, assets/ 파일 추가")
    print("4. 불필요한 예시 파일 삭제")


def main():
    parser = argparse.ArgumentParser(
        description='새 스킬 디렉토리를 초기화합니다.'
    )
    parser.add_argument(
        'skill_name',
        help='스킬 이름 (예: my-skill)'
    )
    parser.add_argument(
        '--path',
        default='.',
        help='스킬을 생성할 디렉토리 (기본값: 현재 디렉토리)'
    )

    args = parser.parse_args()

    # 스킬 이름 검증
    if not args.skill_name.replace('-', '').replace('_', '').isalnum():
        print("에러: 스킬 이름은 영문자, 숫자, 하이픈, 언더스코어만 사용 가능합니다.")
        sys.exit(1)

    # 출력 경로 확인
    output_path = os.path.abspath(args.path)
    if not os.path.exists(output_path):
        print(f"에러: 경로가 존재하지 않습니다: {output_path}")
        sys.exit(1)

    # 이미 존재하는지 확인
    skill_dir = os.path.join(output_path, args.skill_name)
    if os.path.exists(skill_dir):
        print(f"에러: 스킬 디렉토리가 이미 존재합니다: {skill_dir}")
        sys.exit(1)

    init_skill(args.skill_name, output_path)


if __name__ == "__main__":
    main()
