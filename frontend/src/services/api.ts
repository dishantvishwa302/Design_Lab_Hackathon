// React API Service
// Handles all communication with backend

const API_BASE_URL = '/api';

interface UploadResponse {
  id: number;
  filename: string;
  upload_date: string;
  status: string;
  message: string;
}

interface AnalysisScores {
  structure_score: number;
  clarity_score: number;
  methodology_score: number;
  completeness_score: number;
}

interface FeedbackItem {
  id: number;
  category: string;
  severity: 'critical' | 'major' | 'minor';
  issue: string;
  suggestion: string;
  is_addressed: boolean;
}

interface FeedbackResponse {
  paper_id: number;
  analysis_scores: AnalysisScores;
  feedback_by_severity: {
    critical: FeedbackItem[];
    major: FeedbackItem[];
    minor: FeedbackItem[];
  };
  total_feedback: number;
  critical_count: number;
  major_count: number;
  minor_count: number;
}

class ApiService {
  // Papers
  async uploadPaper(file: File): Promise<UploadResponse> {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch(`${API_BASE_URL}/papers/upload`, {
      method: 'POST',
      body: formData
    });
    
    if (!response.ok) throw new Error('Upload failed');
    return response.json();
  }

  async getPaper(paperId: number) {
    const response = await fetch(`${API_BASE_URL}/papers/${paperId}`);
    if (!response.ok) throw new Error('Failed to get paper');
    return response.json();
  }

  async listPapers() {
    const response = await fetch(`${API_BASE_URL}/papers`);
    if (!response.ok) throw new Error('Failed to list papers');
    return response.json();
  }

  // Analysis
  async analyzePaper(paperId: number): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/analysis/analyze/${paperId}`, {
      method: 'POST'
    });
    
    if (!response.ok) throw new Error('Analysis failed');
    return response.json();
  }

  async getAnalysis(paperId: number) {
    const response = await fetch(`${API_BASE_URL}/analysis/${paperId}`);
    if (!response.ok) throw new Error('Failed to get analysis');
    return response.json();
  }

  // Feedback
  async getFeedback(paperId: number): Promise<FeedbackResponse> {
    const response = await fetch(`${API_BASE_URL}/feedback/${paperId}`);
    if (!response.ok) throw new Error('Failed to get feedback');
    return response.json();
  }

  // Health check
  async healthCheck() {
    try {
      const response = await fetch(`${API_BASE_URL.replace('/api', '')}/health`);
      return response.ok;
    } catch {
      return false;
    }
  }
}

export const apiService = new ApiService();
export type { UploadResponse, AnalysisScores, FeedbackItem, FeedbackResponse };
