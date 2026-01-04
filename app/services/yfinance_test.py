"""
Market data service for fetching stock/crypto market data using yfinance
"""
import yfinance as yf
import time
from datetime import datetime
from typing import Optional, Dict, Any
# from app.core.config import settings


class MarketDataService:
    """Service for handling market data operations"""
    
    @staticmethod
    def get_market_data(
        symbol: str,
        period: str = "1mo",
        interval: str = "1d"
    ) -> Dict[str, Any]:
        """
        Fetch market data using yfinance
        
        Args:
            symbol: Stock or crypto symbol (e.g., 'AAPL', 'TSLA', 'BTC-USD')
            period: Period to fetch (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval: Data interval (1m, 2m, 5m, 15m, 30m, 60m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
        
        Returns:
            Dictionary containing market data
        """
        # if not settings.YFINANCE_ENABLED:
        #     raise ValueError("YFinance is not enabled in settings")
        
        try:
            ticker = yf.Ticker("AAPL")
            
            # Rate limiting 방지를 위한 짧은 딜레이
            time.sleep(0.1)
            
            max_retries = 3
            hist = None
            info = {}
            
            # 먼저 히스토리 데이터로 심볼 유효성 확인 (더 안정적)
            # 암호화폐의 경우 더 짧은 기간으로 시작
            test_periods = [period, "5d", "1d"] if period not in ["5d", "1d"] else [period]
            
            for test_period in test_periods:
                for attempt in range(max_retries):
                    try:
                        hist = ticker.history(period=test_period, interval=interval)
                        if hist is not None and not hist.empty:
                            # 성공하면 원하는 기간으로 다시 가져오기
                            if test_period != period:
                                try:
                                    hist = ticker.history(period=period, interval=interval)
                                    if hist.empty:
                                        # 원하는 기간 실패 시 테스트 기간 데이터 사용
                                        hist = ticker.history(period=test_period, interval=interval)
                                except:
                                    # 원하는 기간 실패 시 테스트 기간 데이터 사용
                                    hist = ticker.history(period=test_period, interval=interval)
                            break
                        if attempt < max_retries - 1:
                            time.sleep(1)
                    except Exception as e:
                        error_msg = str(e)
                        # "Expecting value" 에러는 rate limit이나 API 문제
                        if "429" in error_msg or "Too Many Requests" in error_msg or "Expecting value" in error_msg:
                            if attempt < max_retries - 1:
                                wait_time = (attempt + 1) * 2
                                time.sleep(wait_time)
                                continue
                            if test_period == test_periods[-1]:  # 마지막 시도
                                raise ValueError(
                                    f"Yahoo Finance API rate limit exceeded or API error. "
                                    f"Please wait a moment and try again. "
                                    f"Symbol: {symbol}"
                                )
                        elif attempt < max_retries - 1:
                            time.sleep(1)
                            continue
                
                if hist is not None and not hist.empty:
                    break
                
                # 다음 기간으로 시도 전 대기
                if test_period != test_periods[-1]:
                    time.sleep(0.5)
            
            # 히스토리가 없으면 다양한 기간으로 재시도
            if hist is None or hist.empty:
                fallback_periods = ["1y", "6mo", "3mo", "1mo", "5d", "1d"]
                for fallback_period in fallback_periods:
                    try:
                        test_hist = ticker.history(period=fallback_period, interval=interval)
                        if test_hist is not None and not test_hist.empty:
                            hist = test_hist
                            break
                        time.sleep(0.5)
                    except Exception as e:
                        # "Expecting value" 에러는 무시하고 다음 기간 시도
                        if "Expecting value" not in str(e):
                            continue
                        time.sleep(0.5)
                        continue
                
                if hist is None or hist.empty:
                    raise ValueError(
                        f"No data found for symbol: {symbol}. "
                        f"This may be due to:\n"
                        f"  1. Yahoo Finance API temporarily unavailable\n"
                        f"  2. Rate limit exceeded (wait 1-2 minutes)\n"
                        f"  3. Invalid symbol format (Stocks: AAPL, TSLA | Crypto: BTC-USD, ETH-USD)\n"
                        f"  4. Internet connection issue"
                    )
            
            # info 가져오기 (실패해도 계속 진행)
            try:
                info = ticker.info
                if not info:
                    info = {}
            except Exception as e:
                # info 실패해도 히스토리가 있으면 계속 진행
                info = {}
            
            # Get current quote
            current_price = info.get('currentPrice')
            if current_price is None:
                if hist is not None and not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                else:
                    raise ValueError(f"Could not get current price for {symbol}")
            
            # Calculate change
            if len(hist) > 1:
                prev_close = hist['Close'].iloc[-2]
                change = current_price - prev_close
                change_percent = (change / prev_close) * 100
            else:
                change = 0
                change_percent = 0
            
            # Convert history to list of dictionaries
            history = []
            for idx, row in hist.iterrows():
                history.append({
                    "date": idx.isoformat(),
                    "open": float(row['Open']),
                    "high": float(row['High']),
                    "low": float(row['Low']),
                    "close": float(row['Close']),
                    "volume": int(row['Volume'])
                })
            
            return {
                "symbol": symbol,
                "current_price": float(current_price),
                "change": float(change),
                "change_percent": float(change_percent),
                "volume": int(hist['Volume'].iloc[-1]),
                "timestamp": datetime.now().isoformat(),
                "history": history,
                "info": {
                    "name": info.get('longName', symbol),
                    "sector": info.get('sector'),
                    "industry": info.get('industry'),
                    "market_cap": info.get('marketCap'),
                }
            }
        except ValueError:
            # ValueError는 그대로 전달
            raise
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "Too Many Requests" in error_msg:
                raise ValueError(
                    f"Yahoo Finance API rate limit exceeded. "
                    f"Please wait a moment and try again. "
                    f"Symbol: {symbol}"
                )
            raise ValueError(f"Error fetching market data for {symbol}: {error_msg}")
    
    @staticmethod
    def get_current_price(symbol: str) -> float:
        """
        Get current price for a symbol
        
        Args:
            symbol: Stock or crypto symbol
        
        Returns:
            Current price
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            current_price = info.get('currentPrice')
            
            if current_price is None:
                # Fallback to latest close price
                hist = ticker.history(period="1d", interval="1d")
                if not hist.empty:
                    current_price = float(hist['Close'].iloc[-1])
                else:
                    raise ValueError(f"No price data available for {symbol}")
            
            return float(current_price)
        except Exception as e:
            raise ValueError(f"Error fetching current price for {symbol}: {str(e)}")
    
    @staticmethod
    def get_historical_price(symbol: str, date: datetime) -> Optional[float]:
        """
        Get historical price for a specific date
        
        Args:
            symbol: Stock or crypto symbol
            date: Target date
        
        Returns:
            Close price for the date, or None if not available
        """
        try:
            ticker = yf.Ticker(symbol)
            # Fetch data around the target date
            hist = ticker.history(start=date, end=date, interval="1d")
            
            if not hist.empty:
                return float(hist['Close'].iloc[0])
            return None
        except Exception as e:
            print(f"Error fetching historical price for {symbol} on {date}: {str(e)}")
            return None
    
    @staticmethod
    def validate_symbol(symbol: str) -> bool:
        """Validate if a symbol exists"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="5d", interval="1d")
            return not hist.empty
        except:
            return False


def test_yfinance():
    print(MarketDataService.get_market_data('AAPL'))

test_yfinance()