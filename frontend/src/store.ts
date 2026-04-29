// React Zustand store for state management

import { create } from 'zustand';

interface Paper {
  id: number;
  filename: string;
  title?: string;
  upload_date: string;
  processing_status: string;
}

interface AnalysisState {
  scores?: {
    structure_score: number;
    clarity_score: number;
    methodology_score: number;
    completeness_score: number;
  };
  processing: boolean;
  error?: string;
}

interface AppStore {
  // Papers
  papers: Paper[];
  currentPaper: Paper | null;
  setPapers: (papers: Paper[]) => void;
  setCurrentPaper: (paper: Paper | null) => void;
  addPaper: (paper: Paper) => void;
  
  // Analysis
  analysisState: AnalysisState;
  setAnalysisState: (state: AnalysisState) => void;
  setAnalysisProcessing: (processing: boolean) => void;
  setAnalysisError: (error?: string) => void;
  
  // UI
  selectedTab: string;
  setSelectedTab: (tab: string) => void;
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
}

export const useAppStore = create<AppStore>((set) => ({
  // Papers
  papers: [],
  currentPaper: null,
  setPapers: (papers) => set({ papers }),
  setCurrentPaper: (paper) => set({ currentPaper: paper }),
  addPaper: (paper) => set((state) => ({ papers: [paper, ...state.papers] })),
  
  // Analysis
  analysisState: { processing: false },
  setAnalysisState: (state) => set({ analysisState: state }),
  setAnalysisProcessing: (processing) => 
    set((state) => ({ analysisState: { ...state.analysisState, processing } })),
  setAnalysisError: (error) => 
    set((state) => ({ analysisState: { ...state.analysisState, error } })),
  
  // UI
  selectedTab: 'upload',
  setSelectedTab: (tab) => set({ selectedTab: tab }),
  isLoading: false,
  setIsLoading: (loading) => set({ isLoading: loading }),
}));
