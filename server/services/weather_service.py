#server/services/weather_service.py

# הקובץ הזה מגדיר את שכבת השירות (Service Layer)
# שאחראית על שליפת תחזית מזג אוויר משירות חיצוני –
# weatherapi.com
#
# הוא משתמש בספריית
# requests
# כדי לשלוח בקשות
# HTTP
# לשרת חיצוני ולקבל ממנו נתוני מזג אוויר.
import requests

# מפתח
# API
# לשירות
# weatherapi.com
WEATHER_API_KEY = "acecc3119b344218b41132502250107"

# פונקציה שמחזירה תחזית מזג אוויר ל־7 ימים לעיר מסוימת
def get_weather_forecast(city_name: str):
    # כתובת ה־
    # API
    # של
    # weatherapi
    # שמחזירה תחזית מזג אוויר
    url = "http://api.weatherapi.com/v1/forecast.json"

    # פרמטרים שנשלחים בבקשת
    # GET
    # אל ה־
    # API
    params = {
        "key": WEATHER_API_KEY,   # מפתח API
        "q": city_name,           # שם העיר הרצויה
        "days": 7,                # מספר הימים בתחזית
        "aqi": "no",              # ללא מדד זיהום אוויר
        "alerts": "no"            # ללא התראות מזג אוויר
    }

    # שליחת בקשת
    # GET
    # לשרת עם הפרמטרים
    response = requests.get(url, params=params)

    # אם הבקשה נכשלה – מדפיסים שגיאה ומחזירים הודעת שגיאה
    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code}")
        print(response.text)
        return {"error": "Failed to fetch weather data."}

    # המרת התשובה מסוג
    # JSON
    # למבנה נתונים בפייתון (dictionary)
    data = response.json()

    # רשימה שתכיל את התחזית היומית לכל יום
    forecast = []
    for day in data["forecast"]["forecastday"]:
        forecast.append({
            "date": day["date"],                     # תאריך התחזית
            "temp_min": day["day"]["mintemp_c"],     # טמפרטורה מינימלית
            "temp_max": day["day"]["maxtemp_c"]      # טמפרטורה מקסימלית
        })

    # הפונקציה מחזירה מילון 
    # (dictionary) 
    # עם:
    # destination – שם היעד (העיר)
    # forecast – רשימת תחזיות לכל יום
    return {
        "destination": city_name,
        "forecast": forecast
    }
