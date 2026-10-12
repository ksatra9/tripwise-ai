import React, { useState } from 'react';
import { HelpCircle, ArrowRight } from 'lucide-react';
import { ExtractedTripPreferences } from '../types/travel';

interface ClarificationCardProps {
  question: string;
  preferences?: ExtractedTripPreferences | null;
  originalPrompt: string;
  onClarify: (supplementedPrompt: string) => void;
}

export const ClarificationCard: React.FC<ClarificationCardProps> = ({
  question,
  preferences,
  originalPrompt,
  onClarify
}) => {
  const [answer, setAnswer] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!answer.trim()) return;
    
    // Supplement original prompt with clear answer
    const updated = `${originalPrompt}. (Clarification: ${answer.trim()})`;
    onClarify(updated);
  };

  const handleQuickOption = (opt: string) => {
    const updated = `${originalPrompt}. (Clarification: ${opt})`;
    onClarify(updated);
  };

  const isBudgetScope = preferences?.missing_field === 'budget_scope' || question.toLowerCase().includes('per person');

  return (
    <div className="max-w-2xl mx-auto my-8 p-6 bg-amber-50/60 border border-amber-200/90 rounded-2xl shadow-sm">
      <div className="flex items-start gap-4">
        <div className="p-3 bg-amber-100 rounded-xl text-amber-800 shrink-0">
          <HelpCircle className="w-6 h-6" />
        </div>
        <div className="flex-1">
          <span className="text-xs font-bold uppercase tracking-wider text-amber-800">
            One quick detail needed
          </span>
          <h2 className="text-lg font-bold text-slate-900 mt-1">
            {question}
          </h2>
          <p className="text-xs text-slate-600 mt-1">
            We never guess starting cities, party size, or budget scope so your trip cost stays 100% honest.
          </p>

          {/* Quick choices if ambiguous budget scope */}
          {isBudgetScope && (
            <div className="flex flex-wrap gap-2 mt-4">
              <button
                type="button"
                onClick={() => handleQuickOption("This budget is the TOTAL for all travellers combined")}
                className="px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-amber-200/70 hover:bg-amber-200 text-amber-950 border border-amber-300 transition-colors"
              >
                Total for all travellers
              </button>
              <button
                type="button"
                onClick={() => handleQuickOption("This budget is PER PERSON")}
                className="px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-white hover:bg-stone-50 text-slate-800 border border-stone-300 transition-colors"
              >
                Per person
              </button>
            </div>
          )}

          {/* Response Form */}
          <form onSubmit={handleSubmit} className="mt-4 flex gap-2">
            <input
              type="text"
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              placeholder="Type your answer here..."
              className="flex-1 rounded-xl border border-amber-300 bg-white px-3.5 py-2.5 text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-amber-500"
              autoFocus
            />
            <button
              type="submit"
              disabled={!answer.trim()}
              className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-amber-600 hover:bg-amber-700 disabled:opacity-50 text-white text-sm font-semibold transition-colors"
            >
              <span>Continue</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </form>

          {/* Current extracted state preview */}
          {preferences && (
            <div className="mt-4 pt-3 border-t border-amber-200/60 flex flex-wrap gap-3 text-[11px] text-slate-500">
              {preferences.origin_city && <span>Origin: <strong className="text-slate-700">{preferences.origin_city}</strong></span>}
              {preferences.duration_days && <span>Duration: <strong className="text-slate-700">{preferences.duration_days} days</strong></span>}
              {preferences.travellers_count && <span>Travellers: <strong className="text-slate-700">{preferences.travellers_count} pax</strong></span>}
              {preferences.total_budget_inr && <span>Stated: <strong className="text-slate-700">₹{preferences.total_budget_inr.toLocaleString()}</strong></span>}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
