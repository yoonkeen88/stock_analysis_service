# Stock Analysis Service

최신 논문 기반 주식/비트코인 예측 웹 서비스

## 프로젝트 구조

```
stock_analysis_service/
├── app/                    # FastAPI 백엔드
│   ├── __init__.py
│   ├── api/                # API 라우터
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── api.py      # API 라우터 통합
│   │       └── endpoints/  # 엔드포인트별 라우터
│   │           ├── __init__.py
│   │           ├── stocks.py      # 주식 시세 조회
│   │           ├── predictions.py # 예측 결과
│   │           ├── insights.py    # 논문 인사이트
│   │           ├── news.py        # 뉴스 데이터
│   │           ├── evaluation.py  # 예측 검증
│   │           └── dashboard.py   # 통합 대시보드
│   ├── core/               # 핵심 설정
│   │   ├── __init__.py
│   │   ├── config.py       # 설정 관리
│   │   ├── security.py     # 보안 (JWT 등)
│   │   └── database.py     # DB 연결
│   ├── services/           # 비즈니스 로직
│   │   ├── __init__.py
│   │   ├── stock_service.py        # 주식 데이터 서비스 (레거시)
│   │   ├── market_data_service.py   # 시장 데이터 서비스 (yfinance)
│   │   ├── prediction_service.py  # 예측 서비스
│   │   ├── evaluation_service.py   # 예측 검증 서비스
│   │   └── news_service.py         # 뉴스 수집 및 분석 서비스
│   ├── ml_models/          # ML 모델 (논문 기반)
│   │   ├── __init__.py
│   │   ├── predictor.py    # 예측 모델 메인
│   │   └── loader.py       # 모델 로더
│   ├── schemas/            # Pydantic 스키마
│   │   ├── __init__.py
│   │   ├── stock.py        # 주식 데이터 스키마
│   │   ├── prediction.py   # 예측 스키마
│   │   ├── news.py         # 뉴스 스키마
│   │   └── evaluation.py   # 검증 스키마
│   ├── db/                 # 데이터베이스 모델
│   │   ├── __init__.py
│   │   ├── base.py         # Base 모델
│   │   └── models.py       # SQLAlchemy 모델
│   │       ├── StockData
│   │       ├── Prediction
│   │       ├── PredictionLog  # 예측 검증 로그
│   │       ├── NewsLog         # 뉴스 데이터 로그
│   │       └── PaperInsight
│   └── main.py             # FastAPI 앱 진입점
├── frontend/               # React 프론트엔드
│   ├── public/
│   ├── src/
│   │   ├── components/     # React 컴포넌트
│   │   ├── pages/          # 페이지 컴포넌트
│   │   ├── services/       # API 서비스
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── requirements.txt        # Python 의존성
├── env.example            # 환경 변수 예시
└── README.md
```

## 설치 및 실행

### 백엔드 설정

#### 방법 1: venv 사용 (기본)

1. 가상환경 생성 및 활성화:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. 의존성 설치:
```bash
pip install -r requirements.txt
```

#### 방법 2: Anaconda 사용 (권장 - ML 프로젝트에 적합)

**옵션 A: environment.yml 사용 (가장 간단)**
```bash
# 환경 생성 및 의존성 설치를 한 번에
conda env create -f environment.yml

# 환경 활성화
conda activate stock_analysis
```

**옵션 B: 수동으로 환경 생성**
```bash
# Python 3.11 환경 생성
conda create -n stock_analysis python=3.11

# 환경 활성화
conda activate stock_analysis

# 의존성 설치
pip install -r requirements.txt
```

**Anaconda 사용 시 장점:**
- PyTorch, NumPy 등 ML 라이브러리 설치가 더 쉬움
- 패키지 의존성 관리가 용이
- 데이터 과학 프로젝트에 최적화
- `environment.yml`로 환경을 쉽게 재현 가능

**환경 비활성화:**
```bash
conda deactivate
```

**환경 삭제:**
```bash
conda env remove -n stock_analysis
```

3. 환경 변수 설정:
```bash
cp .env.example .env
# .env 파일을 편집하여 필요한 설정 수정
```

4. 데이터베이스 초기화:
```bash
# SQLite는 자동으로 생성됩니다
# PostgreSQL을 사용하는 경우 데이터베이스를 먼저 생성하세요
```

5. 서버 실행:
```bash
python -m app.main
# 또는
uvicorn app.main:app --reload
```

서버는 `http://localhost:8000`에서 실행됩니다.
API 문서는 `http://localhost:8000/docs`에서 확인할 수 있습니다.

### 프론트엔드 설정

1. 디렉토리 이동:
```bash
cd frontend
```

2. 의존성 설치:
```bash
npm install
# 또는
yarn install
```

3. 개발 서버 실행:
```bash
npm run dev
# 또는
yarn dev
```

프론트엔드는 `http://localhost:3000`에서 실행됩니다.

## 주요 기능

### 1. 주식/코인 시세 조회
- 실시간 주식 시세 조회
- 과거 데이터 조회 (기간, 간격 설정 가능)
- 암호화폐 데이터 조회
- 시세 차트 데이터 제공

### 2. AI 예측 결과 조회
- 논문 기반 ML 모델을 사용한 주가 예측
- 예측 이력 조회
- 신뢰도 점수 제공
- 예측 검증 기능 (실제값과 비교)

### 3. 예측 검증 (데이터 분석 학습)
- 예측값과 실제 시장 가격 비교
- 오차율(Error Rate) 계산
- 모델별 정확도(Accuracy) 산출
- 예측 검증 이력 조회

### 4. 뉴스 데이터 분석
- RSS 피드를 통한 최신 뉴스 수집
- 종목별 뉴스 필터링
- 감성 분석 (호재/악재 판단)
- 뉴스 제목, 링크, 게시일자 제공

### 5. 통합 대시보드
- 종목 조회 시 시세 차트, AI 예측, 최신 뉴스를 한 화면에 표시
- 실시간 데이터 통합 제공

### 6. 논문 기반 인사이트
- 연구 논문 기반 인사이트 저장 및 조회
- 읽음 상태 관리
- 심볼별 필터링

## API 엔드포인트

### 주식 데이터
- `GET /api/v1/stocks/quote/{symbol}` - 실시간 시세 조회
- `GET /api/v1/stocks/history/{symbol}` - 과거 데이터 조회
- `GET /api/v1/stocks/crypto/{symbol}` - 암호화폐 데이터 조회

### 예측
- `POST /api/v1/predictions/predict` - 새로운 예측 생성
- `GET /api/v1/predictions/predictions/{symbol}` - 예측 이력 조회

### 예측 검증
- `POST /api/v1/evaluation/evaluate` - 예측 검증 실행
- `POST /api/v1/evaluation/evaluate-pending` - 대기 중인 예측 일괄 검증
- `GET /api/v1/evaluation/accuracy/{model_name}` - 모델 정확도 조회
- `GET /api/v1/evaluation/history` - 검증 이력 조회

### 뉴스
- `GET /api/v1/news/{symbol}` - 종목별 최신 뉴스 조회
- `POST /api/v1/news/fetch` - 뉴스 수집 및 저장
- `GET /api/v1/news/history/{symbol}` - 뉴스 이력 조회

### 통합 대시보드
- `GET /api/v1/dashboard/{symbol}` - 종목별 통합 대시보드 (시세, 예측, 뉴스)

### 인사이트
- `POST /api/v1/insights/insights` - 인사이트 생성
- `GET /api/v1/insights/insights` - 인사이트 목록 조회
- `GET /api/v1/insights/insights/{id}` - 특정 인사이트 조회
- `PATCH /api/v1/insights/insights/{id}/read` - 읽음 표시

## ML 모델 구현 가이드

`app/ml_models/predictor.py` 파일에서 논문 기반 모델을 구현하세요:

1. `_predict_with_model()` 메서드에 모델 예측 로직 구현
2. `train_model()` 메서드에 모델 학습 로직 구현
3. `ModelLoader`를 사용하여 모델 저장/로드

예시:
```python
def _predict_with_model(self, model, df, days_ahead):
    # 논문에서 본 방법론을 여기에 구현
    # 예: LSTM, Transformer, Attention 기반 모델 등
    pass
```

## 데이터베이스 스키마

### 스키마 다이어그램

프로젝트의 데이터베이스 스키마는 `docs/SCHEMA.md`에서 확인할 수 있습니다.

#### 다이어그램 생성

자동으로 스키마 다이어그램을 생성하려면:

```bash
# Mermaid 형식 ERD 생성
python scripts/generate_schema_diagram.py

# PNG 이미지 생성 (선택사항)
# 방법 1: eralchemy 사용
pip install eralchemy
python scripts/generate_schema_image.py

# 방법 2: mermaid-cli 사용
npm install -g @mermaid-js/mermaid-cli
python scripts/generate_schema_image.py
```

생성된 다이어그램은:
- `docs/SCHEMA.md`: 수동 관리되는 스키마 문서
- `docs/SCHEMA_AUTO.md`: 자동 생성된 스키마 다이어그램
- `docs/schema.png`: 이미지 형식 (선택사항)

#### 스키마 관리

모델을 수정한 후에는 다음 명령어로 다이어그램을 업데이트하세요:

```bash
python scripts/generate_schema_diagram.py
```

## 개발 가이드

### 아키텍처 원칙
- **Layered Architecture**: API → Service → Model 계층 분리
- **Modular Design**: 기능별 모듈 분리로 확장성 확보
- **Separation of Concerns**: 백엔드와 프론트엔드 완전 분리

### 코드 스타일
- Python: PEP 8 준수
- Type hints 사용 권장
- Docstring 작성 권장

## 라이선스

MIT License

