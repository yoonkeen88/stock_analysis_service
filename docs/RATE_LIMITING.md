# 요청 제한 (Rate Limiting) 구현

## 문제
백엔드에 요청이 너무 많이 전송되는 문제

## 해결 방법

### 1. 프론트엔드 - 중복 요청 방지

#### Dashboard 컴포넌트
- **이전 symbol 추적**: `useRef`로 이전 symbol 저장, 변경 시에만 요청
- **로딩 중 플래그**: `isLoadingRef`로 동시 요청 방지

```javascript
// symbol이 실제로 변경되었을 때만 실행
if (prevSymbolRef.current === symbol) {
  return; // 중복 요청 방지
}

// 이미 로딩 중이면 중복 요청 방지
if (isLoadingRef.current) {
  return;
}
```

#### API 서비스 - 캐싱
- **5초 캐시**: 같은 요청을 5초 내에 반복하지 않음
- **진행 중 요청 추적**: 같은 요청이 진행 중이면 대기

```javascript
// 캐시 확인
if (requestCache.has(cacheKey)) {
  const cached = requestCache.get(cacheKey);
  if (age < 5000) {
    return cached.data; // 캐시된 데이터 반환
  }
}
```

### 2. 백엔드 - 요청 제한

#### Dashboard 엔드포인트
- **2초 제한**: 같은 심볼에 대해 2초 내 재요청 방지
- **요청 추적**: 함수 속성으로 마지막 요청 시간 저장

```python
# 같은 심볼에 대해 2초 내 재요청 방지
if time_since_last < 2:
    # 경고 로그만 남기고 진행
    print(f"Rate limit: Request too soon")
```

#### yfinance 서비스
- **30초 캐시**: 파일 시스템 캐시 (선택적)
- **재시도 제한**: 최대 3번만 재시도

## 효과

### 이전
- 컴포넌트 리렌더링마다 API 호출
- 같은 요청을 반복적으로 전송
- yfinance API에 과도한 요청

### 개선 후
- ✅ symbol 변경 시에만 요청
- ✅ 5초 내 동일 요청 캐시 사용
- ✅ 진행 중인 요청 재사용
- ✅ 백엔드에서 2초 내 재요청 경고

## 테스트

### 1. 프론트엔드 테스트
```javascript
// 브라우저 콘솔에서
// 같은 symbol로 여러 번 검색
// → 첫 요청만 전송되고 나머지는 캐시 사용
```

### 2. 백엔드 테스트
```bash
# 빠르게 연속 요청
curl http://localhost:8000/api/v1/dashboard/AAPL
curl http://localhost:8000/api/v1/dashboard/AAPL
# → 두 번째 요청에 경고 로그
```

## 추가 개선 가능 사항

1. **Redis 캐싱**: 서버 재시작 후에도 캐시 유지
2. **사용자별 제한**: IP 또는 세션별 요청 제한
3. **동적 캐시 시간**: 데이터 종류에 따라 다른 캐시 시간
4. **캐시 무효화**: 특정 조건에서 캐시 강제 갱신

