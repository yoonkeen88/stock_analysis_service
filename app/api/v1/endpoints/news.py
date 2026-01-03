"""
News endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.news import NewsResponse, NewsFetchRequest
from app.services.news_service import NewsService
from app.db.models import NewsLog

router = APIRouter()


@router.get("/{symbol}", response_model=List[NewsResponse])
async def get_news(
    symbol: str,
    limit: int = 10,
    days_back: int = 7,
    db: Session = Depends(get_db)
):
    """
    Get latest news articles for a symbol
    
    - **symbol**: Stock or cryptocurrency symbol
    - **limit**: Maximum number of articles to return (1-50)
    - **days_back**: Number of days to look back (1-30)
    """
    try:
        service = NewsService()
        news_list = service.get_latest_news(symbol, limit=limit, days_back=days_back)
        
        # Save to database
        saved_news = []
        for news in news_list:
            # Check if news already exists (by link)
            existing = db.query(NewsLog).filter(NewsLog.link == news['link']).first()
            
            if not existing:
                db_news = NewsLog(**news)
                db.add(db_news)
                saved_news.append(db_news)
            else:
                saved_news.append(existing)
        
        db.commit()
        
        # Refresh all items
        for news in saved_news:
            db.refresh(news)
        
        return saved_news
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")


@router.post("/fetch", response_model=List[NewsResponse])
async def fetch_news(
    request: NewsFetchRequest,
    db: Session = Depends(get_db)
):
    """
    Fetch and save news articles for a symbol
    
    - **symbol**: Stock or cryptocurrency symbol
    - **limit**: Maximum number of articles
    - **days_back**: Number of days to look back
    """
    try:
        service = NewsService()
        news_list = service.get_latest_news(
            request.symbol,
            limit=request.limit,
            days_back=request.days_back
        )
        
        # Save to database
        saved_news = []
        for news in news_list:
            # Check if news already exists (by link)
            existing = db.query(NewsLog).filter(NewsLog.link == news['link']).first()
            
            if not existing:
                db_news = NewsLog(**news)
                db.add(db_news)
                saved_news.append(db_news)
            else:
                # Update existing record
                existing.sentiment_score = news.get('sentiment_score')
                existing.sentiment_label = news.get('sentiment_label')
                saved_news.append(existing)
        
        db.commit()
        
        # Refresh all items
        for news in saved_news:
            db.refresh(news)
        
        return saved_news
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")


@router.get("/history/{symbol}", response_model=List[NewsResponse])
async def get_news_history(
    symbol: str,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Get news history from database for a symbol
    
    - **symbol**: Stock or cryptocurrency symbol
    - **limit**: Maximum number of articles to return
    """
    try:
        news_list = db.query(NewsLog)\
            .filter(NewsLog.symbol == symbol)\
            .order_by(NewsLog.published_date.desc())\
            .limit(limit)\
            .all()
        return news_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news history: {str(e)}")

