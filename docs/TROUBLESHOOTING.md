# 문제 해결 가이드

## 검색이 안 될 때

### 1. 백엔드 서버 확인

**백엔드 서버가 실행 중인지 확인:**
```bash
# 서버 실행 확인
ps aux | grep "python.*app.main"

# 또는 직접 확인
curl http://localhost:8000/health
```

**서버가 실행 중이 아니면:**
```bash
# 가상환경 활성화
source venv/bin/activate  # 또는 conda activate stock_analysis

# 서버 실행
python -m app.main
# 또는
uvicorn app.main:app --reload
```

### 2. API 테스트

**스크립트로 API 테스트:**
```bash
python scripts/test_api.py
```

**수동으로 테스트:**
```bash
# 브라우저에서 열기
http://localhost:8000/docs

# 또는 curl로 테스트
curl http://localhost:8000/api/v1/dashboard/AAPL
```

### 3. 프론트엔드 확인

**프론트엔드 서버 실행:**
```bash
cd frontend
npm run dev
```

**브라우저 콘솔 확인:**
- F12로 개발자 도구 열기
- Console 탭에서 에러 확인
- Network 탭에서 API 요청 확인

### 4. CORS 문제

**백엔드 CORS 설정 확인:**
- `app/core/config.py`의 `BACKEND_CORS_ORIGINS` 확인
- 프론트엔드 URL이 포함되어 있는지 확인

### 5. 환경 변수 확인

**프론트엔드 `.env` 파일:**
```bash
# frontend/.env
VITE_API_URL=http://localhost:8000/api/v1
```

## DB에 데이터를 넣어야 하나?

**아니요!** yfinance를 사용하므로 실시간으로 데이터를 가져옵니다.

다만 다음 데이터는 DB에 저장됩니다:
- **예측 결과 (Prediction)**: AI 모델로 예측을 생성해야 저장됨
- **뉴스 (NewsLog)**: 뉴스를 조회하면 자동으로 저장됨
- **예측 검증 (PredictionLog)**: 예측을 검증하면 저장됨

## 초기 데이터가 필요한 경우

### 테스트용 예측 데이터 생성

```python
# scripts/create_test_data.py
from app.core.database import SessionLocal
from app.db.models import Prediction
from datetime import datetime, timedelta

db = SessionLocal()

# 테스트 예측 생성
prediction = Prediction(
    symbol="AAPL",
    model_name="test_model",
    predicted_price=150.0,
    confidence=0.85,
    prediction_date=datetime.now() + timedelta(days=1)
)

db.add(prediction)
db.commit()
print("테스트 데이터 생성 완료!")
```

## 자주 발생하는 문제

### 1. "Network Error" 또는 "서버에 연결할 수 없습니다"

**원인**: 백엔드 서버가 실행되지 않음

**해결**:
```bash
# 백엔드 서버 실행
python -m app.main
```

### 2. "CORS policy" 에러

**원인**: CORS 설정 문제

**해결**: `app/core/config.py`에서 CORS 설정 확인

### 3. "404 Not Found"

**원인**: API 엔드포인트 경로 오류

**해결**: 
- `frontend/src/services/api.js`의 API 경로 확인
- 백엔드 `app/api/v1/api.py`의 라우터 설정 확인

### 4. yfinance 데이터 가져오기 실패

**원인**: 인터넷 연결 또는 yfinance 라이브러리 문제

**해결**:
```bash
# yfinance 재설치
pip install --upgrade yfinance

# 테스트
python -c "import yfinance as yf; print(yf.Ticker('AAPL').info['symbol'])"
```

## 디버깅 팁

### 백엔드 로그 확인
- FastAPI는 자동으로 요청 로그를 출력합니다
- 터미널에서 에러 메시지 확인

### 프론트엔드 로그 확인
- 브라우저 개발자 도구 > Console
- Network 탭에서 API 요청/응답 확인

### API 직접 테스트
- `http://localhost:8000/docs`에서 Swagger UI 사용
- 각 엔드포인트를 직접 테스트 가능

