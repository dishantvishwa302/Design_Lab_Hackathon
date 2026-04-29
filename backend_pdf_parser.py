"""
PDF and document parsing service
"""

import pypdf as PyPDF2
import re
from typing import Dict, List, Tuple
from pathlib import Path
import pdfplumber


class PDFParser:
    """Parse and extract content from research papers"""
    
    @staticmethod
    def extract_text(pdf_path: str) -> str:
        """Extract all text from PDF"""
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        except Exception as e:
            print(f"Error extracting text: {e}")
        return text
    
    @staticmethod
    def extract_metadata(pdf_path: str) -> Dict:
        """Extract metadata from PDF"""
        metadata = {}
        try:
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                if reader.metadata:
                    metadata = {
                        'title': reader.metadata.get('/Title', ''),
                        'author': reader.metadata.get('/Author', ''),
                        'subject': reader.metadata.get('/Subject', ''),
                        'pages': len(reader.pages)
                    }
        except Exception as e:
            print(f"Error extracting metadata: {e}")
        return metadata
    
    @staticmethod
    def extract_sections(text: str) -> Dict[str, str]:
        """Extract main sections of research paper"""
        sections = {
            'abstract': '',
            'introduction': '',
            'methodology': '',
            'results': '',
            'discussion': '',
            'conclusion': '',
            'references': ''
        }
        
        # Simple section extraction based on common patterns
        patterns = {
            'abstract': r'(?:abstract|summary)(.*?)(?:introduction|1\.)',
            'introduction': r'(?:introduction|1\.)(.*?)(?:methodology|method|2\.)',
            'methodology': r'(?:methodology|method|2\.)(.*?)(?:results|3\.)',
            'results': r'(?:results|findings|3\.)(.*?)(?:discussion|4\.)',
            'discussion': r'(?:discussion|4\.)(.*?)(?:conclusion|5\.)',
            'conclusion': r'(?:conclusion|conclusion|5\.)(.*?)(?:references|reference)',
            'references': r'(?:references|reference)(.*?)$'
        }
        
        text_lower = text.lower()
        for section, pattern in patterns.items():
            match = re.search(pattern, text_lower, re.DOTALL | re.IGNORECASE)
            if match:
                sections[section] = match.group(1).strip()[:2000]  # Limit to 2000 chars
        
        return sections
    
    @staticmethod
    def get_word_count(text: str) -> int:
        """Get word count"""
        return len(text.split())
    
    @staticmethod
    def validate_pdf(pdf_path: str) -> Tuple[bool, str]:
        """Validate if file is valid PDF"""
        try:
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                if len(reader.pages) == 0:
                    return False, "PDF has no pages"
            return True, "Valid PDF"
        except Exception as e:
            return False, f"Invalid PDF: {str(e)}"
