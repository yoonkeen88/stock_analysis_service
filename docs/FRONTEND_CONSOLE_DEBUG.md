# 프론트엔드 콘솔 로그 디버깅 가이드

## 문제: 브라우저 콘솔에 로그가 안 찍힘

## 확인 사항

### 1. 브라우저 콘솔 열기
- **Chrome/Edge**: `F12` 또는 `Cmd+Option+I` (Mac) / `Ctrl+Shift+I` (Windows)
- **Firefox**: `F12` 또는 `Cmd+Option+K` (Mac) / `Ctrl+Shift+K` (Windows)
- **Safari**: `Cmd+Option+C` (개발자 메뉴 활성화 필요)

### 2. 콘솔 필터 확인
- 콘솔 상단의 필터 버튼 확인
- "All levels" 또는 "Verbose" 선택
- 필터에 `[` 또는 특정 키워드가 있는지 확인

### 3. 페이지 새로고침
- `F5` 또는 `Cmd+R` (Mac) / `Ctrl+R` (Windows)
- 하드 리프레시: `Cmd+Shift+R` (Mac) / `Ctrl+Shift+R` (Windows)

## 예상되는 로그 순서

### 앱 시작 시
```
[Main] Application starting...
[Main] React version: 18.x.x
[Main] Environment: development
[Main] Root element: <div id="root">
[Main] Creating React root...
[Main] Rendering App component...
[Main] ✅ App rendered
[App] Component rendered
[App] Component mounted
```

### 검색 버튼 클릭 시
```
[SearchBar] handleSearch called { symbol: null, query: "AAPL" }
[SearchBar] searchSymbol: AAPL
[SearchBar] Navigating to: /dashboard/AAPL
[SearchBar] Navigation called, component should unmount
[App] Component rendered
[Dashboard] Module loaded
[Dashboard] Component rendered
[Dashboard] Component mounted with symbol: AAPL
[Dashboard] useEffect triggered { symbol: "AAPL", timestamp: "..." }
[Dashboard] loadDashboardData START { symbol: "AAPL", timestamp: "..." }
[Dashboard] About to call getDashboard('AAPL')
[API] getDashboard called with symbol: AAPL
[API] ========== REQUEST START ==========
```

## 문제 해결

### 문제 1: 아무 로그도 안 보임

**원인:**
- 콘솔이 닫혀있음
- 필터가 너무 제한적
- JavaScript 에러로 앱이 시작되지 않음

**해결:**
1. 콘솔 열기 (F12)
2. "All levels" 선택
3. 에러 탭 확인

### 문제 2: 일부 로그만 보임

**원인:**
- 컴포넌트가 마운트되지 않음
- 조건부 렌더링으로 컴포넌트가 숨겨짐

**해결:**
1. `[Main]` 로그 확인 (앱 시작 확인)
2. `[App]` 로그 확인 (메인 컴포넌트 확인)
3. `[SearchBar]` 로그 확인 (검색 바 확인)

### 문제 3: 검색 후 로그가 멈춤

**원인:**
- navigate가 작동하지 않음
- Dashboard 컴포넌트가 마운트되지 않음

**해결:**
1. `[SearchBar] Navigating to: ...` 로그 확인
2. URL이 변경되는지 확인
3. `[Dashboard]` 로그 확인

## 수동 테스트

### 브라우저 콘솔에서 직접 실행

```javascript
// 1. 콘솔이 작동하는지 확인
console.log('Test log');

// 2. React 컴포넌트 확인
document.querySelector('#root');

// 3. API 호출 테스트
fetch('http://localhost:8000/api/v1/dashboard/AAPL')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error);
```

### 네트워크 탭 확인

1. F12 → Network 탭
2. 검색 버튼 클릭
3. `/api/v1/dashboard/...` 요청 확인
4. 요청 상태 확인 (Pending, 200, 404, 500 등)

## 추가 디버깅

### React DevTools 설치

1. Chrome Extension: React Developer Tools
2. 설치 후 F12 → Components 탭
3. 컴포넌트 트리 확인
4. 각 컴포넌트의 props, state 확인

### Vite 개발 서버 확인

터미널에서 프론트엔드 서버 로그 확인:
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:3000/
➜  Network: use --host to expose
```

## 빠른 체크리스트

- [ ] 브라우저 콘솔 열기 (F12)
- [ ] 콘솔 필터 "All levels" 선택
- [ ] 페이지 새로고침 (F5)
- [ ] `[Main]` 로그 확인
- [ ] `[App]` 로그 확인
- [ ] 검색 버튼 클릭
- [ ] `[SearchBar]` 로그 확인
- [ ] `[Dashboard]` 로그 확인
- [ ] Network 탭에서 API 요청 확인

