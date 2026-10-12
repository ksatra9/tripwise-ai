import pytest
from backend.app.models import Destination, Hotel, Attraction

def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "TripWise AI" in data["app_name"]

def test_list_destinations(client):
    response = client.get("/api/destinations")
    assert response.status_code == 200
    destinations = response.json()
    assert len(destinations) >= 5
    names = [d["name"] for d in destinations]
    assert "Rishikesh" in names
    assert "Jaipur" in names

def test_get_destination_details(client):
    response = client.get("/api/destinations/1")
    assert response.status_code == 200
    details = response.json()
    assert "destination" in details
    assert "transport_routes" in details
    assert "hotels" in details
    assert "attractions" in details

def test_plan_trip_example_input(client):
    prompt = "I am travelling from Delhi with one friend for 3 days. Our total budget is ₹20,000. We like nature and local food."
    response = client.post("/api/plan", json={"prompt": prompt})
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "success"
    assert data["recommended_trip"] is not None
    
    trip = data["recommended_trip"]
    # Destination must be affordable
    assert trip["cost_breakdown"]["is_within_budget"] is True
    assert trip["cost_breakdown"]["total_trip_cost_inr"] <= 20000
    assert trip["cost_breakdown"]["total_trip_cost_inr"] > 0
    assert trip["destination"]["name"] in ["Rishikesh", "Jaipur", "Agra"]

    # Verify transparent cost breakdown components
    items = trip["cost_breakdown"]["items"]
    assert len(items) >= 6
    cat_names = [i["category"] for i in items]
    assert "Round-Trip Transport" in cat_names
    assert "Hotel Accommodation" in cat_names
    assert "Food & Dining" in cat_names
    assert "Emergency Contingency Reserve (10%)" in cat_names

    # Verify day-by-day plan
    assert len(trip["daily_plans"]) == 3

def test_plan_trip_clarification_flow(client):
    # Missing budget and origin
    prompt = "I want to take a 3-day trip with my friend."
    response = client.post("/api/plan", json={"prompt": prompt})
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "clarification_needed"
    assert data["clarification_question"] is not None
    assert data["recommended_trip"] is None

def test_prevent_invented_records(client, db_session):
    # Rule 3: The system must never invent a hotel, restaurant, attraction, or transport option.
    prompt = "I am travelling from Delhi with one friend for 3 days. Our total budget is ₹20,000. We like nature and local food."
    response = client.post("/api/plan", json={"prompt": prompt})
    assert response.status_code == 200
    data = response.json()
    trip = data["recommended_trip"]

    # Verify the recommended hotel actually exists in database
    hotel_name = trip["recommended_hotel"]["name"]
    db_hotel = db_session.query(Hotel).filter(Hotel.name == hotel_name).first()
    assert db_hotel is not None
    assert db_hotel.amount_inr == trip["recommended_hotel"]["amount_inr"]

    # Verify all attractions visited exist in database
    for attr in trip["visited_attractions"]:
        db_attr = db_session.query(Attraction).filter(Attraction.name == attr["name"]).first()
        assert db_attr is not None

def test_plan_trip_unaffordable_budget(client):
    prompt = "I am travelling from Delhi with 4 friends for 5 days. Our total budget is ₹5,000."
    response = client.post("/api/plan", json={"prompt": prompt})
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "no_affordable_options"
    assert len(data["budget_adjustment_suggestions"]) > 0
