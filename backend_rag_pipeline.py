"""
RAG Pipeline using LangChain and OpenAI
"""

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.callbacks import StreamingStdOutCallbackHandler
from typing import List, Dict, Tuple
import json
from backend_config import settings


class RAGPipeline:
    """Retrieval-Augmented Generation pipeline for paper analysis"""
    
    def __init__(self):
        # Initialize LLM with Groq base_url if it's a Groq key
        base_url = None
        if settings.OPENAI_API_KEY.startswith("gsk_"):
            base_url = "https://api.groq.com/openai/v1"
            
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY,
            model=settings.OPENAI_EMBEDDING_MODEL,
            base_url=base_url
        )
        self.llm = ChatOpenAI(
            openai_api_key=settings.OPENAI_API_KEY,
            model_name=settings.OPENAI_MODEL,
            temperature=0.3,
            base_url=base_url
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )

    def _parse_json_response(self, content: str) -> Dict:
        """Robustly parse JSON from LLM response"""
        try:
            # Try direct parsing
            return json.loads(content)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown blocks
            import re
            json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(1))
                except json.JSONDecodeError:
                    pass
            
            # Try to find anything that looks like a JSON object
            json_match = re.search(r'({.*})', content, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(1))
                except json.JSONDecodeError:
                    pass
            
            print(f"Failed to parse JSON response: {content}")
            return {}
    
    def create_vector_store(self, text: str) -> FAISS:
        """Create FAISS vector store from paper text"""
        chunks = self.text_splitter.split_text(text)
        vector_store = FAISS.from_texts(chunks, self.embeddings)
        return vector_store
    
    def retrieve_context(self, vector_store: FAISS, query: str, k: int = 5) -> List[str]:
        """Retrieve relevant context from vector store"""
        try:
            docs = vector_store.similarity_search(query, k=k)
            return [doc.page_content for doc in docs]
        except Exception as e:
            print(f"Error retrieving context: {e}")
            return []
    
    def analyze_paper_structure(self, paper_text: str, sections: Dict) -> Dict:
        """Analyze paper structure using RAG"""
        
        prompt = PromptTemplate(
            input_variables=["paper_content", "sections"],
            template="""Analyze this research paper and provide structure assessment:

Paper Content:
{paper_content}

Identified Sections:
{sections}

Provide assessment in JSON format:
{{
    "structure_quality": score (0-100),
    "missing_sections": ["list of missing sections"],
    "structure_issues": ["list of issues"],
    "structure_recommendations": ["list of recommendations"]
}}"""
        )
        
        try:
            response = self.llm.invoke([
                {"role": "system", "content": "You are an expert academic paper reviewer. You MUST return ONLY valid JSON."},
                {"role": "user", "content": prompt.format(
                    paper_content=paper_text[:2000],
                    sections=json.dumps(sections, indent=2)
                )}
            ])
            return self._parse_json_response(response.content)
        except Exception as e:
            print(f"Error analyzing structure: {e}")
            return {}
    
    def analyze_clarity(self, paper_text: str) -> Dict:
        """Analyze writing clarity"""
        
        prompt = """Analyze the clarity and quality of writing in this research paper:

Paper excerpt:
{text}

Provide assessment in JSON format:
{{
    "clarity_score": score (0-100),
    "clarity_issues": ["list of clarity issues"],
    "writing_quality": "assessment",
    "improvement_suggestions": ["suggestions"]
}}"""
        
        try:
            response = self.llm.invoke([
                {"role": "system", "content": "You are an expert academic writing reviewer. You MUST return ONLY valid JSON."},
                {"role": "user", "content": prompt.format(text=paper_text[:1500])}
            ])
            return self._parse_json_response(response.content)
        except Exception as e:
            print(f"Error analyzing clarity: {e}")
            return {}
    
    def analyze_methodology(self, methodology_text: str) -> Dict:
        """Analyze methodology completeness"""
        
        prompt = """Analyze the research methodology in this section:

Methodology:
{methodology}

Check for presence of:
- Research design/approach
- Sample size and participants
- Data collection methods
- Statistical analysis methods
- Study limitations

Provide assessment in JSON format:
{{
    "methodology_score": score (0-100),
    "completeness_issues": ["missing elements"],
    "rigor_assessment": "assessment",
    "improvement_suggestions": ["suggestions"]
}}"""
        
        try:
            response = self.llm.invoke([
                {"role": "system", "content": "You are an expert research methodology reviewer. You MUST return ONLY valid JSON."},
                {"role": "user", "content": prompt.format(methodology=methodology_text[:1500])}
            ])
            return self._parse_json_response(response.content)
        except Exception as e:
            print(f"Error analyzing methodology: {e}")
            return {}
    
    def generate_feedback(self, paper_text: str, analysis_results: Dict) -> List[Dict]:
        """Generate specific feedback items"""
        
        prompt = """Based on this research paper analysis, generate specific feedback items:

Paper excerpt:
{text}

Analysis results:
{analysis}

For each issue, provide:
- Category (structure/clarity/methodology/literature/etc)
- Severity (critical/major/minor)
- Specific issue description
- Actionable suggestion

Format as JSON array:
[
  {{
    "category": "...",
    "severity": "...",
    "issue": "...",
    "suggestion": "..."
  }}
]"""
        
        try:
            response = self.llm.invoke([
                {"role": "system", "content": "You are an expert academic paper reviewer providing constructive feedback. You MUST return ONLY valid JSON."},
                {"role": "user", "content": prompt.format(
                    text=paper_text[:2000],
                    analysis=json.dumps(analysis_results, indent=2)
                )}
            ])
            result = self._parse_json_response(response.content)
            return result if isinstance(result, list) else []
        except Exception as e:
            print(f"Error generating feedback: {e}")
            return []

