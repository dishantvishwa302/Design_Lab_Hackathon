# Paper Review System - Intelligent Pre-Submission Paper Analysis

An intelligent pre-submission paper review system leveraging **Retrieval-Augmented Generation (RAG)** to analyze research papers, retrieve relevant standards and literature, and provide structured feedback to help authors refine their work before submission.

## Features

### Core Functionality
- **Smart Paper Upload**: Support for PDF, Text, and DOCX files
- **Intelligent Analysis**: Multi-aspect paper evaluation
  - Structure Assessment (IMRAD format compliance)
  - Writing Clarity Evaluation
  - Methodology Rigor Analysis
  - Overall Completeness Scoring
  
- **RAG-Enhanced Context Retrieval**: 
  - Leverages OpenAI embeddings for semantic search
  - Retrieves relevant papers and academic standards
  - Contextualizes feedback with literature references

- **Structured Feedback Generation**:
  - Categorized feedback (structure, clarity, methodology, literature gaps)
  - Severity levels (critical, major, minor)
  - Actionable improvement suggestions
  - Specific issue identification with solutions

- **Analysis Dashboard**:
  - Real-time analysis progress tracking
  - Score visualization (structure, clarity, methodology, completeness)
  - Feedback browsing by severity
  - Paper analysis history


## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   React Frontend                         │
│         (Upload, Dashboard, Analysis, Feedback)         │
└──────────────────┬──────────────────────────────────────┘
                   │ REST API
┌──────────────────▼──────────────────────────────────────┐
│                FastAPI Backend                          │
│  - Paper Management   - Analysis Engine                 │
│  - PDF Parsing        - Feedback Generation             │
└──────────────────┬──────────────────────────────────────┘
                   │
        ┌──────────┼──────────┐
        │          │          │
┌───────▼───┐ ┌────▼────┐   ┌──▼──────┐
│  LangChain │ │OpenAI  │   │Database  │
│  RAG       │ │GROK +  │   │(SQLite)  │
│  Pipeline  │ │Embeddings│ │          │
└────────────┘ └─────────┘  └──────────┘
```



## Quick Start

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your OPENAI_API_KEY

# Run server
python3 main.py
# Backend runs on http://localhost:8000
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
# Frontend runs on http://localhost:5173
```

### 3. Access Application

- **Web UI**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Usage Guide

### Upload a Paper
1. Go to "Upload" tab
2. Drag & drop PDF or click to browse
3. System extracts metadata and prepares for analysis

### Analyze Paper
1. Select paper from Dashboard
2. Click "Start Analysis"
3. System processes:
   - Text extraction
   - Content structure analysis
   - Clarity assessment
   - Methodology evaluation
4. View real-time progress

### Review Feedback
1. Once analysis completes, click "View Feedback"
2. See overall scores (0-100):
   - **Structure**: Paper organization and format
   - **Clarity**: Writing quality and readability
   - **Methodology**: Research rigor and completeness
   - **Completeness**: Overall paper quality


### Improve Paper
1. Address identified issues in your paper
2. Re-upload revised version
3. Re-analyze to track improvements
4. Compare feedback across versions



## Analysis Process

### Phase 1: Document Processing
- Extract text from PDF
- Parse metadata (title, authors)
- Identify sections (intro, methodology, results, etc.)

### Phase 2: RAG Context Retrieval
- Create embeddings of paper chunks
- Search for semantically similar content
- Retrieve related academic standards

### Phase 3: Multi-Aspect Analysis
- **Structure**: Checks IMRAD format compliance
- **Clarity**: Evaluates writing quality and readability
- **Methodology**: Assesses research rigor and completeness
- **Completeness**: Calculates overall quality score

### Phase 4: Feedback Generation
- LLM-powered analysis using GPT-4
- Generates structured feedback items
- Prioritizes issues by severity
- Provides actionable suggestions

## Project Structure

```
paper-review-system/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Configuration
│   ├── app/
│   │   ├── config.py          # Settings
│   │   ├── database.py        # DB setup
│   │   ├── models.py          # SQLAlchemy models
│   │   ├── schemas.py         # Pydantic schemas
│   │   └── services/
│   │       ├── pdf_parser.py
│   │       ├── rag_pipeline.py
│   │       └── web_retrieval.py
│   ├── uploads/               # Paper storage
│   └── logs/                  # Application logs
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx            # Main component
│   │   ├── App.css            # Styles
│   │   ├── main.tsx           # Entry point
│   │   ├── services/
│   │   │   └── api.ts         # API client
│   │   ├── store.ts           # Zustand store
│   │   └── components/
│   │       └── Components.tsx # UI components
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
│
├── SETUP_GUIDE.md             # Detailed setup
├── DEPLOYMENT.md              # Production guide
└── README.md                  # This file
```
## Limitations & Considerations

- **File Size**: Max 50MB per paper
- **Processing Time**: 2-10 minutes depending on paper length
- **Token Usage**: Significant API costs for large papers
- **PDF Format**: Complex layouts may not parse perfectly
- **Language**: Optimized for English academic papers


