# מייבא את ספריית requests לשליחת בקשות HTTP ל־API חיצוני
import requests

# מפתח API לאתר weatherapi.com (מומלץ לשמור כמשתנה סביבה לצורכי אבטחה)
WEATHER_API_KEY = "acecc3119b344218b41132502250107"

# פונקציה שמחזירה תחזית מזג אוויר ל־7 ימים לעיר מסוימת
def get_weather_forecast(city_name: str):
    # כתובת ה־API של weatherapi שמחזיר תחזית
    url = "http://api.weatherapi.com/v1/forecast.json"

    # פרמטרים שישלחו ב־GET request ל־API
    params = {
        "key": WEATHER_API_KEY,   # מפתח API
        "q": city_name,           # שם העיר הרצויה
        "days": 7,                # מספר הימים בתחזית
        "aqi": "no",              # ללא מדד זיהום אוויר
        "alerts": "no"            # ללא התראות מזג אוויר
    }

    # שליחת בקשת GET לשרת עם הפרמטרים
    response = requests.get(url, params=params)

    # אם הבקשה נכשלה – מדפיסים שגיאה ומחזירים הודעת שגיאה
    if response.status_code != 200:
        print(f"שגיאה בקבלת נתונים: {response.status_code}")
        print(response.text)
        return {"error": "שגיאה בקבלת נתוני מזג האוויר."}

    # המרת תגובת JSON למבנה נתונים בפייתון
    data = response.json()

    # רשימה שתכיל את התחזית היומית לכל יום
    forecast = []
    for day in data["forecast"]["forecastday"]:
        forecast.append({
            "date": day["date"],                     # תאריך התחזית
            "temp_min": day["day"]["mintemp_c"],     # טמפרטורה מינימלית
            "temp_max": day["day"]["maxtemp_c"]      # טמפרטורה מקסימלית
        })

    # מחזיר את שם היעד ורשימת התחזיות לכל אחד מהימים
    return {
        "destination": city_name,
        "forecast": forecast
    }
