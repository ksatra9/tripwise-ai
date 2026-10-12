import React from 'react';
import { ArrowUpRight, MapPin } from 'lucide-react';
import { ItineraryCandidate } from '../types/travel';

interface AlternativesListProps {
  alternatives: ItineraryCandidate[];
  onSelectAlternative: (candidate: ItineraryCandidate) => void;
}

export const AlternativesList: React.FC<AlternativesListProps> = ({
  alternatives,
  onSelectAlternative
}) => {
  if (!alternatives || alternatives.length === 0) return null;

  return (
    <div className="mb-10">
      <div className="mb-4">
        <h4 className="text-xl font-bold text-slate-900">
          Alternative Affordable Destinations
        </h4>
        <p className="text-xs text-slate-500">
          Also strictly within your budget with verified routes and accommodation
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {alternatives.map((alt) => (
          <div
            key={alt.destination.id}
            className="bg-white rounded-2xl border border-stone-200 card-shadow p-5 flex flex-col justify-between card-hover group"
          >
            <div>
              <div className="flex items-start justify-between gap-3">
                <div>
                  <span className="text-[10px] font-bold uppercase tracking-wider text-teal-700 bg-teal-50 px-2 py-0.5 rounded border border-teal-200/60">
                    Score: {alt.score.toFixed(0)}/100
                  </span>
                  <h5 className="text-lg font-bold text-slate-900 mt-1 group-hover:text-teal-700 transition-colors">
                    {alt.destination.name}, {alt.destination.state}
                  </h5>
                  <p className="text-xs text-slate-500 flex items-center gap-1 mt-0.5">
                    <MapPin className="w-3.5 h-3.5 text-slate-400" />
                    <span>Via {alt.transport_option.mode}</span>
                  </p>
                </div>

                <div className="text-right">
                  <div className="text-base font-extrabold font-mono text-slate-900">
                    ₹{alt.cost_breakdown.total_trip_cost_inr.toLocaleString()}
                  </div>
                  <div className="text-[10px] text-emerald-600 font-semibold">
                    +₹{alt.cost_breakdown.remaining_budget_inr.toLocaleString()} headroom
                  </div>
                </div>
              </div>

              <p className="text-xs text-slate-600 mt-3 line-clamp-2 leading-relaxed">
                {alt.destination.description}
              </p>

              {/* Match reasons */}
              <div className="mt-3 flex flex-wrap gap-1.5">
                {alt.match_reasons.slice(0, 2).map((reason, idx) => (
                  <span
                    key={idx}
                    className="text-[10px] font-medium text-slate-600 bg-stone-100 px-2 py-0.5 rounded"
                  >
                    • {reason}
                  </span>
                ))}
              </div>
            </div>

            <div className="mt-4 pt-3 border-t border-stone-100 flex items-center justify-between">
              <span className="text-xs text-slate-500">
                Hotel: {alt.recommended_hotel.name}
              </span>
              <button
                type="button"
                onClick={() => onSelectAlternative(alt)}
                className="inline-flex items-center gap-1 text-xs font-semibold text-teal-700 hover:text-teal-800"
              >
                <span>View Full Plan</span>
                <ArrowUpRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
