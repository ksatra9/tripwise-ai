import math
from typing import List, Tuple, Dict, Any, Optional
from backend.app.models import TransportRoute, Hotel, Restaurant, Attraction
from backend.app.schemas import TripCostBreakdown, CostBreakdownItem

# Standard local transport daily group estimate (e.g., auto-rickshaws, metro, local cab) in INR
DAILY_GROUP_LOCAL_TRANSPORT_INR = 700

# Fallback meal cost per person per meal if specific restaurants not provided
DEFAULT_MEAL_COST_INR = 250

def calculate_rooms_needed(travellers: int, capacity_per_room: int = 2) -> int:
    """Calculate rooms required using ceiling division, respecting room capacity."""
    if capacity_per_room <= 0:
        capacity_per_room = 2
    if travellers <= 0:
        return 1
    return math.ceil(travellers / capacity_per_room)

def calculate_nights_from_days(days: int) -> int:
    """Derive overnight stays from trip duration (minimum 1 night)."""
    if days <= 0:
        return 1
    return max(1, days - 1)

def calculate_trip_cost(
    transport: TransportRoute,
    hotel: Hotel,
    days: int,
    travellers: int,
    budget_inr: int,
    restaurants: Optional[List[Restaurant]] = None,
    attractions: Optional[List[Attraction]] = None,
    capacity_per_room: int = 2
) -> TripCostBreakdown:
    """
    Deterministic cost calculator executing integer INR arithmetic.
    
    Formula:
      1. Transport = transport.amount_inr * travellers (round trip)
      2. Hotel = hotel.amount_inr * nights * rooms_needed
      3. Food = avg_meal_rate * 3 meals * travellers * days
      4. Attractions = sum(attraction.amount_inr * travellers)
      5. Local transit = DAILY_GROUP_LOCAL_TRANSPORT_INR * days
      6. Subtotal = Transport + Hotel + Food + Attractions + Local transit
      7. Contingency = math.ceil(Subtotal * 0.10)
      8. Total = Subtotal + Contingency
    """
    safe_days = max(1, int(days))
    safe_travellers = max(1, int(travellers))
    safe_capacity = max(1, int(capacity_per_room))
    safe_budget = max(0, int(budget_inr))

    nights = calculate_nights_from_days(safe_days)
    rooms_needed = calculate_rooms_needed(safe_travellers, safe_capacity)

    # 1. Round-trip transport
    transport_fare = max(0, int(transport.amount_inr))
    transport_total = int(transport_fare * safe_travellers)
    transport_item = CostBreakdownItem(
        category="Round-Trip Transport",
        unit_cost_inr=transport_fare,
        units=safe_travellers,
        multiplier_description=f"{safe_travellers} traveller(s) × ₹{transport_fare:,} round-trip ({transport.mode})",
        total_inr=transport_total,
        price_unit=transport.price_unit or "per_person_round_trip",
        data_status=transport.data_status or "demo",
        price_checked_on=transport.price_checked_on,
        source_url=transport.source_url,
        verification_note="Demo / schedule estimate. Not a live reservation quote."
    )

    # 2. Hotel accommodation
    hotel_rate = max(0, int(hotel.amount_inr))
    hotel_total = int(hotel_rate * nights * rooms_needed)
    hotel_item = CostBreakdownItem(
        category="Hotel Accommodation",
        unit_cost_inr=hotel_rate,
        units=nights * rooms_needed,
        multiplier_description=f"{rooms_needed} room(s) × {nights} night(s) × ₹{hotel_rate:,}/night ({hotel.name})",
        total_inr=hotel_total,
        price_unit=hotel.price_unit or "per_room_per_night",
        data_status=hotel.data_status or "demo",
        price_checked_on=hotel.price_checked_on,
        source_url=hotel.source_url,
        verification_note="Illustrative / cleaned dataset estimate. Confirm with property directly."
    )

    # 3. Food & Dining
    # Calculate average meal cost from valid positive restaurants or standard default
    valid_restaurant_prices = [
        int(r.amount_inr) for r in (restaurants or [])
        if getattr(r, 'amount_inr', None) is not None and r.amount_inr > 0
    ]
    if valid_restaurant_prices:
        avg_meal = int(round(sum(valid_restaurant_prices) / len(valid_restaurant_prices)))
    else:
        avg_meal = DEFAULT_MEAL_COST_INR

    # 3 meals a day per traveller
    meals_count = 3 * safe_travellers * safe_days
    food_total = int(avg_meal * meals_count)
    food_item = CostBreakdownItem(
        category="Food & Dining",
        unit_cost_inr=avg_meal,
        units=meals_count,
        multiplier_description=f"{safe_travellers} traveller(s) × {safe_days} days × 3 meals @ ~₹{avg_meal:,}/meal",
        total_inr=food_total,
        price_unit="per_person_per_meal",
        data_status="demo",
        price_checked_on=None,
        source_url=None,
        verification_note="Estimated average based on local casual dining menu rates."
    )

    # 4. Attractions entry tickets
    attractions_list = [
        a for a in (attractions or [])
        if getattr(a, 'amount_inr', None) is not None and a.amount_inr >= 0
    ]
    attr_entry_per_person = sum(int(a.amount_inr) for a in attractions_list)
    attractions_total = int(attr_entry_per_person * safe_travellers)
    attractions_item = CostBreakdownItem(
        category="Sightseeing & Attraction Tickets",
        unit_cost_inr=attr_entry_per_person,
        units=safe_travellers,
        multiplier_description=f"{len(attractions_list)} planned sights × {safe_travellers} traveller(s)",
        total_inr=attractions_total,
        price_unit="per_person_entry",
        data_status="historical",
        price_checked_on="2025",
        source_url=None,
        verification_note="Historical entry ticket estimates. Surcharges for camera/guide may apply."
    )

    # 5. Local Transport (cab, auto, transit for the entire group)
    local_transport_total = int(DAILY_GROUP_LOCAL_TRANSPORT_INR * safe_days)
    local_transport_item = CostBreakdownItem(
        category="Local Commute & Transfers",
        unit_cost_inr=DAILY_GROUP_LOCAL_TRANSPORT_INR,
        units=safe_days,
        multiplier_description=f"{safe_days} day(s) × ₹{DAILY_GROUP_LOCAL_TRANSPORT_INR:,}/day for group (auto/taxis/metro)",
        total_inr=local_transport_total,
        price_unit="per_group_per_day",
        data_status="demo",
        price_checked_on=None,
        source_url=None,
        verification_note="Standard local intra-city transit buffer for the traveling group."
    )

    # 6. Subtotal & Contingency
    subtotal = transport_total + hotel_total + food_total + attractions_total + local_transport_total
    contingency = math.ceil(subtotal * 0.10)
    contingency_item = CostBreakdownItem(
        category="Emergency Contingency Reserve (10%)",
        unit_cost_inr=contingency,
        units=1,
        multiplier_description="Mandatory 10% safety buffer for unplanned delays or surge pricing",
        total_inr=contingency,
        price_unit="total_reserve",
        data_status="calculated",
        price_checked_on=None,
        source_url=None,
        verification_note="Financial safety reserve calculated mathematically (10% of subtotal)."
    )

    # 7. Total trip cost
    total_trip_cost = subtotal + contingency
    remaining_budget = safe_budget - total_trip_cost
    is_within_budget = total_trip_cost <= safe_budget

    items = [
        transport_item,
        hotel_item,
        food_item,
        attractions_item,
        local_transport_item,
        contingency_item
    ]

    return TripCostBreakdown(
        round_trip_transport_inr=transport_total,
        hotel_stay_inr=hotel_total,
        food_inr=food_total,
        attractions_inr=attractions_total,
        local_transport_inr=local_transport_total,
        subtotal_inr=subtotal,
        contingency_inr=contingency,
        total_trip_cost_inr=total_trip_cost,
        budget_inr=safe_budget,
        remaining_budget_inr=remaining_budget,
        is_within_budget=is_within_budget,
        rooms_needed=rooms_needed,
        nights=nights,
        items=items
    )
