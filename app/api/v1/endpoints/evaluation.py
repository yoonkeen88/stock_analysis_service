"""
Evaluation endpoints for prediction validation
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.evaluation import (
    PredictionLogResponse,
    EvaluationRequest,
    ModelAccuracyResponse
)
from app.services.evaluation_service import EvaluationService

router = APIRouter()


@router.post("/evaluate", response_model=PredictionLogResponse)
async def evaluate_prediction(
    request: EvaluationRequest,
    db: Session = Depends(get_db)
):
    """
    Evaluate a prediction by comparing with actual price
    
    - **prediction_log_id**: ID of the prediction log to evaluate
    - **actual_price**: Actual price (optional, will fetch if not provided)
    """
    try:
        service = EvaluationService(db)
        evaluated_log = service.evaluate_prediction(
            request.prediction_log_id,
            request.actual_price
        )
        return evaluated_log
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating prediction: {str(e)}")


@router.post("/evaluate-pending")
async def evaluate_pending_predictions(
    symbol: Optional[str] = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Evaluate all pending predictions
    
    - **symbol**: Filter by symbol (optional)
    - **limit**: Maximum number of predictions to evaluate
    """
    try:
        service = EvaluationService(db)
        evaluated = service.evaluate_pending_predictions(symbol=symbol, limit=limit)
        return {
            "evaluated_count": len(evaluated),
            "evaluated_logs": evaluated
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating predictions: {str(e)}")


@router.get("/accuracy/{model_name}", response_model=ModelAccuracyResponse)
async def get_model_accuracy(
    model_name: str,
    symbol: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get accuracy metrics for a model
    
    - **model_name**: Name of the model
    - **symbol**: Filter by symbol (optional)
    """
    try:
        service = EvaluationService(db)
        accuracy = service.calculate_model_accuracy(model_name, symbol)
        return accuracy
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating accuracy: {str(e)}")


@router.get("/history", response_model=List[PredictionLogResponse])
async def get_evaluation_history(
    symbol: Optional[str] = None,
    model_name: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Get evaluation history
    
    - **symbol**: Filter by symbol (optional)
    - **model_name**: Filter by model name (optional)
    - **limit**: Maximum number of records to return
    """
    try:
        service = EvaluationService(db)
        history = service.get_evaluation_history(symbol, model_name, limit)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching evaluation history: {str(e)}")

