"""
Paper insights endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.prediction import PaperInsightCreate, PaperInsightResponse
from app.db.models import PaperInsight

router = APIRouter()


@router.post("/insights", response_model=PaperInsightResponse)
async def create_insight(
    insight: PaperInsightCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new paper-based insight
    
    - **paper_title**: Title of the research paper
    - **paper_doi**: DOI of the paper (optional)
    - **symbol**: Related stock/crypto symbol (optional)
    - **insight_summary**: Summary of the insight
    - **methodology**: Methodology used in the paper
    - **key_findings**: Key findings from the paper
    """
    try:
        db_insight = PaperInsight(**insight.model_dump())
        db.add(db_insight)
        db.commit()
        db.refresh(db_insight)
        return db_insight
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating insight: {str(e)}")


@router.get("/insights", response_model=List[PaperInsightResponse])
async def get_insights(
    symbol: Optional[str] = None,
    is_read: Optional[bool] = None,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Get paper insights
    
    - **symbol**: Filter by symbol (optional)
    - **is_read**: Filter by read status (optional)
    - **limit**: Maximum number of insights to return
    """
    try:
        query = db.query(PaperInsight)
        
        if symbol:
            query = query.filter(PaperInsight.symbol == symbol)
        if is_read is not None:
            query = query.filter(PaperInsight.is_read == is_read)
        
        insights = query.order_by(PaperInsight.created_at.desc()).limit(limit).all()
        return insights
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching insights: {str(e)}")


@router.get("/insights/{insight_id}", response_model=PaperInsightResponse)
async def get_insight(
    insight_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific insight by ID"""
    insight = db.query(PaperInsight).filter(PaperInsight.id == insight_id).first()
    if not insight:
        raise HTTPException(status_code=404, detail="Insight not found")
    return insight


@router.patch("/insights/{insight_id}/read", response_model=PaperInsightResponse)
async def mark_insight_read(
    insight_id: int,
    db: Session = Depends(get_db)
):
    """Mark an insight as read"""
    insight = db.query(PaperInsight).filter(PaperInsight.id == insight_id).first()
    if not insight:
        raise HTTPException(status_code=404, detail="Insight not found")
    
    insight.is_read = True
    db.commit()
    db.refresh(insight)
    return insight

