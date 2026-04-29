"""
Paper Review System - Backend
Configuration and environment settings
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Paper Review System"
    VERSION: str = "1.0.0"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database
    DATABASE_URL: str = "sqlite:///./paper_review.db"
    SQLALCHEMY_ECHO: bool = False
    
    # OpenAI Configuration
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    # Web Search Configuration
    SERPAPI_API_KEY: Optional[str] = None
    
    # File Upload Configuration
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # 50 MB
    UPLOAD_DIR: str = "./uploads"
    ALLOWED_EXTENSIONS: list = ["pdf", "txt", "docx"]
    
    # RAG Configuration
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    TOP_K_RETRIEVAL: int = 5
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/app.log"
    
    class Config:
        # Use absolute path so .env is found regardless of which directory
        # python is run from (e.g. running `python main.py` from backend/)
        env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
        case_sensitive = True


settings = Settings()
