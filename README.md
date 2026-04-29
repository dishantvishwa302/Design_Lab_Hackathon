# 📝 Paper Review System - Intelligent Pre-Submission Paper Analysis

An intelligent pre-submission paper review system leveraging **Retrieval-Augmented Generation (RAG)** to analyze research papers, retrieve relevant standards and literature, and provide structured feedback to help authors refine their work before submission.

## 🎯 Features

### Core Functionality
- **📤 Smart Paper Upload**: Support for PDF, Text, and DOCX files
- **🔍 Intelligent Analysis**: Multi-aspect paper evaluation
  - Structure Assessment (IMRAD format compliance)
  - Writing Clarity Evaluation
  - Methodology Rigor Analysis
  - Overall Completeness Scoring
  
- **📚 RAG-Enhanced Context Retrieval**: 
  - Leverages OpenAI embeddings for semantic search
  - Retrieves relevant papers and academic standards
  - Contextualizes feedback with literature references

- **📋 Structured Feedback Generation**:
  - Categorized feedback (structure, clarity, methodology, literature gaps)
  - Severity levels (critical, major, minor)
  - Actionable improvement suggestions
  - Specific issue identification with solutions

- **📊 Analysis Dashboard**:
  - Real-time analysis progress tracking
  - Score visualization (structure, clarity, methodology, completeness)
  - Feedback browsing by severity
  - Paper analysis history

- **🔄 Revision Tracking**:
  - Monitor paper improvements across versions
  - Track addressed issues
  - Calculate improvement metrics

## 🏗️ Architecture

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
┌───────▼───┐ ┌────▼────┐ ┌──▼──────┐
│  LangChain │ │OpenAI   │ │Database │
│  RAG       │ │GPT-4 +  │ │(SQLite) │
│  Pipeline  │ │Embeddings│          │
└────────────┘ └─────────┘ └─────────┘
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** 0.104+: Modern, fast web framework
- **Python 3.10+**: Core language
- **SQLAlchemy**: ORM for database operations
- **LangChain 0.1**: RAG orchestration
- **OpenAI API**: GPT-4 for analysis and embeddings
- **PyPDF2 + pdfplumber**: PDF processing

### Frontend
- **React 18**: UI framework
- **TypeScript**: Type-safe development
- **Zustand**: State management
- **Vite**: Fast build tool
- **Axios**: HTTP client

### Infrastructure
- **SQLite**: Embedded database (dev)
- **FAISS**: Vector similarity search
- **Docker**: Containerization (optional)

## 📋 Requirements

- Python 3.10+
- Node.js 18+
- OpenAI API Key (GPT-4 access)
- 2GB RAM minimum
- 500MB disk space

## 🚀 Quick Start

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

## 📖 Usage Guide

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

3. Browse feedback by severity:
   - **🔴 Critical**: Must fix before submission
   - **🟠 Major**: Important improvements needed
   - **🟡 Minor**: Optional enhancements

### Improve Paper
1. Address identified issues in your paper
2. Re-upload revised version
3. Re-analyze to track improvements
4. Compare feedback across versions

## 📚 API Endpoints

### Papers
```
POST   /api/papers/upload          - Upload research paper
GET    /api/papers                 - List all papers
GET    /api/papers/{paper_id}      - Get paper details
```

### Analysis
```
POST   /api/analysis/analyze/{paper_id}  - Start paper analysis
GET    /api/analysis/{paper_id}          - Get analysis results
```

### Feedback
```
GET    /api/feedback/{paper_id}    - Get feedback for paper
```

### System
```
GET    /health                     - Health check
GET    /                          - API info
```

See http://localhost:8000/docs for interactive API documentation.

## 🔄 Analysis Process

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

## 📁 Project Structure

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

## 🐳 Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access
# Frontend: http://localhost:5173
# Backend: http://localhost:8000
# Stop: docker-compose down
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# Type checking
npm run type-check
```

## 🔧 Configuration

### Environment Variables (.env)

```env
# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# Database
DATABASE_URL=sqlite:///./paper_review.db

# Server
HOST=0.0.0.0
PORT=8000

# Upload
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE=52428800

# RAG
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RETRIEVAL=5

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]

# Logging
LOG_LEVEL=INFO
```

## ⚠️ Limitations & Considerations

- **File Size**: Max 50MB per paper
- **Processing Time**: 2-10 minutes depending on paper length
- **Token Usage**: Significant OpenAI API costs for large papers
- **PDF Format**: Complex layouts may not parse perfectly
- **Language**: Optimized for English academic papers

## 🚨 Troubleshooting

### Backend Won't Start
```bash
# Check Python version
python --version  # Should be 3.10+

# Verify API key
echo $OPENAI_API_KEY

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check logs
cat logs/app.log
```

### Frontend Can't Connect
- Ensure backend runs on port 8000
- Check CORS configuration in .env
- Clear browser cache
- Try http://localhost:8000/health

### PDF Parsing Issues
- Verify PDF is valid (not corrupted)
- Check file size < 50MB
- Try with simple PDF first
- Check `backend/logs/app.log` for details

## 📈 Performance Tips

- Use smaller papers for faster analysis
- Batch multiple papers for efficiency
- Increase CHUNK_SIZE for larger papers
- Cache embeddings for repeated analyses

## 🔐 Security Notes

- Never commit .env files
- Keep OpenAI API key private
- Use environment variables in production
- Implement authentication for production
- Sanitize all uploaded files

## 📝 Citation

If you use this system in research, please cite:

```
Paper Review System (2024)
Intelligent pre-submission paper review using RAG
Built with LangChain, FastAPI, and OpenAI
```

## 📄 License

This project is provided as-is for educational and research purposes.

## 🤝 Contributing

Contributions welcome! Please follow:
1. Code style: Black + isort
2. Type hints required
3. Tests for new features
4. Update documentation

## 📞 Support

- Check SETUP_GUIDE.md for detailed setup
- Review API documentation at /docs
- Check logs in backend/logs/
- See code comments for implementation details

---

**Built with ❤️ using RAG, LangChain, and OpenAI GPT-4**
# Design_Lab_Hackathon
