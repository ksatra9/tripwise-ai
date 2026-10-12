import React, { useState } from 'react';
import { Clock, MapPin, Sun, Sunset, Moon, Utensils, Ticket } from 'lucide-react';
import { DailyItineraryPlan } from '../types/travel';

interface DayByDayPlanProps {
  plans: DailyItineraryPlan[];
}

export const DayByDayPlan: React.FC<DayByDayPlanProps> = ({ plans }) => {
  const [activeDay, setActiveDay] = useState<number>(1);

  if (!plans || plans.length === 0) return null;

  const currentPlan = plans.find((p) => p.day_number === activeDay) || plans[0];

  return (
    <div className="bg-white rounded-2xl border border-stone-200 card-shadow p-5 sm:p-6 mb-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-5 border-b border-stone-100">
        <div>
          <h4 className="text-xl font-bold text-slate-900">
            Day-by-Day Itinerary
          </h4>
          <p className="text-xs text-slate-500">
            Clustered geographically to minimize transit and avoid fatigue
          </p>
        </div>

        {/* Day Selector Tabs */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 sm:pb-0">
          {plans.map((p) => (
            <button
              key={p.day_number}
              onClick={() => setActiveDay(p.day_number)}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all shrink-0 ${
                activeDay === p.day_number
                  ? 'bg-teal-600 text-white shadow-sm shadow-teal-700/20'
                  : 'bg-stone-100 hover:bg-stone-200 text-slate-700'
              }`}
            >
              Day {p.day_number}
            </button>
          ))}
        </div>
      </div>

      {/* Active Day Detail */}
      <div className="mt-6">
        <div className="flex flex-wrap items-center justify-between gap-2 mb-6 bg-teal-50/50 p-3 rounded-xl border border-teal-100">
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold text-teal-800">
              {currentPlan.title}
            </span>
            <span className="text-slate-400">•</span>
            <span className="text-xs text-slate-600 flex items-center gap-1">
              <MapPin className="w-3.5 h-3.5 text-teal-600" />
              <span>Area Focus: {currentPlan.area_cluster}</span>
            </span>
          </div>
          <span className="text-xs font-bold font-mono text-slate-800">
            Est. Day Activities & Meals: ₹{currentPlan.estimated_day_cost_inr.toLocaleString()}
          </span>
        </div>

        {/* Timeline Slots */}
        <div className="space-y-4">
          
          {/* Morning Slot */}
          <div className="p-4 rounded-xl border border-stone-200 bg-stone-50/40 relative">
            <div className="flex items-center justify-between text-xs text-amber-700 font-semibold mb-1.5">
              <span className="flex items-center gap-1.5">
                <Sun className="w-4 h-4 text-amber-500" />
                <span>{currentPlan.morning.time_of_day}</span>
              </span>
              <span className="flex items-center gap-1 text-slate-500">
                <Clock className="w-3 h-3" />
                <span>{currentPlan.morning.est_duration_hours} hrs</span>
              </span>
            </div>
            <h5 className="text-base font-bold text-slate-900">
              {currentPlan.morning.activity_name}
            </h5>
            <p className="text-xs text-slate-600 mt-1 leading-relaxed">
              {currentPlan.morning.description}
            </p>
            <div className="mt-2.5 flex items-center gap-3 text-[11px] text-slate-500">
              <span className="inline-flex items-center gap-1 font-medium bg-white px-2 py-0.5 rounded border border-stone-200">
                <Ticket className="w-3 h-3 text-teal-600" />
                <span>Entry: {currentPlan.morning.entry_fee_inr > 0 ? `₹${currentPlan.morning.entry_fee_inr}/pax` : 'Free entry'}</span>
              </span>
              <span>Cluster: {currentPlan.morning.area_cluster}</span>
            </div>
          </div>

          {/* Lunch Break Card */}
          {currentPlan.lunch && (
            <div className="p-3 rounded-xl bg-amber-50/50 border border-amber-200/60 flex items-center justify-between gap-3 text-xs">
              <div className="flex items-center gap-2.5">
                <div className="p-2 bg-amber-100 rounded-lg text-amber-800">
                  <Utensils className="w-4 h-4" />
                </div>
                <div>
                  <span className="text-[10px] uppercase font-bold text-amber-800">Lunch Recommendation</span>
                  <div className="font-bold text-slate-900">{currentPlan.lunch.name}</div>
                  <div className="text-[11px] text-slate-500">{currentPlan.lunch.cuisine} • {currentPlan.lunch.location}</div>
                </div>
              </div>
              <div className="text-right shrink-0">
                <div className="font-mono font-bold text-slate-900">~₹{currentPlan.lunch.amount_inr}</div>
                <div className="text-[10px] text-slate-400">per person</div>
              </div>
            </div>
          )}

          {/* Afternoon Slot */}
          <div className="p-4 rounded-xl border border-stone-200 bg-stone-50/40 relative">
            <div className="flex items-center justify-between text-xs text-teal-700 font-semibold mb-1.5">
              <span className="flex items-center gap-1.5">
                <Sunset className="w-4 h-4 text-teal-600" />
                <span>{currentPlan.afternoon.time_of_day}</span>
              </span>
              <span className="flex items-center gap-1 text-slate-500">
                <Clock className="w-3 h-3" />
                <span>{currentPlan.afternoon.est_duration_hours} hrs</span>
              </span>
            </div>
            <h5 className="text-base font-bold text-slate-900">
              {currentPlan.afternoon.activity_name}
            </h5>
            <p className="text-xs text-slate-600 mt-1 leading-relaxed">
              {currentPlan.afternoon.description}
            </p>
            <div className="mt-2.5 flex items-center gap-3 text-[11px] text-slate-500">
              <span className="inline-flex items-center gap-1 font-medium bg-white px-2 py-0.5 rounded border border-stone-200">
                <Ticket className="w-3 h-3 text-teal-600" />
                <span>Entry: {currentPlan.afternoon.entry_fee_inr > 0 ? `₹${currentPlan.afternoon.entry_fee_inr}/pax` : 'Free entry'}</span>
              </span>
              <span>Cluster: {currentPlan.afternoon.area_cluster}</span>
            </div>
          </div>

          {/* Evening Slot */}
          <div className="p-4 rounded-xl border border-stone-200 bg-stone-50/40 relative">
            <div className="flex items-center justify-between text-xs text-indigo-700 font-semibold mb-1.5">
              <span className="flex items-center gap-1.5">
                <Moon className="w-4 h-4 text-indigo-500" />
                <span>{currentPlan.evening.time_of_day}</span>
              </span>
              <span className="flex items-center gap-1 text-slate-500">
                <Clock className="w-3 h-3" />
                <span>{currentPlan.evening.est_duration_hours} hrs</span>
              </span>
            </div>
            <h5 className="text-base font-bold text-slate-900">
              {currentPlan.evening.activity_name}
            </h5>
            <p className="text-xs text-slate-600 mt-1 leading-relaxed">
              {currentPlan.evening.description}
            </p>
          </div>

          {/* Dinner Break Card */}
          {currentPlan.dinner && (
            <div className="p-3 rounded-xl bg-amber-50/50 border border-amber-200/60 flex items-center justify-between gap-3 text-xs">
              <div className="flex items-center gap-2.5">
                <div className="p-2 bg-amber-100 rounded-lg text-amber-800">
                  <Utensils className="w-4 h-4" />
                </div>
                <div>
                  <span className="text-[10px] uppercase font-bold text-amber-800">Dinner Recommendation</span>
                  <div className="font-bold text-slate-900">{currentPlan.dinner.name}</div>
                  <div className="text-[11px] text-slate-500">{currentPlan.dinner.cuisine} • {currentPlan.dinner.location}</div>
                </div>
              </div>
              <div className="text-right shrink-0">
                <div className="font-mono font-bold text-slate-900">~₹{currentPlan.dinner.amount_inr}</div>
                <div className="text-[10px] text-slate-400">per person</div>
              </div>
            </div>
          )}

        </div>
      </div>
    </div>
  );
};
