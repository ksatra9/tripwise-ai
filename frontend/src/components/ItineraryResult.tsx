import React from 'react';
import { MapPin, Sparkles, Compass, ShieldCheck } from 'lucide-react';
import { ItineraryCandidate } from '../types/travel';
import { CostBreakdownCard } from './CostBreakdownCard';
import { HotelCard } from './HotelCard';
import { RestaurantList } from './RestaurantList';
import { DayByDayPlan } from './DayByDayPlan';
import { AlternativesList } from './AlternativesList';
import { GlobalDisclaimerBanner } from './DataDisclaimerBadge';

interface ItineraryResultProps {
  candidate: ItineraryCandidate;
  alternatives: ItineraryCandidate[];
  aiExplanation?: string | null;
  travellers: number;
  days: number;
  onSelectAlternative: (alt: ItineraryCandidate) => void;
  onNewSearch?: () => void;
}

export const ItineraryResult: React.FC<ItineraryResultProps> = ({
  candidate,
  alternatives,
  aiExplanation,
  travellers,
  days,
  onSelectAlternative,
}) => {
  const { destination, cost_breakdown, recommended_hotel, hotel_rooms_count, hotel_nights_count } = candidate;

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in">
      
      {/* Top Banner & Destination Hero */}
      <div className="bg-gradient-to-br from-slate-900 via-slate-800 to-teal-950 text-white rounded-3xl p-6 sm:p-10 mb-8 shadow-xl relative overflow-hidden">
        
        {/* Subtle decorative background patterns */}
        <div className="absolute top-0 right-0 -mt-10 -mr-10 w-64 h-64 bg-teal-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute bottom-0 left-1/3 -mb-12 w-80 h-80 bg-amber-500/10 rounded-full blur-3xl pointer-events-none" />

        <div className="relative z-10">
          <div className="flex flex-wrap items-center justify-between gap-3 mb-4">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-teal-500/20 text-teal-300 border border-teal-400/30 text-xs font-semibold uppercase tracking-wider">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Recommended Match • {candidate.score.toFixed(0)}/100 Score</span>
            </div>

            <div className="flex items-center gap-2 text-xs text-slate-300">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              <span>Hard Affordability Verified</span>
            </div>
          </div>

          <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-6">
            <div>
              <h2 className="text-3xl sm:text-4xl md:text-5xl font-black tracking-tight text-white">
                {destination.name}
              </h2>
              <p className="text-base sm:text-lg text-teal-200/90 font-medium mt-1 flex items-center gap-2">
                <MapPin className="w-4 h-4" />
                <span>{destination.state}, {destination.region || "India"} • {days} Days ({hotel_nights_count} Nights) for {travellers} Traveller(s)</span>
              </p>
              <p className="text-sm text-slate-300 mt-3 max-w-2xl leading-relaxed">
                {destination.description}
              </p>
            </div>

            {/* Price Badge */}
            <div className="bg-white/10 backdrop-blur-md border border-white/20 p-4 rounded-2xl shrink-0 text-left lg:text-right">
              <div className="text-xs uppercase font-medium text-teal-300">Total Group Estimate</div>
              <div className="text-3xl font-black font-mono text-white mt-0.5">
                ₹{cost_breakdown.total_trip_cost_inr.toLocaleString()}
              </div>
              <div className="text-xs text-emerald-300 font-semibold mt-0.5">
                ₹{cost_breakdown.remaining_budget_inr.toLocaleString()} within ₹{cost_breakdown.budget_inr.toLocaleString()} budget
              </div>
            </div>
          </div>

          {/* Key match chips */}
          <div className="mt-6 pt-5 border-t border-white/10 flex flex-wrap gap-2">
            {candidate.match_reasons.map((reason, idx) => (
              <span
                key={idx}
                className="text-xs font-medium text-slate-200 bg-white/10 px-3 py-1 rounded-full border border-white/10"
              >
                ✓ {reason}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Grounded Natural Language Explanation */}
      {aiExplanation && (
        <div className="bg-white rounded-2xl border border-stone-200 card-shadow p-6 mb-8">
          <div className="flex items-center gap-2 mb-3">
            <div className="w-6 h-6 rounded-lg bg-teal-50 border border-teal-200/60 flex items-center justify-center text-teal-700">
              <Compass className="w-3.5 h-3.5" />
            </div>
            <h4 className="text-sm font-bold uppercase tracking-wider text-slate-800">
              Trip Overview & Financial Summary
            </h4>
          </div>
          <div className="text-sm text-slate-700 space-y-3 leading-relaxed whitespace-pre-line">
            {aiExplanation}
          </div>
        </div>
      )}

      {/* 1. Transparent Cost Breakdown */}
      <CostBreakdownCard
        cost={cost_breakdown}
        travellers={travellers}
        days={days}
        hotelRooms={hotel_rooms_count}
        hotelNights={hotel_nights_count}
      />

      {/* 2. Hotel Details */}
      <HotelCard
        hotel={recommended_hotel}
        roomsCount={hotel_rooms_count}
        nightsCount={hotel_nights_count}
        totalStayCost={cost_breakdown.hotel_stay_inr}
      />

      {/* 3. Day-by-Day Clustered Itinerary */}
      <DayByDayPlan plans={candidate.daily_plans} />

      {/* 4. Curated Dining Picks */}
      <RestaurantList restaurants={candidate.recommended_restaurants} />

      {/* 5. Alternative Affordable Options */}
      <AlternativesList
        alternatives={alternatives}
        onSelectAlternative={onSelectAlternative}
      />

      {/* 6. Honest Booking Disclaimer */}
      <GlobalDisclaimerBanner />

    </div>
  );
};
