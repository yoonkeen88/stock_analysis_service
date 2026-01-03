"""
Prediction service for managing AI predictions
"""
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.db.models import Prediction, PredictionLog
from app.schemas.prediction import PredictionCreate, PredictionRequest
from app.ml_models.predictor import StockPredictor


class PredictionService:
    """Service for handling prediction operations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.predictor = StockPredictor()
    
    def create_prediction(
        self,
        prediction_data: PredictionCreate
    ) -> Prediction:
        """Create a new prediction record"""
        db_prediction = Prediction(**prediction_data.model_dump())
        self.db.add(db_prediction)
        self.db.commit()
        self.db.refresh(db_prediction)
        return db_prediction
    
    def get_predictions_by_symbol(
        self,
        symbol: str,
        limit: int = 10
    ) -> List[Prediction]:
        """Get predictions for a specific symbol"""
        return self.db.query(Prediction)\
            .filter(Prediction.symbol == symbol)\
            .order_by(Prediction.created_at.desc())\
            .limit(limit)\
            .all()
    
    def generate_prediction(
        self,
        request: PredictionRequest
    ) -> Dict[str, Any]:
        """
        Generate a new prediction using ML models
        
        Args:
            request: Prediction request with symbol and parameters
        
        Returns:
            Dictionary containing prediction results
        """
        try:
            # Use the predictor to generate prediction
            result = self.predictor.predict(
                symbol=request.symbol,
                days_ahead=request.days_ahead,
                model_name=request.model_name
            )
            
            # Save to database
            prediction_data = PredictionCreate(
                symbol=request.symbol,
                model_name=result.get('model_name', 'default'),
                predicted_price=result['predicted_price'],
                confidence=result.get('confidence'),
                prediction_date=datetime.now() + timedelta(days=request.days_ahead)
            )
            
            db_prediction = self.create_prediction(prediction_data)
            
            # Create prediction log for evaluation
            prediction_log = PredictionLog(
                symbol=request.symbol,
                model_name=result.get('model_name', 'default'),
                prediction_id=db_prediction.id,
                predicted_price=result['predicted_price'],
                prediction_date=datetime.now() + timedelta(days=request.days_ahead),
                is_evaluated=False
            )
            self.db.add(prediction_log)
            self.db.commit()
            self.db.refresh(prediction_log)
            
            return {
                "id": db_prediction.id,
                "symbol": db_prediction.symbol,
                "predicted_price": db_prediction.predicted_price,
                "confidence": db_prediction.confidence,
                "prediction_date": db_prediction.prediction_date.isoformat(),
                "model_name": db_prediction.model_name,
                "created_at": db_prediction.created_at.isoformat(),
                "prediction_log_id": prediction_log.id
            }
        except Exception as e:
            raise ValueError(f"Error generating prediction: {str(e)}")

