"""
Prediction endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.prediction_service import PredictionService

router = APIRouter()


@router.post("/predict", response_model=dict)
async def create_prediction(
    request: PredictionRequest,
    db: Session = Depends(get_db)
):
    """
    Generate a new prediction using AI models
    
    - **symbol**: Stock or cryptocurrency symbol
    - **model_name**: Optional specific model to use
    - **days_ahead**: Number of days to predict ahead (1-30)
    """
    try:
        service = PredictionService(db)
        result = service.generate_prediction(request)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/predictions/{symbol}", response_model=List[PredictionResponse])
async def get_predictions(
    symbol: str,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get prediction history for a symbol
    
    - **symbol**: Stock or cryptocurrency symbol
    - **limit**: Maximum number of predictions to return
    """
    try:
        service = PredictionService(db)
        predictions = service.get_predictions_by_symbol(symbol, limit=limit)
        return predictions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

