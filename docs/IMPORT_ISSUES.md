# 모듈 임포트 문제 해결 가이드

## 문제: `app` 모듈을 찾을 수 없음

### 원인
Python이 프로젝트 루트 디렉토리를 모듈 경로에 포함하지 않아서 발생합니다.

### 해결 방법

#### 1. 프로젝트 루트에서 실행 (권장)

```bash
# 프로젝트 루트에서 실행
cd /Users/angwang-yun/Desktop/Project/stock_analysis_service
python -m app.main
```

#### 2. PYTHONPATH 환경 변수 설정

```bash
# 현재 세션에서만
export PYTHONPATH="${PYTHONPATH}:/Users/angwang-yun/Desktop/Project/stock_analysis_service"

# 영구적으로 설정 (zsh)
echo 'export PYTHONPATH="${PYTHONPATH}:/Users/angwang-yun/Desktop/Project/stock_analysis_service"' >> ~/.zshrc
source ~/.zshrc
```

#### 3. Anaconda 환경에서 실행

```bash
# Anaconda 환경 활성화
conda activate stock_analysis

# 프로젝트 루트로 이동
cd /Users/angwang-yun/Desktop/Project/stock_analysis_service

# 실행
python -m app.main
```

#### 4. uvicorn으로 직접 실행

```bash
# 프로젝트 루트에서
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 확인 방법

```bash
# Python 경로 확인
python -c "import sys; print('\n'.join(sys.path))"

# app 모듈 임포트 테스트
python -c "from app.core.config import settings; print('✅ Import successful')"
```

### 일반적인 실수

❌ **잘못된 방법:**
```bash
cd app
python main.py  # app 모듈을 찾을 수 없음
```

✅ **올바른 방법:**
```bash
cd /Users/angwang-yun/Desktop/Project/stock_analysis_service
python -m app.main
```

## Pydantic 경고 해결

### 경고 메시지
```
Field "model_name" has conflict with protected namespace "model_".
```

### 해결 방법

이미 코드에 `model_config = {"protected_namespaces": ()}` 설정이 추가되어 있습니다.

만약 다른 스키마에서도 같은 경고가 발생하면:

```python
class YourSchema(BaseModel):
    model_name: str
    
    model_config = {"protected_namespaces": ()}  # 이 줄 추가
```

## 추가 팁

### VS Code / Cursor에서 실행

`.vscode/settings.json` 또는 프로젝트 설정에서:

```json
{
  "python.analysis.extraPaths": [
    "${workspaceFolder}"
  ],
  "python.terminal.activateEnvironment": true
}
```

### 디버깅 모드로 실행

```bash
# 디버깅 정보와 함께 실행
python -m app.main --debug
```

