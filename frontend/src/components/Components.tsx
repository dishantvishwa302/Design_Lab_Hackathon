// React Components for Paper Review System

import React, { useState } from 'react';
import { apiService } from '../services/api';
import { useAppStore } from '../store';

// ============ UPLOAD COMPONENT ============
export const UploadForm: React.FC = () => {
  const [isDragging, setIsDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const { addPaper, setSelectedTab } = useAppStore();

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileUpload(files[0]);
    }
  };

  const handleFileUpload = async (file: File) => {
    setUploading(true);
    try {
      const response = await apiService.uploadPaper(file);
      addPaper({
        id: response.id,
        filename: response.filename,
        upload_date: response.upload_date,
        processing_status: 'pending'
      });
      setSelectedTab('dashboard');
    } catch (error) {
      alert('Upload failed: ' + (error as Error).message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      className={`upload-zone ${isDragging ? 'dragging' : ''}`}
    >
      <div className="upload-content">
        <div className="upload-icon">📄</div>
        <h3>Upload Research Paper</h3>
        <p>Drag and drop your PDF or click to browse</p>
        <input
          type="file"
          accept=".pdf,.txt,.docx"
          onChange={(e) => {
            if (e.target.files?.[0]) {
              handleFileUpload(e.target.files[0]);
            }
          }}
          style={{ display: 'none' }}
          id="file-input"
          disabled={uploading}
        />
        <label htmlFor="file-input" className="browse-btn" style={{ opacity: uploading ? 0.6 : 1, cursor: uploading ? 'not-allowed' : 'pointer' }}>
          {uploading ? 'Uploading...' : 'Browse Files'}
        </label>
      </div>
    </div>
  );
};

// ============ ANALYSIS PROGRESS ============
export const AnalysisProgress: React.FC<{
  paperId: number;
  onComplete: (paperId: number) => void;
}> = ({ paperId, onComplete }) => {
  const [progress, setProgress] = useState(0);
  const [statusText, setStatusText] = useState('Starting analysis...');
  const [analysisStatus, setAnalysisStatus] = useState<'processing' | 'completed' | 'failed'>('processing');

  // Fake visual progress bar while polling for real status
  React.useEffect(() => {
    const progressInterval = setInterval(() => {
      setProgress((p) => {
        if (p >= 85) return p; // Hold at 85% until completed
        return p + Math.random() * 8;
      });
    }, 1500);
    return () => clearInterval(progressInterval);
  }, []);

  // Real polling: check backend every 5 seconds for actual status
  React.useEffect(() => {
    const steps = [
      'Extracting text from document...',
      'Identifying paper sections...',
      'Analyzing structure with RAG...',
      'Evaluating writing clarity...',
      'Reviewing methodology...',
      'Generating feedback...',
    ];
    let stepIndex = 0;

    const pollInterval = setInterval(async () => {
      try {
        const paper = await apiService.getPaper(paperId);

        // Advance status label
        setStatusText(steps[Math.min(stepIndex++, steps.length - 1)]);

        if (paper.processing_status === 'completed') {
          setProgress(100);
          setStatusText('Analysis complete! ✅');
          setAnalysisStatus('completed');
          clearInterval(pollInterval);
          setTimeout(() => onComplete(paperId), 1200);
        } else if (paper.processing_status === 'failed') {
          setStatusText('Analysis failed ❌');
          setAnalysisStatus('failed');
          clearInterval(pollInterval);
        }
      } catch (e) {
        console.error('Failed to poll analysis status:', e);
      }
    }, 5000);

    return () => clearInterval(pollInterval);
  }, [paperId, onComplete]);

  return (
    <div className="progress-container">
      <h3>
        {analysisStatus === 'failed' ? '❌ Analysis Failed' : 'Analyzing Paper...'}
      </h3>
      <div className="progress-bar">
        <div
          className="progress-fill"
          style={{
            width: `${progress}%`,
            backgroundColor: analysisStatus === 'failed' ? '#e53e3e' : undefined,
            transition: 'width 1s ease'
          }}
        />
      </div>
      <p className="progress-status">{statusText}</p>
      {analysisStatus === 'failed' && (
        <p style={{ color: '#e53e3e', marginTop: '1rem' }}>
          Analysis failed. Please check your OpenAI API key in the .env file and try again.
        </p>
      )}
      <div className="steps">
        <div className={`step ${progress > 20 ? 'done' : ''}`}>
          <span>📖</span> Extracting Content
        </div>
        <div className={`step ${progress > 40 ? 'done' : ''}`}>
          <span>🔍</span> Analyzing Structure
        </div>
        <div className={`step ${progress > 60 ? 'done' : ''}`}>
          <span>📚</span> Evaluating Methodology
        </div>
        <div className={`step ${progress > 80 ? 'done' : ''}`}>
          <span>✍️</span> Generating Feedback
        </div>
      </div>
    </div>
  );
};

// ============ FEEDBACK DISPLAY ============
export const FeedbackDisplay: React.FC<{ paperId: number }> = ({ paperId }) => {
  const [feedback, setFeedback] = React.useState<any>(null);
  const [activeTab, setActiveTab] = React.useState<'critical' | 'major' | 'minor'>('critical');

  React.useEffect(() => {
    apiService.getFeedback(paperId)
      .then(setFeedback)
      .catch(console.error);
  }, [paperId]);

  if (!feedback) return <div style={{ padding: '2rem', textAlign: 'center' }}>Loading feedback...</div>;

  const severityIcons: Record<string, string> = {
    critical: '🔴',
    major: '🟠',
    minor: '🟡'
  };

  const items = feedback.feedback_by_severity[activeTab];

  return (
    <div className="feedback-container">
      <div className="scores-grid">
        <div className="score-card">
          <h4>Structure</h4>
          <div className="score">{Math.round(feedback.analysis_scores.structure_score)}/100</div>
        </div>
        <div className="score-card">
          <h4>Clarity</h4>
          <div className="score">{Math.round(feedback.analysis_scores.clarity_score)}/100</div>
        </div>
        <div className="score-card">
          <h4>Methodology</h4>
          <div className="score">{Math.round(feedback.analysis_scores.methodology_score)}/100</div>
        </div>
        <div className="score-card">
          <h4>Completeness</h4>
          <div className="score">{Math.round(feedback.analysis_scores.completeness_score)}/100</div>
        </div>
      </div>

      <div className="feedback-tabs">
        <button
          className={`tab ${activeTab === 'critical' ? 'active' : ''}`}
          onClick={() => setActiveTab('critical')}
        >
          🔴 Critical ({feedback.critical_count})
        </button>
        <button
          className={`tab ${activeTab === 'major' ? 'active' : ''}`}
          onClick={() => setActiveTab('major')}
        >
          🟠 Major ({feedback.major_count})
        </button>
        <button
          className={`tab ${activeTab === 'minor' ? 'active' : ''}`}
          onClick={() => setActiveTab('minor')}
        >
          🟡 Minor ({feedback.minor_count})
        </button>
      </div>

      <div className="feedback-items">
        {items.length === 0 && (
          <p style={{ color: '#888', textAlign: 'center', padding: '1rem' }}>
            No {activeTab} issues found.
          </p>
        )}
        {items.map((item: any) => (
          <div key={item.id} className={`feedback-item ${item.severity}`}>
            <div className="item-header">
              <span className="severity-icon">{severityIcons[item.severity]}</span>
              <span className="category">{item.category}</span>
            </div>
            <p className="issue"><strong>Issue:</strong> {item.issue}</p>
            <p className="suggestion"><strong>Suggestion:</strong> {item.suggestion}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

// ============ DASHBOARD ============
// Helper: parse a UTC datetime string (no Z suffix) as UTC and display in local time
function formatUploadDate(dateStr: string): string {
  // Backend stores UTC but doesn't append 'Z'. Append it so the browser
  // parses it correctly as UTC and converts to the user's local timezone.
  const utcStr = dateStr.endsWith('Z') ? dateStr : dateStr + 'Z';
  return new Date(utcStr).toLocaleString();
}

interface DashboardProps {
  onAnalyze: (paperId: number) => void;
  onViewFeedback: (paperId: number) => void;
}

export const Dashboard: React.FC<DashboardProps> = ({ onAnalyze, onViewFeedback }) => {
  const { papers, setPapers } = useAppStore();

  // Poll every 8s to refresh paper statuses (e.g. processing → completed)
  React.useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const data = await import('../services/api').then(m => m.apiService.listPapers());
        setPapers(data);
      } catch (e) {
        // silently ignore
      }
    }, 8000);
    return () => clearInterval(interval);
  }, [setPapers]);

  return (
    <div className="dashboard">
      <h2>Paper Review Dashboard</h2>
      {papers.length === 0 && (
        <p style={{ color: '#888', textAlign: 'center', marginTop: '2rem' }}>
          No papers uploaded yet. Go to the Upload tab to get started.
        </p>
      )}
      <div className="papers-list">
        {papers.map((paper) => (
          <div key={paper.id} className="paper-card">
            <div className="paper-header">
              <h3>{paper.filename}</h3>
              <span className={`status ${paper.processing_status}`}>
                {paper.processing_status}
              </span>
            </div>
            <p className="uploaded">
              Uploaded: {formatUploadDate(paper.upload_date)}
            </p>
            {paper.processing_status === 'pending' && (
              <button
                className="analyze-btn"
                onClick={() => onAnalyze(paper.id)}
              >
                Start Analysis
              </button>
            )}
            {paper.processing_status === 'processing' && (
              <button className="analyze-btn" disabled style={{ opacity: 0.6, cursor: 'not-allowed' }}>
                ⏳ Processing...
              </button>
            )}
            {paper.processing_status === 'completed' && (
              <button
                className="view-btn"
                onClick={() => onViewFeedback(paper.id)}
              >
                View Feedback
              </button>
            )}
            {paper.processing_status === 'failed' && (
              <button
                className="analyze-btn"
                onClick={() => onAnalyze(paper.id)}
                style={{ backgroundColor: '#e53e3e' }}
              >
                Retry Analysis
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
