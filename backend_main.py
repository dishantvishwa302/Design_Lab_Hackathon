"""
Paper Review System - Backend Main Application
"""

from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
import os
import aiofiles
from datetime import datetime
import logging

from backend_config import settings
from backend_database import init_db, get_db, SessionLocal
from backend_models import Paper, Analysis, Feedback, Base
from backend_schemas import (
    PaperResponse, PaperUploadResponse, AnalysisResponse, 
    CompleteFeedbackResponse, FeedbackItemResponse
)
from backend_pdf_parser import PDFParser
from backend_rag_pipeline import RAGPipeline

# Setup logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Create app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="RAG-powered intelligent paper review system",
    version=settings.VERSION
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
rag_pipeline = RAGPipeline()
pdf_parser = PDFParser()

# Create upload directory
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)


@app.on_event("startup")
async def startup():
    """Initialize database on startup"""
    init_db()
    logger.info("✓ Application started")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "Paper Review System"}


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "description": "Intelligent pre-submission paper review using RAG"
    }


# ============ PAPER ENDPOINTS ============

@app.post("/api/papers/upload", response_model=PaperUploadResponse)
async def upload_paper(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = None
):
    """Upload a research paper for analysis"""
    
    try:
        # Validate file
        if not file.filename.endswith(('.pdf', '.txt', '.docx')):
            raise HTTPException(status_code=400, detail="Invalid file type")
        
        if file.size > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(status_code=413, detail="File too large")
        
        # Save file
        file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Create paper record
        paper = Paper(
            filename=file.filename,
            file_path=file_path,
            file_size=file.size,
            processing_status="pending"
        )
        db.add(paper)
        db.commit()
        db.refresh(paper)
        
        logger.info(f"✓ Paper uploaded: {file.filename} (ID: {paper.id})")
        
        return PaperUploadResponse(
            id=paper.id,
            filename=file.filename,
            upload_date=paper.upload_date,
            status="pending",
            message="Paper uploaded successfully"
        )
    
    except Exception as e:
        logger.error(f"Error uploading paper: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/papers/{paper_id}", response_model=PaperResponse)
async def get_paper(paper_id: int, db: Session = Depends(get_db)):
    """Get paper details"""
    paper = db.query(Paper).filter(Paper.id == paper_id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    return paper


@app.get("/api/papers", response_model=List[PaperResponse])
async def list_papers(db: Session = Depends(get_db)):
    """List all uploaded papers"""
    papers = db.query(Paper).order_by(Paper.upload_date.desc()).all()
    return papers


# ============ ANALYSIS ENDPOINTS ============

@app.post("/api/analysis/analyze/{paper_id}")
async def analyze_paper(
    paper_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Analyze a research paper"""
    
    try:
        # Get paper
        paper = db.query(Paper).filter(Paper.id == paper_id).first()
        if not paper:
            raise HTTPException(status_code=404, detail="Paper not found")
        
        # Check if valid PDF
        is_valid, message = pdf_parser.validate_pdf(paper.file_path)
        if not is_valid:
            paper.processing_status = "failed"
            db.commit()
            raise HTTPException(status_code=400, detail=message)
        
        # Update status
        paper.processing_status = "processing"
        db.commit()
        
        # Run analysis in background
        background_tasks.add_task(
            process_paper_analysis,
            paper_id=paper_id,
            file_path=paper.file_path
        )
        
        return {
            "status": "processing",
            "paper_id": paper_id,
            "message": "Analysis started"
        }
    
    except Exception as e:
        logger.error(f"Error analyzing paper: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


async def process_paper_analysis(paper_id: int, file_path: str):
    """Background task: Process paper analysis"""
    db = SessionLocal()
    try:
        paper = db.query(Paper).filter(Paper.id == paper_id).first()
        
        # Extract text and metadata
        text = pdf_parser.extract_text(file_path)
        metadata = pdf_parser.extract_metadata(file_path)
        sections = pdf_parser.extract_sections(text)
        
        paper.title = metadata.get('title', '')
        paper.authors = metadata.get('author', '')
        
        # Run RAG analysis
        structure_analysis = rag_pipeline.analyze_paper_structure(text, sections)
        clarity_analysis = rag_pipeline.analyze_clarity(text)
        methodology_analysis = rag_pipeline.analyze_methodology(
            sections.get('methodology', '')
        )
        
        # Create analysis record
        analysis = Analysis(
            paper_id=paper_id,
            sections=str(sections),
            structure_score=structure_analysis.get('structure_quality', 0),
            clarity_score=clarity_analysis.get('clarity_score', 0),
            methodology_score=methodology_analysis.get('methodology_score', 0),
            completeness_score=(
                structure_analysis.get('structure_quality', 0) +
                clarity_analysis.get('clarity_score', 0) +
                methodology_analysis.get('methodology_score', 0)
            ) / 3
        )
        db.add(analysis)
        db.flush()
        
        # Generate feedback
        feedback_items = rag_pipeline.generate_feedback(text, {
            'structure': structure_analysis,
            'clarity': clarity_analysis,
            'methodology': methodology_analysis
        })
        
        for item in feedback_items:
            feedback = Feedback(
                paper_id=paper_id,
                analysis_id=analysis.id,
                category=item.get('category', 'general'),
                severity=item.get('severity', 'minor'),
                issue=item.get('issue', ''),
                suggestion=item.get('suggestion', '')
            )
            db.add(feedback)
        
        paper.processing_status = "completed"
        db.commit()
        logger.info(f"✓ Paper {paper_id} analysis completed")
    
    except Exception as e:
        logger.error(f"Error in paper analysis: {str(e)}")
        paper.processing_status = "failed"
        db.commit()
    finally:
        db.close()


@app.get("/api/analysis/{paper_id}")
async def get_analysis(paper_id: int, db: Session = Depends(get_db)):
    """Get paper analysis results"""
    analysis = db.query(Analysis).filter(Analysis.paper_id == paper_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return AnalysisResponse.from_orm(analysis)


# ============ FEEDBACK ENDPOINTS ============

@app.get("/api/feedback/{paper_id}")
async def get_feedback(paper_id: int, db: Session = Depends(get_db)):
    """Get feedback for a paper"""
    
    paper = db.query(Paper).filter(Paper.id == paper_id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    analysis = db.query(Analysis).filter(Analysis.paper_id == paper_id).first()
    feedback_items = db.query(Feedback).filter(Feedback.paper_id == paper_id).all()
    
    # Categorize feedback
    feedback_by_severity = {
        'critical': [f for f in feedback_items if f.severity == 'critical'],
        'major': [f for f in feedback_items if f.severity == 'major'],
        'minor': [f for f in feedback_items if f.severity == 'minor']
    }
    
    return {
        "paper_id": paper_id,
        "analysis_scores": {
            "structure_score": analysis.structure_score if analysis else 0,
            "clarity_score": analysis.clarity_score if analysis else 0,
            "methodology_score": analysis.methodology_score if analysis else 0,
            "completeness_score": analysis.completeness_score if analysis else 0,
        },
        "feedback_by_severity": {
            "critical": [FeedbackItemResponse.from_orm(f).dict() for f in feedback_by_severity['critical']],
            "major": [FeedbackItemResponse.from_orm(f).dict() for f in feedback_by_severity['major']],
            "minor": [FeedbackItemResponse.from_orm(f).dict() for f in feedback_by_severity['minor']],
        },
        "total_feedback": len(feedback_items),
        "critical_count": len(feedback_by_severity['critical']),
        "major_count": len(feedback_by_severity['major']),
        "minor_count": len(feedback_by_severity['minor'])
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
