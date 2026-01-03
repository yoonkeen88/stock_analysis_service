"""
Pydantic schemas for predictions
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class PredictionBase(BaseModel):
    """Base schema for prediction"""
    symbol: str = Field(..., description="Stock or cryptocurrency symbol")
    model_name: str = Field(..., description="Name of the ML model used")
    predicted_price: float = Field(..., description="Predicted price")
    confidence: Optional[float] = Field(None, ge=0, le=1, description="Confidence score (0-1)")
    prediction_date: datetime = Field(..., description="Date for which prediction is made")


class PredictionCreate(PredictionBase):
    """Schema for creating a prediction"""
    pass


class PredictionResponse(PredictionBase):
    """Schema for prediction response"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class PredictionRequest(BaseModel):
    """Schema for prediction request"""
    symbol: str = Field(..., description="Stock or cryptocurrency symbol")
    model_name: Optional[str] = Field(None, description="Specific model to use (optional)")
    days_ahead: int = Field(default=1, ge=1, le=30, description="Number of days to predict ahead")


class PaperInsightBase(BaseModel):
    """Base schema for paper insight"""
    paper_title: str
    paper_doi: Optional[str] = None
    symbol: Optional[str] = None
    insight_summary: str
    methodology: Optional[str] = None
    key_findings: Optional[str] = None


class PaperInsightCreate(PaperInsightBase):
    """Schema for creating paper insight"""
    pass


class PaperInsightResponse(PaperInsightBase):
    """Schema for paper insight response"""
    id: int
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class StockDashboardResponse(BaseModel):
    """Schema for stock dashboard - combines market data, predictions, and news"""
    symbol: str
    market_data: dict
    predictions: list
    news: list
    timestamp: datetime

