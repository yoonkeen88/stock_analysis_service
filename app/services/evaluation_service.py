"""
Evaluation service for comparing predictions with actual market prices
"""
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.db.models import Prediction, PredictionLog
from app.services.market_data_service import MarketDataService


class EvaluationService:
    """Service for evaluating prediction accuracy"""
    
    def __init__(self, db: Session):
        self.db = db
        self.market_data_service = MarketDataService()
    
    def create_prediction_log(
        self,
        prediction_id: int,
        symbol: str,
        model_name: str,
        predicted_price: float,
        prediction_date: datetime
    ) -> PredictionLog:
        """
        Create a prediction log entry from a prediction
        
        Args:
            prediction_id: ID of the Prediction record
            symbol: Stock or crypto symbol
            model_name: Name of the model used
            predicted_price: Predicted price
            prediction_date: Date for which prediction was made
        
        Returns:
            Created PredictionLog instance
        """
        prediction_log = PredictionLog(
            symbol=symbol,
            model_name=model_name,
            prediction_id=prediction_id,
            predicted_price=predicted_price,
            prediction_date=prediction_date,
            is_evaluated=False
        )
        self.db.add(prediction_log)
        self.db.commit()
        self.db.refresh(prediction_log)
        return prediction_log
    
    def evaluate_prediction(
        self,
        prediction_log_id: int,
        actual_price: Optional[float] = None
    ) -> PredictionLog:
        """
        Evaluate a prediction by comparing with actual price
        
        Args:
            prediction_log_id: ID of the PredictionLog to evaluate
            actual_price: Actual price (if None, will fetch from market data)
        
        Returns:
            Updated PredictionLog instance
        """
        prediction_log = self.db.query(PredictionLog).filter(
            PredictionLog.id == prediction_log_id
        ).first()
        
        if not prediction_log:
            raise ValueError(f"PredictionLog with id {prediction_log_id} not found")
        
        # Get actual price if not provided
        if actual_price is None:
            # Try to get price for the prediction date
            actual_price = self.market_data_service.get_historical_price(
                prediction_log.symbol,
                prediction_log.prediction_date
            )
            
            # If historical price not available, use current price as fallback
            if actual_price is None:
                actual_price = self.market_data_service.get_current_price(
                    prediction_log.symbol
                )
        
        # Calculate error rate
        if actual_price and actual_price > 0:
            error = abs(prediction_log.predicted_price - actual_price)
            error_rate = (error / actual_price) * 100
        else:
            error_rate = None
        
        # Update prediction log
        prediction_log.actual_price = actual_price
        prediction_log.error_rate = error_rate
        prediction_log.is_evaluated = True
        prediction_log.actual_date = datetime.now()
        prediction_log.updated_at = datetime.now()
        
        self.db.commit()
        self.db.refresh(prediction_log)
        
        return prediction_log
    
    def evaluate_pending_predictions(
        self,
        symbol: Optional[str] = None,
        limit: int = 100
    ) -> List[PredictionLog]:
        """
        Evaluate all pending predictions (where actual price is now available)
        
        Args:
            symbol: Filter by symbol (optional)
            limit: Maximum number of predictions to evaluate
        
        Returns:
            List of evaluated PredictionLog instances
        """
        query = self.db.query(PredictionLog).filter(
            PredictionLog.is_evaluated == False
        )
        
        if symbol:
            query = query.filter(PredictionLog.symbol == symbol)
        
        pending_logs = query.limit(limit).all()
        evaluated = []
        
        for log in pending_logs:
            try:
                # Check if prediction date has passed
                if log.prediction_date <= datetime.now():
                    evaluated_log = self.evaluate_prediction(log.id)
                    evaluated.append(evaluated_log)
            except Exception as e:
                print(f"Error evaluating prediction log {log.id}: {str(e)}")
        
        return evaluated
    
    def calculate_model_accuracy(
        self,
        model_name: str,
        symbol: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Calculate accuracy metrics for a model
        
        Args:
            model_name: Name of the model
            symbol: Filter by symbol (optional)
        
        Returns:
            Dictionary with accuracy metrics
        """
        query = self.db.query(PredictionLog).filter(
            PredictionLog.model_name == model_name,
            PredictionLog.is_evaluated == True
        )
        
        if symbol:
            query = query.filter(PredictionLog.symbol == symbol)
        
        evaluated_logs = query.all()
        
        if not evaluated_logs:
            return {
                "model_name": model_name,
                "symbol": symbol,
                "total_predictions": 0,
                "average_error_rate": None,
                "median_error_rate": None,
                "accuracy_score": None
            }
        
        error_rates = [log.error_rate for log in evaluated_logs if log.error_rate is not None]
        
        if not error_rates:
            return {
                "model_name": model_name,
                "symbol": symbol,
                "total_predictions": len(evaluated_logs),
                "average_error_rate": None,
                "median_error_rate": None,
                "accuracy_score": None
            }
        
        avg_error = sum(error_rates) / len(error_rates)
        sorted_errors = sorted(error_rates)
        median_error = sorted_errors[len(sorted_errors) // 2]
        
        # Accuracy score: 100 - average_error_rate (lower error = higher accuracy)
        accuracy_score = max(0, 100 - avg_error)
        
        return {
            "model_name": model_name,
            "symbol": symbol,
            "total_predictions": len(evaluated_logs),
            "average_error_rate": round(avg_error, 2),
            "median_error_rate": round(median_error, 2),
            "accuracy_score": round(accuracy_score, 2),
            "min_error_rate": round(min(error_rates), 2),
            "max_error_rate": round(max(error_rates), 2)
        }
    
    def get_evaluation_history(
        self,
        symbol: Optional[str] = None,
        model_name: Optional[str] = None,
        limit: int = 50
    ) -> List[PredictionLog]:
        """
        Get evaluation history
        
        Args:
            symbol: Filter by symbol (optional)
            model_name: Filter by model name (optional)
            limit: Maximum number of records to return
        
        Returns:
            List of PredictionLog instances
        """
        query = self.db.query(PredictionLog).filter(
            PredictionLog.is_evaluated == True
        )
        
        if symbol:
            query = query.filter(PredictionLog.symbol == symbol)
        if model_name:
            query = query.filter(PredictionLog.model_name == model_name)
        
        return query.order_by(PredictionLog.prediction_date.desc()).limit(limit).all()

