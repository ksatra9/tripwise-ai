import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models import Destination, TransportRoute, Hotel, Restaurant, Attraction
from backend.app.schemas import (
    DestinationOut,
    HotelOut,
    RestaurantOut,
    AttractionOut,
    TransportRouteOut
)
from backend.app.services.data_importer import inspect_dataset_files, import_kaggle_tourism_dataset

logger = logging.getLogger("tripwise.destinations")
router = APIRouter(prefix="/api", tags=["Destinations"])

@router.get("/destinations", response_model=List[DestinationOut])
def list_destinations(
    state: Optional[str] = Query(None, description="Filter by state"),
    region: Optional[str] = Query(None, description="Filter by region (e.g. North India)"),
    db: Session = Depends(get_db)
):
    """Retrieve list of all active travel destinations in the system."""
    query = db.query(Destination)
    if state:
        query = query.filter(Destination.state.ilike(f"%{state}%"))
    if region:
        query = query.filter(Destination.region.ilike(f"%{region}%"))
    return query.all()


@router.get("/destinations/{id}")
def get_destination_details(id: int, db: Session = Depends(get_db)):
    """Retrieve detailed destination records including hotels, routes, and attractions."""
    destination = db.query(Destination).filter(Destination.id == id).first()
    if not destination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Destination with ID {id} not found."
        )

    hotels = db.query(Hotel).filter(Hotel.destination_id == id).all()
    restaurants = db.query(Restaurant).filter(Restaurant.destination_id == id).all()
    attractions = db.query(Attraction).filter(Attraction.destination_id == id).all()
    routes = db.query(TransportRoute).filter(TransportRoute.destination_id == id).all()

    return {
        "destination": destination,
        "transport_routes": routes,
        "hotels": hotels,
        "restaurants": restaurants,
        "attractions": attractions
    }


@router.get("/datasets/inspect")
def inspect_available_datasets():
    """Inspects downloaded Kaggle files and reports real schema metadata."""
    return inspect_dataset_files()


@router.post("/datasets/import-kaggle")
def trigger_kaggle_import(db: Session = Depends(get_db)):
    """Imports destinations and attractions directly from the local Kaggle dataset."""
    imported_count = import_kaggle_tourism_dataset(db)
    return {
        "status": "success",
        "imported_destinations_count": imported_count,
        "note": "Imported actual records from sushanthnaidu24/indian-tourism-dataset"
    }
