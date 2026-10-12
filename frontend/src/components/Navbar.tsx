import React from 'react';
import { Compass, RefreshCw, ShieldCheck } from 'lucide-react';

interface NavbarProps {
  brandName?: string;
  onReset?: () => void;
  showReset?: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({
  brandName = "TripWise AI",
  onReset,
  showReset = false
}) => {
  return (
    <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-stone-200/80 transition-all">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Brand & Logo */}
        <div 
          onClick={onReset}
          className="flex items-center gap-3 cursor-pointer group"
          role="button"
          tabIndex={0}
          aria-label="TripWise Home"
        >
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-teal-700 to-teal-500 flex items-center justify-center text-white shadow-sm shadow-teal-700/20 group-hover:scale-105 transition-transform">
            <Compass className="w-5 h-5 animate-pulse" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl font-bold tracking-tight text-slate-900 group-hover:text-teal-700 transition-colors">
                {brandName}
              </span>
              <span className="text-[10px] uppercase tracking-wider font-semibold bg-teal-50 text-teal-700 px-2 py-0.5 rounded-full border border-teal-200/60">
                India Engine
              </span>
            </div>
            <p className="text-xs text-slate-500 hidden sm:block">
              Budget-honest itinerary recommendations
            </p>
          </div>
        </div>

        {/* Right Nav Utilities */}
        <div className="flex items-center gap-3">
          <div className="hidden md:flex items-center gap-1.5 text-xs text-slate-600 bg-stone-100/80 px-3 py-1.5 rounded-lg border border-stone-200/60">
            <ShieldCheck className="w-4 h-4 text-teal-600" />
            <span>Zero Hallucinated Rates</span>
          </div>

          {showReset && (
            <button
              onClick={onReset}
              className="flex items-center gap-1.5 text-xs font-medium text-slate-700 hover:text-teal-700 bg-stone-100 hover:bg-stone-200 px-3 py-1.5 rounded-lg transition-colors border border-stone-200"
              title="Start a new trip search"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              <span>New Search</span>
            </button>
          )}
        </div>

      </div>
    </header>
  );
};
