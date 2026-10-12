import React, { useEffect, useState } from 'react';
import { Compass, CheckCircle2, CircleDashed } from 'lucide-react';

const STEPS = [
  "Parsing destination intent & party requirements...",
  "Querying verified transport routes from your origin...",
  "Applying room capacity ceiling formula & hotel rates...",
  "Enforcing hard budget filter & 10% contingency buffer...",
  "Assembling day-by-day itinerary & local dining picks..."
];

export const LoadingState: React.FC = () => {
  const [currentStepIndex, setCurrentStepIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentStepIndex((prev) => (prev < STEPS.length - 1 ? prev + 1 : prev));
    }, 700);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="max-w-xl mx-auto my-12 p-8 bg-white rounded-2xl border border-stone-200 card-shadow text-center">
      <div className="w-14 h-14 mx-auto mb-5 rounded-2xl bg-teal-50 border border-teal-200/80 flex items-center justify-center text-teal-600">
        <Compass className="w-7 h-7 animate-spin text-teal-600" />
      </div>

      <h3 className="text-lg font-bold text-slate-900">
        Calculating Your Affordable Itinerary
      </h3>
      <p className="text-xs text-slate-500 mt-1 mb-6">
        Calculating costs in integer INR. LLM never invents prices or hotels.
      </p>

      {/* Steps List */}
      <div className="space-y-3 text-left max-w-md mx-auto">
        {STEPS.map((step, idx) => {
          const isDone = idx < currentStepIndex;
          const isCurrent = idx === currentStepIndex;

          return (
            <div
              key={idx}
              className={`flex items-center gap-3 p-2.5 rounded-xl text-xs transition-all ${
                isCurrent
                  ? 'bg-teal-50/80 text-teal-900 font-semibold border border-teal-200/60'
                  : isDone
                  ? 'text-slate-600 opacity-90'
                  : 'text-slate-400 opacity-50'
              }`}
            >
              {isDone ? (
                <CheckCircle2 className="w-4 h-4 text-teal-600 shrink-0" />
              ) : isCurrent ? (
                <CircleDashed className="w-4 h-4 text-teal-600 animate-spin shrink-0" />
              ) : (
                <div className="w-4 h-4 rounded-full border border-slate-300 shrink-0" />
              )}
              <span>{step}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
