/**
 * API 서비스 - 백엔드 API 호출 함수들
 */
import axios from 'axios';

// API 기본 URL
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

// Axios 인스턴스 생성
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// 요청 인터셉터
apiClient.interceptors.request.use(
  (config) => {
    // 필요시 토큰 추가 등
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 응답 인터셉터
apiClient.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    // 에러 처리
    if (error.response) {
      console.error('API Error:', error.response.data);
      throw new Error(error.response.data.detail || 'API 요청에 실패했습니다.');
    } else if (error.request) {
      console.error('Network Error:', error.request);
      throw new Error('서버에 연결할 수 없습니다.');
    } else {
      throw error;
    }
  }
);

// ========== 주식 데이터 API ==========

/**
 * 실시간 주식 시세 조회
 * @param {string} symbol - 주식 심볼 (예: AAPL, TSLA)
 */
export const getStockQuote = async (symbol) => {
  return apiClient.get(`/stocks/quote/${symbol}`);
};

/**
 * 주식 과거 데이터 조회
 * @param {string} symbol - 주식 심볼
 * @param {string} period - 기간 (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
 * @param {string} interval - 간격 (1m, 2m, 5m, 15m, 30m, 60m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
 */
export const getStockHistory = async (symbol, period = '1mo', interval = '1d') => {
  return apiClient.get(`/stocks/history/${symbol}`, {
    params: { period, interval },
  });
};

/**
 * 암호화폐 데이터 조회
 * @param {string} symbol - 암호화폐 심볼 (예: BTC, ETH)
 */
export const getCryptoData = async (symbol, period = '1mo', interval = '1d') => {
  return apiClient.get(`/stocks/crypto/${symbol}`, {
    params: { period, interval },
  });
};

// ========== 예측 API ==========

/**
 * 새로운 예측 생성
 * @param {Object} predictionData - { symbol, model_name?, days_ahead }
 */
export const createPrediction = async (predictionData) => {
  return apiClient.post('/predictions/predict', predictionData);
};

/**
 * 종목별 예측 이력 조회
 * @param {string} symbol - 주식 심볼
 * @param {number} limit - 최대 개수
 */
export const getPredictions = async (symbol, limit = 10) => {
  return apiClient.get(`/predictions/predictions/${symbol}`, {
    params: { limit },
  });
};

// ========== 뉴스 API ==========

/**
 * 종목별 최신 뉴스 조회
 * @param {string} symbol - 주식 심볼
 * @param {number} limit - 최대 개수
 * @param {number} daysBack - 며칠 전까지 조회
 */
export const getNews = async (symbol, limit = 10, daysBack = 7) => {
  return apiClient.get(`/news/${symbol}`, {
    params: { limit, days_back: daysBack },
  });
};

/**
 * 뉴스 수집 및 저장
 * @param {Object} newsData - { symbol, limit, days_back }
 */
export const fetchNews = async (newsData) => {
  return apiClient.post('/news/fetch', newsData);
};

// ========== 검증 API ==========

/**
 * 예측 검증 실행
 * @param {number} predictionLogId - 예측 로그 ID
 * @param {number} actualPrice - 실제 가격 (선택)
 */
export const evaluatePrediction = async (predictionLogId, actualPrice = null) => {
  return apiClient.post('/evaluation/evaluate', {
    prediction_log_id: predictionLogId,
    actual_price: actualPrice,
  });
};

/**
 * 모델 정확도 조회
 * @param {string} modelName - 모델 이름
 * @param {string} symbol - 주식 심볼 (선택)
 */
export const getModelAccuracy = async (modelName, symbol = null) => {
  return apiClient.get(`/evaluation/accuracy/${modelName}`, {
    params: { symbol },
  });
};

// ========== 대시보드 API ==========

/**
 * 통합 대시보드 데이터 조회
 * @param {string} symbol - 주식 심볼
 */
export const getDashboard = async (symbol) => {
  return apiClient.get(`/dashboard/${symbol}`);
};

export default apiClient;

