import React from 'react';
import { Star, MapPin, Check } from 'lucide-react';
import { Hotel } from '../types/travel';
import { DataDisclaimerBadge } from './DataDisclaimerBadge';

interface HotelCardProps {
  hotel: Hotel;
  roomsCount: number;
  nightsCount: number;
  totalStayCost: number;
}

export const HotelCard: React.FC<HotelCardProps> = ({
  hotel,
  roomsCount,
  nightsCount,
  totalStayCost
}) => {
  const amenitiesList = hotel.amenities
    ? hotel.amenities.split(',').map((a) => a.trim()).filter(Boolean)
    : ["Free Wi-Fi", "Ensuite Bath", "AC Room"];

  return (
    <div className="bg-white rounded-2xl border border-stone-200 card-shadow p-5 mb-8">
      <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4 pb-4 border-b border-stone-100">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[10px] font-bold uppercase tracking-wider text-teal-700 bg-teal-50 px-2 py-0.5 rounded border border-teal-200/60">
              Recommended Stay
            </span>
            <span className="text-xs text-amber-700 font-semibold flex items-center gap-0.5">
              <Star className="w-3.5 h-3.5 fill-amber-400 text-amber-400" />
              <span>{hotel.rating.toFixed(1)}</span>
            </span>
            <span className="text-xs text-slate-400">({hotel.stars})</span>
          </div>

          <h4 className="text-lg font-bold text-slate-900">
            {hotel.name}
          </h4>
          <p className="text-xs text-slate-500 flex items-center gap-1 mt-0.5">
            <MapPin className="w-3.5 h-3.5 text-slate-400" />
            <span>{hotel.city} • Tier: {hotel.tier}</span>
          </p>
        </div>

        {/* Stay Math Box */}
        <div className="bg-stone-50 p-3 rounded-xl border border-stone-200/80 text-right sm:min-w-[190px]">
          <div className="text-xs text-slate-500">
            ₹{hotel.amount_inr.toLocaleString()} / room / night
          </div>
          <div className="text-base font-extrabold text-slate-900 mt-0.5 font-mono">
            ₹{totalStayCost.toLocaleString()} total
          </div>
          <div className="text-[10px] text-slate-500 mt-0.5">
            {roomsCount} room(s) × {nightsCount} night(s)
          </div>
        </div>
      </div>

      {/* Amenities Chips */}
      <div className="mt-4 flex flex-wrap gap-1.5">
        {amenitiesList.slice(0, 5).map((amenity, idx) => (
          <span
            key={idx}
            className="inline-flex items-center gap-1 text-[11px] font-medium text-slate-600 bg-stone-100 px-2.5 py-1 rounded-lg"
          >
            <Check className="w-3 h-3 text-teal-600" />
            <span>{amenity}</span>
          </span>
        ))}
      </div>

      {/* Honesty Note */}
      <div className="mt-4 pt-3 border-t border-stone-100 flex flex-wrap items-center justify-between gap-2">
        <DataDisclaimerBadge
          status={hotel.data_status}
          checkedDate={hotel.price_checked_on}
          sourceUrl={hotel.source_url}
        />
        {hotel.is_sample_entry && (
          <span className="text-[11px] text-amber-800 bg-amber-50 px-2 py-0.5 rounded border border-amber-200/60 font-medium">
            Demo data — illustrative estimates, not verified listings or bookable prices
          </span>
        )}
      </div>
    </div>
  );
};
