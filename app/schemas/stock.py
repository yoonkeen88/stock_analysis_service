"""
Pydantic schemas for stock data
"""
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

# 공통 설정
COMMON_CONFIG = ConfigDict(protected_namespaces=(), from_attributes=True)


class StockDataBase(BaseModel):
    model_config = COMMON_CONFIG
    
    """Base schema for stock data"""
    symbol: str = Field(..., description="Stock symbol (e.g., AAPL, TSLA)")
    date: datetime
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    volume: Optional[int] = None


class StockDataCreate(StockDataBase):
    """Schema for creating stock data"""
    pass


class StockDataResponse(StockDataBase):
    """Schema for stock data response"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class StockQuoteResponse(BaseModel):
    model_config = COMMON_CONFIG
    
    """Schema for real-time stock quote"""
    symbol: str
    current_price: float
    change: float
    change_percent: float
    volume: int
    timestamp: datetime


class StockHistoryRequest(BaseModel):
    model_config = COMMON_CONFIG
    """Schema for stock history request"""
    symbol: str = Field(..., description="Stock symbol")
    period: str = Field(default="1mo", description="Period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max")
    interval: str = Field(default="1d", description="Interval: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo")

