# # client/presenters/newtrip_presenter.py
# from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
# from client.services import api_client


# class NewTripPresenter:
#     """
#     מחלקת
#     Presenter
#     שאחראית על מסך יצירת טיול חדש.

#     התפקיד שלה:
#     - לטעון את רשימת האתרים מהשרת דרך ה־
#     API Client
#     - להציג פרטי אתר בחלון
#     Dialog
#     - לשמור טיול חדש בשרת (קריאה ל־
#     API
#     )
#     - לעדכן תחזית מזג אוויר דרך ה־
#     API
#     """

#     def __init__(self, view):
#         # שמירה של ה־
#         # View
#         # שמחובר לפרזנטר הזה
#         self.view = view

#         # כאן נשמור את רשימת האתרים מהשרת
#         self.sites = []

#         # חיבור כפתורים מה־
#         # View
#         # (אם קיימים בשכבת התצוגה)
#         if hasattr(self.view, "create_btn"):
#             self.view.create_btn.clicked.connect(self._on_create_clicked)
#         if hasattr(self.view, "refresh_weather_btn"):
#             self.view.refresh_weather_btn.clicked.connect(self._on_refresh_weather)

#     # ===== אתרים לחיפוש =====
#     def load_sites(self, city, address, profile):
#         """
#         שולחת בקשה לשירות דרך ה־
#         API Client
#         כדי לקבל אתרים בעיר נתונה
#         + חישובי מסלול בהתאם ל־
#         profile
#         .
#         """
#         try:
#             sites = api_client.get_sites(city=city, address=address, profile=profile)
#             self.sites = sites or []
#             self.view.show_sites(self.sites)
#         except Exception as e:
#             # כל הודעת משתמש — באנגלית
#             self.view.show_error(f"Failed to load sites: {e}")

#     def show_site_details(self, index: int):
#         """
#         מציגה חלון
#         Dialog
#         עם פרטי אתר שנבחר,
#         כולל כפתור להוספה לרשימת האטרקציות של המשתמש.
#         """
#         if index < 0 or index >= len(self.sites):
#             return

#         site = self.sites[index]
#         place = site.get("place", {})
#         name = place.get("name", "---")
#         category = place.get("category", "---")

#         dialog = QDialog(self.view)
#         dialog.setWindowTitle(name or "Site details")

#         layout = QVBoxLayout()
#         layout.addWidget(QLabel(f"Site name: {name}"))
#         layout.addWidget(QLabel(f"Category: {category}"))

#         add_btn = QPushButton("➕ Add to My Attractions")

#         def on_add():
#             # מוסיף לרשימה ב־
#             # View
#             self.view.add_site_to_my_list(name or "---")
#             # סוגר את ה־
#             # Dialog
#             dialog.accept()

#         add_btn.clicked.connect(on_add)
#         layout.addWidget(add_btn)

#         dialog.setLayout(layout)
#         dialog.exec()

#     # ===== שמירת טיול =====
#     def save_trip(self, username, start, end, city, transport, selected_sites):
#         """
#         שומר טיול חדש בשרת דרך ה־
#         API Client
#         .
#         הפרמטר
#         transport
#         צפוי להיות רשימה:
#         ["car"] /
#         ["foot"] /
#         ["bike"]
#         .
#         """
#         try:
#             trip_data = {
#                 "username": username,
#                 "destination": city,
#                 "start_date": start,
#                 "end_date": end,
#                 "selected_sites": selected_sites,
#                 "transport": transport,
#                 "notes": ""
#             }
#             api_client.create_trip(trip_data)
#             self.view.show_message("Trip saved successfully!")
#         except Exception as e:
#             self.view.show_error(f"Error saving trip: {e}")

#     # ===== מזג אוויר (דרך השרת) =====
#     def update_weather(self, city: str):
#         """
#         מבקשת תחזית מזג אוויר לעיר דרך ה־
#         API Client
#         (קריאה אל שרת ה־
#         FastAPI
#         שלך).
#         """
#         try:
#             forecast = api_client.get_weather(city)
#             self.view.show_weather(forecast)
#         except Exception as e:
#             self.view.show_weather({"error": f"Failed to fetch forecast: {e}"})

#     # ===== חיבורי כפתורים אופציונליים מה־View =====
#     def _on_create_clicked(self):
#         """
#         מופעל אם ה־
#         View
#         מספק פונקציה בשם
#         collect_form
#         שמחזירה מילון נתונים.
#         """
#         if hasattr(self.view, "collect_form"):
#             data = self.view.collect_form()

#             # תמיכה בשני פורמטים:
#             # 1) transport  -> למשל ["car"]
#             # 2) has_car    -> bool (נמיר לרשימת transport)
#             transport = data.get("transport")
#             if transport is None:  # לא סופק transport, ננסה לגזור מ־has_car
#                 has_car = bool(data.get("has_car"))
#                 transport = ["car"] if has_car else ["foot"]

#             self.save_trip(
#                 username=data["username"],
#                 start=data["start_date"],
#                 end=data["end_date"],
#                 city=data["destination"],
#                 transport=transport,
#                 selected_sites=data["selected_sites"],
#             )

#     def _on_refresh_weather(self):
#         """
#         רענון תחזית מהיר לפי ערך שנמצא בשדה קלט של ה־
#         View
#         (אם קיים).
#         """
#         if hasattr(self.view, "destination_edit"):
#             city = (self.view.destination_edit.text() or "").strip()
#             if city:
#                 self.update_weather(city)


# client/presenters/newtrip_presenter.py
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from client.services import api_client


class NewTripPresenter:
    """
    מחלקת
    Presenter
    שאחראית על מסך יצירת טיול חדש.

    התפקיד שלה:
    - לטעון את רשימת האתרים מהשרת דרך ה־
    API Client
    - להציג פרטי אתר בחלון
    Dialog
    - לשמור טיול חדש בשרת (קריאה ל־
    API
    )
    - לעדכן תחזית מזג אוויר דרך ה־
    API
    """

    def __init__(self, view):
        # שמירה של ה־
        # View
        # שמחובר לפרזנטר הזה
        self.view = view

        # כאן נשמור את רשימת האתרים מהשרת
        self.sites = []

        # חיבור כפתורים מה־
        # View
        # (אם קיימים בשכבת התצוגה)
        if hasattr(self.view, "create_btn"):
            self.view.create_btn.clicked.connect(self._on_create_clicked)
        if hasattr(self.view, "refresh_weather_btn"):
            self.view.refresh_weather_btn.clicked.connect(self._on_refresh_weather)

    # ===== אתרים לחיפוש =====
    def load_sites(self, city, address, profile, limit=50):#self, city, address, profile):
        """
        שולחת בקשה לשירות דרך ה־
        API Client
        כדי לקבל אתרים בעיר נתונה
        + חישובי מסלול בהתאם ל־
        profile
        .
        """

        try:
            sites = api_client.get_sites(city=city, address=address, profile=profile, limit=limit)
            self.sites = sites or []
            self.view.show_sites(self.sites)
        except Exception as e:
            self.view.show_error(f"Failed to load sites: {e}")

    def show_site_details(self, index: int):
        """
        מציגה חלון
        Dialog
        עם פרטי אתר שנבחר,
        כולל כפתור להוספה לרשימת האטרקציות של המשתמש.
        """

        if index < 0 or index >= len(self.sites):
            return

        site = self.sites[index]
        place = site.get("place", {})
        name = place.get("name", "---")
        category = place.get("category", "---")
        rating = place.get("rating") or "N/A"
        description = place.get("description") or "No description available."
        image_url = place.get("image")

        dialog = QDialog(self.view)
        dialog.setWindowTitle(name or "Site details")

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Site name: {name}"))
        layout.addWidget(QLabel(f"Category: {category}"))
        layout.addWidget(QLabel(f"Rating: {rating}"))
        layout.addWidget(QLabel(description))

        if image_url:
            from PySide6.QtGui import QPixmap
            from urllib.request import urlopen
            try:
                data = urlopen(image_url).read()
                pixmap = QPixmap()
                pixmap.loadFromData(data)
                img_label = QLabel()
                img_label.setPixmap(pixmap.scaledToWidth(250, Qt.SmoothTransformation))
                layout.addWidget(img_label)
            except Exception:
                pass

        add_btn = QPushButton("➕ Add to My Attractions")
        add_btn.clicked.connect(lambda: (self.view.add_site_to_my_list(name or "---"), dialog.accept()))
        layout.addWidget(add_btn)

        dialog.setLayout(layout)
        dialog.exec()

    # ===== שמירת טיול =====
    def save_trip(self, username, start, end, city, transport, selected_sites):
        """
        שומר טיול חדש בשרת דרך ה־
        API Client
        .
        הפרמטר
        transport
        צפוי להיות רשימה:
        ["car"] /
        ["foot"] /
        ["bike"]
        .
        """
        try:
            trip_data = {
                "username": username,
                "destination": city,
                "start_date": start,
                "end_date": end,
                "selected_sites": selected_sites,
                "transport": transport,
                "notes": ""
            }
            api_client.create_trip(trip_data)
            self.view.show_message("Trip saved successfully!")
        except Exception as e:
            self.view.show_error(f"Error saving trip: {e}")

    # ===== מזג אוויר (דרך השרת) =====
    def update_weather(self, city: str):
        """
        מבקשת תחזית מזג אוויר לעיר דרך ה־
        API Client
        (קריאה אל שרת ה־
        FastAPI
        שלך).
        """
        try:
            forecast = api_client.get_weather(city)
            self.view.show_weather(forecast)
        except Exception as e:
            self.view.show_weather({"error": f"Failed to fetch forecast: {e}"})

    # ===== חיבורי כפתורים אופציונליים מה־View =====
    def _on_create_clicked(self):
        """
        מופעל אם ה־
        View
        מספק פונקציה בשם
        collect_form
        שמחזירה מילון נתונים.
        """
        if hasattr(self.view, "collect_form"):
            data = self.view.collect_form()

            # תמיכה בשני פורמטים:
            # 1) transport  -> למשל ["car"]
            # 2) has_car    -> bool (נמיר לרשימת transport)
            transport = data.get("transport")
            if transport is None:  # לא סופק transport, ננסה לגזור מ־has_car
                has_car = bool(data.get("has_car"))
                transport = ["car"] if has_car else ["foot"]

            self.save_trip(
                username=data["username"],
                start=data["start_date"],
                end=data["end_date"],
                city=data["destination"],
                transport=transport,
                selected_sites=data["selected_sites"],
            )

    def _on_refresh_weather(self):
        """
        רענון תחזית מהיר לפי ערך שנמצא בשדה קלט של ה־
        View
        (אם קיים).
        """
        if hasattr(self.view, "destination_edit"):
            city = (self.view.destination_edit.text() or "").strip()
            if city:
                self.update_weather(city)
