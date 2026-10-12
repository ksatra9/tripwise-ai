from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from backend.app.database import Base

class Destination(Base):
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False, unique=True, index=True)
    state = Column(String(100), nullable=False, index=True)
    region = Column(String(50), nullable=True) # North, South, West, East, Northeast, Central
    category = Column(String(150), nullable=True) # e.g. "Nature;Spiritual;Adventure"
    trip_types = Column(Text, nullable=True) # JSON or comma-separated: "Beach, Cultural, Food"
    best_seasons = Column(String(100), nullable=True) # e.g. "Winter, Post-Monsoon, Summer"
    ideal_days = Column(Integer, default=3)
    minimum_days = Column(Integer, default=2)
    maximum_days = Column(Integer, default=7)
    popularity_score = Column(Float, default=7.0)
    safety_rating = Column(Float, default=8.0)
    nearest_major_city = Column(String(100), nullable=True)
    nearest_airport = Column(String(120), nullable=True)
    nearest_railway = Column(String(120), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
    suggested_itinerary_text = Column(Text, nullable=True)
    source_dataset = Column(String(120), default="sushanthnaidu24/indian-tourism-dataset")
    data_status = Column(String(50), default="historical") # demo, historical, verified_snapshot

    # Relationships
    transport_routes = relationship("TransportRoute", back_populates="destination", cascade="all, delete-orphan")
    hotels = relationship("Hotel", back_populates="destination", cascade="all, delete-orphan")
    restaurants = relationship("Restaurant", back_populates="destination", cascade="all, delete-orphan")
    attractions = relationship("Attraction", back_populates="destination", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_dest_state_region", "state", "region"),
    )


class TransportRoute(Base):
    __tablename__ = "transport_routes"

    id = Column(Integer, primary_key=True, index=True)
    origin_city = Column(String(100), nullable=False, index=True)
    destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=False, index=True)
    mode = Column(String(50), nullable=False) # Flight, Express Train, Deluxe Bus, Road Cab
    duration_hours = Column(Float, default=4.0)
    
    # Cost record fields
    amount_inr = Column(Integer, nullable=False) # round trip per person
    price_unit = Column(String(50), default="per_person_round_trip") # per_person_round_trip
    price_checked_on = Column(String(50), nullable=True) # e.g. "2025-10" or None
    source_url = Column(String(255), nullable=True)
    data_status = Column(String(50), default="demo") # demo, historical, verified_snapshot, live_quote
    notes = Column(String(255), nullable=True)

    destination = relationship("Destination", back_populates="transport_routes")

    __table_args__ = (
        Index("idx_origin_destination", "origin_city", "destination_id"),
    )


class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, index=True)
    destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=False, index=True)
    name = Column(String(150), nullable=False)
    city = Column(String(100), nullable=False, index=True)
    stars = Column(String(50), default="3-star")
    rating = Column(Float, default=4.0)
    amenities = Column(Text, nullable=True) # Comma-separated or JSON: "Free Wi-Fi, Breakfast, AC"
    tier = Column(String(50), default="Budget") # Budget, Mid-range, Luxury
    
    # Cost record fields
    amount_inr = Column(Integer, nullable=False) # per room per night
    price_unit = Column(String(50), default="per_room_per_night")
    price_checked_on = Column(String(50), nullable=True)
    source_url = Column(String(255), nullable=True)
    data_status = Column(String(50), default="demo") # demo, historical, verified_snapshot, live_quote
    is_sample_entry = Column(Boolean, default=True)

    destination = relationship("Destination", back_populates="hotels")


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=False, index=True)
    name = Column(String(150), nullable=False)
    city = Column(String(100), nullable=False, index=True)
    cuisine = Column(String(100), default="Local & North Indian")
    price_band = Column(String(50), default="Budget") # Budget, Mid, Premium
    rating = Column(Float, default=4.0)
    location = Column(String(150), nullable=True)
    famous_dish = Column(String(150), nullable=True)
    
    # Cost record fields
    amount_inr = Column(Integer, nullable=False) # estimated meal cost per person
    price_unit = Column(String(50), default="per_person_per_meal")
    price_checked_on = Column(String(50), nullable=True)
    source_url = Column(String(255), nullable=True)
    data_status = Column(String(50), default="demo") # demo, historical, verified_snapshot, live_quote
    is_sample_entry = Column(Boolean, default=True)

    destination = relationship("Destination", back_populates="restaurants")


class Attraction(Base):
    __tablename__ = "attractions"

    id = Column(Integer, primary_key=True, index=True)
    destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=False, index=True)
    name = Column(String(150), nullable=False)
    category = Column(String(100), default="Sightseeing") # Nature, Heritage, Beach, Adventure, Spiritual
    opening_time = Column(String(100), default="09:00 AM - 05:30 PM")
    est_duration_hours = Column(Float, default=2.0)
    recommended_time_of_day = Column(String(50), default="Morning") # Morning, Afternoon, Evening
    area_cluster = Column(String(100), nullable=True) # For logical itinerary grouping
    description = Column(Text, nullable=True)
    
    # Cost record fields
    amount_inr = Column(Integer, default=0) # Entry fee per person
    price_unit = Column(String(50), default="per_person_entry")
    price_checked_on = Column(String(50), nullable=True)
    source_url = Column(String(255), nullable=True)
    data_status = Column(String(50), default="historical") # demo, historical, verified_snapshot

    destination = relationship("Destination", back_populates="attractions")


class PlanningRequestLog(Base):
    __tablename__ = "planning_requests"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(Text, nullable=False)
    origin_city = Column(String(100), nullable=True)
    budget_inr = Column(Integer, nullable=True)
    days = Column(Integer, nullable=True)
    travellers = Column(Integer, nullable=True)
    status = Column(String(50), default="processed") # processed, clarification_required, over_budget
    recommended_destination = Column(String(120), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
