# 빠른 시작 가이드

## 검색이 안 될 때 체크리스트

### ✅ 1단계: 백엔드 서버 실행 확인

```bash
# 터미널 1: 백엔드 실행
cd /Users/angwang-yun/Desktop/Project/stock_analysis_service

# 가상환경 활성화
source venv/bin/activate  # 또는 conda activate stock_analysis

# 서버 실행
python -m app.main
```

**확인**: `http://localhost:8000/docs`가 열리면 성공!

### ✅ 2단계: yfinance 작동 확인

```bash
# yfinance 테스트
python scripts/check_yfinance.py
```

**문제가 있으면:**
```bash
pip install --upgrade yfinance
```

### ✅ 3단계: 프론트엔드 실행

```bash
# 터미널 2: 프론트엔드 실행
cd frontend
npm install  # 처음 한 번만
npm run dev
```

**확인**: `http://localhost:3000`이 열리면 성공!

### ✅ 4단계: API 테스트

```bash
# API 테스트 스크립트 실행
python scripts/test_api.py
```

## DB에 데이터를 넣어야 하나?

**아니요!** yfinance가 실시간으로 데이터를 가져옵니다.

다만 다음은 DB에 저장됩니다:
- ✅ **예측 결과**: AI 예측을 생성하면 저장
- ✅ **뉴스**: 뉴스를 조회하면 자동 저장
- ✅ **검증 로그**: 예측 검증 시 저장

## 올바른 심볼 형식

### 주식
- ✅ `AAPL` (Apple)
- ✅ `TSLA` (Tesla)
- ✅ `MSFT` (Microsoft)

### 암호화폐
- ✅ `BTC-USD` (Bitcoin)
- ✅ `ETH-USD` (Ethereum)
- ❌ `BTC` (잘못된 형식)

**암호화폐는 반드시 `-USD`를 붙여야 합니다!**

## 문제 해결

### "서버에 연결할 수 없습니다"
→ 백엔드 서버가 실행 중인지 확인

### "종목 데이터를 찾을 수 없습니다"
→ 심볼 형식 확인 (암호화폐는 -USD 필요)

### "CORS 에러"
→ `app/core/config.py`의 CORS 설정 확인

더 자세한 내용은 `docs/TROUBLESHOOTING.md` 참고!

