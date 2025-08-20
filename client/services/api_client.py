# client/services/api_client.py
# -----------------------------
# שכבת שירות (Service) בצד הלקוח שמנהלת את התקשורת מול השרת (FastAPI).
# הרעיון: Presenter לא מדבר ישירות עם requests, אלא קורא לפונקציות כאן.
# זה שומר על קוד נקי, ניתן לבדיקה, ומרכז טיפול בשגיאות/זמנים.

import requests
from typing import Any, Dict, List
from utils.constants import BASE_URL

# יוצרים Session כדי למחזר חיבורים ולשפר ביצועים/ניהול כותרות (Headers)
_session = requests.Session()

# זמן קצוב ברירת מחדל לבקשות (בשניות)
DEFAULT_TIMEOUT = 15


def login(username: str, password: str) -> Dict[str, Any]:
    """
    התחברות משתמש.
    שולח POST ל-/login ומחזיר JSON (לרוב יכיל access_token).
    זורק requests.HTTPError אם השרת ענה בשגיאה (401/400 וכו').
    """
    r = _session.post(
        f"{BASE_URL}/login",
        json={"username": username, "password": password},
        timeout=DEFAULT_TIMEOUT,
    )
    r.raise_for_status()   # יזרוק חריגה אם הקוד אינו 2xx
    return r.json()


def register(username: str, password: str) -> Dict[str, Any]:
    """
    רישום משתמש חדש.
    שולח POST ל-/register. במקרה של כישלון השרת יחזיר 400 עם detail.
    """
    r = _session.post(
        f"{BASE_URL}/register",
        json={"username": username, "password": password},
        timeout=DEFAULT_TIMEOUT,
    )
    r.raise_for_status()
    return r.json()


def get_sites(city: str, address: str = "Default Address", profile: str = "driving-car") -> List[Dict[str, Any]]:
    """
    שליפת אתרים/תוצאות חיפוש לפי עיר (endpoint חיפוש, לא ישות Trip).
    מחזיר רשימת מילונים (dict) כפי שהשרת מחזיר—Raw JSON.
    """
    r = _session.get(
        f"{BASE_URL}/get_sites",
        params={"city": city, "address": address, "profile": profile},
        timeout=DEFAULT_TIMEOUT,
    )
    r.raise_for_status()
    return r.json()


def create_trip(trip: Dict[str, Any]) -> Dict[str, Any]:
    """
    יצירת טיול חדש בשרת.
    trip הוא dict שחייב להתאים לסכמה של Trip בשרת:
    username, destination, start_date, end_date, selected_sites, transport, notes
    (אין צורך לשלוח weather—השרת ימלא).
    """
    r = _session.post(f"{BASE_URL}/create_trip", json=trip, timeout=DEFAULT_TIMEOUT)
    r.raise_for_status()
    return r.json()


def get_my_trips(username: str) -> List[Dict[str, Any]]:
    """
    שליפת כל הטיולים של משתמש מסוים.
    מחזיר רשימת dicts שכל אחד מהם במבנה Trip כפי שהשרת מחזיר.
    """
    r = _session.get(f"{BASE_URL}/my_trips/{username}", timeout=DEFAULT_TIMEOUT)
    r.raise_for_status()
    return r.json()
