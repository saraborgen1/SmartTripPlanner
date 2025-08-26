# #מאפשר שליחת בקשות לאתרים ושרתים חיצוניים
# import requests

# # מגדיר מפתח  (מזהה אישי) לשירות 
# # OpenTripMap – 
# # כדי להשתמש בו יש להזדהות עם מפתח זה 
# OPENTRIPMAP_API_KEY = "5ae2e3f221c38a28845f05b6b33b5e6712dcb459cd56890412563af3"
# # מפתח זה משמש כדי לאמת את הבקשות שנשלחות ל־
# # OpenTripMap API
# OPENROUTESERVICE_API_KEY = "5b3ce3597851110001cf62489fc3a4ec2b704508ab748117d9ecd490"


# # פונקציה זו ממירה כתובת (כמו רחוב ומספר) לקואורדינטות (קו אורך ורוחב)
# def geocode_address(address: str):
#     try:
#         url = "https://api.openrouteservice.org/geocode/search"
#         params = {
#             "api_key": OPENROUTESERVICE_API_KEY,
#             "text": address,
#             "size": 1  # נחזיר רק תוצאה אחת – הכי רלוונטית
#         }
#         response = requests.get(url, params=params)
#         data = response.json()

#         # נשלוף קואורדינטות אם קיימות
#         features = data.get("features", [])
#         if not features:
#             return {"error": "לא נמצאו קואורדינטות לכתובת שסופקה"}

#         coords = features[0]["geometry"]["coordinates"]  # [lon, lat]
#         return (coords[0], coords[1])  # מחזירים כ-tuple
#     except Exception as e:
#         return {"error": str(e)}


# # פונקציה זו מחזירה גם אתרי תיירות בעיר וגם דרכי הגעה אליהם
# # city_name – שם העיר לחיפוש
# # start_address – כתובת התחלה (מחרוזת) ממנה נרצה להתחיל כל מסלול
# # profile – סוג תחבורה (ברירת מחדל: רכב פרטי)
# # limit – מספר האתרים המקסימלי להחזיר (ברירת מחדל 5)
# def get_sites_with_routes(city_name: str, start_address: str, profile: str = "driving-car", limit: int = 5):
#     # ממירים את הכתובת לקואורדינטות
#     start_coords = geocode_address(start_address)
#     if isinstance(start_coords, dict) and "error" in start_coords:
#         return start_coords  # מחזירים שגיאה אם לא הצלחנו

#     # נשתמש בפונקציה הקיימת כדי לקבל את המקומות בעיר
#     places = get_places_in_city(city_name, limit)
#     if isinstance(places, dict) and "error" in places:
#         return places

#     # נשלוף שוב את קואורדינטות העיר עבור המסלולים
#     geoname_url = f"https://api.opentripmap.com/0.1/en/places/geoname"
#     geo_resp = requests.get(geoname_url, params={"name": city_name, "apikey": OPENTRIPMAP_API_KEY})
#     geo_data = geo_resp.json()
#     city_lat = geo_data.get("lat")
#     city_lon = geo_data.get("lon")

#     # נבדוק אם חסר מידע
#     if not city_lat or not city_lon:
#         return {"error": f"לא ניתן לחשב מסלול עבור {city_name}"}

#     enriched_places = []
#     for place in places:
#         # נבנה קואורדינטות יעד (בהנחה שהאתר נמצא קרוב לעיר המרכזית)
#         end_coords = (city_lon, city_lat)
#         # נחשב מסלול
#         route = get_route(start_coords, end_coords, profile)
#         # נוסיף את המידע למקום
#         enriched_places.append({
#             "place": place,
#             "route": route
#         })

#     return enriched_places


# # פונקציה זו מחפשת אתרים בעיר נתונה ומחזירה רשימה של אתרים עם פרטים
# # city_name – שם העיר לחיפוש
# # limit – מספר האתרים המקסימלי להחזיר (ברירת מחדל 5)
# def get_places_in_city(city_name: str, limit: int = 5):
#     try:
#         # מחזירה את הקואורדינטות (קו אורך ורוחב) של עיר לפי השם
#         geoname_url = f"https://api.opentripmap.com/0.1/en/places/geoname"
#         #אובייקט שמכיל את הפרמטרים של הבקשה
#         geo_resp = requests.get(geoname_url, params={"name": city_name, "apikey": OPENTRIPMAP_API_KEY})
#         #המרה של התגובה לאובייקט 
#         # JSON
#         geo_data = geo_resp.json()
#         #חילוץ קו אורך וקו רוחב לפרמטרים שונים מתוך מה שהתקבל
#         lat = geo_data.get("lat")
#         lon = geo_data.get("lon")

#         # אם לא נמצאו קואורדינטות, מחזירה הודעת שגיאה
#         if not lat or not lon:
#             return {"error": f"לא נמצאו קואורדינטות עבור {city_name}"}

#         # מחזירה אתרים תיירותיים בתוך רדיוס סביב נקודת מיקום (קו רוחב ואורך)
#         places_url = f"https://api.opentripmap.com/0.1/en/places/radius"
#         #אובייקט שמכיל את הפרמטרים של הבקשה
#         #טווח החיפוש הוא 10 קילומטרים
#         #המיקום שנמצא
#         #מספר מקסימלי של אתרים להחזיר
#         #פורמט התגובה הוא       
#         # JSON
#         places_params = {
#             "apikey": OPENTRIPMAP_API_KEY,
#             "radius": 10000,
#             "lon": lon,
#             "lat": lat,
#             "limit": limit,
#             "format": "json"
#         }

#         #שליחת הבקשה ל־
#         #OpenTripMap 
#         #עם כל הפרמטרים
#         resp = requests.get(places_url, params=places_params)
#         #קבלת התשובה (רשימת מקומות גולמית) והמרה למילון או רשימה בפייתון
#         raw_places = resp.json()

#         # יצירת רשימה ריקה שתכיל את המידע המעובד על המקומות
#         cleaned_places = []
#         # עבור כל מקום ברשימה הגולמית, יוצרת מילון עם המידע הנדרש
#         #כמו שם המקום, קטגוריה (סוג) ומרחק מהמרכז
#         #המרחק מחושב במטרים
#         for place in raw_places:
#             cleaned_places.append({
#                 "name": place.get("name") or "לא צויין",
#                 "category": place.get("kinds", "").split(",")[0],
#                 "distance_meters": round(place.get("dist", 0))
#             })

#         # מחזירה את הרשימה של המקומות עם המידע הנדרש
#         return cleaned_places

#     # במקרה של שגיאה (לדוגמה: אין אינטרנט, או פורמט לא תקין) – מחזיר הודעת שגיאה מפורשת
#     except Exception as e:
#         return {"error": str(e)}


# # פונקציה זו מחזירה מסלול בין שתי נקודות גאוגרפיות
# # start_coords – קואורדינטות של נקודת התחלה (קו רוחב, קו אורך)
# # end_coords – קואורדינטות של נקודת סיום (קו רוחב, קו אורך)
# # profile – סוג התחבורה (ברירת מחדל היא רכב פרטי)
# def get_route(start_coords: tuple, end_coords: tuple, profile: str = "driving-car"):
#     try:
#         # בונה את הכתובת של ה־
#         # API 
#         # עם סוג התחבורה שנבחר
#         url = f"https://api.openrouteservice.org/v2/directions/{profile}"
#         # שולח בקשה ל־
#         # OpenRouteService
#         # עם קואורדינטות התחלה וסיום
#         headers = {
#             "Authorization": OPENROUTESERVICE_API_KEY,
#             "Content-Type": "application/json"
#         }
#         # גוף הבקשה מכיל את הקואורדינטות של התחלה וסיום
#         # הקואורדינטות צריכות להיות ברשימה של רשימות, כל אחת מכילה קו אורך וקו רוחב
#         body = {
#             "coordinates": [list(start_coords), list(end_coords)]
#         }
#         # מבצע את הבקשה ל־
#         # OpenRouteService  
#         # עם הכתובת, גוף הבקשה והכותרות
#         response = requests.post(url, json=body, headers=headers)
#         return response.json()

#     # במקרה של שגיאה (לדוגמה: אין אינטרנט, או פורמט לא תקין) – מחזיר הודעת שגיאה מפורשת
#     except Exception as e:
#         return {"error": str(e)}


# #מאפשר שליחת בקשות לאתרים ושרתים חיצוניים
# import requests

# # מגדיר מפתח  (מזהה אישי) לשירות 
# # OpenTripMap – 
# # כדי להשתמש בו יש להזדהות עם מפתח זה 
# OPENTRIPMAP_API_KEY = "5ae2e3f221c38a28845f05b6b33b5e6712dcb459cd56890412563af3"
# # מפתח זה משמש כדי לאמת את הבקשות שנשלחות ל־
# # OpenTripMap API
# OPENROUTESERVICE_API_KEY = "5b3ce3597851110001cf62489fc3a4ec2b704508ab748117d9ecd490"


# # פונקציה זו ממירה כתובת (כמו רחוב ומספר) לקואורדינטות (קו אורך ורוחב)
# def geocode_address(address: str):
#     try:
#         url = "https://api.openrouteservice.org/geocode/search"
#         params = {
#             "api_key": OPENROUTESERVICE_API_KEY,
#             "text": address,
#             "size": 1  # נחזיר רק תוצאה אחת – הכי רלוונטית
#         }
#         response = requests.get(url, params=params)
#         data = response.json()

#         # נשלוף קואורדינטות אם קיימות
#         features = data.get("features", [])
#         if not features:
#             return {"error": "לא נמצאו קואורדינטות לכתובת שסופקה"}

#         coords = features[0]["geometry"]["coordinates"]  # [lon, lat]
#         return (coords[0], coords[1])  # מחזירים כ-tuple
#     except Exception as e:
#         return {"error": str(e)}


# # פונקציה זו מחזירה גם אתרי תיירות בעיר וגם דרכי הגעה אליהם
# # city_name – שם העיר לחיפוש
# # start_address – כתובת התחלה (מחרוזת) ממנה נרצה להתחיל כל מסלול
# # profile – סוג תחבורה (ברירת מחדל: רכב פרטי)
# # limit – מספר האתרים המקסימלי להחזיר (ברירת מחדל 5)
# def get_sites_with_routes(city_name: str, start_address: str, profile: str = "driving-car", limit: int = 5):
#     # ממירים את הכתובת לקואורדינטות
#     start_coords = geocode_address(start_address)
#     if isinstance(start_coords, dict) and "error" in start_coords:
#         return start_coords  # מחזירים שגיאה אם לא הצלחנו

#     # נשתמש בפונקציה הקיימת כדי לקבל את המקומות בעיר
#     places = get_places_in_city(city_name, limit)
#     if isinstance(places, dict) and "error" in places:
#         return places

#     # נשלוף שוב את קואורדינטות העיר עבור המסלולים
#     geoname_url = f"https://api.opentripmap.com/0.1/en/places/geoname"
#     geo_resp = requests.get(geoname_url, params={"name": city_name, "apikey": OPENTRIPMAP_API_KEY})
#     geo_data = geo_resp.json()
#     city_lat = geo_data.get("lat")
#     city_lon = geo_data.get("lon")

#     # נבדוק אם חסר מידע
#     if not city_lat or not city_lon:
#         return {"error": f"לא ניתן לחשב מסלול עבור {city_name}"}

#     enriched_places = []
#     for place in places:
#         # נבנה קואורדינטות יעד (בהנחה שהאתר נמצא קרוב לעיר המרכזית)
#         end_coords = (city_lon, city_lat)
#         # נחשב מסלול
#         route = get_route(start_coords, end_coords, profile)
#         # נוסיף את המידע למקום
#         enriched_places.append({
#             "place": place,
#             "route": route
#         })

#     return enriched_places


# # פונקציה זו מחפשת אתרים בעיר נתונה ומחזירה רשימה של אתרים עם פרטים
# # city_name – שם העיר לחיפוש
# # limit – מספר האתרים המקסימלי להחזיר (ברירת מחדל 5)
# def get_places_in_city(city_name: str, limit: int = 5):
#     try:
#         # מחזירה את הקואורדינטות (קו אורך ורוחב) של עיר לפי השם
#         geoname_url = f"https://api.opentripmap.com/0.1/en/places/geoname"
#         #אובייקט שמכיל את הפרמטרים של הבקשה
#         geo_resp = requests.get(geoname_url, params={"name": city_name, "apikey": OPENTRIPMAP_API_KEY})
#         #המרה של התגובה לאובייקט 
#         # JSON
#         geo_data = geo_resp.json()
#         #חילוץ קו אורך וקו רוחב לפרמטרים שונים מתוך מה שהתקבל
#         lat = geo_data.get("lat")
#         lon = geo_data.get("lon")

#         # אם לא נמצאו קואורדינטות, מחזירה הודעת שגיאה
#         if not lat or not lon:
#             return {"error": f"לא נמצאו קואורדינטות עבור {city_name}"}

#         # מחזירה אתרים תיירותיים בתוך רדיוס סביב נקודת מיקום (קו רוחב ואורך)
#         places_url = f"https://api.opentripmap.com/0.1/en/places/radius"
#         #אובייקט שמכיל את הפרמטרים של הבקשה
#         #טווח החיפוש הוא 10 קילומטרים
#         #המיקום שנמצא
#         #מספר מקסימלי של אתרים להחזיר
#         #פורמט התגובה הוא       
#         # JSON
#         places_params = {
#             "apikey": OPENTRIPMAP_API_KEY,
#             "radius": 10000,
#             "lon": lon,
#             "lat": lat,
#             "limit": limit,
#             "format": "json"
#         }

#         #שליחת הבקשה ל־
#         #OpenTripMap 
#         #עם כל הפרמטרים
#         resp = requests.get(places_url, params=places_params)
#         #קבלת התשובה (רשימת מקומות גולמית) והמרה למילון או רשימה בפייתון
#         raw_places = resp.json()

#         # יצירת רשימה ריקה שתכיל את המידע המעובד על המקומות
#         cleaned_places = []
#         # עבור כל מקום ברשימה הגולמית, יוצרת מילון עם המידע הנדרש
#         #כמו שם המקום, קטגוריה (סוג) ומרחק מהמרכז
#         #המרחק מחושב במטרים
#         for place in raw_places:
#             cleaned_places.append({
#                 "name": place.get("name") or "לא צויין",
#                 "category": place.get("kinds", "").split(",")[0],
#                 "distance_meters": round(place.get("dist", 0))
#             })

#         # מחזירה את הרשימה של המקומות עם המידע הנדרש
#         return cleaned_places

#     # במקרה של שגיאה (לדוגמה: אין אינטרנט, או פורמט לא תקין) – מחזיר הודעת שגיאה מפורשת
#     except Exception as e:
#         return {"error": str(e)}


# # פונקציה זו מחזירה מסלול בין שתי נקודות גאוגרפיות
# # start_coords – קואורדינטות של נקודת התחלה (קו רוחב, קו אורך)
# # end_coords – קואורדינטות של נקודת סיום (קו רוחב, קו אורך)
# # profile – סוג התחבורה (ברירת מחדל היא רכב פרטי)
# def get_route(start_coords: tuple, end_coords: tuple, profile: str = "driving-car"):
#     try:
#         # בונה את הכתובת של ה־
#         # API 
#         # עם סוג התחבורה שנבחר
#         url = f"https://api.openrouteservice.org/v2/directions/{profile}"
#         # שולח בקשה ל־
#         # OpenRouteService
#         # עם קואורדינטות התחלה וסיום
#         headers = {
#             "Authorization": OPENROUTESERVICE_API_KEY,
#             "Content-Type": "application/json"
#         }
#         # גוף הבקשה מכיל את הקואורדינטות של התחלה וסיום
#         # הקואורדינטות צריכות להיות ברשימה של רשימות, כל אחת מכילה קו אורך וקו רוחב
#         body = {
#             "coordinates": [list(start_coords), list(end_coords)]
#         }
#         # מבצע את הבקשה ל־
#         # OpenRouteService  
#         # עם הכתובת, גוף הבקשה והכותרות
#         response = requests.post(url, json=body, headers=headers)
#         return response.json()

#     # במקרה של שגיאה (לדוגמה: אין אינטרנט, או פורמט לא תקין) – מחזיר הודעת שגיאה מפורשת
#     except Exception as e:
#         return {"error": str(e)}


# services/opentripmap_service.py
import requests

OPENTRIPMAP_API_KEY = "5ae2e3f221c38a28845f05b6b33b5e6712dcb459cd56890412563af3"
OPENROUTESERVICE_API_KEY = "5b3ce3597851110001cf62489fc3a4ec2b704508ab748117d9ecd490"


# פונקציה זו ממירה כתובת (כמו רחוב ומספר) לקואורדינטות (קו אורך ורוחב)
def geocode_address(address: str):
    try:
        url = "https://api.openrouteservice.org/geocode/search"
        params = {
            "api_key": OPENROUTESERVICE_API_KEY,
            "text": address,
            "size": 1
        }
        response = requests.get(url, params=params)
        data = response.json()

        features = data.get("features", [])
        if not features:
            return {"error": "לא נמצאו קואורדינטות לכתובת שסופקה"}

        coords = features[0]["geometry"]["coordinates"]  # [lon, lat]
        return (coords[0], coords[1])
    except Exception as e:
        return {"error": str(e)}


# פונקציה שמביאה מידע מפורט על אתר לפי XID
def get_place_details(xid: str):
    try:
        url = f"https://api.opentripmap.com/0.1/en/places/xid/{xid}"
        resp = requests.get(url, params={"apikey": OPENTRIPMAP_API_KEY})
        data = resp.json()
        return {
            "rating": data.get("rate"),
            "image": data.get("preview", {}).get("source"),
            "description": data.get("wikipedia_extracts", {}).get("text", "")
        }
    except Exception:
        return {}


# פונקציה זו מחפשת אתרים בעיר נתונה ומחזירה רשימה של אתרים עם פרטים בסיסיים
def get_places_in_city(city_name: str, limit: int = 50):  # ברירת מחדל 50 תוצאות
    try:
        geoname_url = "https://api.opentripmap.com/0.1/en/places/geoname"
        geo_resp = requests.get(geoname_url, params={"name": city_name, "apikey": OPENTRIPMAP_API_KEY})
        geo_data = geo_resp.json()
        lat = geo_data.get("lat")
        lon = geo_data.get("lon")

        if not lat or not lon:
            return {"error": f"לא נמצאו קואורדינטות עבור {city_name}"}

        places_url = "https://api.opentripmap.com/0.1/en/places/radius"
        places_params = {
            "apikey": OPENTRIPMAP_API_KEY,
            "radius": 10000,
            "lon": lon,
            "lat": lat,
            "limit": limit,
            "format": "json"
        }

        resp = requests.get(places_url, params=places_params)
        raw_places = resp.json()

        cleaned_places = []
        for place in raw_places:
            cleaned_places.append({
                "xid": place.get("xid"),
                "name": place.get("name") or "לא צויין",
                "category": place.get("kinds", "").split(",")[0],
                "distance_meters": round(place.get("dist", 0))
            })

        return cleaned_places

    except Exception as e:
        return {"error": str(e)}


# פונקציה זו מחזירה מסלול בין שתי נקודות
def get_route(start_coords: tuple, end_coords: tuple, profile: str = "driving-car"):
    try:
        url = f"https://api.openrouteservice.org/v2/directions/{profile}"
        headers = {
            "Authorization": OPENROUTESERVICE_API_KEY,
            "Content-Type": "application/json"
        }
        body = {"coordinates": [list(start_coords), list(end_coords)]}
        response = requests.post(url, json=body, headers=headers)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


# הפונקציה הראשית – מחזירה אתרים בעיר עם מסלולים אליהם
def get_sites_with_routes(city_name: str, start_address: str, profile: str = "driving-car", limit: int = 50):
    start_coords = geocode_address(start_address)
    if isinstance(start_coords, dict) and "error" in start_coords:
        return start_coords

    places = get_places_in_city(city_name, limit)
    if isinstance(places, dict) and "error" in places:
        return places

    geoname_url = "https://api.opentripmap.com/0.1/en/places/geoname"
    geo_resp = requests.get(geoname_url, params={"name": city_name, "apikey": OPENTRIPMAP_API_KEY})
    geo_data = geo_resp.json()
    city_lat = geo_data.get("lat")
    city_lon = geo_data.get("lon")

    if not city_lat or not city_lon:
        return {"error": f"לא ניתן לחשב מסלול עבור {city_name}"}

    enriched_places = []
    for place in places:
        details = get_place_details(place["xid"]) if place.get("xid") else {}

        end_coords = (city_lon, city_lat)  # כרגע למסלול – מרכז העיר
        route = get_route(start_coords, end_coords, profile)

        enriched_places.append({
            "place": {
                "name": place["name"],
                "category": place["category"],
                "distance_meters": place["distance_meters"],
                "rating": details.get("rating"),
                "image": details.get("image"),
                "description": details.get("description")
            },
            "route": route
        })

    return enriched_places
