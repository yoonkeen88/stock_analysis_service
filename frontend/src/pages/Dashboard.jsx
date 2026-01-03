import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getDashboard } from '../services/api';
import './Dashboard.css';

/**
 * 대시보드 페이지 - 종목별 통합 정보 표시
 */
const Dashboard = () => {
  const { symbol } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadDashboardData();
  }, [symbol]);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);
      const result = await getDashboard(symbol);
      setData(result);
    } catch (err) {
      setError(err.message);
      console.error('Dashboard load error:', err);
    } finally {
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
        <p className="text-error">⚠️ {error}</p>
        <button className="btn btn-primary" onClick={loadDashboardData}>
          다시 시도
        </button>
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
          <h2>시세 차트</h2>
          <div className="chart-placeholder">
            <p>차트 라이브러리 연동 필요 (예: Recharts)</p>
            <p className="text-secondary">데이터: {market_data.history?.length || 0}개 포인트</p>
          </div>
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

