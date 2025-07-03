#APIRouter-
#מאפשר לנו להגדיר קבוצת נתיבים בקובץ נפרד ולחבר אותם לאפליקציה הראשית
#Query-
#משמש להגדרת פרמטרים של שאילתא עם תיאור, ערך ברירת מחדל ועוד
from fastapi import APIRouter, Query
from ..services.opentripmap_service import get_sites_with_routes

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
#/get_sites
#כל פעם שמישהו יגלוש לשם בדפדפן זה יקרא לפונקציה שמתחתיו
@router.get("/get_sites")
#מגדיר את הפונקציה שתטפל בבקשות לנתיב זה
#היא מקבלת פרמטרים:
# city – שם העיר (חובה)
# address – כתובת התחלה (חובה), למשל רחוב ומספר
# profile – סוג תחבורה, ברירת מחדל רכב
def get_sites(
    city: str = Query(..., description="שם יעד"),
    address: str = Query(..., description="הכתובת הנוכחית שלך (למשל רחוב ומספר)"),
    profile: str = Query("driving-car", description="סוג התחבורה (driving-car, foot-walking, cycling-regular)")
):
    #הפונקציה תקבל את שם העיר, הכתובת והתחבורה ותשלח בקשה לקבלת אתרים ומסלולים
    return get_sites_with_routes(city_name=city, start_address=address, profile=profile)
