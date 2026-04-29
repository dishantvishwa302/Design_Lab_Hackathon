// Main React App Component

import React, { useState, useEffect } from 'react';
import { apiService } from './services/api';
import { useAppStore } from './store';
import { UploadForm, AnalysisProgress, FeedbackDisplay, Dashboard } from './components/Components';
import './App.css';

export function App() {
  const { selectedTab, setSelectedTab, papers, setPapers, isLoading, setIsLoading } = useAppStore();
  const [currentPaperId, setCurrentPaperId] = useState<number | null>(null);

  useEffect(() => {
    loadPapers();
    apiService.healthCheck().then(healthy => {
      if (!healthy) {
        console.warn('Backend not available');
      }
    });
  }, []);

  const loadPapers = async () => {
    try {
      const data = await apiService.listPapers();
      setPapers(data);
    } catch (error) {
      console.error('Failed to load papers:', error);
    }
  };

  // Called when "Start Analysis" is clicked in the Dashboard
  const handleAnalyzePaper = async (paperId: number) => {
    try {
      setIsLoading(true);
      setCurrentPaperId(paperId);
      await apiService.analyzePaper(paperId);
      setSelectedTab('progress');
      // Refresh paper list so status shows "processing"
      await loadPapers();
    } catch (error) {
      alert('Failed to start analysis: ' + (error as Error).message);
    } finally {
      setIsLoading(false);
    }
  };

  // Called by AnalysisProgress when backend reports status = "completed"
  const handleAnalysisComplete = async (paperId: number) => {
    await loadPapers();         // Refresh dashboard statuses
    setCurrentPaperId(paperId);
    setSelectedTab('feedback'); // Auto-navigate to Feedback tab
  };

  // Called when "View Feedback" is clicked on a completed paper
  const handleViewFeedback = (paperId: number) => {
    setCurrentPaperId(paperId);
    setSelectedTab('feedback');
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>📝 Paper Review System</h1>
          <p>Intelligent Pre-submission Paper Review using RAG</p>
        </div>
        <nav className="nav-tabs">
          <button
            className={`nav-tab ${selectedTab === 'upload' ? 'active' : ''}`}
            onClick={() => setSelectedTab('upload')}
          >
            Upload
          </button>
          <button
            className={`nav-tab ${selectedTab === 'dashboard' ? 'active' : ''}`}
            onClick={() => setSelectedTab('dashboard')}
          >
            Dashboard
          </button>
          <button
            className={`nav-tab ${selectedTab === 'progress' ? 'active' : ''}`}
            onClick={() => setSelectedTab('progress')}
          >
            Analysis
          </button>
          <button
            className={`nav-tab ${selectedTab === 'feedback' ? 'active' : ''}`}
            onClick={() => setSelectedTab('feedback')}
          >
            Feedback
          </button>
        </nav>
      </header>

      <main className="app-main">
        {selectedTab === 'upload' && <UploadForm />}

        {selectedTab === 'dashboard' && (
          <Dashboard
            onAnalyze={handleAnalyzePaper}
            onViewFeedback={handleViewFeedback}
          />
        )}

        {selectedTab === 'progress' && currentPaperId ? (
          <AnalysisProgress
            paperId={currentPaperId}
            onComplete={handleAnalysisComplete}
          />
        ) : selectedTab === 'progress' && (
          <p style={{ textAlign: 'center', padding: '2rem', color: '#888' }}>
            No paper selected. Go to the Dashboard and click "Start Analysis".
          </p>
        )}

        {selectedTab === 'feedback' && currentPaperId ? (
          <FeedbackDisplay paperId={currentPaperId} />
        ) : selectedTab === 'feedback' && (
          <p style={{ textAlign: 'center', padding: '2rem', color: '#888' }}>
            No paper selected. Go to the Dashboard and click "View Feedback" on a completed paper.
          </p>
        )}
      </main>

      <footer className="app-footer">
        <p>© 2024 Paper Review System | Powered by RAG + GPT-4</p>
      </footer>
    </div>
  );
}

export default App;
