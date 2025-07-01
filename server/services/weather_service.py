def get_fake_weather_data(city: str):
    # טמפרטורות פיקטיביות (אפשר לשנות לפי יעד)
    fake_data = {
        "destination": city,
        "monthly_temperatures": [
            {"month": "ינואר", "temp": 5},
            {"month": "פברואר", "temp": 7},
            {"month": "מרץ", "temp": 10},
            {"month": "אפריל", "temp": 15},
            {"month": "מאי", "temp": 19},
            {"month": "יוני", "temp": 23},
            {"month": "יולי", "temp": 26},
            {"month": "אוגוסט", "temp": 25},
            {"month": "ספטמבר", "temp": 21},
            {"month": "אוקטובר", "temp": 16},
            {"month": "נובמבר", "temp": 10},
            {"month": "דצמבר", "temp": 6}
        ]
    }
    return fake_data
