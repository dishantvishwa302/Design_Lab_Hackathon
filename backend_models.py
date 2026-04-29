"""
Database models for Paper Review System
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

Base = declarative_base()


class Paper(Base):
    __tablename__ = "papers"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    title = Column(String, nullable=True)
    abstract = Column(Text, nullable=True)
    authors = Column(String, nullable=True)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer)
    upload_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    processing_status = Column(String, default="pending")  # pending, processing, completed, failed
    
    # Relationships
    analysis = relationship("Analysis", back_populates="paper", cascade="all, delete-orphan")
    feedback = relationship("Feedback", back_populates="paper", cascade="all, delete-orphan")


class Analysis(Base):
    __tablename__ = "analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    paper_id = Column(Integer, ForeignKey("papers.id"), nullable=False)
    
    # Extracted content
    sections = Column(Text)  # JSON: {intro, methodology, results, conclusion, etc}
    structure_score = Column(Float)  # 0-100: How well structured
    clarity_score = Column(Float)  # 0-100: Clarity of writing
    methodology_score = Column(Float)  # 0-100: Methodology completeness
    completeness_score = Column(Float)  # 0-100: Overall completeness
    
    # RAG Context
    retrieved_papers = Column(Text)  # JSON: List of related papers
    retrieved_standards = Column(Text)  # JSON: Relevant academic standards
    
    analysis_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    processing_time = Column(Float)  # seconds
    
    paper = relationship("Paper", back_populates="analysis")


class Feedback(Base):
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    paper_id = Column(Integer, ForeignKey("papers.id"), nullable=False)
    analysis_id = Column(Integer, ForeignKey("analysis.id"), nullable=True)
    
    # Feedback content
    category = Column(String)  # structure, clarity, methodology, literature, etc
    severity = Column(String)  # critical, major, minor
    issue = Column(Text)
    suggestion = Column(Text)
    references = Column(Text)  # JSON: Related papers/standards
    
    # Metadata
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_addressed = Column(Boolean, default=False)
    
    paper = relationship("Paper", back_populates="feedback")


class ReviewHistory(Base):
    __tablename__ = "review_history"
    
    id = Column(Integer, primary_key=True, index=True)
    paper_id = Column(Integer, ForeignKey("papers.id"), nullable=False)
    revision_number = Column(Integer, default=1)
    
    # Changes made
    changes_summary = Column(Text)
    issues_fixed = Column(Integer)
    new_issues = Column(Integer)
    
    improved_score = Column(Float)  # Overall improvement percentage
    review_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
