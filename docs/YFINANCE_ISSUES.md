# yfinance 알려진 문제 및 해결 방법

## "Expecting value: line 1 column 1 (char 0)" 에러

이 에러는 Yahoo Finance API가 빈 응답을 반환할 때 발생합니다.

### 원인
- Yahoo Finance API rate limit
- API 일시적 장애
- 특정 종목에 대한 데이터 제한

### 해결 방법

1. **잠시 대기 후 재시도**
   - 1-2분 정도 기다린 후 다시 시도
   - Rate limit은 시간이 지나면 자동으로 해제됨

2. **다른 종목으로 테스트**
   - 주식: AAPL, TSLA, MSFT 등
   - 암호화폐는 때때로 더 불안정할 수 있음

3. **더 짧은 기간으로 시도**
   - 코드에서 자동으로 5d, 1d로 fallback 시도

## BTC-USD, ETH-USD 등 암호화폐 문제

암호화폐는 주식보다 더 자주 문제가 발생할 수 있습니다.

### 해결 방법

1. **심볼 형식 확인**
   - ✅ 올바른 형식: `BTC-USD`, `ETH-USD`
   - ❌ 잘못된 형식: `BTC`, `ETH`

2. **대안 종목 시도**
   - 주식으로 먼저 테스트 (AAPL, TSLA 등)
   - 암호화폐는 나중에 테스트

3. **시간대 문제**
   - "No timezone found" 에러는 일시적일 수 있음
   - 잠시 후 재시도

## Rate Limit 대응

### 증상
- "429 Too Many Requests"
- "Expecting value" 에러
- 연속된 요청 실패

### 해결
1. 요청 간 딜레이 추가 (코드에 포함됨)
2. 1-2분 대기 후 재시도
3. 한 번에 여러 종목 검색하지 않기

## 테스트 권장 순서

1. **먼저 주식 테스트**
   - AAPL (Apple) - 가장 안정적
   - TSLA (Tesla)
   - MSFT (Microsoft)

2. **그 다음 암호화폐**
   - BTC-USD
   - ETH-USD

3. **문제 발생 시**
   - 1-2분 대기
   - 서버 재시작
   - 다른 종목으로 테스트

## 코드 개선 사항

현재 코드에는 다음이 포함되어 있습니다:
- ✅ 여러 기간으로 자동 fallback (1mo → 5d → 1d)
- ✅ "Expecting value" 에러 감지 및 처리
- ✅ Rate limit 자동 재시도
- ✅ 점진적 대기 시간

## 추가 개선 가능 사항

1. **캐싱**: 같은 종목 데이터를 일정 시간 캐시
2. **대체 API**: 다른 데이터 소스 추가
3. **사용자 알림**: Rate limit 시 사용자에게 명확한 안내

