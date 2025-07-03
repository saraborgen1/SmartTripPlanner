
from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime

# מודל של Trip
class Trip(BaseModel):
    # שם המשתמש שיצר את הטיול
    username: str
    #יעד הטיול
    destination: str
    # תאריך היציאה והחזרה
    # תאריכים בפורמט YYYY-MM-DD
    start_date: str
    end_date: str
    # רשימת אתרים לביקור בטיול
    # כל אתר הוא מחרוזת
    selected_sites: List[str]
    # אמצעי תחבורה לטיול
    # רשימה של מחרוזות (למשל: "רכב", "אוטובוס", "רכבת") 
    transport: Optional[List[str]] = []
    # הערות נוספות על הטיול
    # מחרוזת ריקה אם אין הערות
    notes: Optional[str] = ""
    weather: Optional[str] = None  # תחזית מזג האוויר (נוסף חדש)


    #בודק שתאריך היציאה לא יכול להיות אחרי תאריך החזרה
    @validator("end_date")
    def end_after_start(cls, end_date, values):
        start_date = values.get("start_date")
        if start_date:
            try:
                start = datetime.strptime(start_date, "%Y-%m-%d")
                end = datetime.strptime(end_date, "%Y-%m-%d")
                if end < start:
                    raise ValueError("תאריך חזרה חייב להיות אחרי תאריך יציאה")
            except ValueError:
                raise ValueError("פורמט תאריכים חייב להיות YYYY-MM-DD")
        return end_date
