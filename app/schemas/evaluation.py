"""
Pydantic schemas for prediction evaluation
"""
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

# 공통 설정: model_name 필드 충돌 해결
COMMON_CONFIG = ConfigDict(protected_namespaces=(), from_attributes=True)


class PredictionLogBase(BaseModel):
    """Base schema for prediction log"""
    model_config = COMMON_CONFIG
    
    symbol: str = Field(..., description="Stock or cryptocurrency symbol")
    model_name: str = Field(..., description="Name of the ML model used")
    predicted_price: float = Field(..., description="Predicted price")
    actual_price: Optional[float] = Field(None, description="Actual market price")
    error_rate: Optional[float] = Field(None, description="Error rate percentage")
    prediction_date: datetime = Field(..., description="Date for which prediction was made")
    is_evaluated: bool = Field(default=False, description="Whether evaluation is complete")


class PredictionLogCreate(PredictionLogBase):
    """Schema for creating prediction log"""
    prediction_id: Optional[int] = Field(None, description="Reference to Prediction.id")


class PredictionLogResponse(PredictionLogBase):
    """Schema for prediction log response"""
    model_config = COMMON_CONFIG
    
    id: int
    prediction_id: Optional[int]
    actual_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime


class EvaluationRequest(BaseModel):
    """Schema for evaluation request"""
    model_config = COMMON_CONFIG
    
    prediction_log_id: int = Field(..., description="ID of prediction log to evaluate")
    actual_price: Optional[float] = Field(None, description="Actual price (optional, will fetch if not provided)")


class ModelAccuracyResponse(BaseModel):
    """Schema for model accuracy metrics"""
    model_config = COMMON_CONFIG
    
    model_name: str
    symbol: Optional[str]
    total_predictions: int
    average_error_rate: Optional[float]
    median_error_rate: Optional[float]
    accuracy_score: Optional[float]
    min_error_rate: Optional[float] = None
    max_error_rate: Optional[float] = None

