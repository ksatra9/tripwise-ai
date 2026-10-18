import pytest
from backend.app.schemas import ExtractedTripPreferences
from backend.app.services.recommendation_engine import find_recommendations
from backend.app.services.cost_calculator import calculate_trip_cost
from backend.app.models import TransportRoute, Hotel

def test_exactly_at_budget_acceptance():
    route = TransportRoute(amount_inr=1000, mode="Bus")
    hotel = Hotel(amount_inr=1000, name="Base Hotel")
    
    # Calculate a sample cost
    cost = calculate_trip_cost(
        transport=route,
        hotel=hotel,
        days=2,
        travellers=1,
        budget_inr=10000
    )
    # Total trip cost is known
    exact_cost = cost.total_trip_cost_inr
    
    # Set budget exactly equal to total_trip_cost
    exact_match_cost = calculate_trip_cost(
        transport=route,
        hotel=hotel,
        days=2,
        travellers=1,
        budget_inr=exact_cost
    )
    assert exact_match_cost.is_within_budget is True
    assert exact_match_cost.remaining_budget_inr == 0

def test_over_budget_rejection(db_session):
    # User has budget of only ₹3,000 for 2 travellers and 3 days from Delhi
    # Minimum realistic trip starts around ₹14,000
    prefs = ExtractedTripPreferences(
        origin_city="Delhi",
        total_budget_inr=3000,
        duration_days=3,
        travellers_count=2,
        interests=["nature"],
        is_complete=True
    )

    recommended, alternatives, suggestions = find_recommendations(db_session, prefs)
    
    # Must reject over-budget trip
    assert recommended is None
    assert len(alternatives) == 0
    assert len(suggestions) > 0
    assert any("increase your budget" in s.lower() for s in suggestions)

def test_no_supported_transport_route(db_session):
    prefs = ExtractedTripPreferences(
        origin_city="Srinagar", # Unsupported origin in current seed dataset
        total_budget_inr=50000,
        duration_days=3,
        travellers_count=2,
        interests=["nature"],
        is_complete=True
    )

    recommended, alternatives, suggestions = find_recommendations(db_session, prefs)
    assert recommended is None
    assert any("do not have verified transport routes starting from" in s.lower() for s in suggestions)

def test_successful_recommendation_with_score_breakdown(db_session):
    prefs = ExtractedTripPreferences(
        origin_city="Delhi",
        total_budget_inr=20000,
        duration_days=3,
        travellers_count=2,
        interests=["nature", "food"],
        is_complete=True
    )

    recommended, alternatives, suggestions = find_recommendations(db_session, prefs)
    assert recommended is not None
    assert recommended.cost_breakdown.is_within_budget is True
    assert recommended.cost_breakdown.total_trip_cost_inr <= 20000
    assert recommended.destination.name in ["Rishikesh", "Jaipur", "Agra"]
    
    # Verify score breakdown transparency
    assert "interest_match" in recommended.score_breakdown
    assert "season_suitability" in recommended.score_breakdown
    assert "budget_headroom" in recommended.score_breakdown
    assert "travel_convenience" in recommended.score_breakdown
    assert "itinerary_variety" in recommended.score_breakdown
    assert recommended.score > 0

def test_preferred_destination_prioritization_jaipur(db_session):
    prefs = ExtractedTripPreferences(
        origin_city="Delhi",
        preferred_destination="Jaipur",
        total_budget_inr=20000,
        duration_days=3,
        travellers_count=2,
        interests=["culture"],
        is_complete=True
    )
    recommended, alternatives, suggestions = find_recommendations(db_session, prefs)
    assert recommended is not None
    assert recommended.destination.name == "Jaipur"
    assert any("Jaipur" in r for r in recommended.match_reasons)

def test_preferred_destination_manali(db_session):
    prefs = ExtractedTripPreferences(
        origin_city="Delhi",
        preferred_destination="Manali",
        total_budget_inr=25000,
        duration_days=4,
        travellers_count=2,
        interests=["mountains"],
        is_complete=True
    )
    recommended, alternatives, suggestions = find_recommendations(db_session, prefs)
    assert recommended is not None
    assert recommended.destination.name == "Manali"

def test_hotel_tier_classification_mutual_exclusion():
    from backend.app.services.recommendation_engine import classify_hotel_tier
    # Conflicting case 1: explicitly marked Budget, but high amount
    h1 = Hotel(tier="Budget", amount_inr=7500, stars="3-star")
    assert classify_hotel_tier(h1) == "Budget"

    # Conflicting case 2: explicitly marked Luxury, but modest amount
    h2 = Hotel(tier="Luxury", amount_inr=1800, stars="5-star")
    assert classify_hotel_tier(h2) == "Luxury"

    # Missing tier: derived from stars/amount
    h3 = Hotel(tier=None, amount_inr=8000, stars="5-star")
    assert classify_hotel_tier(h3) == "Luxury"

    h4 = Hotel(tier=None, amount_inr=3200, stars="4-star")
    assert classify_hotel_tier(h4) == "Mid-range"

    h5 = Hotel(tier=None, amount_inr=1500, stars="2-star")
    assert classify_hotel_tier(h5) == "Budget"

def test_recommendation_determinism(db_session):
    prefs = ExtractedTripPreferences(
        origin_city="Delhi",
        total_budget_inr=22000,
        duration_days=3,
        travellers_count=2,
        interests=["heritage"],
        is_complete=True
    )
    rec1, alt1, _ = find_recommendations(db_session, prefs)
    rec2, alt2, _ = find_recommendations(db_session, prefs)

    assert rec1 is not None and rec2 is not None
    assert rec1.destination.id == rec2.destination.id
    assert rec1.recommended_hotel.id == rec2.recommended_hotel.id
    assert rec1.transport_option.id == rec2.transport_option.id
    assert rec1.score == rec2.score
    assert rec1.cost_breakdown.total_trip_cost_inr == rec2.cost_breakdown.total_trip_cost_inr

def test_hard_affordability_overrides_preference(db_session):
    # User prefers Goa with an impossibly small budget of ₹5,000 for 4 people over 4 days
    prefs = ExtractedTripPreferences(
        origin_city="Delhi",
        preferred_destination="Goa",
        total_budget_inr=5000,
        duration_days=4,
        travellers_count=4,
        is_complete=True
    )
    recommended, alternatives, suggestions = find_recommendations(db_session, prefs)
    # Even though Goa is requested, over-budget trip MUST NOT be recommended
    assert recommended is None
    assert len(suggestions) > 0
    # Suggestions should mention Goa and not produce negative shortfall
    assert any("Goa" in s for s in suggestions)


