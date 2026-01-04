"""
Market data service for fetching stock/crypto market data using yfinance
"""
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
from typing import Optional, Dict, Any

try:
    from app.core.config import settings
except ImportError:
    # app 모듈을 찾을 수 없을 때를 위한 fallback
    settings = None


class MarketDataService:
    """Service for handling market data operations"""
    
    @staticmethod
    def get_market_data(
        symbol: str = "AAPL",
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
        if settings and not settings.YFINANCE_ENABLED:
            raise ValueError("YFinance is not enabled in settings")
        
        try:
            print(f"[YFINANCE] ========== START get_market_data ==========")
            print(f"[YFINANCE] Symbol: {symbol}")
            print(f"[YFINANCE] Period: {period}, Interval: {interval}")
            print(f"[YFINANCE] Timestamp: {datetime.now().isoformat()}")
            
            # yf.download() 사용 (더 안정적)
            print(f"[YFINANCE] Using yf.download() for {symbol}...")
            
            # Rate limiting 방지를 위한 짧은 딜레이
            print(f"[YFINANCE] Sleeping 0.1s for rate limiting...")
            time.sleep(0.1)
            
            max_retries = 3
            hist = None
            info = {}
            
            # 먼저 yf.download()로 시도 (더 안정적)
            test_periods = [period, "5d", "1d"] if period not in ["5d", "1d"] else [period]
            
            # 요청 제한: 같은 심볼에 대해 짧은 시간 내 재시도 방지
            import hashlib
            cache_key = f"{symbol}_{period}_{interval}"
            cache_file = f"/tmp/yfinance_cache_{hashlib.md5(cache_key.encode()).hexdigest()}.txt"
            cache_duration = 30  # 30초 캐시
            
            try:
                import os
                if os.path.exists(cache_file):
                    import time as time_module
                    file_age = time_module.time() - os.path.getmtime(cache_file)
                    if file_age < cache_duration:
                        print(f"[YFINANCE] ⚡ Using cached data (age: {file_age:.1f}s)")
                        # 캐시된 데이터 로드 (간단한 구현)
                        pass
            except:
                pass
            
            for test_period in test_periods:
                print(f"[YFINANCE] Trying period: {test_period}")
                for attempt in range(max_retries):
                    try:
                        print(f"[YFINANCE] Attempt {attempt + 1}/{max_retries}: Calling yf.download('{symbol}', period='{test_period}', interval='{interval}')...")
                        
                        # yf.download() 사용 (더 안정적)
                        try:
                            hist = yf.download(
                                symbol, 
                                period=test_period, 
                                interval=interval,
                                progress=False,
                                show_errors=False
                            )
                            print(f"[YFINANCE] ✅ yf.download() completed successfully")
                            
                            # MultiIndex 컬럼 처리 (yf.download는 MultiIndex 반환)
                            if isinstance(hist.columns, pd.MultiIndex):
                                # 'Close', 'Open' 등이 튜플로 되어 있음
                                if ('Close', symbol) in hist.columns:
                                    # 단일 심볼인 경우
                                    hist = hist.xs(symbol, axis=1, level=1, drop_level=True)
                                else:
                                    # 첫 번째 레벨만 사용
                                    hist.columns = hist.columns.get_level_values(0)
                            
                            print(f"[YFINANCE] History received: {len(hist) if hist is not None and not hist.empty else 0} rows")
                            print(f"[YFINANCE] Columns: {list(hist.columns) if hist is not None and not hist.empty else 'None'}")
                            
                        except Exception as download_err:
                            print(f"[YFINANCE] ⚠️ yf.download() failed: {download_err}")
                            # Fallback: ticker.history() 시도
                            print(f"[YFINANCE] Falling back to ticker.history()...")
                            ticker = yf.Ticker(symbol)
                            hist = ticker.history(period=test_period, interval=interval)
                            print(f"[YFINANCE] ✅ ticker.history() fallback successful")
                        
                        if hist is not None and not hist.empty:
                            # 성공하면 원하는 기간으로 다시 가져오기
                            if test_period != period:
                                try:
                                    hist_full = yf.download(
                                        symbol,
                                        period=period,
                                        interval=interval,
                                        progress=False,
                                        show_errors=False
                                    )
                                    # MultiIndex 처리
                                    if isinstance(hist_full.columns, pd.MultiIndex):
                                        if ('Close', symbol) in hist_full.columns:
                                            hist_full = hist_full.xs(symbol, axis=1, level=1, drop_level=True)
                                        else:
                                            hist_full.columns = hist_full.columns.get_level_values(0)
                                    
                                    if not hist_full.empty:
                                        hist = hist_full
                                except:
                                    # 원하는 기간 실패 시 테스트 기간 데이터 사용
                                    pass
                            break
                        if attempt < max_retries - 1:
                            time.sleep(1)
                    except TimeoutError as e:
                        error_msg = str(e)
                        print(f"[YFINANCE] ⚠️ Timeout error: {error_msg}")
                        if attempt < max_retries - 1:
                            wait_time = (attempt + 1) * 2
                            print(f"[YFINANCE] Waiting {wait_time}s before retry...")
                            time.sleep(wait_time)
                            continue
                        if test_period == test_periods[-1]:  # 마지막 시도
                            raise ValueError(
                                f"Yahoo Finance API timeout. Please try again later. "
                                f"Symbol: {symbol}"
                            )
                    except Exception as e:
                        error_msg = str(e)
                        error_type = type(e).__name__
                        print(f"[YFINANCE] ⚠️ Exception ({error_type}): {error_msg}")
                        print(f"[YFINANCE] Exception details: {repr(e)}")
                        # "Expecting value" 에러는 rate limit이나 API 문제
                        if "429" in error_msg or "Too Many Requests" in error_msg or "Expecting value" in error_msg:
                            if attempt < max_retries - 1:
                                wait_time = (attempt + 1) * 2
                                print(f"[YFINANCE] Rate limit detected, waiting {wait_time}s...")
                                time.sleep(wait_time)
                                continue
                            if test_period == test_periods[-1]:  # 마지막 시도
                                raise ValueError(
                                    f"Yahoo Finance API rate limit exceeded or API error. "
                                    f"Please wait a moment and try again. "
                                    f"Symbol: {symbol}"
                                )
                        elif attempt < max_retries - 1:
                            print(f"[YFINANCE] Retrying in 1s...")
                            time.sleep(1)
                            continue
                        else:
                            print(f"[YFINANCE] ❌ All retries failed for period {test_period}")
                
                if hist is not None and not hist.empty:
                    break
                
                # 다음 기간으로 시도 전 대기
                if test_period != test_periods[-1]:
                    time.sleep(0.5)
            
            # 히스토리가 없으면 다양한 기간으로 재시도
            if hist is None or hist.empty:
                print(f"[YFINANCE] No history data, trying fallback periods...")
                fallback_periods = ["5d", "1d", "1y", "6mo", "3mo", "1mo"]  # 짧은 기간부터
                for fallback_period in fallback_periods:
                    print(f"[YFINANCE] Fallback: Trying period {fallback_period}...")
                    try:
                        # 타임아웃 설정
                        try:
                            signal.signal(signal.SIGALRM, timeout_handler)
                            signal.alarm(5)  # 5초 타임아웃
                        except:
                            pass
                        
                        try:
                            test_hist = ticker.history(period=fallback_period, interval=interval)
                        finally:
                            try:
                                signal.alarm(0)
                            except:
                                pass
                        
                        if test_hist is not None and not test_hist.empty:
                            print(f"[YFINANCE] ✅ Fallback success with period {fallback_period}: {len(test_hist)} rows")
                            hist = test_hist
                            break
                        else:
                            print(f"[YFINANCE] ⚠️ Fallback period {fallback_period} returned empty data")
                        time.sleep(0.5)
                    except TimeoutError as e:
                        print(f"[YFINANCE] ⚠️ Fallback timeout for period {fallback_period}: {str(e)}")
                        time.sleep(0.5)
                        continue
                    except Exception as e:
                        error_str = str(e)
                        print(f"[YFINANCE] ⚠️ Fallback error for period {fallback_period}: {error_str}")
                        # "Expecting value" 에러는 무시하고 다음 기간 시도
                        if "Expecting value" not in error_str:
                            time.sleep(0.5)
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
            print(f"[YFINANCE] Fetching ticker.info...")
            try:
                info = ticker.info
                print(f"[YFINANCE] ✅ Info received: {len(info) if info else 0} keys")
                if not info:
                    info = {}
            except Exception as e:
                print(f"[YFINANCE] ⚠️ Info fetch failed: {str(e)}")
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
            
            result = {
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
            print(f"[YFINANCE] ✅ Returning result with {len(history)} history points")
            print(f"[YFINANCE] ========== END get_market_data ==========")
            return result
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
