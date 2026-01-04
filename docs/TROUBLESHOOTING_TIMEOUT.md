# 타임아웃 문제 해결 가이드

## 증상
- 검색 시 타임아웃 발생
- 프론트엔드와 백엔드 서버 모두 실행 중이지만 응답 없음
- 브라우저 콘솔에 타임아웃 에러

## 원인

### 1. Yahoo Finance API 응답 지연
- yfinance가 Yahoo Finance API에서 데이터를 가져올 때 시간이 오래 걸릴 수 있음
- Rate limit에 걸리면 더 느려짐

### 2. 타임아웃 설정이 너무 짧음
- 기본 타임아웃: 10초
- 변경: 30초로 증가

## 해결 방법

### 1. 타임아웃 증가 (이미 적용됨)
```javascript
// frontend/src/services/api.js
timeout: 30000, // 30초
```

### 2. 브라우저 콘솔 확인
1. F12로 개발자 도구 열기
2. Console 탭에서 에러 메시지 확인
3. Network 탭에서 API 요청 상태 확인

### 3. 백엔드 로그 확인
터미널에서 백엔드 서버 로그를 확인:
```
INFO:     127.0.0.1:xxxxx - "GET /api/v1/dashboard/AAPL HTTP/1.1" 200 OK
```

### 4. 수동 테스트
```bash
# 백엔드 직접 테스트
curl http://localhost:8000/api/v1/dashboard/AAPL

# 응답이 오는지 확인
```

## 디버깅 단계

### 1단계: 서버 상태 확인
```bash
# 백엔드
curl http://localhost:8000/health

# 프론트엔드
curl http://localhost:3000
```

### 2단계: API 직접 호출
```bash
# 브라우저에서 직접 접속
http://localhost:8000/api/v1/dashboard/AAPL
```

### 3단계: 브라우저 콘솔 확인
- F12 → Console 탭
- 에러 메시지 확인
- `[API Request]`, `[API Response]` 로그 확인

### 4단계: 네트워크 탭 확인
- F12 → Network 탭
- `/api/v1/dashboard/...` 요청 찾기
- Status, Time 확인

## 일반적인 문제

### 문제 1: CORS 에러
**증상:** 브라우저 콘솔에 CORS 에러
**해결:** `app/core/config.py`의 `BACKEND_CORS_ORIGINS` 확인

### 문제 2: 연결 거부
**증상:** "서버에 연결할 수 없습니다"
**해결:** 백엔드 서버가 실행 중인지 확인

### 문제 3: 타임아웃
**증상:** "요청 시간이 초과되었습니다"
**해결:** 
- 30초로 타임아웃 증가 (이미 적용됨)
- Yahoo Finance API가 느릴 수 있으므로 잠시 후 재시도

## 빠른 해결

1. **브라우저 새로고침** (F5)
2. **서버 재시작**
   ```bash
   # 백엔드
   python -m app.main
   
   # 프론트엔드
   npm run dev
   ```
3. **다른 종목으로 테스트** (AAPL, TSLA 등)
4. **1-2분 대기 후 재시도** (Rate limit 해제 대기)

## 로그 확인

### 프론트엔드 로그
브라우저 콘솔에서:
- `[API Request]` - 요청 시작
- `[API Response]` - 응답 받음
- `[Dashboard]` - Dashboard 로딩 상태

### 백엔드 로그
터미널에서:
- `INFO: ... GET /api/v1/dashboard/...` - 요청 받음
- 에러 메시지 확인

## 추가 팁

- **개발 모드**: 타임아웃을 더 길게 설정 가능
- **프로덕션**: 캐싱을 추가하여 성능 개선
- **모니터링**: API 응답 시간 추적

