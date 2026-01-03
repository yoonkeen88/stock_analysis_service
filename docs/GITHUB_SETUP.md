# GitHub 저장소 설정 가이드

## 1. Git 초기화 및 첫 커밋

### 방법 1: 자동 스크립트 사용 (권장)

```bash
# 스크립트 실행
./scripts/setup_git.sh
```

### 방법 2: 수동 설정

```bash
# Git 초기화
git init

# 모든 파일 추가
git add .

# 첫 커밋
git commit -m "Initial commit: Stock Analysis Service"
```

## 2. GitHub에서 새 저장소 생성

1. GitHub에 로그인: https://github.com
2. 새 저장소 생성: https://github.com/new
   - Repository name: `stock_analysis_service`
   - Description: `최신 논문 기반 주식/비트코인 예측 웹 서비스`
   - Public 또는 Private 선택
   - **README, .gitignore, license는 추가하지 마세요** (이미 프로젝트에 있음)

## 3. 원격 저장소 연결 및 푸시

```bash
# 원격 저장소 추가 (YOUR_USERNAME을 실제 GitHub 사용자명으로 변경)
git remote add origin https://github.com/YOUR_USERNAME/stock_analysis_service.git

# 기본 브랜치를 main으로 설정
git branch -M main

# GitHub에 푸시
git push -u origin main
```

## 4. GitHub Actions 설정 (선택사항)

프로젝트에 포함된 GitHub Actions 워크플로우:

- **`.github/workflows/update-schema.yml`**: `app/db/models.py` 변경 시 스키마 다이어그램 자동 업데이트

이 워크플로우는 자동으로 활성화되며, `models.py`가 변경되면 스키마 다이어그램을 자동으로 업데이트합니다.

## 5. 저장소 설정 확인

GitHub 저장소에서 다음을 확인하세요:

- ✅ README.md가 제대로 표시되는지
- ✅ 스키마 다이어그램이 렌더링되는지 (`docs/SCHEMA_AUTO.md`)
- ✅ .gitignore가 제대로 작동하는지
- ✅ Issues와 Pull Requests가 활성화되어 있는지

## 6. 팀 협업 설정

### 브랜치 전략

- `main`: 프로덕션 배포용
- `develop`: 개발 브랜치
- `feature/*`: 기능 개발 브랜치
- `fix/*`: 버그 수정 브랜치

### 브랜치 보호 규칙 설정 (권장)

GitHub 저장소 설정에서:
1. Settings → Branches
2. Add rule for `main` branch
3. 다음 옵션 활성화:
   - Require pull request reviews before merging
   - Require status checks to pass before merging

## 7. 추가 설정 (선택사항)

### GitHub Pages 설정

문서를 GitHub Pages로 호스팅하려면:

1. Settings → Pages
2. Source: `main` branch, `/docs` folder 선택
3. 저장 후 `https://YOUR_USERNAME.github.io/stock_analysis_service/`에서 접근 가능

### Secrets 설정

환경 변수를 GitHub Secrets로 관리하려면:

1. Settings → Secrets and variables → Actions
2. 필요한 환경 변수 추가 (예: `DATABASE_URL`, `SECRET_KEY`)

## 문제 해결

### 인증 오류

```bash
# Personal Access Token 사용 (권장)
# GitHub → Settings → Developer settings → Personal access tokens → Generate new token
# 권한: repo (전체)

git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/stock_analysis_service.git
```

### 푸시 거부 오류

```bash
# 원격 저장소의 변경사항이 있는 경우
git pull origin main --allow-unrelated-histories
git push -u origin main
```

## 다음 단계

저장소가 설정되면:

1. ✅ Issues를 사용하여 작업 관리
2. ✅ Pull Requests로 코드 리뷰
3. ✅ GitHub Actions로 CI/CD 설정
4. ✅ 프로젝트 보드로 작업 추적

