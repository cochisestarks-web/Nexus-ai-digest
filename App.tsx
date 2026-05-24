
import React, { useState, useEffect, useCallback, useRef } from 'react';
import Sidebar from './components/Sidebar';
import DigestCard from './components/DigestCard';
import { PipelineState, TechnicalProfile, DigestItem } from './types';
import { DEFAULT_PROFILE, APP_STORAGE_KEY } from './constants';
import { GeminiService } from './services/geminiService';

const App: React.FC = () => {
  const [state, setState] = useState<PipelineState>(() => {
    const saved = localStorage.getItem(APP_STORAGE_KEY);
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        return { ...parsed, isProcessing: false };
      } catch (e) {
        console.error("Failed to load state", e);
      }
    }
    return {
      isProcessing: false,
      lastRun: null,
      history: [],
      profile: DEFAULT_PROFILE,
    };
  });

  const geminiRef = useRef<GeminiService | null>(null);

  useEffect(() => {
    localStorage.setItem(APP_STORAGE_KEY, JSON.stringify(state));
  }, [state]);

  const runPipeline = useCallback(async () => {
    if (state.isProcessing) return;

    if (!geminiRef.current) {
      geminiRef.current = new GeminiService();
    }

    setState(prev => ({ ...prev, isProcessing: true }));

    try {
      const previousTitles = state.history.slice(0, 5).map(h => h.title);
      const newDigest = await geminiRef.current.generateDigest(state.profile, previousTitles);
      
      setState(prev => ({
        ...prev,
        isProcessing: false,
        lastRun: Date.now(),
        history: [newDigest, ...prev.history].slice(0, 50), // Keep last 50
      }));
    } catch (error) {
      console.error("Pipeline failed", error);
      alert("Failed to synthesize intelligence. Check console for details.");
      setState(prev => ({ ...prev, isProcessing: false }));
    }
  }, [state.isProcessing, state.profile, state.history]);

  const updateProfile = (profile: TechnicalProfile) => {
    setState(prev => ({ ...prev, profile }));
  };

  return (
    <div className="flex h-screen w-full bg-[#09090b] text-zinc-100 overflow-hidden">
      <Sidebar 
        profile={state.profile} 
        setProfile={updateProfile} 
        onRefresh={runPipeline}
        isProcessing={state.isProcessing}
      />
      
      <main className="flex-1 flex flex-col min-w-0">
        <header className="h-16 border-b border-zinc-800 flex items-center justify-between px-8 bg-zinc-950/50 backdrop-blur-md sticky top-0 z-10">
          <div className="flex items-center space-x-4">
            <span className="text-xs font-mono text-zinc-500 uppercase tracking-widest">Pipeline Status</span>
            <div className="flex items-center">
              <div className={`w-2 h-2 rounded-full mr-2 ${state.isProcessing ? 'bg-amber-500 animate-pulse' : 'bg-emerald-500'}`}></div>
              <span className="text-xs font-medium">{state.isProcessing ? 'Processing Streams' : 'Standby'}</span>
            </div>
          </div>
          <div className="flex items-center space-x-6 text-xs text-zinc-500">
            {state.lastRun && (
              <span>Last Run: {new Date(state.lastRun).toLocaleTimeString()}</span>
            )}
            <div className="px-3 py-1 bg-zinc-900 border border-zinc-800 rounded text-zinc-400">
              v2.4 Autonomous
            </div>
          </div>
        </header>

        <div className="flex-1 overflow-y-auto custom-scrollbar p-8 lg:p-12">
          <div className="max-w-4xl mx-auto">
            {state.history.length === 0 && !state.isProcessing && (
              <div className="h-[60vh] flex flex-col items-center justify-center text-center space-y-6">
                <div className="w-20 h-20 bg-zinc-900 rounded-3xl flex items-center justify-center border border-zinc-800 text-zinc-700">
                  <i className="fas fa-brain text-4xl"></i>
                </div>
                <div className="space-y-2">
                  <h2 className="text-2xl font-bold">Neural Engine Idle</h2>
                  <p className="text-zinc-500 max-w-sm">
                    Initiate the pipeline to transform the daily stream of AI news into high-density intelligence tailored to your profile.
                  </p>
                </div>
                <button
                  onClick={runPipeline}
                  className="px-8 py-3 bg-white text-black rounded-full font-bold hover:bg-zinc-200 transition-colors"
                >
                  Initiate First Run
                </button>
              </div>
            )}

            {state.isProcessing && state.history.length === 0 && (
              <div className="space-y-8 animate-pulse">
                <div className="h-64 bg-zinc-900/50 rounded-2xl border border-zinc-800"></div>
                <div className="h-64 bg-zinc-900/50 rounded-2xl border border-zinc-800 opacity-50"></div>
              </div>
            )}

            {state.history.map((digest) => (
              <DigestCard key={digest.id} item={digest} />
            ))}
          </div>
        </div>
      </main>
    </div>
  );
};

export default App;
