"""
Pydantic schemas for news data
"""
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

# 공통 설정
COMMON_CONFIG = ConfigDict(protected_namespaces=(), from_attributes=True)


class NewsBase(BaseModel):
    model_config = COMMON_CONFIG
    """Base schema for news"""
    symbol: str = Field(..., description="Stock or cryptocurrency symbol")
    title: str = Field(..., description="News title")
    link: str = Field(..., description="News article URL")
    summary: Optional[str] = Field(None, description="News summary")
    published_date: datetime = Field(..., description="Publication date")
    sentiment_score: Optional[float] = Field(None, ge=-1, le=1, description="Sentiment score (-1 to 1)")
    sentiment_label: Optional[str] = Field(None, description="Sentiment label (positive/negative/neutral)")
    source: Optional[str] = Field(None, description="News source")


class NewsCreate(NewsBase):
    """Schema for creating news log"""
    pass


class NewsResponse(NewsBase):
    """Schema for news response"""
    id: int
    collected_at: datetime
    
    class Config:
        from_attributes = True


class NewsFetchRequest(BaseModel):
    model_config = COMMON_CONFIG
    
    """Schema for news fetch request"""
    symbol: str = Field(..., description="Stock or cryptocurrency symbol")
    limit: int = Field(default=10, ge=1, le=50, description="Maximum number of news articles")
    days_back: int = Field(default=7, ge=1, le=30, description="Number of days to look back")

