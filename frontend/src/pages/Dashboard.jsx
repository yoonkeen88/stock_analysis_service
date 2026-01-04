import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getDashboard } from '../services/api';
import StockChart from '../components/StockChart';
import './Dashboard.css';

/**
 * 대시보드 페이지 - 종목별 통합 정보 표시
 */
const Dashboard = () => {
  console.log('[Dashboard] Component rendered');
  
  const { symbol } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // 컴포넌트 마운트 확인
  useEffect(() => {
    console.log('[Dashboard] Component mounted with symbol:', symbol);
    return () => {
      console.log('[Dashboard] Component unmounted');
    };
  }, []);

  // 이전 symbol을 추적하여 중복 요청 방지
  const prevSymbolRef = useRef(null);
  
  useEffect(() => {
    // symbol이 실제로 변경되었을 때만 실행
    if (prevSymbolRef.current === symbol) {
      console.log('[Dashboard] Symbol unchanged, skipping API call');
      return;
    }
    
    console.log('[Dashboard] useEffect triggered', { 
      symbol, 
      prevSymbol: prevSymbolRef.current,
      timestamp: new Date().toISOString() 
    });
    
    prevSymbolRef.current = symbol;
    loadDashboardData();
  }, [symbol]);

  // 로딩 중 플래그로 중복 요청 방지
  const isLoadingRef = useRef(false);
  
  const loadDashboardData = async () => {
    // 이미 로딩 중이면 중복 요청 방지
    if (isLoadingRef.current) {
      console.log('[Dashboard] ⚠️ Already loading, skipping duplicate request');
      return;
    }
    
    console.log('[Dashboard] loadDashboardData START', { symbol, timestamp: new Date().toISOString() });
    
    isLoadingRef.current = true;
    
    try {
      setLoading(true);
      setError(null);
      
      if (!symbol) {
        console.error('[Dashboard] No symbol provided');
        throw new Error('종목 심볼이 없습니다.');
      }
      
      console.log(`[Dashboard] About to call getDashboard('${symbol}')`);
      const startTime = Date.now();
      
      // ⭐ API 호출 전 로그
      console.log('[Dashboard] Calling getDashboard API...');
      const result = await getDashboard(symbol);
      
      const loadTime = Date.now() - startTime;
      console.log(`[Dashboard] ✅ API call completed in ${loadTime}ms`);
      console.log('[Dashboard] Response data:', result);
      
      if (!result) {
        console.error('[Dashboard] Result is null or undefined');
        throw new Error('데이터를 받지 못했습니다.');
      }
      
      console.log('[Dashboard] Setting data state...');
      setData(result);
      console.log('[Dashboard] ✅ Data set successfully');
    } catch (err) {
      console.error('[Dashboard] ❌ ERROR in loadDashboardData:', {
        message: err.message,
        name: err.name,
        response: err.response?.data,
        status: err.response?.status,
        code: err.code,
        config: err.config,
        stack: err.stack
      });
      
      const errorMessage = err.response?.data?.detail || err.message || '알 수 없는 오류가 발생했습니다.';
      setError(errorMessage);
    } finally {
      console.log('[Dashboard] loadDashboardData FINALLY - setting loading to false');
      isLoadingRef.current = false;
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="spinner"></div>
        <p>데이터를 불러오는 중...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-error">
        <div className="error-content">
          <h2>⚠️ 데이터를 불러올 수 없습니다</h2>
          <p className="text-error">{error}</p>
          <div className="error-details">
            <p className="text-secondary">
              종목: <strong>{symbol}</strong>
            </p>
            <p className="text-secondary">
              가능한 원인:
            </p>
            <ul className="error-list">
              <li>백엔드 서버가 실행 중인지 확인하세요</li>
              <li>심볼 형식이 올바른지 확인하세요 (예: AAPL, BTC-USD)</li>
              <li>인터넷 연결을 확인하세요</li>
              <li>Yahoo Finance API rate limit에 걸렸을 수 있습니다 (잠시 후 재시도)</li>
            </ul>
          </div>
          <div className="error-actions">
            <button className="btn btn-primary" onClick={loadDashboardData}>
              다시 시도
            </button>
            <button className="btn btn-secondary" onClick={() => navigate('/')}>
              홈으로 돌아가기
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!data) {
    return <div className="dashboard-empty">데이터가 없습니다.</div>;
  }

  const { market_data, predictions, news } = data;

  return (
    <div className="dashboard fade-in">
      <div className="dashboard-header">
        <div className="header-top">
          <button className="btn btn-ghost" onClick={() => navigate('/')}>
            ← 홈으로
          </button>
        </div>
        <h1>{market_data.symbol}</h1>
        <div className="price-info">
          <span className="current-price">${market_data.current_price?.toFixed(2)}</span>
          <span className={`price-change ${market_data.change >= 0 ? 'positive' : 'negative'}`}>
            {market_data.change >= 0 ? '+' : ''}
            {market_data.change?.toFixed(2)} ({market_data.change_percent?.toFixed(2)}%)
          </span>
        </div>
      </div>

      <div className="dashboard-grid">
        {/* 시세 차트 영역 */}
        <div className="dashboard-card chart-card">
          <StockChart 
            data={market_data.history || []} 
            symbol={market_data.symbol}
          />
        </div>

        {/* 예측 결과 */}
        <div className="dashboard-card predictions-card">
          <h2>AI 예측 결과</h2>
          {predictions && predictions.length > 0 ? (
            <div className="predictions-list">
              {predictions.map((pred) => (
                <div key={pred.id} className="prediction-item">
                  <div className="prediction-header">
                    <span className="model-name">{pred.model_name}</span>
                    <span className="confidence">신뢰도: {(pred.confidence * 100).toFixed(1)}%</span>
                  </div>
                  <div className="prediction-price">
                    ${pred.predicted_price?.toFixed(2)}
                  </div>
                  <div className="prediction-date">
                    {new Date(pred.prediction_date).toLocaleDateString('ko-KR')}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-secondary">예측 데이터가 없습니다.</p>
          )}
        </div>

        {/* 최신 뉴스 */}
        <div className="dashboard-card news-card">
          <h2>최신 뉴스</h2>
          {news && news.length > 0 ? (
            <div className="news-list">
              {news.map((item, index) => (
                <a
                  key={index}
                  href={item.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="news-item"
                >
                  <div className="news-header">
                    <h3 className="news-title">{item.title}</h3>
                    <span className={`sentiment-badge ${item.sentiment_label}`}>
                      {item.sentiment_label === 'positive' ? '📈' : 
                       item.sentiment_label === 'negative' ? '📉' : '➡️'}
                    </span>
                  </div>
                  {item.summary && (
                    <p className="news-summary">{item.summary}</p>
                  )}
                  <div className="news-meta">
                    <span>{new Date(item.published_date).toLocaleDateString('ko-KR')}</span>
                    {item.source && <span className="news-source">{item.source}</span>}
                  </div>
                </a>
              ))}
            </div>
          ) : (
            <p className="text-secondary">뉴스 데이터가 없습니다.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

