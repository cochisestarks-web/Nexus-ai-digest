
import React from 'react';
import { DigestItem } from '../types';

interface DigestCardProps {
  item: DigestItem;
}

const DigestCard: React.FC<DigestCardProps> = ({ item }) => {
  const dateStr = new Date(item.timestamp).toLocaleDateString(undefined, {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });

  return (
    <div className="bg-zinc-900/50 border border-zinc-800 rounded-2xl p-8 mb-8 hover:border-zinc-700 transition-colors group">
      <div className="flex justify-between items-start mb-6">
        <div>
          <div className="text-indigo-400 text-xs font-mono mb-2">{dateStr}</div>
          <h3 className="text-2xl font-bold tracking-tight text-white group-hover:text-indigo-300 transition-colors">
            {item.title}
          </h3>
        </div>
        <div className="flex items-center space-x-2">
          <span className="text-xs text-zinc-500 font-mono">IMPACT</span>
          <div className={`px-3 py-1 rounded-full text-xs font-bold border ${
            item.impactScore >= 8 ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' : 
            item.impactScore >= 5 ? 'bg-orange-500/10 text-orange-400 border-orange-500/20' : 
            'bg-zinc-500/10 text-zinc-400 border-zinc-500/20'
          }`}>
            {item.impactScore}/10
          </div>
        </div>
      </div>

      <div className="prose prose-invert max-w-none">
        <p className="text-zinc-400 leading-relaxed text-lg mb-8">
          {item.summary}
        </p>

        <div className="grid md:grid-cols-2 gap-8 mb-8">
          <div className="bg-zinc-950/50 border border-zinc-800/50 rounded-xl p-6">
            <h4 className="text-sm font-semibold text-zinc-300 mb-4 flex items-center">
              <i className="fas fa-list-check mr-2 text-indigo-400"></i>
              Key Takeaways
            </h4>
            <ul className="space-y-3">
              {item.keyTakeaways.map((point, idx) => (
                <li key={idx} className="text-sm text-zinc-400 flex items-start">
                  <span className="text-indigo-500 mr-3">•</span>
                  {point}
                </li>
              ))}
            </ul>
          </div>

          <div className="bg-zinc-950/50 border border-zinc-800/50 rounded-xl p-6">
            <h4 className="text-sm font-semibold text-zinc-300 mb-4 flex items-center">
              <i className="fas fa-microchip mr-2 text-indigo-400"></i>
              Technical Analysis
            </h4>
            <div className="text-sm text-zinc-400 leading-relaxed mono whitespace-pre-line">
              {item.technicalAnalysis}
            </div>
          </div>
        </div>

        <div>
          <h4 className="text-xs font-semibold text-zinc-500 uppercase tracking-widest mb-4">
            Grounding Sources & Verifications
          </h4>
          <div className="flex flex-wrap gap-2">
            {item.sources.map((source, idx) => (
              <a
                key={idx}
                href={source.uri}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center px-3 py-1.5 rounded-lg bg-zinc-800 text-xs text-zinc-300 hover:bg-zinc-700 transition-colors border border-transparent hover:border-zinc-600"
              >
                <i className="fas fa-link mr-2 text-zinc-500"></i>
                {source.title.length > 40 ? source.title.substring(0, 40) + '...' : source.title}
              </a>
            ))}
            {item.sources.length === 0 && (
              <span className="text-xs text-zinc-600 italic">Self-synthesized via internal context</span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default DigestCard;
