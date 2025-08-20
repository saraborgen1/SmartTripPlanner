# client/utils/trip_select.py
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple

DATE_FMT = "%Y-%m-%d"

def _parse_dates(t: Dict) -> Optional[Tuple[date, date]]:
    try:
        start = datetime.strptime(t.get("start_date", ""), DATE_FMT).date()
        end   = datetime.strptime(t.get("end_date", ""), DATE_FMT).date()
        return start, end
    except Exception:
        return None

def select_current_or_next(trips: List[Dict]) -> Optional[Dict]:
    """
    מקבל רשימת טיולים (dict כפי שהשרת מחזיר)
    מחזיר:
      - טיול שמתקיים היום (start <= היום <= end) — אם יש
      - אחרת הטיול הקרוב ביותר שמתחיל היום/בעתיד
      - אם אין בכלל — None
    """
    today = date.today()

    best_current = None
    best_current_delta = None  # כמה ימים נשארו עד סוף הטיול

    upcoming: List[Tuple[date, Dict]] = []

    for t in trips:
        parsed = _parse_dates(t)
        if not parsed:
            continue
        start, end = parsed

        if start <= today <= end:
            # בטיולים חופפים – נעדיף מי שנגמר מוקדם יותר (קרוב יותר)
            delta = (end - today).days
            if best_current is None or delta < best_current_delta:
                best_current = t
                best_current_delta = delta
        elif start >= today:
            upcoming.append((start, t))

    if best_current:
        return best_current

    if upcoming:
        # נבחר את הטיול עם תאריך התחלה המינימלי (הקרוב ביותר)
        upcoming.sort(key=lambda x: x[0])
        return upcoming[0][1]

    return None
