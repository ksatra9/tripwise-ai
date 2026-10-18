export type DataStatus = 'demo' | 'historical' | 'verified_snapshot' | 'live_quote' | 'calculated';

export interface ExtractedTripPreferences {
  origin_city?: string;
  total_budget_inr?: number;
  is_budget_ambiguous_or_per_person: boolean;
  duration_days?: number;
  travellers_count?: number;
  interests: string[];
  preferred_destination?: string;
  accommodation_tier?: string;
  is_complete: boolean;
  missing_field?: string;
  follow_up_question?: string;
}

export interface CostBreakdownItem {
  category: string;
  unit_cost_inr: number;
  units: number;
  multiplier_description: string;
  total_inr: number;
  price_unit: string;
  data_status: DataStatus;
  price_checked_on?: string | null;
  source_url?: string | null;
  verification_note: string;
}

export interface TripCostBreakdown {
  round_trip_transport_inr: number;
  hotel_stay_inr: number;
  food_inr: number;
  attractions_inr: number;
  local_transport_inr: number;
  subtotal_inr: number;
  contingency_inr: number;
  total_trip_cost_inr: number;
  budget_inr: number;
  remaining_budget_inr: number;
  is_within_budget: boolean;
  items: CostBreakdownItem[];
}

export interface TransportRoute {
  id: number;
  origin_city: string;
  destination_id: number;
  mode: string;
  duration_hours: number;
  amount_inr: number;
  price_unit: string;
  price_checked_on?: string | null;
  source_url?: string | null;
  data_status: DataStatus;
  notes?: string | null;
}

export interface Hotel {
  id: number;
  destination_id: number;
  name: string;
  city: string;
  stars: string;
  rating: number;
  amenities?: string | null;
  tier: string;
  amount_inr: number;
  price_unit: string;
  price_checked_on?: string | null;
  source_url?: string | null;
  data_status: DataStatus;
  is_sample_entry: boolean;
}

export interface Restaurant {
  id: number;
  destination_id: number;
  name: string;
  city: string;
  cuisine: string;
  price_band: string;
  rating: number;
  location?: string | null;
  famous_dish?: string | null;
  amount_inr: number;
  price_unit: string;
  price_checked_on?: string | null;
  source_url?: string | null;
  data_status: DataStatus;
  is_sample_entry: boolean;
}

export interface Attraction {
  id: number;
  destination_id: number;
  name: string;
  category: string;
  opening_time: string;
  est_duration_hours: number;
  recommended_time_of_day: string;
  area_cluster?: string | null;
  description?: string | null;
  amount_inr: number;
  price_unit: string;
  price_checked_on?: string | null;
  source_url?: string | null;
  data_status: DataStatus;
}

export interface Destination {
  id: number;
  name: string;
  state: string;
  region?: string | null;
  category?: string | null;
  trip_types?: string | null;
  best_seasons?: string | null;
  ideal_days: number;
  minimum_days: number;
  maximum_days: number;
  popularity_score: number;
  safety_rating: number;
  nearest_major_city?: string | null;
  nearest_airport?: string | null;
  nearest_railway?: string | null;
  description?: string | null;
  suggested_itinerary_text?: string | null;
  source_dataset?: string | null;
  data_status: DataStatus;
}

export interface ActivitySlot {
  time_of_day: string;
  activity_name: string;
  category: string;
  entry_fee_inr: number;
  est_duration_hours: number;
  area_cluster?: string | null;
  description?: string | null;
}

export interface DailyItineraryPlan {
  day_number: number;
  title: string;
  area_cluster: string;
  morning: ActivitySlot;
  afternoon: ActivitySlot;
  evening: ActivitySlot;
  lunch?: Restaurant | null;
  dinner?: Restaurant | null;
  estimated_day_cost_inr: number;
}

export interface ItineraryCandidate {
  destination: Destination;
  cost_breakdown: TripCostBreakdown;
  recommended_hotel: Hotel;
  hotel_rooms_count: number;
  hotel_nights_count: number;
  transport_option: TransportRoute;
  recommended_restaurants: Restaurant[];
  visited_attractions: Attraction[];
  daily_plans: DailyItineraryPlan[];
  score: number;
  score_breakdown: Record<string, number>;
  match_reasons: string[];
}

export interface PlanResponse {
  status: 'success' | 'clarification_needed' | 'no_affordable_options' | 'error';
  clarification_question?: string | null;
  extracted_preferences?: ExtractedTripPreferences | null;
  recommended_trip?: ItineraryCandidate | null;
  alternatives: ItineraryCandidate[];
  ai_explanation?: string | null;
  budget_adjustment_suggestions: string[];
  disclaimer: string;
}
