import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Home.css';

/**
 * 홈 페이지 - 종목 검색 및 대시보드로 이동
 */
const Home = () => {
  const [symbol, setSymbol] = useState('');
  const navigate = useNavigate();

  const handleSearch = (e) => {
    e.preventDefault();
    if (symbol.trim()) {
      navigate(`/dashboard/${symbol.trim().toUpperCase()}`);
    }
  };

  const popularSymbols = ['AAPL', 'TSLA', 'MSFT', 'GOOGL', 'BTC-USD', 'ETH-USD'];

  return (
    <div className="home fade-in">
      <div className="home-hero">
        <h1 className="hero-title">Stock Analysis Service</h1>
        <p className="hero-subtitle">
          최신 논문 기반 AI 모델로 주식과 비트코인을 예측하고 분석하세요
        </p>
        
        <form onSubmit={handleSearch} className="search-form">
          <div className="search-input-wrapper">
            <input
              type="text"
              placeholder="종목 심볼 입력 (예: AAPL, TSLA, BTC-USD)"
              value={symbol}
              onChange={(e) => setSymbol(e.target.value)}
              className="search-input"
            />
            <button type="submit" className="btn btn-primary search-button">
              검색
            </button>
          </div>
        </form>

        <div className="popular-symbols">
          <p className="popular-label">인기 종목:</p>
          <div className="symbol-tags">
            {popularSymbols.map((sym) => (
              <button
                key={sym}
                onClick={() => navigate(`/dashboard/${sym}`)}
                className="symbol-tag"
              >
                {sym}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="home-features">
        <div className="feature-card">
          <div className="feature-icon">📈</div>
          <h3>실시간 시세</h3>
          <p>최신 주식 및 암호화폐 시세를 실시간으로 확인하세요</p>
        </div>
        <div className="feature-card">
          <div className="feature-icon">🤖</div>
          <h3>AI 예측</h3>
          <p>논문 기반 머신러닝 모델로 미래 가격을 예측합니다</p>
        </div>
        <div className="feature-card">
          <div className="feature-icon">📰</div>
          <h3>뉴스 분석</h3>
          <p>관련 뉴스를 수집하고 감성 분석을 제공합니다</p>
        </div>
        <div className="feature-card">
          <div className="feature-icon">✅</div>
          <h3>예측 검증</h3>
          <p>예측 정확도를 추적하고 모델 성능을 평가합니다</p>
        </div>
      </div>
    </div>
  );
};

export default Home;

