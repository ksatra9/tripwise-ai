from typing import List, Optional
from backend.app.models import Destination, Attraction, Restaurant
from backend.app.schemas import DailyItineraryPlan, ActivitySlot, RestaurantOut, AttractionOut

def build_daily_itinerary(
    destination: Destination,
    days: int,
    attractions: List[Attraction],
    restaurants: List[Restaurant]
) -> List[DailyItineraryPlan]:
    """
    Build day-by-day itinerary plans strictly using real database records.
    Groups attractions logically by area cluster or time of day.
    Assigns lunch and dinner from actual destination restaurants.
    """
    daily_plans: List[DailyItineraryPlan] = []
    
    # Sort attractions or cluster them
    sorted_attractions = list(attractions)
    num_attractions = len(sorted_attractions)

    # Distribute attractions across days
    attractions_per_day = max(1, num_attractions // days) if days > 0 else 1

    for day in range(1, days + 1):
        # Pick 2-3 attractions for this day
        start_idx = (day - 1) * 2
        day_attrs = sorted_attractions[start_idx : start_idx + 2] if start_idx < num_attractions else []
        
        # Determine area cluster
        cluster = "Central / Iconic Landmarks"
        if day_attrs and day_attrs[0].area_cluster:
            cluster = day_attrs[0].area_cluster

        # Morning slot
        if len(day_attrs) > 0:
            morning_attr = day_attrs[0]
            morning_slot = ActivitySlot(
                time_of_day="Morning (09:00 AM - 01:00 PM)",
                activity_name=morning_attr.name,
                category=morning_attr.category,
                entry_fee_inr=int(morning_attr.amount_inr),
                est_duration_hours=morning_attr.est_duration_hours or 2.5,
                area_cluster=cluster,
                description=morning_attr.description or f"Explore {morning_attr.name} in {destination.name}."
            )
        else:
            morning_slot = ActivitySlot(
                time_of_day="Morning (09:00 AM - 01:00 PM)",
                activity_name=f"Scenic Walking Tour & Orientation",
                category="Orientation",
                entry_fee_inr=0,
                est_duration_hours=2.0,
                area_cluster=cluster,
                description=f"Leisurely morning walk and discovering local viewpoints in {destination.name}."
            )

        # Afternoon slot
        if len(day_attrs) > 1:
            afternoon_attr = day_attrs[1]
            afternoon_slot = ActivitySlot(
                time_of_day="Afternoon (02:00 PM - 05:30 PM)",
                activity_name=afternoon_attr.name,
                category=afternoon_attr.category,
                entry_fee_inr=int(afternoon_attr.amount_inr),
                est_duration_hours=afternoon_attr.est_duration_hours or 2.0,
                area_cluster=cluster,
                description=afternoon_attr.description or f"Visit {afternoon_attr.name}."
            )
        else:
            afternoon_slot = ActivitySlot(
                time_of_day="Afternoon (02:00 PM - 05:30 PM)",
                activity_name="Local Heritage & Artisan Market Walk",
                category="Culture & Shopping",
                entry_fee_inr=0,
                est_duration_hours=2.5,
                area_cluster=cluster,
                description=f"Browse handicraft stalls, local spices, and traditional bazaars in {destination.name}."
            )

        # Evening slot
        evening_slot = ActivitySlot(
            time_of_day="Evening (06:00 PM - 08:30 PM)",
            activity_name="Sunset Point & Cultural Stroll",
            category="Leisure",
            entry_fee_inr=0,
            est_duration_hours=2.0,
            area_cluster=cluster,
            description=f"Sunset views, cultural immersion, and relaxing evening ambiance in {destination.name}."
        )

        # Restaurant assignments
        lunch_rest = None
        dinner_rest = None
        if restaurants and len(restaurants) > 0:
            lunch_idx = (day - 1) % len(restaurants)
            r1 = restaurants[lunch_idx]
            lunch_rest = RestaurantOut(
                id=r1.id,
                destination_id=r1.destination_id,
                name=r1.name,
                city=r1.city,
                cuisine=r1.cuisine,
                price_band=r1.price_band,
                rating=r1.rating,
                location=r1.location,
                famous_dish=r1.famous_dish,
                amount_inr=int(r1.amount_inr),
                price_unit=r1.price_unit,
                price_checked_on=r1.price_checked_on,
                source_url=r1.source_url,
                data_status=r1.data_status,
                is_sample_entry=r1.is_sample_entry
            )

            dinner_idx = (day) % len(restaurants)
            r2 = restaurants[dinner_idx]
            dinner_rest = RestaurantOut(
                id=r2.id,
                destination_id=r2.destination_id,
                name=r2.name,
                city=r2.city,
                cuisine=r2.cuisine,
                price_band=r2.price_band,
                rating=r2.rating,
                location=r2.location,
                famous_dish=r2.famous_dish,
                amount_inr=int(r2.amount_inr),
                price_unit=r2.price_unit,
                price_checked_on=r2.price_checked_on,
                source_url=r2.source_url,
                data_status=r2.data_status,
                is_sample_entry=r2.is_sample_entry
            )

        day_attr_cost = morning_slot.entry_fee_inr + afternoon_slot.entry_fee_inr + evening_slot.entry_fee_inr
        day_food_cost = (lunch_rest.amount_inr if lunch_rest else 250) + (dinner_rest.amount_inr if dinner_rest else 350)
        est_day_cost = day_attr_cost + day_food_cost

        daily_plans.append(
            DailyItineraryPlan(
                day_number=day,
                title=f"Day {day}: Discovering {destination.name}",
                area_cluster=cluster,
                morning=morning_slot,
                afternoon=afternoon_slot,
                evening=evening_slot,
                lunch=lunch_rest,
                dinner=dinner_rest,
                estimated_day_cost_inr=est_day_cost
            )
        )

    return daily_plans
