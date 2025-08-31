# מייבא את המחלקות והפונקציות הדרושות
# APIRouter – מאפשר להגדיר קבוצת נתיבים בקובץ נפרד ולחבר אותם לאפליקציה הראשית
# HTTPException – משמש להחזרת שגיאות מותאמות עם קוד סטטוס והודעה
from fastapi import APIRouter
from server.models import user       # מודל של משתמש
from server.models import trip       # מודל של טיול
from server.services import trip_service  # שירותים לטיפול בטיולים (שמירה, שליפה, יצירה)
from server.services import user_service  # שירותים לניהול משתמשים מול מסד הנתונים

# יוצרת אובייקט router – שבו נרשום את כל הנתיבים (endpoints) של משתמשים וטיולים
# אובייקט זה יחובר בהמשך לאפליקציה הראשית של FastAPI באמצעות include_router
router = APIRouter()

# נתיב POST בשם /register
# נקודת קצה לרישום משתמש חדש
# מקבלת אובייקט מסוג User – שם משתמש וסיסמה
# בודקת אם שם המשתמש כבר קיים במסד הנתונים, ואם לא – מוסיפה אותו
@router.post("/register")
def register(user: user.User):
    return user_service.register_user(user)

# נתיב POST בשם /login
# נקודת קצה להתחברות משתמש קיים
# מקבלת שם משתמש וסיסמה, ובודקת אם הם תואמים לרשומה במסד הנתונים
@router.post("/login")
def login(user: user.User):
    return user_service.login_user(user)

# נתיב POST בשם /create_trip
# נקודת קצה ליצירת טיול חדש
# מקבלת אובייקט מסוג Trip (טיול חדש), ומעבירה אותו לשירות שמתמודד עם שמירתו
@router.post("/create_trip")
def create_new_trip(trip: trip.Trip):
    return trip_service.create_trip(trip)

# נתיב GET בשם /my_trips/{username}
# נקודת קצה שמחזירה את כל הטיולים של משתמש מסוים
# מקבלת את שם המשתמש כפרמטר מהנתיב ומחזירה את רשימת הטיולים שלו
@router.get("/my_trips/{username}")
def get_my_trips(username: str):
    return trip_service.get_user_trips(username)

# נתיב PUT בשם /update_trip/{trip_id}
# נקודת קצה לעדכון טיול קיים לפי ה־id שלו
@router.put("/update_trip/{trip_id}")
def update_trip(trip_id: int, trip: trip.Trip):
    return trip_service.update_trip(trip_id, trip)
