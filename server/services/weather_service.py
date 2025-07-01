import requests

WEATHER_API_KEY = "acecc3119b344218b41132502250107"

def get_weather_forecast(city_name: str):
    url = "http://api.weatherapi.com/v1/forecast.json"
    params = {
        "key": WEATHER_API_KEY,
        "q": city_name,
        "days": 7,
        "aqi": "no",
        "alerts": "no"
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"שגיאה בקבלת נתונים: {response.status_code}")
        print(response.text)
        return {"error": "שגיאה בקבלת נתוני מזג האוויר."}

    data = response.json()

    forecast = []
    for day in data["forecast"]["forecastday"]:
        forecast.append({
            "date": day["date"],
            "temp_min": day["day"]["mintemp_c"],
            "temp_max": day["day"]["maxtemp_c"]
        })

    return {
        "destination": city_name,
        "forecast": forecast
    }
