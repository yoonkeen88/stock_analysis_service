# 개발 가이드 - 기능 추가 방법

## 프로젝트 구조 이해하기

### 프론트엔드 구조
```
frontend/src/
├── components/          # 재사용 가능한 컴포넌트
├── pages/               # 페이지 컴포넌트
├── services/            # API 호출 함수
│   └── api.js          # 백엔드 API 연결
└── styles/             # 전역 스타일
```

### 백엔드 구조
```
app/
├── api/v1/endpoints/    # API 엔드포인트
├── services/           # 비즈니스 로직
├── schemas/            # 데이터 검증
└── db/models.py        # 데이터베이스 모델
```

## 기능 추가 워크플로우

### 1. 새 기능 추가 시 체크리스트

1. **백엔드 API 확인/생성**
   - `app/api/v1/endpoints/`에 엔드포인트 추가
   - `app/services/`에 비즈니스 로직 추가
   - `app/schemas/`에 데이터 검증 스키마 추가

2. **프론트엔드 API 서비스 추가**
   - `frontend/src/services/api.js`에 함수 추가

3. **컴포넌트 생성**
   - `frontend/src/components/` 또는 `pages/`에 컴포넌트 생성

4. **스타일 추가**
   - 컴포넌트별 CSS 파일 생성
   - 전역 스타일은 `styles/global.css` 활용

5. **라우팅 추가**
   - `App.jsx`에 Route 추가

## 예시: 검색 기능 + 그래프 추가

### Step 1: 검색 기능 개선

**위치**: `frontend/src/pages/Home.jsx`

개선 사항:
- 자동완성 기능
- 검색 히스토리
- 인기 종목 추천

### Step 2: 그래프 컴포넌트 생성

**위치**: `frontend/src/components/StockChart.jsx`

사용 라이브러리: Recharts (이미 설치됨)

기능:
- 시세 차트 표시
- 호버 시 툴팁 (날짜, 시가, 종가, 고가, 저가)
- 반응형 디자인

### Step 3: Dashboard에 그래프 통합

**위치**: `frontend/src/pages/Dashboard.jsx`

차트 컴포넌트를 import하고 데이터 전달

## 코드 작성 패턴

### API 호출 패턴
```javascript
// services/api.js에 함수 추가
export const getStockHistory = async (symbol, period, interval) => {
  return apiClient.get(`/stocks/history/${symbol}`, {
    params: { period, interval },
  });
};

// 컴포넌트에서 사용
import { getStockHistory } from '../services/api';

const [chartData, setChartData] = useState([]);

useEffect(() => {
  const loadData = async () => {
    try {
      const data = await getStockHistory('AAPL', '1mo', '1d');
      setChartData(data.history);
    } catch (error) {
      console.error('Error loading chart data:', error);
    }
  };
  loadData();
}, [symbol]);
```

### 컴포넌트 생성 패턴
```javascript
// 1. 컴포넌트 파일 생성
// components/StockChart.jsx

import { useState } from 'react';
import './StockChart.css';

const StockChart = ({ data }) => {
  // 상태 관리
  // 이벤트 핸들러
  // 렌더링
  return <div>...</div>;
};

export default StockChart;
```

### 스타일 작성 패턴
```css
/* 컴포넌트명.css */
.component-name {
  /* 전역 CSS 변수 활용 */
  background: var(--bg-primary);
  color: var(--text-primary);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  padding: var(--spacing-md);
}

/* 다크 모드 자동 지원 (CSS 변수 사용 시) */
```

## 디버깅 팁

1. **브라우저 개발자 도구**
   - Network 탭: API 요청 확인
   - Console: 에러 확인
   - React DevTools: 컴포넌트 상태 확인

2. **백엔드 로그**
   - FastAPI는 자동으로 요청 로그 출력
   - `print()` 또는 `logger` 사용

3. **API 테스트**
   - `http://localhost:8000/docs`에서 Swagger UI 사용
   - 직접 API 호출 테스트 가능

## 다음 단계

1. 검색 기능 개선
2. 그래프 컴포넌트 생성
3. 호버 툴팁 구현
4. 반응형 디자인 적용

각 단계별로 예시 코드를 제공하겠습니다!

