from fastapi import APIRouter, Query
from ..services.opentripmap_service import get_places_in_city

router = APIRouter()

@router.get("/get_sites")
def get_sites(city: str = Query(..., description="שם יעד")):
    return get_places_in_city(city)
