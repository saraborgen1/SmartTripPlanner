#APIRouter-
#מאפשר לנו להגדיר קבוצת נתיבים בקובץ נפרד ולחבר אותם לאפליקציה הראשית
#Query-
#משמש להגדרת פרמטרים של שאילתא עם תיאור, ערך ברירת מחדל ועוד
from fastapi import APIRouter, Query
from ..services.ai_service import get_ai_answer

#יוצר מופע של 
# router — 
# כלומר, אובייקט שבו נגדיר את כל הנתיבים של המודול הזה
#בסוף, האובייקט הזה יחובר ל־
# FastAPI
# הראשי דרך 
# include_router
router = APIRouter()

#מגדיר נתיב
#GET
#בשם
# /ai
#כל פעם שמישהו יגלוש לשם בדפדפן זה יקרא לפונקציה שמתחתיו
@router.get("/ai")
#מגדיר את הפונקציה שתטפל בבקשות לנתיב זה
#היא מקבלת פרמטר בשם
# question
#שהוא מחרוזת חובה (עם סימן ה־
# ...   
# ב־Query)
#והיא מחזירה מילון עם התשובה לשאלה  
def ai_endpoint(question: str = Query(..., description="שאלה לסוכן AI")):
    #שולח את השאלה למודל 
    # AI
    # ומחזיר את התשובה
    return {"answer": get_ai_answer(question)}
