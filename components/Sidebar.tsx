
import React from 'react';
import { TechnicalDepth, TechnicalProfile } from '../types';
import { CATEGORIES } from '../constants';

interface SidebarProps {
  profile: TechnicalProfile;
  setProfile: (p: TechnicalProfile) => void;
  onRefresh: () => void;
  isProcessing: boolean;
}

const Sidebar: React.FC<SidebarProps> = ({ profile, setProfile, onRefresh, isProcessing }) => {
  const toggleArea = (area: string) => {
    const newAreas = profile.focusAreas.includes(area)
      ? profile.focusAreas.filter(a => a !== area)
      : [...profile.focusAreas, area];
    setProfile({ ...profile, focusAreas: newAreas });
  };

  return (
    <div className="w-80 h-full border-r border-zinc-800 bg-zinc-950 flex flex-col p-6 space-y-8 overflow-y-auto shrink-0">
      <div className="flex items-center space-x-3 mb-4">
        <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center">
          <i className="fas fa-bolt text-white"></i>
        </div>
        <h1 className="text-xl font-bold tracking-tight">NEXUS AI</h1>
      </div>

      <section className="space-y-4">
        <h2 className="text-xs font-semibold text-zinc-500 uppercase tracking-widest">Technical Depth</h2>
        <div className="grid grid-cols-1 gap-2">
          {Object.values(TechnicalDepth).map((depth) => (
            <button
              key={depth}
              onClick={() => setProfile({ ...profile, depth })}
              className={`text-sm px-4 py-2.5 rounded-lg text-left transition-all duration-200 border ${
                profile.depth === depth 
                  ? 'bg-indigo-600/10 border-indigo-500 text-indigo-400' 
                  : 'bg-zinc-900 border-zinc-800 text-zinc-400 hover:border-zinc-700'
              }`}
            >
              {depth}
            </button>
          ))}
        </div>
      </section>

      <section className="space-y-4">
        <h2 className="text-xs font-semibold text-zinc-500 uppercase tracking-widest">Focus Vectors</h2>
        <div className="flex flex-wrap gap-2">
          {CATEGORIES.map((area) => (
            <button
              key={area}
              onClick={() => toggleArea(area)}
              className={`text-xs px-3 py-1.5 rounded-full border transition-all ${
                profile.focusAreas.includes(area)
                  ? 'bg-zinc-100 text-zinc-900 border-zinc-100'
                  : 'bg-zinc-900 text-zinc-400 border-zinc-800 hover:border-zinc-700'
              }`}
            >
              {area}
            </button>
          ))}
        </div>
      </section>

      <section className="space-y-4">
        <h2 className="text-xs font-semibold text-zinc-500 uppercase tracking-widest">Schedule</h2>
        <select 
          value={profile.digestInterval}
          onChange={(e) => setProfile({...profile, digestInterval: e.target.value as any})}
          className="w-full bg-zinc-900 border border-zinc-800 text-sm rounded-lg p-2.5 outline-none focus:border-indigo-500"
        >
          <option value="4h">Every 4 Hours</option>
          <option value="12h">Every 12 Hours</option>
          <option value="24h">Daily (24h)</option>
        </select>
      </section>

      <div className="pt-6 mt-auto border-t border-zinc-800">
        <button
          onClick={onRefresh}
          disabled={isProcessing}
          className={`w-full flex items-center justify-center space-x-2 py-3 rounded-lg font-medium transition-all ${
            isProcessing 
              ? 'bg-zinc-800 text-zinc-500 cursor-not-allowed' 
              : 'bg-white text-black hover:bg-zinc-200'
          }`}
        >
          {isProcessing ? (
            <i className="fas fa-circle-notch fa-spin"></i>
          ) : (
            <i className="fas fa-sync"></i>
          )}
          <span>{isProcessing ? 'Synthesizing...' : 'Run Pipeline'}</span>
        </button>
        <p className="text-[10px] text-center text-zinc-600 mt-4 leading-relaxed">
          Powered by Gemini 3 Pro & Google Search Grounding.
          Deduplication active.
        </p>
      </div>
    </div>
  );
};

export default Sidebar;
