# yfinance 타임아웃 문제 해결

## 문제 증상

터미널 로그에서 확인된 문제:
```
[YFINANCE] Attempt 1/3: Calling ticker.history(period='1mo', interval='1d')...
[YFINANCE] Attempt 2/3: Calling ticker.history(period='1mo', interval='1d')...
[YFINANCE] Attempt 3/3: Calling ticker.history(period='1mo', interval='1d')...
```

`ticker.history()` 호출이 응답하지 않고 계속 재시도만 하고 있습니다.

## 원인

1. **Yahoo Finance API 응답 지연**: API가 매우 느리거나 응답하지 않음
2. **Rate Limit**: 너무 많은 요청으로 인한 차단
3. **네트워크 문제**: 인터넷 연결 문제

## 해결 방법

### 1. 타임아웃 추가

각 `ticker.history()` 호출에 10초 타임아웃을 추가했습니다:

```python
signal.alarm(10)  # 10초 타임아웃
hist = ticker.history(period=test_period, interval=interval)
signal.alarm(0)  # 타임아웃 취소
```

### 2. Fallback 기간 순서 변경

짧은 기간부터 시도하도록 변경:
- 이전: `["1y", "6mo", "3mo", "1mo", "5d", "1d"]`
- 변경: `["5d", "1d", "1y", "6mo", "3mo", "1mo"]`

### 3. 상세 로깅

각 단계마다 로그를 출력하여 어디서 멈추는지 확인 가능

## 테스트 방법

### 1. 서버 재시작
```bash
python -m app.main
```

### 2. 검색 테스트
- 브라우저에서 종목 검색 (예: AAPL, TSLA)
- 터미널 로그 확인

### 3. 예상 로그

**성공 시:**
```
[YFINANCE] Attempt 1/3: Calling ticker.history...
[YFINANCE] History received: 30 rows
[YFINANCE] ✅ Returning result
```

**타임아웃 시:**
```
[YFINANCE] Attempt 1/3: Calling ticker.history...
[YFINANCE] ⚠️ Timeout error: ticker.history() timeout after 10 seconds
[YFINANCE] Waiting 2s before retry...
```

## 추가 개선 사항

### Windows 호환성

`signal.alarm()`은 Unix/macOS에서만 작동합니다. Windows에서는:
- `threading.Timer` 사용
- 또는 타임아웃 없이 진행 (더 긴 대기)

### 대안 방법

1. **더 짧은 타임아웃**: 5초로 줄이기
2. **캐싱**: 같은 종목 데이터를 일정 시간 캐시
3. **비동기 처리**: 백그라운드에서 데이터 가져오기

## 현재 상태

- ✅ 타임아웃 추가됨 (10초)
- ✅ Fallback 기간 순서 개선
- ✅ 상세 로깅 추가
- ⚠️ Windows에서는 signal.alarm이 작동하지 않을 수 있음

## 다음 단계

1. 서버 재시작 후 테스트
2. 로그 확인하여 타임아웃 발생 여부 확인
3. 필요시 타임아웃 시간 조정

