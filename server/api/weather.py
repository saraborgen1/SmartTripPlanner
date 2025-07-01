from fastapi import APIRouter, Query
from ..services.weather_service import get_fake_weather_data

router = APIRouter()

@router.get("/weather_data")
def weather(city: str = Query(..., description="שם העיר")):
    return get_fake_weather_data(city)
