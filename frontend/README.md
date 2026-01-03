# Frontend - Stock Analysis Service

React + Vite 기반 프론트엔드 애플리케이션

## 주요 기능

- 🎨 토스 UI 스타일의 모던한 디자인
- 📱 반응형 레이아웃
- 🚀 스플래시 화면
- 📊 실시간 주식 데이터 표시
- 🤖 AI 예측 결과 시각화
- 📰 뉴스 피드 및 감성 분석

## 설치 및 실행

```bash
# 의존성 설치
npm install

# 개발 서버 실행
npm run dev

# 프로덕션 빌드
npm run build
```

## 프로젝트 구조

```
src/
├── components/          # 재사용 가능한 컴포넌트
│   └── SplashScreen.jsx # 스플래시 화면
├── pages/               # 페이지 컴포넌트
│   ├── Home.jsx         # 홈 페이지
│   └── Dashboard.jsx    # 대시보드 페이지
├── services/            # API 서비스
│   └── api.js          # 백엔드 API 호출 함수
├── styles/             # 전역 스타일
│   └── global.css      # 토스 UI 스타일 기반 전역 CSS
├── App.jsx             # 메인 App 컴포넌트
└── main.jsx            # 진입점
```

## 환경 변수

`.env` 파일을 생성하고 다음을 설정하세요:

```
VITE_API_URL=http://localhost:8000/api/v1
```

## 스타일 가이드

프로젝트는 토스 UI 스타일을 기반으로 합니다:

- **컬러**: CSS 변수로 전역 관리 (`src/styles/global.css`)
- **스페이싱**: 일관된 간격 시스템
- **타이포그래피**: 시스템 폰트 사용
- **애니메이션**: 부드러운 전환 효과

## API 연결

모든 API 호출은 `src/services/api.js`에서 관리됩니다:

```javascript
import { getDashboard, getStockQuote } from './services/api';

// 대시보드 데이터 가져오기
const data = await getDashboard('AAPL');

// 주식 시세 조회
const quote = await getStockQuote('TSLA');
```

## 주요 컴포넌트

### SplashScreen
앱 시작 시 표시되는 스플래시 화면

### Home
종목 검색 및 주요 기능 소개

### Dashboard
종목별 통합 대시보드 (시세, 예측, 뉴스)

