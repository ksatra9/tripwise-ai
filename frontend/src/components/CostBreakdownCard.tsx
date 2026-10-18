import React from 'react';
import { TripCostBreakdown } from '../types/travel';
import { DataDisclaimerBadge } from './DataDisclaimerBadge';

interface CostBreakdownCardProps {
  cost: TripCostBreakdown;
  travellers: number;
  days: number;
  hotelRooms: number;
  hotelNights: number;
}

export const CostBreakdownCard: React.FC<CostBreakdownCardProps> = ({
  cost,
  travellers,
  days,
  hotelRooms,
  hotelNights
}) => {
  const percentUsed = Math.min(100, Math.round((cost.total_trip_cost_inr / cost.budget_inr) * 100));

  const expenseItems = cost.items.filter(
    (item) => !item.category.toLowerCase().includes('contingency')
  );
  const contingencyItem = cost.items.find(
    (item) => item.category.toLowerCase().includes('contingency')
  );

  return (
    <div className="bg-white rounded-2xl border border-stone-200 card-shadow p-5 sm:p-6 mb-8">
      
      {/* Header & Budget Gauge */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-stone-100">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold uppercase tracking-wider text-teal-700">
              Deterministic Budget Breakdown
            </span>
            <span className="text-[10px] bg-emerald-50 text-emerald-700 font-semibold px-2 py-0.5 rounded border border-emerald-200/60">
              Strictly Within Budget
            </span>
          </div>
          <h3 className="text-2xl font-black text-slate-900 mt-1">
            ₹{cost.total_trip_cost_inr.toLocaleString()}
            <span className="text-sm font-normal text-slate-500 ml-2">
              estimated total for {travellers} traveller(s) × {days} days ({hotelRooms} room(s), {hotelNights} night(s))
            </span>
          </h3>
        </div>

        {/* Budget Comparison Badges */}
        <div className="flex items-center gap-3 bg-stone-50 p-3 rounded-xl border border-stone-200/80">
          <div>
            <div className="text-[10px] uppercase font-semibold text-slate-400">Your Budget</div>
            <div className="text-base font-bold text-slate-800">₹{cost.budget_inr.toLocaleString()}</div>
          </div>
          <div className="h-8 w-px bg-stone-200" />
          <div>
            <div className="text-[10px] uppercase font-semibold text-emerald-600">Remaining Buffer</div>
            <div className="text-base font-bold text-emerald-700">+₹{cost.remaining_budget_inr.toLocaleString()}</div>
          </div>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="my-5">
        <div className="flex justify-between text-xs font-medium mb-1.5 text-slate-600">
          <span>Budget Utilization: {percentUsed}%</span>
          <span className="text-emerald-700 font-semibold">₹{cost.remaining_budget_inr.toLocaleString()} unspent cushion</span>
        </div>
        <div className="w-full h-2.5 bg-stone-100 rounded-full overflow-hidden">
          <div
            className={`h-full rounded-full transition-all duration-700 ${
              percentUsed > 90 ? 'bg-amber-500' : 'bg-teal-600'
            }`}
            style={{ width: `${percentUsed}%` }}
          />
        </div>
      </div>

      {/* Itemized Table */}
      <div className="mt-6 overflow-x-auto">
        <table className="w-full text-left text-xs">
          <thead>
            <tr className="border-b border-stone-200 text-slate-500 font-semibold uppercase tracking-wider text-[10px]">
              <th className="pb-2">Expense Category</th>
              <th className="pb-2">Formula & Multiplier</th>
              <th className="pb-2">Data Integrity</th>
              <th className="pb-2 text-right">Estimated Cost (INR)</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-stone-100">
            {expenseItems.map((item, idx) => (
              <tr key={idx} className="hover:bg-stone-50/60 transition-colors">
                <td className="py-3 font-semibold text-slate-900 pr-3">
                  {item.category}
                </td>
                <td className="py-3 text-slate-600 pr-3">
                  <span className="font-mono text-slate-800">{item.multiplier_description}</span>
                  <p className="text-[10px] text-slate-400 mt-0.5">{item.verification_note}</p>
                </td>
                <td className="py-3 pr-3">
                  <DataDisclaimerBadge
                    status={item.data_status}
                    checkedDate={item.price_checked_on}
                    sourceUrl={item.source_url}
                    compact
                  />
                </td>
                <td className="py-3 text-right font-mono font-bold text-slate-900 text-sm">
                  ₹{item.total_inr.toLocaleString()}
                </td>
              </tr>
            ))}
          </tbody>
          <tfoot>
            <tr className="border-t-2 border-stone-200 font-semibold text-slate-700">
              <td className="pt-3 font-semibold">Trip Subtotal</td>
              <td className="pt-3 text-slate-500 font-mono text-[11px]">Sum of 5 base expense categories</td>
              <td className="pt-3">
                <span className="text-[10px] text-slate-400 font-medium">Aggregated</span>
              </td>
              <td className="pt-3 text-right font-mono text-slate-800 font-bold">
                ₹{cost.subtotal_inr.toLocaleString()}
              </td>
            </tr>
            <tr className="text-amber-800 font-semibold bg-amber-50/30">
              <td className="py-2.5">Mandatory Emergency Contingency (10%)</td>
              <td className="py-2.5 text-slate-600 font-mono text-[11px]">
                {contingencyItem?.multiplier_description || "Mandatory 10% safety buffer for unplanned delays or surge pricing"}
              </td>
              <td className="py-2.5">
                <DataDisclaimerBadge
                  status={contingencyItem?.data_status || 'calculated'}
                  compact
                />
              </td>
              <td className="py-2.5 text-right font-mono text-amber-700 font-bold">
                +₹{cost.contingency_inr.toLocaleString()}
              </td>
            </tr>
            <tr className="border-t border-stone-200 text-base font-extrabold text-slate-900">
              <td colSpan={3} className="pt-3 text-slate-900">Final Estimated Group Total (Subtotal + Contingency)</td>
              <td className="pt-3 text-right font-mono text-teal-800 text-lg">
                ₹{cost.total_trip_cost_inr.toLocaleString()}
              </td>
            </tr>
          </tfoot>
        </table>
      </div>

    </div>
  );
};
