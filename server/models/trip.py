#Server/models/trip.py
# הקובץ הזה מגדיר את מודל הנתונים
# Trip
# באמצעות ספריית
# Pydantic
# המודל מייצג טיול יחיד במערכת, כולל פרטים על המשתמש, היעד,
# תאריכים, אתרים לביקור, תחבורה, הערות ותחזית מזג אוויר.
from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime

# מודל של טיול –
# Trip
# יורש מ־
# BaseModel
# של
# Pydantic
# זה אומר שכל שדה מוגדר כאן נבדק אוטומטית מבחינת סוג נתון וערך.
class Trip(BaseModel):
    # שם המשתמש שיצר את הטיול
    # מחרוזת חובה
    username: str

    # יעד הטיול (עיר, מדינה או כל יעד אחר)
    destination: str

    # תאריך יציאה
    # ותאריך חזרה
    # בפורמט מוגדר –
    # YYYY-MM-DD
    start_date: str
    end_date: str

    # רשימת אתרים שנבחרו לביקור בטיול
    # כל אתר מיוצג כמחרוזת
    selected_sites: List[str]

    # אמצעי תחבורה לטיול
    # רשימה אופציונלית של מחרוזות
    # למשל: "car", "bus", "train"
    transport: Optional[List[str]] = []

    # הערות נוספות על הטיול
    # מחרוזת ריקה אם אין הערות
    notes: Optional[str] = ""

    # תחזית מזג אוויר ליעד הטיול
    # מחרוזת אופציונלית
    weather: Optional[str] = None 


    # ולידטור (Validator)
    # בודק שתאריך החזרה 
    # (end_date)
    #  אינו מוקדם מתאריך היציאה 
    # (start_date).
    # אם תאריכים לא תואמים את הפורמט
    # YYYY-MM-DD
    # או שתאריך החזרה מוקדם – תיזרק שגיאה עם הודעה מתאימה.
    @field_validator("end_date")
    @classmethod
    def end_after_start(cls, end_date: str, values):
        start_date = values.get("start_date")
        if start_date:
            try:
                # המרה של המחרוזות לאובייקטים מסוג
                # datetime
                start = datetime.strptime(start_date, "%Y-%m-%d")
                end = datetime.strptime(end_date, "%Y-%m-%d")
                if end < start:
                    raise ValueError("Return date must be after start date")
            except ValueError:
                raise ValueError("Dates must be in format YYYY-MM-DD")
        return end_date
