from server.models import trip
from server.database import db_config

# יצירת טיול חדש – שמירה לקובץ JSON
def create_trip(trip: trip.Trip):
    trips = load_data(TRIPS_FILE)      # טען את כל הטיולים הקיימים
    trips.append(trip.dict())          # המר את הטיול למילון והוסף לרשימה
    save_data(TRIPS_FILE, trips)       # שמור את הרשימה המעודכנת לקובץ
    return trip                        # החזר את הטיול שנשמר (כקבלה ללקוח)

# שליפת כל הטיולים של משתמש לפי שם משתמש
def get_user_trips(username: str):
    trips = load_data(TRIPS_FILE)      # טען את כל הטיולים מהקובץ
    user_trips = [t for t in trips if t["username"] == username]  # סינון לפי המשתמש
    return user_trips                  # החזר את רשימת הטיולים של המשתמש
