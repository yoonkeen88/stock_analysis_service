/**
 * API 서비스 - 백엔드 API 호출 함수들
 */
import axios from 'axios';

// 전역 콘솔 확인
console.log('[API] Module loaded');

// API 기본 URL
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';
console.log('[API] API_BASE_URL:', API_BASE_URL);

// 요청 캐시 (같은 요청을 짧은 시간 내에 반복하지 않도록)
const requestCache = new Map();
const CACHE_DURATION = 5000; // 5초 캐시

// Axios 인스턴스 생성
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30초로 증가 (yfinance API가 느릴 수 있음)
});

// 요청 인터셉터
apiClient.interceptors.request.use(
  (config) => {
    console.log('[API] ========== REQUEST START ==========');
    console.log('[API] Method:', config.method.toUpperCase());
    console.log('[API] URL:', config.url);
    console.log('[API] Full URL:', config.baseURL + config.url);
    console.log('[API] Headers:', config.headers);
    console.log('[API] Params:', config.params);
    console.log('[API] Timestamp:', new Date().toISOString());
    console.log('[API] ===================================');
    return config;
  },
  (error) => {
    console.error('[API] ❌ REQUEST ERROR:', error);
    console.error('[API] Error details:', {
      message: error.message,
      stack: error.stack
    });
    return Promise.reject(error);
  }
);

// 응답 인터셉터
apiClient.interceptors.response.use(
  (response) => {
    console.log('[API] ========== RESPONSE RECEIVED ==========');
    console.log('[API] Status:', response.status);
    console.log('[API] URL:', response.config.url);
    console.log('[API] Headers:', response.headers);
    console.log('[API] Data keys:', Object.keys(response.data || {}));
    console.log('[API] Timestamp:', new Date().toISOString());
    console.log('[API] ======================================');
    return response.data;
  },
  (error) => {
    // 에러 처리
    console.error('[API Error]', {
      message: error.message,
      code: error.code,
      response: error.response?.data,
      status: error.response?.status,
      url: error.config?.url
    });
    
    if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
      throw new Error('요청 시간이 초과되었습니다. Yahoo Finance API가 느릴 수 있습니다. 잠시 후 다시 시도해주세요.');
    }
    
    if (error.response) {
      const errorData = error.response.data;
      const errorMessage = errorData.detail || errorData.message || 'API 요청에 실패했습니다.';
      
      // 사용자 친화적인 에러 메시지
      let userMessage = errorMessage;
      if (errorMessage.includes('No data found')) {
        userMessage = '종목 데이터를 찾을 수 없습니다. 심볼을 확인해주세요.\n예: 주식(AAPL, TSLA), 암호화폐(BTC-USD, ETH-USD)';
      } else if (errorMessage.includes('Invalid symbol')) {
        userMessage = '올바르지 않은 심볼입니다. 주식은 심볼만, 암호화폐는 -USD를 붙여주세요.';
      } else if (errorMessage.includes('rate limit')) {
        userMessage = 'Yahoo Finance API 요청 한도에 도달했습니다. 1-2분 후 다시 시도해주세요.';
      }
      
      throw new Error(userMessage);
    } else if (error.request) {
      console.error('Network Error - No response received:', error.request);
      throw new Error('서버에 연결할 수 없습니다. 백엔드 서버가 실행 중인지 확인하세요. (http://localhost:8000)');
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
  console.log('[API] getDashboard called with symbol:', symbol);
  
  // 캐시 키 생성
  const cacheKey = `dashboard-${symbol}`;
  const now = Date.now();
  
  // 캐시 확인
  if (requestCache.has(cacheKey)) {
    const cached = requestCache.get(cacheKey);
    const age = now - cached.timestamp;
    
    if (age < CACHE_DURATION) {
      console.log(`[API] ⚡ Using cached response (${age}ms old)`);
      return cached.data;
    } else {
      // 캐시 만료
      requestCache.delete(cacheKey);
      console.log(`[API] Cache expired (${age}ms old), making new request`);
    }
  }
  
  // 진행 중인 요청 확인
  if (requestCache.has(`${cacheKey}-pending`)) {
    console.log('[API] ⚠️ Request already in progress, waiting...');
    const pending = requestCache.get(`${cacheKey}-pending`);
    return await pending;
  }
  
  console.log('[API] API_BASE_URL:', API_BASE_URL);
  console.log('[API] Full endpoint will be:', `${API_BASE_URL}/dashboard/${symbol}`);
  
  // 진행 중인 요청으로 표시
  const requestPromise = apiClient.get(`/dashboard/${symbol}`)
    .then(result => {
      // 성공 시 캐시 저장
      requestCache.set(cacheKey, {
        data: result.data,
        timestamp: Date.now()
      });
      requestCache.delete(`${cacheKey}-pending`);
      console.log('[API] getDashboard SUCCESS, cached result');
      return result.data;
    })
    .catch(error => {
      requestCache.delete(`${cacheKey}-pending`);
      console.error('[API] getDashboard ERROR:', error);
      throw error;
    });
  
  requestCache.set(`${cacheKey}-pending`, requestPromise);
  
  return await requestPromise;
};

export default apiClient;

