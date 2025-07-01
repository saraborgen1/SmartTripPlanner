from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime

class Trip(BaseModel):
    username: str
    destination: str
    start_date: str
    end_date: str
    selected_sites: List[str]
    transport: Optional[List[str]] = []
    accommodation: Optional[str] = None
    notes: Optional[str] = ""
    budget: Optional[float] = None

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
