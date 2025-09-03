# client/presenters/newtrip_presenter.py

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from client.services import api_client

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
class NewTripPresenter:
 
    def __init__(self, view, session_manager):
        # שמירה של ה־
        # View
        # שמחובר לפרזנטר הזה
        self.view = view

        # שמירה של מנהל הסשן –  
        # session_manager
        self.session_manager = session_manager  

        # כאן נשמור את רשימת האתרים מהשרת
        self.sites = []

        # חיבור כפתורים מה־
        # View
        # (אם קיימים בשכבת התצוגה)
        if hasattr(self.view, "create_btn"):
            self.view.create_btn.clicked.connect(self._on_create_clicked)
        if hasattr(self.view, "refresh_weather_btn"):
            self.view.refresh_weather_btn.clicked.connect(self._on_refresh_weather)


    """
        שולחת בקשה לשירות דרך ה־
        API Client  
        כדי לקבל אתרים בעיר נתונה
        וחישובי מסלול בהתאם ל־
        profile.
    """
    def load_sites(self, city, address, profile, limit=20):
     
        try:
            sites = api_client.get_sites(city=city, address=address, profile=profile, limit=limit)
            self.sites = sites or []
            self.view.show_sites(self.sites)
        except Exception as e:
            self.view.show_error(f"Failed to load sites: {e}")


    """
        מציגה חלון  
        Dialog  
        עם פרטי אתר שנבחר,
        כולל כפתור להוספה לרשימת האטרקציות של המשתמש.
    """
    def show_site_details(self, index: int):
   
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

        # אם יש תמונה – נציג אותה בחלון
        if image_url:
            from PySide6.QtGui import QPixmap
            from PySide6.QtCore import Qt
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

        # כפתור הוספה לרשימת האטרקציות
        add_btn = QPushButton("➕ Add to My Attractions")
        add_btn.clicked.connect(lambda: (self.view.add_site_to_my_list(name or "---"), dialog.accept()))
        layout.addWidget(add_btn)

        dialog.setLayout(layout)
        dialog.exec()

        
    """
    שמירה או עדכון של טיול חדש דרך השרת.
    """
    def save_trip(self, username, start, end, city, transport, selected_sites,
                  notes: str = "", on_success=None, trip_id=None):

        token = self.session_manager.user_token
        if not token:
            self.view.show_error("User is not logged in. Please log in first.")
            return

        try:
            trip_data = {
                "username": username,
                "destination": city,
                "start_date": start,
                "end_date": end,
                "selected_sites": [str(site) for site in selected_sites],
                "transport": [str(t) for t in (transport or [])],
                "notes": notes or ""
            }

            # אם יש trip_id → עדכון
            if trip_id:  
                api_client.update_trip(trip_id, trip_data, token=token)
                self.view.show_message("Trip updated successfully!")
            # יצירת טיול חדש
            else:       
                api_client.create_trip(trip_data, token=token)
                self.view.show_message("Trip created successfully!")

            if on_success:
                on_success()

        except Exception as e:
            self.view.show_error(f"Error saving trip: {e}")


    """
    מבקשת תחזית מזג אוויר לעיר דרך ה־
    API Client  
    (קריאה אל שרת ה־
    FastAPI).
    """
    def update_weather(self, city: str):
  
        try:
            forecast = api_client.get_weather(city)
            self.view.show_weather(forecast)
        except Exception as e:
            self.view.show_weather({"error": f"Failed to fetch forecast: {e}"})


    """
        מופעל אם ה־
        View  
        מספק פונקציה בשם  
        collect_form  
        שמחזירה מילון נתונים.
    """
    def _on_create_clicked(self):
     
        if hasattr(self.view, "collect_form"):
            data = self.view.collect_form()

            # תמיכה בשני פורמטים:
            # 1) transport  -> למשל ["car"]
            # 2) has_car    -> bool (נמיר לרשימת transport)
            transport = data.get("transport")
            if transport is None:  
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


    """
    רענון תחזית לפי ערך שנמצא בשדה קלט של ה־
    View  
    (אם קיים).
    """
    def _on_refresh_weather(self):
   
        if hasattr(self.view, "destination_edit"):
            city = (self.view.destination_edit.text() or "").strip()
            if city:
                self.update_weather(city)