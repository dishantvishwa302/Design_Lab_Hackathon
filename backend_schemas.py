"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class PaperBase(BaseModel):
    filename: str
    title: Optional[str] = None
    authors: Optional[str] = None


class PaperCreate(PaperBase):
    pass


class PaperResponse(PaperBase):
    id: int
    file_path: str
    upload_date: datetime
    processing_status: str
    
    class Config:
        from_attributes = True


class AnalysisScores(BaseModel):
    structure_score: float
    clarity_score: float
    methodology_score: float
    completeness_score: float
    overall_score: Optional[float] = None


class AnalysisResponse(BaseModel):
    id: int
    paper_id: int
    structure_score: float
    clarity_score: float
    methodology_score: float
    completeness_score: float
    sections: Optional[Dict[str, Any]] = None
    analysis_date: datetime
    processing_time: float
    
    class Config:
        from_attributes = True


class FeedbackItemResponse(BaseModel):
    id: int
    category: str
    severity: str  # critical, major, minor
    issue: str
    suggestion: str
    references: Optional[List[str]] = None
    is_addressed: bool
    
    class Config:
        from_attributes = True


class CompleteFeedbackResponse(BaseModel):
    paper_id: int
    analysis_scores: AnalysisScores
    feedback_items: List[FeedbackItemResponse]
    retrieved_papers: Optional[List[str]] = None
    total_issues: int
    critical_issues: int
    major_issues: int
    minor_issues: int


class ReviewHistoryResponse(BaseModel):
    id: int
    paper_id: int
    revision_number: int
    changes_summary: str
    issues_fixed: int
    new_issues: int
    improved_score: float
    review_date: datetime
    
    class Config:
        from_attributes = True


class PaperAnalysisRequest(BaseModel):
    paper_id: int
    retrieve_context: bool = True
    depth: str = "standard"  # quick, standard, deep


class PaperUploadResponse(BaseModel):
    id: int
    filename: str
    upload_date: datetime
    status: str
    message: str
