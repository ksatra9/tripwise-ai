import React, { useState } from 'react';
import { Navbar } from './components/Navbar';
import { HeroSearch } from './components/HeroSearch';
import { ClarificationCard } from './components/ClarificationCard';
import { LoadingState } from './components/LoadingState';
import { ItineraryResult } from './components/ItineraryResult';
import { NoTripFound } from './components/NoTripFound';
import { planTrip } from './services/api';
import { PlanResponse, ItineraryCandidate } from './types/travel';
import { AlertTriangle } from 'lucide-react';

export const App: React.FC = () => {
  const [prompt, setPrompt] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [planResult, setPlanResult] = useState<PlanResponse | null>(null);
  const [activeCandidate, setActiveCandidate] = useState<ItineraryCandidate | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const handlePlanSubmit = async (searchQuery: string) => {
    setIsLoading(true);
    setErrorMsg(null);
    setPrompt(searchQuery);

    try {
      const result = await planTrip(searchQuery);
      if (result.status === 'error') {
        setErrorMsg(
          result.budget_adjustment_suggestions?.join(' ') ||
          'Unable to communicate with the planning engine.'
        );
        setPlanResult(null);
        return;
      }
      setPlanResult(result);
      if (result.status === 'success' && result.recommended_trip) {
        setActiveCandidate(result.recommended_trip);
      } else {
        setActiveCandidate(null);
      }
    } catch (err: any) {
      setErrorMsg(err.message || 'An unexpected error occurred while communicating with the planning engine.');
      setPlanResult(null);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClarify = (updatedPrompt: string) => {
    handlePlanSubmit(updatedPrompt);
  };

  const handleReset = () => {
    setPlanResult(null);
    setActiveCandidate(null);
    setErrorMsg(null);
  };

  const handleSelectAlternative = (alt: ItineraryCandidate) => {
    setActiveCandidate(alt);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const travellersCount = planResult?.extracted_preferences?.travellers_count || 2;
  const durationDays = planResult?.extracted_preferences?.duration_days || 3;

  return (
    <div className="min-h-screen flex flex-col bg-stone-50 text-slate-900">
      {/* Navigation */}
      <Navbar
        brandName="TripWise AI"
        onReset={handleReset}
        showReset={Boolean(planResult || isLoading)}
      />

      <main className="flex-1">
        {/* Search Hero (always visible at top or in fresh state) */}
        {!planResult && !isLoading && (
          <HeroSearch
            onSubmit={handlePlanSubmit}
            isLoading={isLoading}
            initialPrompt={prompt}
          />
        )}

        {/* Loading Spinner / Calculation Radar */}
        {isLoading && <LoadingState />}

        {/* Error State */}
        {errorMsg && !isLoading && (
          <div className="max-w-xl mx-auto my-12 p-6 bg-red-50 border border-red-200 rounded-2xl text-center">
            <AlertTriangle className="w-8 h-8 text-red-600 mx-auto mb-2" />
            <h3 className="text-lg font-bold text-red-900">Unable to Complete Request</h3>
            <p className="text-xs text-red-700 mt-1">{errorMsg}</p>
            <button
              onClick={handleReset}
              className="mt-4 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-xl text-xs font-semibold"
            >
              Try Again
            </button>
          </div>
        )}

        {/* Clarification State */}
        {planResult?.status === 'clarification_needed' && !isLoading && (
          <ClarificationCard
            question={planResult.clarification_question || "Could you provide additional details?"}
            preferences={planResult.extracted_preferences}
            originalPrompt={prompt}
            onClarify={handleClarify}
          />
        )}

        {/* No Affordable Options State */}
        {planResult?.status === 'no_affordable_options' && !isLoading && (
          <NoTripFound
            suggestions={planResult.budget_adjustment_suggestions}
            onModifySearch={handleReset}
          />
        )}

        {/* Successful Itinerary Result */}
        {planResult?.status === 'success' && activeCandidate && !isLoading && (
          <ItineraryResult
            candidate={activeCandidate}
            alternatives={
              // Show remaining options excluding the active candidate
              planResult.recommended_trip && planResult.recommended_trip.destination.id !== activeCandidate.destination.id
                ? [planResult.recommended_trip, ...planResult.alternatives.filter((a) => a.destination.id !== activeCandidate.destination.id)]
                : planResult.alternatives
            }
            aiExplanation={planResult.ai_explanation}
            travellers={travellersCount}
            days={durationDays}
            onSelectAlternative={handleSelectAlternative}
            onNewSearch={handleReset}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-stone-200 bg-white/70 py-8 px-4 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto space-y-2">
          <p className="font-semibold text-slate-700">
            TripWise AI — Personalized Travel Itinerary Recommendation System
          </p>
          <p className="max-w-2xl mx-auto text-[11px] text-slate-400">
            Powered by Python integer cost math, verified Kaggle tourism datasets, and Google Gemini NLP. 
            All accommodation and restaurant prices are illustrative estimates. Always confirm rates with operators before booking.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default App;
