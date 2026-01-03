"""
Database models using SQLAlchemy
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.sql import func
from app.db.base import Base


class StockData(Base):
    """Stock market data model"""
    __tablename__ = "stock_data"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True, nullable=False)
    date = Column(DateTime, nullable=False)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())


class Prediction(Base):
    """AI prediction results model"""
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True, nullable=False)
    model_name = Column(String, nullable=False)
    predicted_price = Column(Float, nullable=False)
    confidence = Column(Float)
    prediction_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class PaperInsight(Base):
    """Research paper insights model"""
    __tablename__ = "paper_insights"
    
    id = Column(Integer, primary_key=True, index=True)
    paper_title = Column(String, nullable=False)
    paper_doi = Column(String)
    symbol = Column(String, index=True)
    insight_summary = Column(Text, nullable=False)
    methodology = Column(Text)
    key_findings = Column(Text)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())


class PredictionLog(Base):
    """Prediction validation log - stores predictions and actual values for evaluation"""
    __tablename__ = "prediction_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True, nullable=False)
    model_name = Column(String, nullable=False)
    prediction_id = Column(Integer, nullable=True)  # Reference to Prediction.id
    predicted_price = Column(Float, nullable=False)
    actual_price = Column(Float, nullable=True)  # Filled when actual price is available
    error_rate = Column(Float, nullable=True)  # Calculated: |predicted - actual| / actual
    prediction_date = Column(DateTime, nullable=False)  # Date for which prediction was made
    actual_date = Column(DateTime, nullable=True)  # Date when actual price was recorded
    is_evaluated = Column(Boolean, default=False)  # Whether actual price has been compared
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class NewsLog(Base):
    """News data log - stores collected news articles with sentiment analysis"""
    __tablename__ = "news_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True, nullable=False)
    title = Column(String, nullable=False)
    link = Column(String, nullable=False)
    summary = Column(Text, nullable=True)
    published_date = Column(DateTime, nullable=False)
    sentiment_score = Column(Float, nullable=True)  # -1 (악재) to 1 (호재)
    sentiment_label = Column(String, nullable=True)  # 'positive', 'negative', 'neutral'
    source = Column(String, nullable=True)  # News source (e.g., 'rss', 'crawler')
    collected_at = Column(DateTime, server_default=func.now())

