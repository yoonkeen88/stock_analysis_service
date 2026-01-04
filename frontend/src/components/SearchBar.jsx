import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import './SearchBar.css';

// 전역 콘솔 확인
console.log('[SearchBar] Module loaded');

/**
 * 개선된 검색 바 컴포넌트
 * - 자동완성
 * - 검색 히스토리
 * - 인기 종목 추천
 */
const SearchBar = () => {
  console.log('[SearchBar] Component rendered');
  
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [searchHistory, setSearchHistory] = useState([]);
  const navigate = useNavigate();
  const inputRef = useRef(null);
  const suggestionsRef = useRef(null);
  
  // 컴포넌트 마운트 확인
  useEffect(() => {
    console.log('[SearchBar] Component mounted');
    return () => {
      console.log('[SearchBar] Component unmounted');
    };
  }, []);

  // 인기 종목 목록
  const popularSymbols = [
    'AAPL', 'TSLA', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA',
    'BTC-USD', 'ETH-USD', 'BNB-USD', 'SOL-USD'
  ];

  // 로컬 스토리지에서 검색 히스토리 불러오기
  useEffect(() => {
    const history = localStorage.getItem('searchHistory');
    if (history) {
      setSearchHistory(JSON.parse(history));
    }
  }, []);

  // 자동완성 제안 생성
  useEffect(() => {
    if (query.trim().length > 0) {
      const filtered = popularSymbols.filter(symbol =>
        symbol.toLowerCase().includes(query.toLowerCase())
      );
      setSuggestions(filtered.slice(0, 5));
    } else {
      setSuggestions([]);
    }
  }, [query]);

  // 외부 클릭 감지
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        suggestionsRef.current &&
        !suggestionsRef.current.contains(event.target) &&
        inputRef.current &&
        !inputRef.current.contains(event.target)
      ) {
        setShowSuggestions(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSearch = (symbol = null) => {
    console.log('[SearchBar] handleSearch called', { symbol, query });
    
    const searchSymbol = symbol || query.trim().toUpperCase();
    console.log('[SearchBar] searchSymbol:', searchSymbol);
    
    if (!searchSymbol) {
      console.warn('[SearchBar] No search symbol, returning');
      return;
    }

    // 검색 히스토리에 추가
    const newHistory = [
      searchSymbol,
      ...searchHistory.filter(item => item !== searchSymbol)
    ].slice(0, 10); // 최대 10개만 저장

    setSearchHistory(newHistory);
    localStorage.setItem('searchHistory', JSON.stringify(newHistory));

    // 대시보드로 이동
    const targetPath = `/dashboard/${searchSymbol}`;
    console.log('[SearchBar] Navigating to:', targetPath);
    navigate(targetPath);
    setQuery('');
    setShowSuggestions(false);
    console.log('[SearchBar] Navigation called, component should unmount');
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  const handleSuggestionClick = (symbol) => {
    handleSearch(symbol);
  };

  const clearHistory = () => {
    setSearchHistory([]);
    localStorage.removeItem('searchHistory');
  };

  return (
    <div className="search-bar-container">
      <div className="search-input-wrapper">
        <input
          ref={inputRef}
          type="text"
          placeholder="종목 심볼 검색 (예: AAPL, TSLA, BTC-USD)"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setShowSuggestions(true);
          }}
          onKeyPress={handleKeyPress}
          onFocus={() => setShowSuggestions(true)}
          className="search-input"
        />
        <button
          onClick={() => handleSearch()}
          className="btn btn-primary search-button"
        >
          검색
        </button>
      </div>

      {/* 자동완성 및 히스토리 드롭다운 */}
      {showSuggestions && (suggestions.length > 0 || searchHistory.length > 0 || query.length === 0) && (
        <div ref={suggestionsRef} className="suggestions-dropdown">
          {/* 자동완성 제안 */}
          {suggestions.length > 0 && (
            <div className="suggestions-section">
              <div className="suggestions-header">추천</div>
              {suggestions.map((symbol) => (
                <div
                  key={symbol}
                  className="suggestion-item"
                  onClick={() => handleSuggestionClick(symbol)}
                >
                  <span className="suggestion-icon">🔍</span>
                  <span className="suggestion-text">{symbol}</span>
                </div>
              ))}
            </div>
          )}

          {/* 검색 히스토리 */}
          {searchHistory.length > 0 && query.length === 0 && (
            <div className="suggestions-section">
              <div className="suggestions-header">
                <span>최근 검색</span>
                <button
                  className="clear-history-btn"
                  onClick={clearHistory}
                  title="검색 히스토리 삭제"
                >
                  삭제
                </button>
              </div>
              {searchHistory.map((symbol) => (
                <div
                  key={symbol}
                  className="suggestion-item history-item"
                  onClick={() => handleSuggestionClick(symbol)}
                >
                  <span className="suggestion-icon">🕐</span>
                  <span className="suggestion-text">{symbol}</span>
                </div>
              ))}
            </div>
          )}

          {/* 인기 종목 (검색어가 없을 때) */}
          {query.length === 0 && suggestions.length === 0 && (
            <div className="suggestions-section">
              <div className="suggestions-header">인기 종목</div>
              <div className="popular-symbols-grid">
                {popularSymbols.slice(0, 8).map((symbol) => (
                  <button
                    key={symbol}
                    className="popular-symbol-btn"
                    onClick={() => handleSuggestionClick(symbol)}
                  >
                    {symbol}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default SearchBar;

