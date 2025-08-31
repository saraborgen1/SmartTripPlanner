# server/services/trip_service.py
# הקובץ הזה מגדיר את שכבת ה"שירות" 
# (Service Layer)
# שאחראית על כל הפעולות שקשורות לטיולים מול מסד הנתונים
# SQL
# כולל יצירה, שליפה, ועדכון טיולים.
# הוא משתמש במודל
# Trip
# שמוגדר בקובץ models/trip.py
# ובפונקציה לחיבור למסד הנתונים שמוגדרת בקובץ
# db_config
# וכן בשירות חיצוני שמחזיר תחזית מזג אוויר.
# מייבא את המודלים וההגדרות הדרושים
from server.models import trip                      # מודל Trip שמייצג טיול
from server.database import db_config               # פונקציה לקבלת חיבור למסד הנתונים
from server.services.weather_service import get_weather_forecast  # פונקציה לקבלת תחזית מזג אוויר

# פונקציה זו יוצרת טיול חדש ושומרת אותו במסד הנתונים
# SQL
def create_trip(trip: trip.Trip):
    # יצירת חיבור למסד הנתונים
    conn = db_config.get_connection()
    cursor = conn.cursor()

    # המרה של שדות מסוג רשימה למחרוזות:
    # selected_sites
    # transport
    # לדוגמה:
    # ["Museum", "Park"] -> "Museum,Park"
    selected_sites_str = ",".join(trip.selected_sites)
    transport_str = ",".join(trip.transport or [])  

    # שליפת תחזית מזג אוויר לשבעה ימים קדימה
    weather_data = get_weather_forecast(trip.destination)

    # המרה של תחזית מזג האוויר למחרוזת אחת מסודרת
    if "forecast" in weather_data:
        # יצירת מחרוזת שכוללת את התאריך וטווח הטמפרטורות לכל יום
        forecast_str = "; ".join(
            f"{day['date']}: {day['temp_min']}°C - {day['temp_max']}°C"
            for day in weather_data["forecast"]
        )
        trip.weather = forecast_str  
    else:
        trip.weather = "No forecast available"

    # הכנסת נתוני הטיול לטבלה
    # trips
    # במסד הנתונים    
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

    # מחזירים את אובייקט הטיול עם התחזית שנשמרה
    return trip

# פונקציה זו מעדכנת טיול קיים לפי מזהה
# id
def update_trip(trip_id: int, updated_trip: trip.Trip):
    conn = db_config.get_connection()
    cursor = conn.cursor()

    try:
        # המרת רשימות למחרוזות לשמירה במסד הנתונים
        selected_sites_str = ",".join(updated_trip.selected_sites or [])
        transport_str = ",".join(updated_trip.transport or [])

        # עדכון תחזית מזג אוויר
        weather_data = get_weather_forecast(updated_trip.destination)
        if "forecast" in weather_data:
            forecast_str = "; ".join(
                f"{day['date']}: {day['temp_min']}°C - {day['temp_max']}°C"
                for day in weather_data["forecast"]
            )
            updated_trip.weather = forecast_str
        else:
            updated_trip.weather = "No forecast available"

        # ביצוע שאילתת
        # UPDATE
        # בטבלה
        # trips
        cursor.execute("""
            UPDATE trips
            SET destination = ?, start_date = ?, end_date = ?,
                selected_sites = ?, transport = ?, notes = ?, weather = ?
            WHERE id = ?
        """, (
            updated_trip.destination,
            updated_trip.start_date,
            updated_trip.end_date,
            selected_sites_str,
            transport_str,
            updated_trip.notes,
            updated_trip.weather,
            trip_id
        ))

        conn.commit()
        if cursor.rowcount == 0:
            return {"error": "Trip not found"}

        return {"message": "Trip updated successfully", "trip_id": trip_id}

    except Exception as e:
            # במקרה של שגיאה – ביטול השינויים 
            # (Rollback)
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

# פונקציה זו מחזירה את כל הטיולים של משתמש לפי שם המשתמש
def get_user_trips(username: str):
    conn = db_config.get_connection()
    cursor = conn.cursor()
    try:

        query = "SELECT * FROM trips WHERE username = ?"

        cursor.execute(query, (username,))
        rows = cursor.fetchall()

        # שמות העמודות בטבלה
        columns = [column[0] for column in cursor.description]
        trips = []

        # יצירת רשימת מילונים 
        # (dict)
        #  שכל אחד מייצג טיול
        for row in rows:
            # המרה של שדות שנשמרו כמחרוזות חזרה לרשימות
            trip_dict = dict(zip(columns, row))
            trip_dict["selected_sites"] = (
                trip_dict["selected_sites"].split(",")
                if trip_dict["selected_sites"] else []
            )
            trip_dict["transport"] = trip_dict["transport"].split(",") if trip_dict["transport"] else []
            trips.append(trip_dict)

        return trips

    except Exception as e:
        # הדפסת שגיאה אם משהו נכשל
        print(f"❌ ERROR in get_user_trips: {e}") 
        raise
    finally:
        cursor.close()
        conn.close()


