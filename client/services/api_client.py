import requests
from utils.constants import BASE_URL

def get_trips(city: str, address: str = "Default Address", profile: str = "driving-car"):
    """מחזיר רשימת טיולים משרת FastAPI"""
    try:
        response = requests.get(f"{BASE_URL}/get_sites", params={
            "city": city,
            "address": address,
            "profile": profile
        })
        response.raise_for_status()
        return response.json()  # רשימת טיולים
    except Exception as e:
        print(f"Error fetching trips: {e}")
        return []
