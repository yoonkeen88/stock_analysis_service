"""
News service for collecting and analyzing news articles related to stocks/crypto
"""
import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse
import re


class NewsService:
    """Service for handling news collection and analysis"""
    
    # RSS feed sources for financial news
    RSS_FEEDS = {
        "yahoo_finance": "https://feeds.finance.yahoo.com/rss/2.0/headline",
        "marketwatch": "https://www.marketwatch.com/rss/topstories",
        "bloomberg": "https://feeds.bloomberg.com/markets/news.rss",
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_news_from_rss(
        self,
        symbol: str,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Fetch news articles from RSS feeds related to a symbol
        
        Args:
            symbol: Stock or crypto symbol (e.g., 'AAPL', 'BTC')
            limit: Maximum number of articles to return
        
        Returns:
            List of news articles with title, link, published_date, summary
        """
        all_news = []
        
        # Yahoo Finance RSS with symbol filter
        try:
            yahoo_url = f"{self.RSS_FEEDS['yahoo_finance']}?s={symbol}"
            feed = feedparser.parse(yahoo_url)
            
            for entry in feed.entries[:limit]:
                # Parse published date
                published_date = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published_date = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'published'):
                    try:
                        published_date = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z')
                    except:
                        published_date = datetime.now()
                else:
                    published_date = datetime.now()
                
                # Extract summary
                summary = ""
                if hasattr(entry, 'summary'):
                    summary = entry.summary
                elif hasattr(entry, 'description'):
                    summary = entry.description
                
                # Clean HTML from summary
                summary = self._clean_html(summary)
                
                all_news.append({
                    "symbol": symbol,
                    "title": entry.title,
                    "link": entry.link,
                    "summary": summary[:500] if summary else None,  # Limit summary length
                    "published_date": published_date,
                    "source": "yahoo_finance"
                })
        except Exception as e:
            print(f"Error fetching Yahoo Finance RSS for {symbol}: {str(e)}")
        
        # Sort by published date (newest first)
        all_news.sort(key=lambda x: x['published_date'], reverse=True)
        
        return all_news[:limit]
    
    def fetch_news_by_keyword(
        self,
        keyword: str,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Fetch news articles by keyword search
        
        Args:
            keyword: Search keyword (e.g., 'Apple stock', 'Bitcoin')
            limit: Maximum number of articles to return
        
        Returns:
            List of news articles
        """
        # This is a placeholder - you can extend this with actual search APIs
        # For now, we'll use RSS feeds with keyword filtering
        all_news = []
        
        try:
            # Search Yahoo Finance
            search_url = f"{self.RSS_FEEDS['yahoo_finance']}?s={keyword}"
            feed = feedparser.parse(search_url)
            
            for entry in feed.entries[:limit]:
                published_date = datetime.now()
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published_date = datetime(*entry.published_parsed[:6])
                
                summary = ""
                if hasattr(entry, 'summary'):
                    summary = self._clean_html(entry.summary)
                
                all_news.append({
                    "title": entry.title,
                    "link": entry.link,
                    "summary": summary[:500] if summary else None,
                    "published_date": published_date,
                    "source": "yahoo_finance"
                })
        except Exception as e:
            print(f"Error fetching news by keyword {keyword}: {str(e)}")
        
        return all_news[:limit]
    
    def analyze_sentiment(
        self,
        title: str,
        summary: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze sentiment of news article (basic keyword-based approach)
        
        TODO: Replace with proper ML-based sentiment analysis model
        
        Args:
            title: News title
            summary: News summary (optional)
        
        Returns:
            Dictionary with sentiment_score (-1 to 1) and sentiment_label
        """
        text = f"{title} {summary or ''}".lower()
        
        # Simple keyword-based sentiment (placeholder)
        positive_keywords = [
            'surge', 'rally', 'gain', 'up', 'rise', 'growth', 'profit', 'beat',
            'positive', 'bullish', 'outperform', 'upgrade', 'buy', 'strong'
        ]
        negative_keywords = [
            'drop', 'fall', 'decline', 'down', 'loss', 'miss', 'negative',
            'bearish', 'underperform', 'downgrade', 'sell', 'weak', 'crash'
        ]
        
        positive_count = sum(1 for word in positive_keywords if word in text)
        negative_count = sum(1 for word in negative_keywords if word in text)
        
        # Calculate sentiment score
        total_keywords = positive_count + negative_count
        if total_keywords == 0:
            sentiment_score = 0.0
            sentiment_label = "neutral"
        else:
            sentiment_score = (positive_count - negative_count) / max(total_keywords, 1)
            if sentiment_score > 0.1:
                sentiment_label = "positive"
            elif sentiment_score < -0.1:
                sentiment_label = "negative"
            else:
                sentiment_label = "neutral"
        
        return {
            "sentiment_score": round(sentiment_score, 3),
            "sentiment_label": sentiment_label
        }
    
    def _clean_html(self, text: str) -> str:
        """Remove HTML tags from text"""
        if not text:
            return ""
        soup = BeautifulSoup(text, 'html.parser')
        return soup.get_text().strip()
    
    def get_latest_news(
        self,
        symbol: str,
        limit: int = 10,
        days_back: int = 7
    ) -> List[Dict[str, Any]]:
        """
        Get latest news for a symbol with sentiment analysis
        
        Args:
            symbol: Stock or crypto symbol
            limit: Maximum number of articles
            days_back: Number of days to look back
        
        Returns:
            List of news articles with sentiment analysis
        """
        news_list = self.fetch_news_from_rss(symbol, limit=limit * 2)
        
        # Filter by date and add sentiment
        cutoff_date = datetime.now() - timedelta(days=days_back)
        filtered_news = []
        
        for news in news_list:
            if news['published_date'] >= cutoff_date:
                # Analyze sentiment
                sentiment = self.analyze_sentiment(news['title'], news.get('summary'))
                news['sentiment_score'] = sentiment['sentiment_score']
                news['sentiment_label'] = sentiment['sentiment_label']
                filtered_news.append(news)
                
                if len(filtered_news) >= limit:
                    break
        
        return filtered_news

