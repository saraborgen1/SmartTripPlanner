from fastapi import APIRouter, HTTPException
from server.models import user
from server.models import trip
from server.services import trip_service

#יוצרת אובייקט router – שבו נרשום את כל הנתיבים (endpoints) של המשתמשים והטיולים
router = APIRouter()

# נקודת קצה לרישום משתמש חדש
@router.post("/register")
def register(user: user.User):
    users = load_data(USERS_FILE)  # טען את המשתמשים מקובץ JSON
    # בדיקה אם שם המשתמש כבר קיים
    if any(u["username"] == user.username for u in users):
        raise HTTPException(status_code=400, detail="Username already exists")
    users.append(user.dict())  # הוסף את המשתמש החדש
    save_data(USERS_FILE, users)  # שמור לקובץ
    return {"message": "User registered successfully"}

# נקודת קצה להתחברות משתמש קיים
@router.post("/login")
def login(user: user.User):
    users = load_data(USERS_FILE)
    if any(u["username"] == user.username and u["password"] == user.password for u in users):
        return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid username or password")

# נקודת קצה ליצירת טיול חדש
@router.post("/create_trip")
def create_new_trip(trip: trip.Trip):
    return trip_service.create_trip(trip)

# נקודת קצה לשליפת כל הטיולים של משתמש מסוים
@router.get("/my_trips/{username}")
def get_my_trips(username: str):
    return trip_service.get_user_trips(username)
