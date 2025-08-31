#server/api/opentrip.py
# הקובץ הזה מגדיר ממשק
# API
# שמוקדש לקבלת אתרים (POI) ומסלולי נסיעה לעיר מסוימת.
#
# כאן אנחנו משתמשים ב־
# APIRouter
# כדי לרכז את הנתיבים של המודול הזה בנפרד, ולחבר אותם בהמשך לאפליקציה הראשית.
#
# בנוסף אנחנו משתמשים ב־
# Query
# של ספריית
# FastAPI
# כדי להגדיר פרמטרים שמגיעים מהשאילתא (query parameters) –
# למשל: עיר, כתובת התחלה, וסוג התחבורה.
from fastapi import APIRouter, Query
from ..services.opentripmap_service import get_sites_with_routes

# יוצרים מופע של
# APIRouter
# כלומר – אובייקט שבו נגדיר את כל הנתיבים (routes) השייכים למודול הזה.
# בסיום, האובייקט הזה יחובר ל־
# FastAPI
# הראשי על ידי הפונקציה
# include_router
router = APIRouter()


# מגדירים נתיב מסוג
# GET
# הנתיב נקרא:
# /get_sites
# כלומר – כאשר גולשים לכתובת זו בדפדפן, או שולחים בקשת
# GET
# דרך לקוח
# HTTP
# אחר – יופעל הקוד שמוגדר בפונקציה הבאה.
@router.get("/get_sites")
# מגדירים את הפונקציה שתטפל בכל בקשה לנתיב זה.
# הפונקציה מקבלת 3 פרמטרים דרך שורת השאילתא:
# city –
# שם העיר. זהו פרמטר חובה (מוגדר עם
# ...
# ב־
# Query
# ).
# address –
# כתובת התחלה (למשל רחוב ומספר). גם זה פרמטר חובה.
# profile –
# סוג התחבורה. ברירת המחדל היא:
# driving-car
# ניתן גם לבחור אופציות אחרות כמו:
# foot-walking
# או
# cycling-regular
def get_sites(
    city: str = Query(..., description="Destination city"),
    address: str = Query(..., description="Your starting address (e.g., street and number)"),
    profile: str = Query("driving-car",
                          description="Transport type (driving-car, foot-walking, cycling-regular)")
):
    # הפונקציה אוספת את שם העיר, הכתובת ואת סוג התחבורה שנבחרו.
    # לאחר מכן היא מעבירה את הנתונים לפונקציה
    # get_sites_with_routes
    # שמוגדרת בשכבת השירות.
    # הפונקציה בשירות מבצעת את הקריאה בפועל ל־
    # API
    # החיצוני (OpenTripMap / OpenRouteService),
    # ושולחת בחזרה רשימת אתרים ומסלול הגעה לכל אחד מהם.
    return get_sites_with_routes(city_name=city, start_address=address, profile=profile)
