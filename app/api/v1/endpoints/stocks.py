"""
Stock data endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.stock import StockHistoryRequest, StockQuoteResponse
from app.services.stock_service import StockService

router = APIRouter()


@router.get("/quote/{symbol}", response_model=StockQuoteResponse)
async def get_stock_quote(
    symbol: str,
    db: Session = Depends(get_db)
):
    """
    Get real-time stock quote
    
    - **symbol**: Stock symbol (e.g., AAPL, TSLA, BTC-USD)
    """
    try:
        service = StockService()
        data = service.get_stock_data(symbol, period="1d", interval="1m")
        
        return StockQuoteResponse(
            symbol=data["symbol"],
            current_price=data["current_price"],
            change=data["change"],
            change_percent=data["change_percent"],
            volume=data["volume"],
            timestamp=data["timestamp"]
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/history/{symbol}")
async def get_stock_history(
    symbol: str,
    period: str = "1mo",
    interval: str = "1d",
    db: Session = Depends(get_db)
):
    """
    Get historical stock data
    
    - **symbol**: Stock symbol
    - **period**: Period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
    - **interval**: Interval (1m, 2m, 5m, 15m, 30m, 60m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
    """
    try:
        service = StockService()
        data = service.get_stock_data(symbol, period=period, interval=interval)
        return data
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/crypto/{symbol}")
async def get_crypto_data(
    symbol: str,
    period: str = "1mo",
    interval: str = "1d",
    db: Session = Depends(get_db)
):
    """
    Get cryptocurrency data
    
    - **symbol**: Crypto symbol (e.g., BTC, ETH) - will be converted to BTC-USD format
    - **period**: Period to fetch
    - **interval**: Data interval
    """
    try:
        service = StockService()
        data = service.get_crypto_data(symbol, period=period, interval=interval)
        return data
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

