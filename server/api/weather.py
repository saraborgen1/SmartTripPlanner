from fastapi import APIRouter, Query
from ..services.weather_service import get_weather_forecast

router = APIRouter()

@router.get("/weather_data")
def weather(city: str = Query(..., description="שם העיר")):
    return get_weather_forecast(city)
