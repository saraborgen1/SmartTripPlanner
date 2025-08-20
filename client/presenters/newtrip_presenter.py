# from services import api_client
# from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton


# class NewTripPresenter:
#     def __init__(self, view):
#         self.view = view
#         self.sites = []

#     def load_sites(self, city, address, profile):
#         try:
#             sites = api_client.get_sites(city=city, address=address, profile=profile)
#             self.sites = sites
#             self.view.show_sites(sites)
#         except Exception as e:
#             self.view.show_error(f"שגיאה בשליפת אתרים: {e}")

#     def show_site_details(self, index):
#         site = self.sites[index]
#         place = site.get("place", {})

#         dialog = QDialog(self.view)
#         dialog.setWindowTitle(place.get("name", "פירוט אתר"))

#         layout = QVBoxLayout()
#         layout.addWidget(QLabel(f"שם האתר: {place.get('name', '---')}"))
#         layout.addWidget(QLabel(f"קטגוריה: {place.get('category', '---')}"))

#         # כפתור פלוס להוספה לרשימה
#         add_btn = QPushButton("➕ הוסף לרשימת האטרקציות שלי")
#         add_btn.clicked.connect(lambda: self.view.add_site_to_my_list(place.get("name", "---")))
#         layout.addWidget(add_btn)

#         dialog.setLayout(layout)
#         dialog.exec()

#     def save_trip(self, username, start, end, city, has_car, selected_sites):
#         try:
#             trip_data = {
#                 "username": username,
#                 "destination": city,
#                 "start_date": start,
#                 "end_date": end,
#                 "selected_sites": selected_sites,
#                 "transport": ["car"] if has_car else ["public"],
#                 "notes": ""
#             }
#             api_client.create_trip(trip_data)
#             self.view.show_message("הטיול נשמר בהצלחה!")
#         except Exception as e:
#             self.view.show_error(f"שגיאה בשמירת טיול: {e}")

from client.services import api_client
from server.services.weather_service import get_weather_forecast
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton


class NewTripPresenter:
    def __init__(self, view):
        self.view = view
        self.sites = []

    def load_sites(self, city, address, profile):
        try:
            sites = api_client.get_sites(city=city, address=address, profile=profile)
            self.sites = sites
            self.view.show_sites(sites)
        except Exception as e:
            self.view.show_error(f"שגיאה בשליפת אתרים: {e}")

    def show_site_details(self, index):
        site = self.sites[index]
        place = site.get("place", {})

        dialog = QDialog(self.view)
        dialog.setWindowTitle(place.get("name", "פירוט אתר"))

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"שם האתר: {place.get('name', '---')}"))
        layout.addWidget(QLabel(f"קטגוריה: {place.get('category', '---')}"))

        # כפתור פלוס להוספה לרשימה
        add_btn = QPushButton("➕ הוסף לרשימת האטרקציות שלי")
        add_btn.clicked.connect(lambda: self.view.add_site_to_my_list(place.get("name", "---")))
        layout.addWidget(add_btn)

        dialog.setLayout(layout)
        dialog.exec()

    def save_trip(self, username, start, end, city, has_car, selected_sites):
        try:
            trip_data = {
                "username": username,
                "destination": city,
                "start_date": start,
                "end_date": end,
                "selected_sites": selected_sites,
                "transport": ["car"] if has_car else ["public"],
                "notes": ""
            }
            api_client.create_trip(trip_data)
            self.view.show_message("הטיול נשמר בהצלחה!")
        except Exception as e:
            self.view.show_error(f"שגיאה בשמירת טיול: {e}")

    # ===== חיבור למזג אוויר =====
    def update_weather(self, city):
        try:
            forecast = get_weather_forecast(city)
            self.view.show_weather(forecast)
        except Exception as e:
            self.view.show_weather({"error": f"שגיאה בקבלת תחזית: {e}"})
