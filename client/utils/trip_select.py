# client/utils/trip_select.py

from datetime import datetime, date
from typing import Dict, List, Optional, Tuple

# פורמט ברירת מחדל לתאריכים
# DATE_FMT
DATE_FMT = "%Y-%m-%d"


def _parse_dates(t: Dict) -> Optional[Tuple[date, date]]:
    """
    פונקציה פנימית שמנסה להמיר את שדות התאריכים מתוך מילון טיול.

    t – 
    dict
    שמייצג טיול (כפי שהשרת מחזיר).

    מחזירה זוג 
    Tuple
    של תאריכי התחלה וסיום כ־
    date
    אם ההמרה הצליחה.
    
    אם נכשל – מחזירה
    None
    """
    try:
        start = datetime.strptime(t.get("start_date", ""), DATE_FMT).date()
        end   = datetime.strptime(t.get("end_date", ""), DATE_FMT).date()
        return start, end
    except Exception:
        return None


def select_current_or_next(trips: List[Dict]) -> Optional[Dict]:
    """
    פונקציה שבוחרת את הטיול הרלוונטי ביותר עבור המשתמש מתוך רשימת טיולים.

    trips – רשימה של 
    dict
    שכל אחד מייצג טיול (כפי שהשרת מחזיר).

    מחזירה:
      - טיול שמתרחש כרגע (אם היום נמצא בין start ל־ end)
      - אם אין – הטיול הקרוב ביותר שעתיד להתחיל (תאריך start קרוב להיום)
      - אם אין בכלל – מחזירה
        None
    """

    # תאריך היום הנוכחי
    # today
    today = date.today()

    # משתנים לשמירת טיול נוכחי (אם קיים)
    best_current = None
    best_current_delta = None  # כמה ימים נשארו עד סוף הטיול

    # רשימת טיולים עתידיים, נשמור כזוגות (תאריך התחלה, טיול)
    upcoming: List[Tuple[date, Dict]] = []

    for t in trips:
        parsed = _parse_dates(t)
        if not parsed:
            continue
        start, end = parsed

        if start <= today <= end:
            # אם היום נמצא בתוך הטיול
            # במקרה שיש כמה טיולים חופפים – ניקח את זה שמסתיים מוקדם יותר
            delta = (end - today).days
            if best_current is None or delta < best_current_delta:
                best_current = t
                best_current_delta = delta
        elif start >= today:
            # טיולים שעדיין לא התחילו – נוסיף לרשימה
            upcoming.append((start, t))

    # אם מצאנו טיול שמתרחש עכשיו – נחזיר אותו
    if best_current:
        return best_current

    # אחרת, נבחר את הטיול הקרוב ביותר שעתיד להתחיל
    if upcoming:
        upcoming.sort(key=lambda x: x[0])  # מיון לפי תאריך התחלה
        return upcoming[0][1]

    # אם אין טיולים רלוונטיים – נחזיר None
    return None
