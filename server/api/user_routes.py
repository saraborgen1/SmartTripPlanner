# server/api/user_routes.py

# הקובץ הזה מגדיר את שכבת ה־
# API
# עבור משתמשים וטיולים במערכת,
# באמצעות ספריית
# FastAPI
# כאן נגדיר את כל נקודות הקצה 
# (Endpoints)
# שקשורות לרישום, התחברות, יצירה, שליפה ועדכון טיולים.
from fastapi import APIRouter
from server.models import user       # מודל של משתמש
from server.models import trip       # מודל של טיול
from server.services import trip_service  # שירותים לטיפול בטיולים (שמירה, שליפה, יצירה)
from server.services import user_service  # שירותים לניהול משתמשים מול מסד הנתונים

# יוצרים אובייקט מסוג
# APIRouter
# שבו נרשום את כל הנתיבים 
# (Routes)
# הקשורים למשתמשים וטיולים.
# בסוף יחובר האובייקט הזה לאפליקציה הראשית של
# FastAPI
# באמצעות
# include_router
router = APIRouter()

# נתיב מסוג
# POST
# בשם:
# /register
# נקודת קצה לרישום משתמש חדש.
# מקבלת אובייקט מסוג
# User
# (שם משתמש + סיסמה),
# שולחת אותו לשירות המשתמשים,
# ובודקת אם שם המשתמש כבר קיים.
@router.post("/register")
def register(user: user.User):
    return user_service.register_user(user)

# נתיב מסוג
# POST
# בשם:
# /login
# נקודת קצה להתחברות משתמש קיים.
# מקבלת שם משתמש וסיסמה,
# ושולחת לשירות המשתמשים.
# אם ההתחברות הצליחה מוחזר
# access_token
@router.post("/login")
def login(user: user.User):
    return user_service.login_user(user)

# נתיב מסוג
# POST
# בשם:
# /create_trip
# נקודת קצה ליצירת טיול חדש.
# מקבלת אובייקט מסוג
# Trip
# ושולחת אותו לשירות הטיולים
# trip_service
# כדי לשמור אותו במסד הנתונים.
@router.post("/create_trip")
def create_new_trip(trip: trip.Trip):
    return trip_service.create_trip(trip)

# נתיב מסוג
# GET
# בשם:
# /my_trips/{username}
# נקודת קצה שמחזירה את כל הטיולים של משתמש מסוים.
# מקבלת את שם המשתמש מהנתיב (Path Parameter),
# ושולחת אותו לשירות הטיולים
# trip_service
# כדי להחזיר את כל הטיולים של אותו משתמש.
@router.get("/my_trips/{username}")
def get_my_trips(username: str):
    return trip_service.get_user_trips(username)

# נתיב מסוג
# PUT
# בשם:
# /update_trip/{trip_id}
# נקודת קצה לעדכון טיול קיים לפי המזהה שלו
# id
# מקבלת גם את ה־
# trip_id
# כפרמטר מהנתיב,
# וגם את האובייקט
# Trip
# עם הנתונים החדשים לעדכון.
@router.put("/update_trip/{trip_id}")
def update_trip(trip_id: int, trip: trip.Trip):
    return trip_service.update_trip(trip_id, trip)
