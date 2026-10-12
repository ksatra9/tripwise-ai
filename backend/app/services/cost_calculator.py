import math
from typing import List, Tuple, Dict, Any, Optional
from backend.app.models import TransportRoute, Hotel, Restaurant, Attraction
from backend.app.schemas import TripCostBreakdown, CostBreakdownItem

# Standard local transport daily group estimate (e.g., auto-rickshaws, metro, local cab) in INR
DAILY_GROUP_LOCAL_TRANSPORT_INR = 700

# Fallback meal cost per person per meal if specific restaurants not provided
DEFAULT_MEAL_COST_INR = 250

def calculate_rooms_needed(travellers: int, capacity_per_room: int = 2) -> int:
    """Calculate rooms required using ceiling division."""
    if travellers <= 0:
        return 1
    return math.ceil(travellers / capacity_per_room)

def calculate_nights_from_days(days: int) -> int:
    """Derive overnight stays from trip duration."""
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
    nights = calculate_nights_from_days(days)
    rooms_needed = calculate_rooms_needed(travellers, capacity_per_room)

    # 1. Round-trip transport
    transport_total = int(transport.amount_inr * travellers)
    transport_item = CostBreakdownItem(
        category="Round-Trip Transport",
        unit_cost_inr=int(transport.amount_inr),
        units=travellers,
        multiplier_description=f"{travellers} traveller(s) × ₹{transport.amount_inr:,} round-trip ({transport.mode})",
        total_inr=transport_total,
        price_unit=transport.price_unit or "per_person_round_trip",
        data_status=transport.data_status or "demo",
        price_checked_on=transport.price_checked_on,
        source_url=transport.source_url,
        verification_note="Demo / schedule estimate. Not a live reservation quote."
    )

    # 2. Hotel accommodation
    hotel_total = int(hotel.amount_inr * nights * rooms_needed)
    hotel_item = CostBreakdownItem(
        category="Hotel Accommodation",
        unit_cost_inr=int(hotel.amount_inr),
        units=nights * rooms_needed,
        multiplier_description=f"{rooms_needed} room(s) × {nights} night(s) × ₹{hotel.amount_inr:,}/night ({hotel.name})",
        total_inr=hotel_total,
        price_unit=hotel.price_unit or "per_room_per_night",
        data_status=hotel.data_status or "demo",
        price_checked_on=hotel.price_checked_on,
        source_url=hotel.source_url,
        verification_note="Illustrative / cleaned dataset estimate. Confirm with property directly."
    )

    # 3. Food & Dining
    # Calculate average meal cost from provided restaurants or standard default
    if restaurants and len(restaurants) > 0:
        avg_meal = int(sum(r.amount_inr for r in restaurants) / len(restaurants))
    else:
        avg_meal = DEFAULT_MEAL_COST_INR
    # 3 meals a day per traveller
    meals_count = 3 * travellers * days
    food_total = int(avg_meal * meals_count)
    food_item = CostBreakdownItem(
        category="Food & Dining",
        unit_cost_inr=avg_meal,
        units=meals_count,
        multiplier_description=f"{travellers} traveller(s) × {days} days × 3 meals @ ~₹{avg_meal:,}/meal",
        total_inr=food_total,
        price_unit="per_person_per_meal",
        data_status="demo",
        price_checked_on=None,
        source_url=None,
        verification_note="Estimated average based on local casual dining menu rates."
    )

    # 4. Attractions entry tickets
    attractions_list = attractions or []
    attr_entry_per_person = sum(int(a.amount_inr) for a in attractions_list)
    attractions_total = int(attr_entry_per_person * travellers)
    attractions_item = CostBreakdownItem(
        category="Sightseeing & Attraction Tickets",
        unit_cost_inr=attr_entry_per_person,
        units=travellers,
        multiplier_description=f"{len(attractions_list)} planned sights × {travellers} traveller(s)",
        total_inr=attractions_total,
        price_unit="per_person_entry",
        data_status="historical",
        price_checked_on="2025",
        source_url=None,
        verification_note="Historical entry ticket estimates. Surcharges for camera/guide may apply."
    )

    # 5. Local Transport (cab, auto, transit for the entire group)
    local_transport_total = int(DAILY_GROUP_LOCAL_TRANSPORT_INR * days)
    local_transport_item = CostBreakdownItem(
        category="Local Commute & Transfers",
        unit_cost_inr=DAILY_GROUP_LOCAL_TRANSPORT_INR,
        units=days,
        multiplier_description=f"{days} day(s) × ₹{DAILY_GROUP_LOCAL_TRANSPORT_INR:,}/day for group (auto/taxis/metro)",
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
        data_status="verified_snapshot",
        price_checked_on=None,
        source_url=None,
        verification_note="Financial safety margin calculated mathematically."
    )

    # 7. Total trip cost
    total_trip_cost = subtotal + contingency
    remaining_budget = budget_inr - total_trip_cost
    is_within_budget = total_trip_cost <= budget_inr

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
        budget_inr=budget_inr,
        remaining_budget_inr=remaining_budget,
        is_within_budget=is_within_budget,
        items=items
    )
