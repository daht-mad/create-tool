# 설치 가이드

## Step 1: 설치 확인

```bash
which dahtmad-md2pdf
```

## Step 2: 설치되어 있지 않으면 자동 설치

```bash
git clone https://github.com/daht-mad/md2pdf.git /tmp/dahtmad-md2pdf
cd /tmp/dahtmad-md2pdf && npm install && npm link
```

## Step 3: 설치 확인

```bash
which dahtmad-md2pdf
# 출력: /usr/local/bin/dahtmad-md2pdf (또는 유사 경로)
```

## 의존성

- Node.js 18+
- npm
- git

## 문제 해결

### npm link 권한 오류

```bash
sudo npm link
```

### Node.js 버전 오류

```bash
node --version
# v18 이상이어야 함
```
