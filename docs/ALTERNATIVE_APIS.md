# yfinance 대안 API 가이드 (참고용)

> **참고**: 현재는 `yf.download()`를 사용하여 안정적으로 작동합니다.  
> 대안 API는 필요시 참고용으로만 사용하세요.

## 문제점 (해결됨)
- ~~yfinance가 불안정하고 타임아웃 발생~~ → `yf.download()` 사용으로 해결
- ~~Rate limit 문제~~ → `yf.download()`가 더 안정적
- ~~응답이 느림~~ → 개선됨

## 현재 상태
- ✅ `yf.download()` 사용 중 (안정적)
- ✅ MultiIndex 컬럼 자동 처리
- ✅ 동적 컬럼 파싱

## 대안 API (필요시 참고용)

### 1. Yahoo Finance 직접 API (권장) ⭐

**장점:**
- ✅ yfinance 라이브러리 없이 직접 호출
- ✅ 더 빠르고 안정적
- ✅ API 키 불필요
- ✅ 무료

**사용법:**
```python
# app/core/config.py
USE_ALTERNATIVE_API = True  # .env 파일에 추가
```

**구현:**
- `market_data_service_alternative.py`에 구현됨
- Yahoo Finance 공식 API 엔드포인트 사용
- yfinance보다 안정적

### 2. Alpha Vantage API

**장점:**
- ✅ 공식 API
- ✅ 안정적
- ✅ 상세한 데이터

**제한:**
- ⚠️ 무료: 5 calls/min, 500 calls/day
- ⚠️ API 키 필요

**사용법:**
1. https://www.alphavantage.co/support/#api-key 에서 키 발급
2. `.env` 파일에 추가:
   ```
   ALPHA_VANTAGE_API_KEY=your_key_here
   USE_ALTERNATIVE_API=True
   ```

### 3. CoinGecko API (암호화폐 전용)

**장점:**
- ✅ API 키 불필요
- ✅ 무료
- ✅ 안정적
- ✅ 많은 암호화폐 지원

**제한:**
- ⚠️ 암호화폐만 지원
- ⚠️ Rate limit: 10-50 calls/min (무료)

**지원 심볼:**
- BTC-USD → bitcoin
- ETH-USD → ethereum
- BNB-USD → binancecoin
- SOL-USD → solana

### 4. 기타 옵션

#### Polygon.io
- 무료: 5 calls/min
- API 키 필요
- 주식 데이터 제공

#### Finnhub
- 무료: 60 calls/min
- API 키 필요
- 실시간 데이터

## 설정 방법

### 방법 1: Yahoo Finance 직접 API 사용 (가장 간단)

`.env` 파일:
```env
USE_ALTERNATIVE_API=True
```

### 방법 2: Alpha Vantage 사용

`.env` 파일:
```env
USE_ALTERNATIVE_API=True
ALPHA_VANTAGE_API_KEY=your_key_here
```

### 방법 3: yfinance 계속 사용

`.env` 파일:
```env
USE_ALTERNATIVE_API=False
# 또는 설정 안 함
```

## 코드 변경 사항

### 1. 새로운 서비스 파일
- `app/services/market_data_service_alternative.py` 생성
- 여러 API 소스 지원

### 2. 설정 추가
- `app/core/config.py`에 `USE_ALTERNATIVE_API` 추가
- 선택적 API 키 설정

### 3. Dashboard 엔드포인트
- 설정에 따라 자동으로 yfinance 또는 대안 API 선택

## 테스트

### 1. Yahoo Finance 직접 API 테스트
```bash
# .env에 추가
USE_ALTERNATIVE_API=True

# 서버 재시작
python -m app.main

# 테스트
curl http://localhost:8000/api/v1/dashboard/AAPL
```

### 2. Alpha Vantage 테스트
```bash
# .env에 추가
USE_ALTERNATIVE_API=True
ALPHA_VANTAGE_API_KEY=your_key

# 서버 재시작 후 테스트
```

## 비교

| API | 속도 | 안정성 | 무료 제한 | API 키 |
|-----|------|--------|----------|--------|
| yfinance | 느림 | 불안정 | 제한 없음 | 불필요 |
| Yahoo 직접 | 빠름 | 안정적 | 제한 없음 | 불필요 ⭐ |
| Alpha Vantage | 보통 | 안정적 | 5/min, 500/day | 필요 |
| CoinGecko | 빠름 | 안정적 | 10-50/min | 불필요 |

## 권장 사항

1. **Yahoo Finance 직접 API 사용** (가장 추천)
   - yfinance 문제 해결
   - 추가 설정 불필요
   - 빠르고 안정적

2. **Alpha Vantage** (API 키 있으면)
   - 더 많은 기능
   - 공식 API

3. **CoinGecko** (암호화폐만)
   - 암호화폐에 최적화

## 마이그레이션

기존 코드는 그대로 작동합니다:
- `USE_ALTERNATIVE_API=False` → yfinance 사용 (기본)
- `USE_ALTERNATIVE_API=True` → 대안 API 사용

서비스 인터페이스가 동일하므로 다른 코드 변경 불필요!

