import React from 'react';
import { AlertCircle, Sliders, RefreshCcw } from 'lucide-react';

interface NoTripFoundProps {
  suggestions: string[];
  onModifySearch: () => void;
}

export const NoTripFound: React.FC<NoTripFoundProps> = ({
  suggestions,
  onModifySearch
}) => {
  return (
    <div className="max-w-2xl mx-auto my-10 p-6 sm:p-8 bg-white rounded-2xl border border-stone-200 card-shadow text-center">
      <div className="w-14 h-14 mx-auto mb-4 rounded-2xl bg-amber-50 border border-amber-200/80 flex items-center justify-center text-amber-600">
        <AlertCircle className="w-7 h-7" />
      </div>

      <h3 className="text-2xl font-bold text-slate-900">
        No Verified Trip Fits This Budget
      </h3>
      <p className="text-sm text-slate-600 mt-2 max-w-lg mx-auto leading-relaxed">
        We refuse to fabricate impossible rates or cut corners on your safety margin. After calculating round-trip transit, room capacity, meals, and local commuting, no complete itinerary meets your exact criteria.
      </p>

      {/* Suggested adjustments */}
      {suggestions && suggestions.length > 0 && (
        <div className="mt-6 text-left bg-amber-50/50 p-4 rounded-xl border border-amber-200/70">
          <span className="text-xs font-bold uppercase tracking-wider text-amber-900 flex items-center gap-1.5 mb-2">
            <Sliders className="w-3.5 h-3.5" />
            <span>Recommended Adjustments</span>
          </span>
          <ul className="space-y-2 text-xs text-slate-700">
            {suggestions.map((s, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-amber-700 font-bold shrink-0">•</span>
                <span className="leading-relaxed">{s}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Action button */}
      <div className="mt-6 flex justify-center">
        <button
          onClick={onModifySearch}
          className="inline-flex items-center gap-2 px-5 py-3 rounded-xl bg-teal-600 hover:bg-teal-700 text-white font-semibold text-sm shadow-md transition-colors"
        >
          <RefreshCcw className="w-4 h-4" />
          <span>Adjust Trip Criteria</span>
        </button>
      </div>
    </div>
  );
};
