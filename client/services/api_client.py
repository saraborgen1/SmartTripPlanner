# client/services/api_client.py

# הקובץ הזה מגדיר שכבת שירות –
# Service –
# בצד הלקוח שמנהלת את התקשורת מול השרת
# FastAPI.
# הרעיון:
# ה־Presenter
# לא מתקשר ישירות עם
# requests,
# אלא קורא לפונקציות כאן.
# זה שומר על קוד נקי, ניתן לבדיקה, ומרכז את הטיפול בשגיאות ו־
# timeout.

import requests
from typing import Any, Dict, List
from client.utils.constants import BASE_URL

# יוצרים אובייקט 
# Session
# כדי למחזר חיבורים ולשפר ביצועים / ניהול כותרות
# Headers
_session = requests.Session()

# זמן קצוב ברירת מחדל לבקשות (בשניות)
DEFAULT_TIMEOUT = 30
# זמן מיוחד עבור קריאות ל־
# AI
# (ארוך יותר כי עיבוד עשוי לקחת זמן)
AI_TIMEOUT = 90


"""
התחברות משתמש:
שולח בקשת 
POST
לנתיב /login ומחזיר תשובת 
JSON
"""
def login(username: str, password: str) -> Dict[str, Any]:
 
    r = _session.post(
        f"{BASE_URL}/login",
        json={"username": username, "password": password},
        timeout=DEFAULT_TIMEOUT,
    )
    r.raise_for_status()   
    return r.json()


"""
רישום משתמש חדש:
שולח בקשת
POST
לנתיב 
/register.
במקרה של כישלון השרת יחזיר קוד שגיאה (400) עם 
detail.
"""
def register(username: str, password: str) -> Dict[str, Any]:
  
    r = _session.post(
        f"{BASE_URL}/register",
        json={"username": username, "password": password},
        timeout=DEFAULT_TIMEOUT,
    )
    r.raise_for_status()
    return r.json()


"""
שליפת אתרים / נקודות עניין בעיר מסוימת.
שולח בקשת
GET
לנתיב 
/get_sites
עם פרמטרים:
    - city (עיר)
    - address (כתובת התחלה)
    - profile (סוג תחבורה: driving-car / foot-walking / cycling-regular)
    - limit (מספר תוצאות להחזיר)
"""
def get_sites(
    city: str,
    address: str,
    profile: str = "driving-car",
    limit: int = 8
) -> List[Dict[str, Any]]:
    
    r = _session.get(
        f"{BASE_URL}/get_sites",
        params={"city": city, "address": address, "profile": profile, "limit": limit},
        timeout=DEFAULT_TIMEOUT,
    )
    r.raise_for_status()
    return r.json()


"""
יצירת טיול חדש עם אימות משתמש:
שולח בקשת
POST
לנתיב 
/create_trip 
עם גוף 
JSON.
כולל כותרת 
Authorization 
עם ה־
Token.
"""
def create_trip(trip: Dict[str, Any], token: str | None = None) -> Dict[str, Any]:
    if not token:
        raise ValueError("User is not logged in. Cannot create a trip.")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    r = _session.post(
        f"{BASE_URL}/create_trip",
        json=trip,
        headers=headers,
        timeout=DEFAULT_TIMEOUT
    )
    r.raise_for_status()
    return r.json()


"""
שליפת כל הטיולים של משתמש מסוים:
שולח בקשת
GET
לנתיב 
/my_trips/{username}.
מחזיר רשימה של
dict
שכל אחד מייצג טיול.
"""
def get_my_trips(username: str) -> List[Dict[str, Any]]:

    r = _session.get(f"{BASE_URL}/my_trips/{username}", timeout=DEFAULT_TIMEOUT)
    r.raise_for_status()
    return r.json()


"""
שליחת שאלה לסוכן
AI:
שולח בקשת
GET
לנתיב 
/ai 
עם פרמטר 
"question".
מחזיר את המחרוזת 
answer
מתוך תשובת השרת.
"""
def ask_ai(question: str) -> str:

    r = _session.get(f"{BASE_URL}/ai", params={"question": question}, timeout=AI_TIMEOUT)
    r.raise_for_status()
    data = r.json()
    return data.get("answer", "")


"""
שליפת תחזית מזג אוויר לעיר מסוימת:
שולח בקשת
GET
לנתיב 
/weather_data 
עם פרמטר 
"city".
מחזיר
dict
עם המידע מהשרת.
"""
def get_weather(city: str) -> dict:

    r = _session.get(f"{BASE_URL}/weather_data", params={"city": city}, timeout=DEFAULT_TIMEOUT)
    r.raise_for_status()
    return r.json()


"""
עדכון טיול קיים לפי ה־
id 
שלו:
שולח בקשת
PUT
לנתיב 
/update_trip/{trip_id}.
כולל כותרת 
Authorization 
עם ה־
Token.
"""
def update_trip(trip_id: int, trip: Dict[str, Any], token: str | None = None) -> Dict[str, Any]:
  
    if not token:
        raise ValueError("User is not logged in. Cannot update a trip.")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    r = _session.put(
        f"{BASE_URL}/update_trip/{trip_id}",
        json=trip,
        headers=headers,
        timeout=DEFAULT_TIMEOUT
    )
    r.raise_for_status()
    return r.json()
