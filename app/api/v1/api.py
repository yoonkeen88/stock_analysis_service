"""
API v1 router aggregation
"""
from fastapi import APIRouter
from app.api.v1.endpoints import stocks, predictions, insights, news, evaluation, dashboard

api_router = APIRouter()

api_router.include_router(stocks.router, prefix="/stocks", tags=["stocks"])
api_router.include_router(predictions.router, prefix="/predictions", tags=["predictions"])
api_router.include_router(insights.router, prefix="/insights", tags=["insights"])
api_router.include_router(news.router, prefix="/news", tags=["news"])
api_router.include_router(evaluation.router, prefix="/evaluation", tags=["evaluation"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])

