import React, { useState } from 'react';
import { Sparkles, MapPin, Users, Calendar, Wallet, Compass } from 'lucide-react';

interface HeroSearchProps {
  onSubmit: (prompt: string) => void;
  isLoading: boolean;
  initialPrompt?: string;
}

const EXAMPLE_PROMPTS = [
  {
    title: "Weekend Nature & Food",
    text: "I am travelling from Delhi with one friend for 3 days. Our total budget is ₹20,000. We like nature and local food.",
    tags: ["Delhi origin", "2 pax", "₹20k budget", "3 days"]
  },
  {
    title: "Heritage & Royal Culture",
    text: "I am travelling from Delhi with 2 friends for 3 days. Our total budget is ₹25,000. We love historic palaces, forts, and Rajasthani cuisine.",
    tags: ["Delhi origin", "3 pax", "₹25k budget", "Heritage"]
  },
  {
    title: "Solo Coastal Escape",
    text: "Solo trip from Mumbai for 4 days. Total budget is ₹18,000. I want beaches, seafood, and relaxed sunset cafes.",
    tags: ["Mumbai origin", "Solo", "₹18k budget", "Beaches"]
  },
  {
    title: "South Indian Cultural Odyssey",
    text: "Family of 4 travelling from Bangalore for 3 days. Total budget is ₹35,000. We want heritage, temples, and coastal backwaters.",
    tags: ["Bangalore origin", "4 pax", "₹35k budget", "Family"]
  }
];

export const HeroSearch: React.FC<HeroSearchProps> = ({
  onSubmit,
  isLoading,
  initialPrompt = ""
}) => {
  const [prompt, setPrompt] = useState(initialPrompt || EXAMPLE_PROMPTS[0].text);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim() || isLoading) return;
    onSubmit(prompt.trim());
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      handleSubmit(e);
    }
  };

  return (
    <section className="relative pt-8 pb-14 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto">
      {/* Hero Header */}
      <div className="text-center max-w-3xl mx-auto mb-8">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-teal-50 border border-teal-200/70 text-teal-800 text-xs font-semibold uppercase tracking-wider mb-4 shadow-sm">
          <Sparkles className="w-3.5 h-3.5 text-teal-600" />
          <span>India-Wide Honest Travel Intelligence</span>
        </div>
        <h1 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-slate-900 tracking-tight leading-tight">
          Describe your dream trip. <br className="hidden sm:inline" />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-teal-700 via-teal-600 to-amber-600">
            We guarantee it fits your budget.
          </span>
        </h1>
        <p className="mt-4 text-base sm:text-lg text-slate-600 leading-relaxed max-w-2xl mx-auto">
          One free-text box. No hidden markups. We calculate round-trip transport, hotel rooms, dining, entry tickets, and a 10% contingency strictly within your total budget.
        </p>
      </div>

      {/* Main Form Card */}
      <div className="bg-white rounded-2xl border border-stone-200 card-shadow p-4 sm:p-6 transition-all">
        <form onSubmit={handleSubmit}>
          <div className="relative">
            <label htmlFor="trip-prompt" className="sr-only">
              Trip Description
            </label>
            <textarea
              id="trip-prompt"
              rows={4}
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={isLoading}
              placeholder="e.g. I am travelling from Delhi with one friend for 3 days. Our total budget is ₹20,000. We like nature and local food..."
              className="w-full rounded-xl border border-stone-200 bg-stone-50/50 p-4 text-slate-900 text-base placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-teal-600 focus:border-teal-600 focus:bg-white resize-y transition-all disabled:opacity-60"
            />
          </div>

          {/* Action Row */}
          <div className="mt-4 flex flex-col sm:flex-row items-center justify-between gap-3 pt-2">
            <div className="flex flex-wrap items-center gap-3 text-xs text-slate-500 w-full sm:w-auto">
              <span className="flex items-center gap-1 font-medium">
                <MapPin className="w-3.5 h-3.5 text-teal-600" /> Origin City
              </span>
              <span className="flex items-center gap-1 font-medium">
                <Users className="w-3.5 h-3.5 text-teal-600" /> Travellers
              </span>
              <span className="flex items-center gap-1 font-medium">
                <Calendar className="w-3.5 h-3.5 text-teal-600" /> Days
              </span>
              <span className="flex items-center gap-1 font-medium">
                <Wallet className="w-3.5 h-3.5 text-teal-600" /> Total Budget
              </span>
            </div>

            <button
              type="submit"
              disabled={isLoading || !prompt.trim()}
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl bg-teal-600 hover:bg-teal-700 active:bg-teal-800 text-white font-semibold text-sm shadow-md shadow-teal-700/20 hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed group"
            >
              <Compass className={`w-4 h-4 ${isLoading ? 'animate-spin' : 'group-hover:rotate-45 transition-transform'}`} />
              <span>{isLoading ? 'Calculating Trip...' : 'Plan My Trip'}</span>
            </button>
          </div>
        </form>

        {/* Suggestion Chips */}
        <div className="mt-6 pt-5 border-t border-stone-100">
          <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3">
            Or try one of these example trips:
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
            {EXAMPLE_PROMPTS.map((ex, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => setPrompt(ex.text)}
                className="text-left p-3 rounded-xl border border-stone-200/80 hover:border-teal-300 hover:bg-teal-50/40 transition-all group"
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-800 group-hover:text-teal-800">
                    {ex.title}
                  </span>
                  <span className="text-[10px] text-teal-600 opacity-0 group-hover:opacity-100 transition-opacity">
                    Use prompt →
                  </span>
                </div>
                <p className="text-xs text-slate-500 line-clamp-1 mt-1">
                  {ex.text}
                </p>
              </button>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};
