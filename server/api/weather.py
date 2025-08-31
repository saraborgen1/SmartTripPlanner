#server/api/weather.py

# הקובץ הזה מגדיר את שכבת ה־
# API
# עבור תחזית מזג האוויר במערכת.
# מייבאים כלים מתוך
# FastAPI:
# APIRouter –
# מאפשר להגדיר קבוצת נתיבים (Routes) בקובץ נפרד
# ולחבר אותם לאפליקציה הראשית.
# Query –
# מאפשר להגדיר פרמטרים בשאילתת
# GET
# כולל תיאור, חובה/ברירת מחדל ועוד.
from fastapi import APIRouter, Query

# מייבא את פונקציית השירות שאחראית על שליפת תחזית מזג אוויר
from ..services.weather_service import get_weather_forecast

# יוצרים מופע של
# APIRouter
# שבו נרשום את כל הנתיבים 
# (Endpoints)
# הקשורים למודול מזג האוויר.
router = APIRouter()

# מגדירים נתיב מסוג
# GET
# בשם:
# /weather_data
# כאשר תתקבל בקשה לנתיב הזה,
# תופעל הפונקציה
# weather
@router.get("/weather_data")
def weather(city: str = Query(..., description="City name")):
    # הפרמטר
    # city
    # מתקבל משורת השאילתה 
    # (Query String).
    # הפרמטר מוגדר כחובה (מסומן עם
    # ...
    # ב־
    # Query)
    # ויש לו תיאור שיופיע בתיעוד האוטומטי.
    # דוגמה לכתובת בקשה:
    # /weather_data?city=Tel+Aviv
    # הפונקציה מפנה את הבקשה לשכבת השירות –
    # get_weather_forecast
    # שמעבירה את הבקשה לשירות חיצוני של מזג אוויר.
    # התוצאה המוחזרת היא תחזית מזג האוויר לעיר שצוינה.
    return get_weather_forecast(city)
