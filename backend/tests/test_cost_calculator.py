import math
import pytest
from backend.app.models import TransportRoute, Hotel, Restaurant, Attraction
from backend.app.services.cost_calculator import (
    calculate_rooms_needed,
    calculate_nights_from_days,
    calculate_trip_cost
)

def test_room_capacity_ceiling():
    assert calculate_rooms_needed(1, 2) == 1
    assert calculate_rooms_needed(2, 2) == 1
    assert calculate_rooms_needed(3, 2) == 2
    assert calculate_rooms_needed(4, 2) == 2
    assert calculate_rooms_needed(5, 2) == 3

def test_nights_from_days():
    assert calculate_nights_from_days(1) == 1
    assert calculate_nights_from_days(3) == 2
    assert calculate_nights_from_days(5) == 4

def test_group_transport_cost():
    route = TransportRoute(amount_inr=1500, mode="Train")
    hotel = Hotel(amount_inr=2000, name="Sample Inn")
    
    # 3 travellers
    cost = calculate_trip_cost(
        transport=route,
        hotel=hotel,
        days=3,
        travellers=3,
        budget_inr=30000,
        restaurants=[],
        attractions=[]
    )
    # Transport = 1500 * 3 = 4500
    assert cost.round_trip_transport_inr == 4500
    assert isinstance(cost.round_trip_transport_inr, int)

def test_multiple_night_hotel_cost():
    route = TransportRoute(amount_inr=1000, mode="Bus")
    hotel = Hotel(amount_inr=2500, name="Hilltop Resort")
    
    # 4 travellers, 4 days (3 nights), 2 rooms
    cost = calculate_trip_cost(
        transport=route,
        hotel=hotel,
        days=4,
        travellers=4,
        budget_inr=50000,
        restaurants=[],
        attractions=[]
    )
    # 4 travellers = 2 rooms; 4 days = 3 nights
    # Hotel stay = 2500 * 3 nights * 2 rooms = 15,000
    assert cost.hotel_stay_inr == 15000

def test_contingency_calculation():
    route = TransportRoute(amount_inr=1200, mode="Train")
    hotel = Hotel(amount_inr=1800, name="Riverside Retreat")
    
    cost = calculate_trip_cost(
        transport=route,
        hotel=hotel,
        days=3,
        travellers=2,
        budget_inr=20000,
        restaurants=[],
        attractions=[]
    )
    # Subtotal check
    expected_subtotal = (
        cost.round_trip_transport_inr +
        cost.hotel_stay_inr +
        cost.food_inr +
        cost.attractions_inr +
        cost.local_transport_inr
    )
    assert cost.subtotal_inr == expected_subtotal
    assert cost.contingency_inr == math.ceil(expected_subtotal * 0.10)
    assert cost.total_trip_cost_inr == cost.subtotal_inr + cost.contingency_inr

def test_integer_arithmetic():
    route = TransportRoute(amount_inr=1450, mode="Train")
    hotel = Hotel(amount_inr=1850, name="Nature Stay")
    
    cost = calculate_trip_cost(
        transport=route,
        hotel=hotel,
        days=3,
        travellers=2,
        budget_inr=20000
    )
    # Verify all currency fields are pure integers
    assert isinstance(cost.round_trip_transport_inr, int)
    assert isinstance(cost.hotel_stay_inr, int)
    assert isinstance(cost.food_inr, int)
    assert isinstance(cost.attractions_inr, int)
    assert isinstance(cost.local_transport_inr, int)
    assert isinstance(cost.subtotal_inr, int)
    assert isinstance(cost.contingency_inr, int)
    assert isinstance(cost.total_trip_cost_inr, int)
    assert isinstance(cost.remaining_budget_inr, int)

def test_exact_budget_boundary():
    route = TransportRoute(amount_inr=1000, mode="Train")
    hotel = Hotel(amount_inr=1000, name="Budget Inn")
    # 2 travellers, 2 days (1 night), 1 room
    # Transport = 1000 * 2 = 2000
    # Hotel = 1000 * 1 * 1 = 1000
    # Food (default 250) = 250 * 3 * 2 * 2 = 3000
    # Attractions = 0
    # Local transport = 700 * 2 = 1400
    # Subtotal = 2000 + 1000 + 3000 + 0 + 1400 = 7400
    # Contingency = ceil(7400 * 0.10) = 740
    # Total = 8140
    exact_cost = calculate_trip_cost(
        transport=route,
        hotel=hotel,
        days=2,
        travellers=2,
        budget_inr=8140,
        restaurants=[],
        attractions=[]
    )
    assert exact_cost.total_trip_cost_inr == 8140
    assert exact_cost.remaining_budget_inr == 0
    assert exact_cost.is_within_budget is True

def test_one_rupee_over_budget_boundary():
    route = TransportRoute(amount_inr=1000, mode="Train")
    hotel = Hotel(amount_inr=1000, name="Budget Inn")
    # Total = 8140, Budget = 8139
    over_cost = calculate_trip_cost(
        transport=route,
        hotel=hotel,
        days=2,
        travellers=2,
        budget_inr=8139,
        restaurants=[],
        attractions=[]
    )
    assert over_cost.total_trip_cost_inr == 8140
    assert over_cost.remaining_budget_inr == -1
    assert over_cost.is_within_budget is False

def test_missing_restaurants_and_attractions():
    route = TransportRoute(amount_inr=1000, mode="Train")
    hotel = Hotel(amount_inr=1000, name="Budget Inn")
    cost_none = calculate_trip_cost(
        transport=route,
        hotel=hotel,
        days=3,
        travellers=2,
        budget_inr=20000,
        restaurants=None,
        attractions=None
    )
    # Default meal rate is 250 -> 250 * 3 meals * 2 travellers * 3 days = 4500
    assert cost_none.food_inr == 4500
    assert cost_none.attractions_inr == 0
    # Check contingency data status is 'calculated', not 'verified_snapshot'
    contingency_item = [i for i in cost_none.items if "Contingency" in i.category][0]
    assert contingency_item.data_status == "calculated"

def test_invalid_input_guards():
    route = TransportRoute(amount_inr=1000, mode="Train")
    hotel = Hotel(amount_inr=1000, name="Budget Inn")
    # Non-positive days and travellers should be clamped safely to at least 1
    cost = calculate_trip_cost(
        transport=route,
        hotel=hotel,
        days=0,
        travellers=-1,
        budget_inr=-500
    )
    assert cost.total_trip_cost_inr > 0
    assert cost.budget_inr == 0
    assert cost.is_within_budget is False
    assert cost.remaining_budget_inr == 0 - cost.total_trip_cost_inr

