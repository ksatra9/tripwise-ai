import React from 'react';
import { Info, Database } from 'lucide-react';
import { DataStatus } from '../types/travel';

interface DataDisclaimerBadgeProps {
  status: DataStatus;
  sourceUrl?: string | null;
  checkedDate?: string | null;
  compact?: boolean;
}

export const DataDisclaimerBadge: React.FC<DataDisclaimerBadgeProps> = ({
  status,
  sourceUrl,
  checkedDate,
  compact = false
}) => {
  let badgeLabel = "Demo Estimate";
  let badgeColor = "bg-amber-50 text-amber-800 border-amber-200";

  if (status === 'verified_snapshot') {
    badgeLabel = "Source Snapshot";
    badgeColor = "bg-emerald-50 text-emerald-800 border-emerald-200";
  } else if (status === 'historical') {
    badgeLabel = "Historical Data";
    badgeColor = "bg-blue-50 text-blue-800 border-blue-200";
  } else if (status === 'live_quote') {
    badgeLabel = "Live Quote";
    badgeColor = "bg-teal-50 text-teal-800 border-teal-200";
  } else if (status === 'calculated') {
    badgeLabel = "Calculated Reserve";
    badgeColor = "bg-purple-50 text-purple-800 border-purple-200";
  }

  if (compact) {
    return (
      <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-medium border ${badgeColor}`}>
        <Database className="w-2.5 h-2.5" />
        <span>{badgeLabel}</span>
      </span>
    );
  }

  return (
    <div className="flex flex-wrap items-center gap-2 text-xs text-slate-500 py-1">
      <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-md text-[11px] font-semibold border ${badgeColor}`}>
        <Database className="w-3 h-3" />
        <span>{badgeLabel}</span>
      </span>
      <span>•</span>
      <span>
        {checkedDate ? `Estimate checked: ${checkedDate}` : "Source/date not verified"}
      </span>
      {sourceUrl && (
        <>
          <span>•</span>
          <a
            href={sourceUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="text-teal-700 hover:underline"
          >
            Source
          </a>
        </>
      )}
    </div>
  );
};

export const GlobalDisclaimerBanner: React.FC = () => {
  return (
    <div className="my-6 p-4 rounded-xl bg-stone-100 border border-stone-200/90 text-xs text-slate-600 flex items-start gap-3">
      <Info className="w-4 h-4 text-slate-500 shrink-0 mt-0.5" />
      <div>
        <p className="font-semibold text-slate-800">
          Estimated prices; confirm before booking
        </p>
        <p className="mt-0.5 leading-relaxed">
          Hotel room rates, restaurant bills, and transport costs reflect cleaned sample estimates and historical Kaggle snapshots—not live bookable quotes. All math reflects integer INR calculations for the full party and duration.
        </p>
      </div>
    </div>
  );
};
