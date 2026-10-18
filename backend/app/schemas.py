from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class TripQuery(BaseModel):
    prompt: str = Field(..., min_length=3, description="Free-text trip description")

class ExtractedTripPreferences(BaseModel):
    origin_city: Optional[str] = None
    total_budget_inr: Optional[int] = None
    is_budget_ambiguous_or_per_person: bool = False
    duration_days: Optional[int] = None
    travellers_count: Optional[int] = None
    interests: List[str] = Field(default_factory=list)
    preferred_destination: Optional[str] = None
    accommodation_tier: Optional[str] = None # Budget, Mid-range, Luxury
    transport_preference: Optional[str] = None # Flight, Train, Bus, Any
    is_complete: bool = False
    missing_field: Optional[str] = None
    follow_up_question: Optional[str] = None

class CostBreakdownItem(BaseModel):
    category: str
    unit_cost_inr: int
    units: int
    multiplier_description: str
    total_inr: int
    price_unit: str
    data_status: str # demo, historical, verified_snapshot, live_quote
    price_checked_on: Optional[str] = None
    source_url: Optional[str] = None
    verification_note: str

class TripCostBreakdown(BaseModel):
    round_trip_transport_inr: int
    hotel_stay_inr: int
    food_inr: int
    attractions_inr: int
    local_transport_inr: int
    subtotal_inr: int
    contingency_inr: int # 10%
    total_trip_cost_inr: int
    budget_inr: int
    remaining_budget_inr: int
    is_within_budget: bool
    rooms_needed: int = 1
    nights: int = 1
    items: List[CostBreakdownItem] = Field(default_factory=list)

class TransportRouteOut(BaseModel):
    id: int
    origin_city: str
    destination_id: int
    mode: str
    duration_hours: float
    amount_inr: int
    price_unit: str
    price_checked_on: Optional[str] = None
    source_url: Optional[str] = None
    data_status: str
    notes: Optional[str] = None

class HotelOut(BaseModel):
    id: int
    destination_id: int
    name: str
    city: str
    stars: str
    rating: float
    amenities: Optional[str] = None
    tier: str
    amount_inr: int
    price_unit: str
    price_checked_on: Optional[str] = None
    source_url: Optional[str] = None
    data_status: str
    is_sample_entry: bool = True

class RestaurantOut(BaseModel):
    id: int
    destination_id: int
    name: str
    city: str
    cuisine: str
    price_band: str
    rating: float
    location: Optional[str] = None
    famous_dish: Optional[str] = None
    amount_inr: int
    price_unit: str
    price_checked_on: Optional[str] = None
    source_url: Optional[str] = None
    data_status: str
    is_sample_entry: bool = True

class AttractionOut(BaseModel):
    id: int
    destination_id: int
    name: str
    category: str
    opening_time: str
    est_duration_hours: float
    recommended_time_of_day: str
    area_cluster: Optional[str] = None
    description: Optional[str] = None
    amount_inr: int
    price_unit: str
    price_checked_on: Optional[str] = None
    source_url: Optional[str] = None
    data_status: str

class DestinationOut(BaseModel):
    id: int
    name: str
    state: str
    region: Optional[str] = None
    category: Optional[str] = None
    trip_types: Optional[str] = None
    best_seasons: Optional[str] = None
    ideal_days: float = 3.0
    minimum_days: float = 2.0
    maximum_days: float = 7.0
    popularity_score: float
    safety_rating: float
    nearest_major_city: Optional[str] = None
    nearest_airport: Optional[str] = None
    nearest_railway: Optional[str] = None
    description: Optional[str] = None
    suggested_itinerary_text: Optional[str] = None
    source_dataset: Optional[str] = None
    data_status: str

class ActivitySlot(BaseModel):
    time_of_day: str # Morning, Afternoon, Evening
    activity_name: str
    category: str
    entry_fee_inr: int
    est_duration_hours: float
    area_cluster: Optional[str] = None
    description: Optional[str] = None

class DailyItineraryPlan(BaseModel):
    day_number: int
    title: str
    area_cluster: str
    morning: ActivitySlot
    afternoon: ActivitySlot
    evening: ActivitySlot
    lunch: Optional[RestaurantOut] = None
    dinner: Optional[RestaurantOut] = None
    estimated_day_cost_inr: int

class ItineraryCandidate(BaseModel):
    destination: DestinationOut
    cost_breakdown: TripCostBreakdown
    recommended_hotel: HotelOut
    hotel_rooms_count: int
    hotel_nights_count: int
    transport_option: TransportRouteOut
    recommended_restaurants: List[RestaurantOut] = Field(default_factory=list)
    visited_attractions: List[AttractionOut] = Field(default_factory=list)
    daily_plans: List[DailyItineraryPlan] = Field(default_factory=list)
    score: float
    score_breakdown: Dict[str, float] = Field(default_factory=dict)
    match_reasons: List[str] = Field(default_factory=list)
    budget_tier: str = "Mid-range" # Budget, Mid-range, Luxury

class PlanResponse(BaseModel):
    status: str # "success", "clarification_needed", "no_affordable_options", "error"
    clarification_question: Optional[str] = None
    extracted_preferences: Optional[ExtractedTripPreferences] = None
    recommended_trip: Optional[ItineraryCandidate] = None
    alternatives: List[ItineraryCandidate] = Field(default_factory=list)
    ai_explanation: Optional[str] = None
    budget_adjustment_suggestions: List[str] = Field(default_factory=list)
    diagnostics: Optional[Dict[str, Any]] = None
    disclaimer: str = (
        "Estimated prices; confirm before booking. All hotel, restaurant, and transport rates are "
        "sample or historical estimates, not live verified bookable quotes."
    )
