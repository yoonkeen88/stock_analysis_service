# 검색 버튼 클릭 시 호출 흐름

## 전체 흐름 다이어그램

```
[사용자] 검색 버튼 클릭
    ↓
[SearchBar.jsx] handleSearch()
    ↓
[React Router] navigate('/dashboard/AAPL')
    ↓
[Dashboard.jsx] useEffect() → loadDashboardData()
    ↓
[api.js] getDashboard('AAPL')
    ↓
[Axios] GET http://localhost:8000/api/v1/dashboard/AAPL
    ↓
[백엔드] FastAPI Router
    ↓
[dashboard.py] get_stock_dashboard('AAPL')
    ↓
[market_data_service.py] get_market_data('AAPL')
    ↓
[yfinance] ticker.history() + ticker.info
    ↓
[응답] JSON 데이터 반환
    ↓
[프론트엔드] Dashboard.jsx에 데이터 표시
```

## 상세 단계별 설명

### 1단계: 프론트엔드 - SearchBar 컴포넌트

**파일:** `frontend/src/components/SearchBar.jsx`

```javascript
// 사용자가 검색 버튼 클릭
<button onClick={() => handleSearch()}>검색</button>

// handleSearch() 함수 실행
const handleSearch = (symbol = null) => {
  const searchSymbol = symbol || query.trim().toUpperCase();
  
  if (!searchSymbol) return;
  
  // 검색 히스토리에 추가
  const newHistory = [searchSymbol, ...searchHistory.filter(item => item !== searchSymbol)].slice(0, 10);
  setSearchHistory(newHistory);
  localStorage.setItem('searchHistory', JSON.stringify(newHistory));
  
  // ⭐ 핵심: React Router로 페이지 이동
  navigate(`/dashboard/${searchSymbol}`);  // 예: '/dashboard/AAPL'
  
  setQuery('');
  setShowSuggestions(false);
};
```

**결과:** React Router가 `/dashboard/AAPL` 경로로 이동

---

### 2단계: 프론트엔드 - Dashboard 컴포넌트 마운트

**파일:** `frontend/src/pages/Dashboard.jsx`

```javascript
// Dashboard 컴포넌트가 마운트되거나 symbol이 변경될 때
useEffect(() => {
  loadDashboardData();  // ⭐ API 호출 시작
}, [symbol]);

// loadDashboardData() 함수
const loadDashboardData = async () => {
  try {
    setLoading(true);
    setError(null);
    
    if (!symbol) {
      throw new Error('종목 심볼이 없습니다.');
    }
    
    console.log(`[Dashboard] Loading data for: ${symbol}`);
    
    // ⭐ API 호출
    const result = await getDashboard(symbol);
    
    if (!result) {
      throw new Error('데이터를 받지 못했습니다.');
    }
    
    setData(result);
  } catch (err) {
    setError(err.message);
    console.error('[Dashboard] Load error:', err);
  } finally {
    setLoading(false);
  }
};
```

**결과:** `getDashboard(symbol)` 함수 호출

---

### 3단계: 프론트엔드 - API 서비스

**파일:** `frontend/src/services/api.js`

```javascript
// getDashboard 함수
export const getDashboard = async (symbol) => {
  // ⭐ Axios로 HTTP GET 요청
  return apiClient.get(`/dashboard/${symbol}`);
  // 실제 URL: http://localhost:8000/api/v1/dashboard/AAPL
};

// apiClient 설정
const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api/v1',  // 또는 VITE_API_URL
  timeout: 30000,  // 30초 타임아웃
});
```

**Axios 인터셉터:**
```javascript
// 요청 전
apiClient.interceptors.request.use((config) => {
  console.log(`[API Request] ${config.method.toUpperCase()} ${config.url}`);
  return config;
});

// 응답 후
apiClient.interceptors.response.use(
  (response) => {
    console.log(`[API Response] ${response.config.url}:`, response.status);
    return response.data;  // ⭐ response.data 반환
  },
  (error) => {
    // 에러 처리
    throw error;
  }
);
```

**결과:** HTTP GET 요청이 백엔드로 전송됨

---

### 4단계: 백엔드 - FastAPI Router

**파일:** `app/api/v1/api.py`

```python
# API 라우터 등록
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
```

**파일:** `app/main.py`

```python
# 메인 앱에 라우터 포함
app.include_router(api_router, prefix=settings.API_V1_STR)  # /api/v1
```

**결과:** `/api/v1/dashboard/{symbol}` 경로가 등록됨

---

### 5단계: 백엔드 - Dashboard 엔드포인트

**파일:** `app/api/v1/endpoints/dashboard.py`

```python
@router.get("/{symbol}", response_model=dict)
async def get_stock_dashboard(
    symbol: str,  # 예: "AAPL"
    db: Session = Depends(get_db)
):
    """
    Get comprehensive dashboard data for a symbol
    """
    try:
        # ⭐ 1. Market Data 가져오기
        market_service = MarketDataService()
        market_data = market_service.get_market_data(symbol, period="1mo", interval="1d")
        
        # ⭐ 2. Predictions 가져오기
        prediction_service = PredictionService(db)
        predictions = db.query(Prediction)\
            .filter(Prediction.symbol == symbol)\
            .order_by(Prediction.created_at.desc())\
            .limit(5)\
            .all()
        
        # ⭐ 3. News 가져오기
        news_service = NewsService()
        news_list = news_service.get_latest_news(symbol, limit=10, days_back=7)
        
        # ⭐ 4. 응답 반환
        return {
            "symbol": symbol,
            "market_data": market_data,
            "predictions": predictions_data,
            "news": news_data,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
```

**결과:** `MarketDataService.get_market_data()` 호출

---

### 6단계: 백엔드 - Market Data Service

**파일:** `app/services/market_data_service.py`

```python
@staticmethod
def get_market_data(
    symbol: str,  # 예: "AAPL"
    period: str = "1mo",
    interval: str = "1d"
) -> Dict[str, Any]:
    """
    Fetch market data using yfinance
    """
    try:
        # ⭐ 1. yfinance Ticker 생성
        ticker = yf.Ticker(symbol)
        
        # ⭐ 2. 히스토리 데이터 가져오기 (여러 기간 시도)
        hist = ticker.history(period=period, interval=interval)
        
        # ⭐ 3. 정보 가져오기
        info = ticker.info
        
        # ⭐ 4. 현재 가격 계산
        current_price = info.get('currentPrice') or hist['Close'].iloc[-1]
        
        # ⭐ 5. 데이터 변환 및 반환
        return {
            "symbol": symbol,
            "current_price": float(current_price),
            "change": float(change),
            "change_percent": float(change_percent),
            "volume": int(hist['Volume'].iloc[-1]),
            "history": history,  # 차트 데이터
            "info": {...}
        }
    except Exception as e:
        raise ValueError(f"Error fetching market data: {str(e)}")
```

**결과:** yfinance에서 데이터를 가져와서 딕셔너리로 반환

---

### 7단계: 응답 반환 및 프론트엔드 표시

**백엔드 → 프론트엔드:**
```json
{
  "symbol": "AAPL",
  "market_data": {
    "current_price": 150.25,
    "change": 2.5,
    "change_percent": 1.69,
    "history": [...]
  },
  "predictions": [...],
  "news": [...]
}
```

**프론트엔드 - Dashboard.jsx:**
```javascript
// 응답 받음
const result = await getDashboard(symbol);
setData(result);  // ⭐ 상태 업데이트

// 렌더링
const { market_data, predictions, news } = data;
return (
  <div className="dashboard">
    <StockChart data={market_data.history} />
    {/* 예측, 뉴스 표시 */}
  </div>
);
```

---

## 디버깅 체크리스트

### 프론트엔드 확인
1. ✅ 브라우저 콘솔: `[Dashboard] Loading data for: AAPL`
2. ✅ 브라우저 콘솔: `[API Request] GET /dashboard/AAPL`
3. ✅ Network 탭: `/api/v1/dashboard/AAPL` 요청 확인
4. ❌ 타임아웃: 30초 내 응답 없음

### 백엔드 확인
1. ✅ 서버 로그: `INFO: ... GET /api/v1/dashboard/AAPL HTTP/1.1`
2. ✅ yfinance 호출 시작
3. ❌ yfinance 응답 대기 중 (타임아웃 가능)

### 문제 지점 확인
- **1단계 실패**: SearchBar에서 navigate가 작동 안 함
- **2단계 실패**: Dashboard 컴포넌트가 마운트 안 됨
- **3단계 실패**: API 요청이 전송 안 됨 (CORS, 네트워크)
- **4-5단계 실패**: 백엔드 라우터가 요청을 받지 못함
- **6단계 실패**: yfinance API 호출이 너무 느림/실패

## 빠른 테스트

### 1. 프론트엔드만 테스트
```javascript
// 브라우저 콘솔에서
fetch('http://localhost:8000/api/v1/dashboard/AAPL')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error);
```

### 2. 백엔드만 테스트
```bash
curl http://localhost:8000/api/v1/dashboard/AAPL
```

### 3. 각 단계별 로그 확인
- SearchBar: `console.log` 추가
- Dashboard: `[Dashboard]` 로그 확인
- API: `[API Request]` 로그 확인
- 백엔드: 서버 로그 확인

