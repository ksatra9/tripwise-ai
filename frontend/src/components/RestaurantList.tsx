import React from 'react';
import { Utensils, Star, MapPin } from 'lucide-react';
import { Restaurant } from '../types/travel';
import { DataDisclaimerBadge } from './DataDisclaimerBadge';

interface RestaurantListProps {
  restaurants: Restaurant[];
}

export const RestaurantList: React.FC<RestaurantListProps> = ({ restaurants }) => {
  if (!restaurants || restaurants.length === 0) return null;

  return (
    <div className="mb-8">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h4 className="text-lg font-bold text-slate-900">
            Curated Local Dining Picks
          </h4>
          <p className="text-xs text-slate-500">
            Authentic culinary spots matched with regional specialties
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {restaurants.map((rest) => (
          <div
            key={rest.id}
            className="bg-white rounded-xl border border-stone-200 card-shadow p-4 flex flex-col justify-between card-hover"
          >
            <div>
              <div className="flex items-start justify-between gap-2">
                <div>
                  <span className="text-[10px] font-bold uppercase tracking-wider text-teal-700 bg-teal-50 px-2 py-0.5 rounded border border-teal-200/60">
                    {rest.price_band} Dining
                  </span>
                  <h5 className="text-base font-bold text-slate-900 mt-1">
                    {rest.name}
                  </h5>
                  <p className="text-xs text-slate-500 flex items-center gap-1 mt-0.5">
                    <MapPin className="w-3 h-3 text-slate-400" />
                    <span>{rest.location || rest.city}</span>
                  </p>
                </div>

                <div className="text-right">
                  <div className="text-sm font-bold font-mono text-slate-900">
                    ~₹{rest.amount_inr}
                  </div>
                  <div className="text-[10px] text-slate-400">per person / meal</div>
                </div>
              </div>

              {rest.famous_dish && (
                <div className="mt-3 p-2 rounded-lg bg-stone-50 border border-stone-200/60 text-xs text-slate-700 flex items-start gap-1.5">
                  <Utensils className="w-3.5 h-3.5 text-amber-600 shrink-0 mt-0.5" />
                  <div>
                    <span className="font-semibold text-slate-800">Must Try: </span>
                    <span>{rest.famous_dish}</span>
                  </div>
                </div>
              )}
            </div>

            <div className="mt-3 pt-2.5 border-t border-stone-100 flex items-center justify-between">
              <span className="text-xs text-amber-700 font-semibold flex items-center gap-1">
                <Star className="w-3 h-3 fill-amber-400 text-amber-400" />
                <span>{rest.rating.toFixed(1)} rating</span>
              </span>
              <DataDisclaimerBadge
                status={rest.data_status}
                checkedDate={rest.price_checked_on}
                compact
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
