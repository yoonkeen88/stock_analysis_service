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
    period: str = "1mo",
    interval: str = "1d",
    db: Session = Depends(get_db)
):
    """
    Get comprehensive dashboard data for a symbol
    
    Returns:
    - Market data (current price, history chart)
    - Latest predictions
    - Latest news articles
    
    - **symbol**: Stock or cryptocurrency symbol
    - **period**: Period to fetch (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max) - default: 1mo
    - **interval**: Data interval (1m, 2m, 5m, 15m, 30m, 60m, 1h, 1d, 5d, 1wk, 1mo, 3mo) - default: 1d
    """
    import logging
    logger = logging.getLogger(__name__)
    
    # 요청 제한: 같은 심볼에 대해 짧은 시간 내 재요청 방지
    import time as time_module
    request_tracker = getattr(get_stock_dashboard, '_request_tracker', {})
    now = time_module.time()
    
    if symbol in request_tracker:
        last_request_time = request_tracker[symbol]
        time_since_last = now - last_request_time
        if time_since_last < 2:  # 2초 내 재요청 방지
            print(f"[BACKEND] ⚠️ Rate limit: Request for {symbol} too soon ({time_since_last:.2f}s ago), returning cached or blocking")
            # 여기서는 단순히 로그만 남기고 진행 (실제로는 캐시된 데이터 반환 가능)
    
    request_tracker[symbol] = now
    get_stock_dashboard._request_tracker = request_tracker
    
    print(f"[BACKEND] ========== DASHBOARD REQUEST START ==========")
    print(f"[BACKEND] Symbol: {symbol}")
    print(f"[BACKEND] Timestamp: {datetime.now().isoformat()}")
    print(f"[BACKEND] =============================================")
    
    try:
        # Get market data (with error handling for rate limits)
        print(f"[BACKEND] Creating MarketDataService...")
        market_service = MarketDataService()
        print(f"[BACKEND] Calling get_market_data('{symbol}', period='{period}', interval='{interval}')...")
        try:
            market_data = market_service.get_market_data(symbol, period=period, interval=interval)
            print(f"[BACKEND] ✅ Market data received: {len(market_data.get('history', []))} history points")
        except ValueError as e:
            error_msg = str(e)
            if "rate limit" in error_msg.lower() or "429" in error_msg:
                raise HTTPException(
                    status_code=429,
                    detail=f"Yahoo Finance API rate limit exceeded. Please wait a moment and try again. ({symbol})"
                )
            raise HTTPException(status_code=404, detail=error_msg)
        
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
        
        result = {
            "symbol": symbol,
            "market_data": market_data,
            "predictions": predictions_data,
            "news": news_data,
            "timestamp": datetime.now().isoformat()
        }
        print(f"[BACKEND] ✅ Preparing response...")
        print(f"[BACKEND] Response keys: {list(result.keys())}")
        print(f"[BACKEND] ========== DASHBOARD REQUEST END ==========")
        return result
    except HTTPException:
        # 이미 HTTPException이면 그대로 전달
        raise
    except ValueError as e:
        error_msg = str(e) if str(e) else "Invalid request"
        raise HTTPException(status_code=404, detail=error_msg)
    except Exception as e:
        import traceback
        error_msg = str(e) if str(e) else "Unknown error occurred"
        error_type = type(e).__name__
        print(f"Dashboard error for {symbol}: {error_type}: {error_msg}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500, 
            detail=f"Error fetching dashboard data: {error_msg} (Type: {error_type})"
        )

