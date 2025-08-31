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

        image_url = data.get("preview", {}).get("source")
        image_info = None
        if image_url:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/120.0.0.0 Safari/537.36"
            }
            image_info = {"url": image_url, "headers": headers}

        return {
            "rating": data.get("rate"),
            "image": image_info,
            "description": data.get("wikipedia_extracts", {}).get("text", "")
        }
    except Exception:
        return {}


# פונקציה זו מחפשת אתרים בעיר נתונה ומחזירה רשימה של אתרים עם פרטים בסיסיים
def get_places_in_city(city_name: str, limit: int = 20):  # ברירת מחדל 50 תוצאות
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
        # מדלגים על אתרים בלי שם
            if not place.get("name"):
                continue

            cleaned_places.append({
                "xid": place.get("xid"),
                "name": place.get("name"),
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
def get_sites_with_routes(city_name: str, start_address: str, profile: str = "driving-car", limit: int = 20):
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
