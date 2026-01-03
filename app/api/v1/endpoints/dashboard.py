"""
Dashboard endpoint - combines market data, predictions, and news for a symbol
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db
from app.schemas.prediction import StockDashboardResponse
from app.services.market_data_service import MarketDataService
from app.services.prediction_service import PredictionService
from app.services.news_service import NewsService
from app.db.models import Prediction, NewsLog

router = APIRouter()


@router.get("/{symbol}", response_model=dict)
async def get_stock_dashboard(
    symbol: str,
    db: Session = Depends(get_db)
):
    """
    Get comprehensive dashboard data for a symbol
    
    Returns:
    - Market data (current price, history chart)
    - Latest predictions
    - Latest news articles
    
    - **symbol**: Stock or cryptocurrency symbol
    """
    try:
        # Get market data
        market_service = MarketDataService()
        market_data = market_service.get_market_data(symbol, period="1mo", interval="1d")
        
        # Get latest predictions
        prediction_service = PredictionService(db)
        predictions = db.query(Prediction)\
            .filter(Prediction.symbol == symbol)\
            .order_by(Prediction.created_at.desc())\
            .limit(5)\
            .all()
        
        predictions_data = [
            {
                "id": p.id,
                "model_name": p.model_name,
                "predicted_price": p.predicted_price,
                "confidence": p.confidence,
                "prediction_date": p.prediction_date.isoformat(),
                "created_at": p.created_at.isoformat()
            }
            for p in predictions
        ]
        
        # Get latest news
        news_service = NewsService()
        news_list = news_service.get_latest_news(symbol, limit=10, days_back=7)
        
        # Also get from database
        db_news = db.query(NewsLog)\
            .filter(NewsLog.symbol == symbol)\
            .order_by(NewsLog.published_date.desc())\
            .limit(10)\
            .all()
        
        # Combine and deduplicate news
        news_dict = {}
        for news in news_list:
            news_dict[news['link']] = {
                "title": news['title'],
                "link": news['link'],
                "summary": news.get('summary'),
                "published_date": news['published_date'].isoformat(),
                "sentiment_score": news.get('sentiment_score'),
                "sentiment_label": news.get('sentiment_label'),
                "source": news.get('source', 'rss')
            }
        
        for news in db_news:
            if news.link not in news_dict:
                news_dict[news.link] = {
                    "title": news.title,
                    "link": news.link,
                    "summary": news.summary,
                    "published_date": news.published_date.isoformat(),
                    "sentiment_score": news.sentiment_score,
                    "sentiment_label": news.sentiment_label,
                    "source": news.source
                }
        
        news_data = list(news_dict.values())
        news_data.sort(key=lambda x: x['published_date'], reverse=True)
        news_data = news_data[:10]
        
        return {
            "symbol": symbol,
            "market_data": market_data,
            "predictions": predictions_data,
            "news": news_data,
            "timestamp": datetime.now().isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching dashboard data: {str(e)}")

