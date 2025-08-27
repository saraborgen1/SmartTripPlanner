# client/services/api_client.py
# -----------------------------
# שכבת שירות
# Service
# בצד הלקוח שמנהלת את התקשורת מול השרת 
# FastAPI
#
# הרעיון:
# Presenter
# לא מדבר ישירות עם 
# requests
# אלא קורא לפונקציות כאן.
# זה שומר על קוד נקי, ניתן לבדיקה, ומרכז את הטיפול בשגיאות/timeout.

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
# זמן מיוחד עבור קריאות ל־AI (ארוך יותר כי עיבוד עשוי לקחת זמן)
AI_TIMEOUT = 90


def login(username: str, password: str) -> Dict[str, Any]:
    """
    התחברות משתמש:
    שולח בקשת 
    POST
    לנתיב /login ומחזיר תשובת 
    JSON
    (לרוב תכיל access_token).
    """
    r = _session.post(
        f"{BASE_URL}/login",
        json={"username": username, "password": password},
        timeout=DEFAULT_TIMEOUT,
    )
    r.raise_for_status()   # יזרוק חריגה אם הקוד שהוחזר מהשרת אינו 2xx
    return r.json()


def register(username: str, password: str) -> Dict[str, Any]:
    """
    רישום משתמש חדש:
    שולח בקשת 
    POST
    לנתיב /register.
    במקרה של כישלון השרת יחזיר קוד שגיאה (400) עם detail.
    """
    r = _session.post(
        f"{BASE_URL}/register",
        json={"username": username, "password": password},
        timeout=DEFAULT_TIMEOUT,
    )
    r.raise_for_status()
    return r.json()


def get_sites(city: str, address: str, profile: str = "driving-car", limit: int = 8) -> List[Dict[str, Any]]:
    """
    שליפת אתרים / נקודות עניין בעיר מסוימת.
    שולח בקשת 
    GET
    לנתיב /get_sites עם פרמטרים:
    - city (עיר)
    - address (כתובת התחלה)
    - profile (סוג תחבורה: driving-car / foot-walking / cycling-regular)
    - limit (מספר תוצאות להחזיר)

    מחזיר רשימת מילונים 
    dict
    כפי שהשרת מחזיר ב־JSON.
    """
    r = _session.get(
        f"{BASE_URL}/get_sites",
        params={"city": city, "address": address, "profile": profile, "limit": limit},
        timeout=DEFAULT_TIMEOUT,
    )
    r.raise_for_status()
    return r.json()


def create_trip(trip: Dict[str, Any], token: str | None = None) -> Dict[str, Any]:
    """
    יצירת טיול חדש עם אימות משתמש:
    שולח בקשת POST לנתיב /create_trip עם גוף JSON.
    כולל כותרת Authorization עם ה-Token.
    """
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



def get_my_trips(username: str) -> List[Dict[str, Any]]:
    """
    שליפת כל הטיולים של משתמש מסוים:
    שולח בקשת 
    GET
    לנתיב /my_trips/{username}.
    
    מחזיר רשימה של 
    dict
    שכל אחד מייצג טיול.
    """
    r = _session.get(f"{BASE_URL}/my_trips/{username}", timeout=DEFAULT_TIMEOUT)
    r.raise_for_status()
    return r.json()


def ask_ai(question: str) -> str:
    """
    שליחת שאלה לסוכן 
    AI.
    שולח בקשת 
    GET
    לנתיב /ai עם פרמטר "question".
    
    מחזיר את המחרוזת answer מתוך תשובת השרת.
    """
    r = _session.get(f"{BASE_URL}/ai", params={"question": question}, timeout=AI_TIMEOUT)
    r.raise_for_status()
    data = r.json()
    return data.get("answer", "")


def get_weather(city: str) -> dict:
    """
    שליפת תחזית מזג אוויר לעיר מסוימת:
    שולח בקשת 
    GET
    לנתיב /weather_data עם פרמטר "city".
    
    מחזיר 
    dict
    עם המידע מהשרת.
    """
    r = _session.get(f"{BASE_URL}/weather_data", params={"city": city}, timeout=DEFAULT_TIMEOUT)
    r.raise_for_status()
    return r.json()
