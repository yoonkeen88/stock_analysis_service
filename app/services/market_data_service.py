"""
Market data service for fetching stock/crypto market data using yfinance
"""
import yfinance as yf
from datetime import datetime
from typing import Optional, Dict, Any
from app.core.config import settings


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
        if not settings.YFINANCE_ENABLED:
            raise ValueError("YFinance is not enabled in settings")
        
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period, interval=interval)
            
            if hist.empty:
                raise ValueError(f"No data found for symbol: {symbol}")
            
            # Get current quote
            info = ticker.info
            current_price = info.get('currentPrice') or hist['Close'].iloc[-1]
            
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
        except Exception as e:
            raise ValueError(f"Error fetching market data for {symbol}: {str(e)}")
    
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
            info = ticker.info
            return info.get('symbol') is not None
        except:
            return False

