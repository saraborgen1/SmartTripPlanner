# מייבא את הכלים הדרושים מ־FastAPI
# APIRouter – מאפשר להגדיר קבוצת נתיבים (routes) בקובץ נפרד
# Query – מאפשר להגדיר פרמטרים בשאילתת GET כולל תיאור, חובה/ברירת מחדל ועוד
from fastapi import APIRouter, Query

# מייבא את פונקציית השירות שאחראית על שליפת תחזית מזג אוויר
from ..services.weather_service import get_weather_forecast

# יוצר מופע של router – שבו נגדיר את כל הנתיבים (endpoints) של מודול מזג האוויר
router = APIRouter()

# מגדיר נתיב מסוג GET בשם /weather_data
# כאשר מתבצעת בקשה לנתיב זה, תופעל הפונקציה weather
@router.get("/weather_data")
def weather(city: str = Query(..., description="שם העיר")):
    # הפרמטר 'city' מתקבל משורת השאילתה (query string)
    # הוא חובה (מסומן עם ...) ויש לו תיאור שיוצג בתיעוד האוטומטי
    # לדוגמה: /weather_data?city=Tel+Aviv

    # הפונקציה מפנה את הבקשה לפונקציית השירות get_weather_forecast
    # ומחזירה את תחזית מזג האוויר לעיר שצוינה
    return get_weather_forecast(city)
