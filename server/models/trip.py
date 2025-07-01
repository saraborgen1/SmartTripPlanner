from pydantic import BaseModel
from typing import List, Optional

# מודל להזמנת טיול – מתאר את כל פרטי הטיול של משתמש
class Trip(BaseModel):
    username: str                       # שם המשתמש שביצע את ההזמנה
    destination: str                    # יעד הטיול (למשל: פריז, רומא)
    start_date: str                     # תאריך התחלה של הטיול (כמחרוזת)
    end_date: str                       # תאריך סיום של הטיול (כמחרוזת)
    selected_sites: List[str]           # רשימת אתרים שנבחרו לטיול
    transport: Optional[List[str]] = [] # רשימת אמצעי תחבורה (למשל: טיסה, רכבת) – לא חובה
    accommodation: Optional[str] = None # מקום לינה (למשל שם המלון או כתובת) – לא חובה
    notes: Optional[str] = ""           # הערות אישיות שהמשתמש רשם – לא חובה
    budget: Optional[float] = None      # תקציב מוערך לטיול – לא חובה

    #בדיקה שהתאריך סיום הוא אחרי תאריך התחלה
    @validator("end_date")
    def end_after_start(cls, end_date, values):
        start_date = values.get("start_date")
        if start_date and end_date < start_date:
            raise ValueError("תאריך חזרה חייב להיות אחרי תאריך יציאה")
        return end_date