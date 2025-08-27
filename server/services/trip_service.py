# מייבא את המודלים וההגדרות הדרושים
from server.models import trip                      # מודל Trip שמייצג טיול
from server.database import db_config               # פונקציה לקבלת חיבור למסד הנתונים
from server.services.weather_service import get_weather_forecast  # פונקציה לקבלת תחזית מזג אוויר

# פונקציה זו שומרת טיול חדש למסד הנתונים SQL
def create_trip(trip: trip.Trip):
    # התחברות למסד הנתונים
    conn = db_config.get_connection()
    cursor = conn.cursor()

    # המרה של שדות רשימה (selected_sites ו־transport) למחרוזת אחת מופרדת בפסיקים
    # לדוגמה: ["מוזיאון", "פארק"] -> "מוזיאון,פארק"
    selected_sites_str = ",".join(trip.selected_sites)
    transport_str = ",".join(trip.transport or [])  # אם transport ריק, נשתמש ברשימה ריקה

    # שליפת תחזית מזג האוויר מלאה ל־7 ימים באמצעות השירות
    weather_data = get_weather_forecast(trip.destination)

    # המרה של רשימת התחזיות למחרוזת אחת מפורמטת לשמירה במסד הנתונים
    if "forecast" in weather_data:
        # בניית מחרוזת הכוללת כל יום עם הטמפ' המינימלית והמקסימלית
        forecast_str = "; ".join(
            f"{day['date']}: {day['temp_min']}°C - {day['temp_max']}°C"
            for day in weather_data["forecast"]
        )
        trip.weather = forecast_str  # שמירת התחזית בשדה weather של הטיול
    else:
        trip.weather = "No forecast available"  # במקרה של שגיאה או חוסר נתונים

    # ביצוע שאילתת INSERT – הכנסת כל נתוני הטיול לטבלת trips במסד הנתונים
    cursor.execute("""
        INSERT INTO trips (
            username, destination, start_date, end_date,
            selected_sites, transport, notes, weather
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        trip.username,              # שם המשתמש
        trip.destination,           # יעד הטיול
        trip.start_date,            # תאריך יציאה
        trip.end_date,              # תאריך חזרה
        selected_sites_str,         # אתרים נבחרים, כמחרוזת
        transport_str,              # אמצעי תחבורה, כמחרוזת
        trip.notes,                 # הערות כלליות
        trip.weather                # תחזית מזג אוויר כטקסט
    ))

    # שמירת הנתונים במסד וסגירת הקשר
    conn.commit()
    cursor.close()
    conn.close()

    # מחזירים את האובייקט trip עם התחזית שנשמרה, כתגובה ללקוח
    return trip

def get_user_trips(username: str):
    conn = db_config.get_connection()
    cursor = conn.cursor()
    try:
        print(f"DEBUG - Fetching trips for: {username}")  # 🟢

        query = "SELECT * FROM trips WHERE username = ?"
        print(f"DEBUG - Running query: {query} with param: {username}")  # 🟢

        cursor.execute(query, (username,))
        rows = cursor.fetchall()
        print(f"DEBUG - Got {len(rows)} rows from DB")  # 🟢

        columns = [column[0] for column in cursor.description]
        trips = []

        for row in rows:
            trip_dict = dict(zip(columns, row))
            trip_dict["selected_sites"] = trip_dict["selected_sites"].split(",") if trip_dict["selected_sites"] else []
            trip_dict["transport"] = trip_dict["transport"].split(",") if trip_dict["transport"] else []
            trips.append(trip_dict)

        return trips

    except Exception as e:
        print(f"❌ ERROR in get_user_trips: {e}")  # 🟢 נבין מה נופל
        raise
    finally:
        cursor.close()
        conn.close()

