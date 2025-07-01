import requests

API_KEY = "5ae2e3f221c38a28845f05b6b33b5e6712dcb459cd56890412563af3"

def get_places_in_city(city_name: str, limit: int = 5):
    try:
        # שלב 1: קבלת קואורדינטות של העיר
        geoname_url = f"https://api.opentripmap.com/0.1/en/places/geoname"
        geo_resp = requests.get(geoname_url, params={"name": city_name, "apikey": API_KEY})
        geo_data = geo_resp.json()
        lat = geo_data.get("lat")
        lon = geo_data.get("lon")

        if not lat or not lon:
            return {"error": f"לא נמצאו קואורדינטות עבור {city_name}"}

        # שלב 2: חיפוש אתרים לפי קואורדינטות
        places_url = f"https://api.opentripmap.com/0.1/en/places/radius"
        places_params = {
            "apikey": API_KEY,
            "radius": 10000,
            "lon": lon,
            "lat": lat,
            "limit": limit,
            "format": "json"
        }

        resp = requests.get(places_url, params=places_params)
        raw_places = resp.json()

        # שלב 3: עיבוד וסינון מידע
        cleaned_places = []
        for place in raw_places:
            cleaned_places.append({
                "name": place.get("name") or "לא צויין",
                "category": place.get("kinds", "").split(",")[0],
                "distance_meters": round(place.get("dist", 0))
            })

        return cleaned_places

    except Exception as e:
        return {"error": str(e)}
