"""
Market data service using yf.download() - more stable than ticker.history()
"""
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
from typing import Optional, Dict, Any

try:
    from app.core.config import settings
except ImportError:
    settings = None


class MarketDataService:
    """Service for handling market data operations using yf.download()"""
    
    @staticmethod
    def get_market_data(
        symbol: str = "AAPL",
        period: str = "1mo",
        interval: str = "1d"
    ) -> Dict[str, Any]:
        """
        Fetch market data using yf.download() - more stable than ticker.history()
        
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
            print(f"[YFINANCE] Using yf.download() (more stable)")
            
            # Rate limiting 방지
            time.sleep(0.1)
            
            max_retries = 3
            hist = None
            info = {}
            
            # yf.download()로 시도 (더 안정적)
            test_periods = [period, "5d", "1d"] if period not in ["5d", "1d"] else [period]
            
            for test_period in test_periods:
                print(f"[YFINANCE] Trying period: {test_period}")
                for attempt in range(max_retries):
                    try:
                        print(f"[YFINANCE] Attempt {attempt + 1}/{max_retries}: yf.download('{symbol}', period='{test_period}', interval='{interval}')...")
                        
                        # yf.download() 사용 (더 안정적)
                        hist = yf.download(
                            symbol,
                            period=test_period,
                            interval=interval,
                            progress=False,
                            show_errors=False,
                            threads=True
                        )
                        
                        print(f"[YFINANCE] ✅ yf.download() completed")
                        print(f"[YFINANCE] Raw data shape: {hist.shape if hist is not None else 'None'}")
                        print(f"[YFINANCE] Raw columns: {list(hist.columns) if hist is not None and not hist.empty else 'None'}")
                        
                        # MultiIndex 컬럼 처리
                        if hist is not None and not hist.empty:
                            if isinstance(hist.columns, pd.MultiIndex):
                                print(f"[YFINANCE] MultiIndex detected, processing...")
                                # 여러 심볼이 있을 수 있음
                                if len(hist.columns.levels[1]) == 1:
                                    # 단일 심볼인 경우
                                    symbol_name = hist.columns.levels[1][0]
                                    hist = hist.xs(symbol_name, axis=1, level=1, drop_level=True)
                                    print(f"[YFINANCE] Extracted single symbol: {symbol_name}")
                                else:
                                    # 여러 심볼인 경우 첫 번째 레벨만 사용
                                    hist.columns = hist.columns.get_level_values(0)
                                    print(f"[YFINANCE] Using first level columns")
                            
                            print(f"[YFINANCE] Processed columns: {list(hist.columns)}")
                            print(f"[YFINANCE] History rows: {len(hist)}")
                            
                            if not hist.empty:
                                # 성공하면 원하는 기간으로 다시 가져오기
                                if test_period != period:
                                    try:
                                        print(f"[YFINANCE] Fetching full period: {period}...")
                                        hist_full = yf.download(
                                            symbol,
                                            period=period,
                                            interval=interval,
                                            progress=False,
                                            show_errors=False,
                                            threads=True
                                        )
                                        
                                        # MultiIndex 처리
                                        if isinstance(hist_full.columns, pd.MultiIndex):
                                            if len(hist_full.columns.levels[1]) == 1:
                                                symbol_name = hist_full.columns.levels[1][0]
                                                hist_full = hist_full.xs(symbol_name, axis=1, level=1, drop_level=True)
                                            else:
                                                hist_full.columns = hist_full.columns.get_level_values(0)
                                        
                                        if not hist_full.empty:
                                            hist = hist_full
                                            print(f"[YFINANCE] ✅ Full period data received: {len(hist)} rows")
                                    except Exception as e:
                                        print(f"[YFINANCE] ⚠️ Full period fetch failed: {e}, using test period data")
                                
                                break
                        
                        if hist is None or hist.empty:
                            print(f"[YFINANCE] ⚠️ Empty data, retrying...")
                            if attempt < max_retries - 1:
                                time.sleep(1)
                            continue
                            
                    except Exception as e:
                        error_msg = str(e)
                        error_type = type(e).__name__
                        print(f"[YFINANCE] ⚠️ Exception ({error_type}): {error_msg}")
                        
                        if attempt < max_retries - 1:
                            wait_time = (attempt + 1) * 1
                            print(f"[YFINANCE] Retrying in {wait_time}s...")
                            time.sleep(wait_time)
                            continue
                        else:
                            print(f"[YFINANCE] ❌ All attempts failed for period {test_period}")
                
                if hist is not None and not hist.empty:
                    break
                
                if test_period != test_periods[-1]:
                    time.sleep(0.5)
            
            # 히스토리가 없으면 fallback
            if hist is None or hist.empty:
                print(f"[YFINANCE] No data, trying fallback periods...")
                fallback_periods = ["5d", "1d", "1y", "6mo", "3mo", "1mo"]
                for fallback_period in fallback_periods:
                    try:
                        print(f"[YFINANCE] Fallback: {fallback_period}...")
                        test_hist = yf.download(
                            symbol,
                            period=fallback_period,
                            interval=interval,
                            progress=False,
                            show_errors=False,
                            threads=True
                        )
                        
                        # MultiIndex 처리
                        if isinstance(test_hist.columns, pd.MultiIndex):
                            if len(test_hist.columns.levels[1]) == 1:
                                test_hist = test_hist.xs(test_hist.columns.levels[1][0], axis=1, level=1, drop_level=True)
                            else:
                                test_hist.columns = test_hist.columns.get_level_values(0)
                        
                        if not test_hist.empty:
                            print(f"[YFINANCE] ✅ Fallback success: {len(test_hist)} rows")
                            hist = test_hist
                            break
                    except Exception as e:
                        print(f"[YFINANCE] ⚠️ Fallback error: {e}")
                        continue
            
            if hist is None or hist.empty:
                raise ValueError(
                    f"No data found for symbol: {symbol}. "
                    f"Please check symbol format and try again."
                )
            
            # info 가져오기
            print(f"[YFINANCE] Fetching ticker.info...")
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                if not info:
                    info = {}
            except Exception as e:
                print(f"[YFINANCE] ⚠️ Info fetch failed: {e}")
                info = {}
            
            # 데이터 파싱
            print(f"[YFINANCE] Parsing data...")
            print(f"[YFINANCE] Available columns: {list(hist.columns)}")
            
            # 컬럼 이름 확인 및 정규화
            close_col = None
            open_col = None
            high_col = None
            low_col = None
            volume_col = None
            
            for col in hist.columns:
                col_lower = str(col).lower()
                if 'close' in col_lower and close_col is None:
                    close_col = col
                elif 'open' in col_lower and open_col is None:
                    open_col = col
                elif 'high' in col_lower and high_col is None:
                    high_col = col
                elif 'low' in col_lower and low_col is None:
                    low_col = col
                elif 'volume' in col_lower and volume_col is None:
                    volume_col = col
            
            # 기본값 설정
            if close_col is None:
                close_col = 'Close' if 'Close' in hist.columns else hist.columns[0]
            if open_col is None:
                open_col = 'Open' if 'Open' in hist.columns else close_col
            if high_col is None:
                high_col = 'High' if 'High' in hist.columns else close_col
            if low_col is None:
                low_col = 'Low' if 'Low' in hist.columns else close_col
            if volume_col is None:
                volume_col = 'Volume' if 'Volume' in hist.columns else None
            
            print(f"[YFINANCE] Using columns - Close: {close_col}, Open: {open_col}, High: {high_col}, Low: {low_col}, Volume: {volume_col}")
            
            # 현재 가격
            current_price = float(hist[close_col].iloc[-1])
            
            # 변화량 계산
            if len(hist) > 1:
                prev_close = float(hist[close_col].iloc[-2])
                change = current_price - prev_close
                change_percent = (change / prev_close) * 100
            else:
                change = 0
                change_percent = 0
            
            # 히스토리 데이터 변환
            history = []
            for idx, row in hist.iterrows():
                history.append({
                    "date": idx.isoformat() if hasattr(idx, 'isoformat') else str(idx),
                    "open": float(row[open_col]),
                    "high": float(row[high_col]),
                    "low": float(row[low_col]),
                    "close": float(row[close_col]),
                    "volume": int(row[volume_col]) if volume_col and pd.notna(row[volume_col]) else 0
                })
            
            result = {
                "symbol": symbol,
                "current_price": current_price,
                "change": change,
                "change_percent": change_percent,
                "volume": int(hist[volume_col].iloc[-1]) if volume_col and pd.notna(hist[volume_col].iloc[-1]) else 0,
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
            raise
        except Exception as e:
            error_msg = str(e)
            print(f"[YFINANCE] ❌ Error: {error_msg}")
            raise ValueError(f"Error fetching market data for {symbol}: {error_msg}")

