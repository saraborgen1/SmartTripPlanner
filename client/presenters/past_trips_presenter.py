#client/presenters/past_trips_presenter.py
from typing import List, Dict
import requests
from client.services import api_client
from PySide6.QtWidgets import QMessageBox
from client.views.trip_detail_view import TripDetailView


class PastTripsPresenter:
    """
    מחלקת  
    Presenter  

    אחראית על מסך **All Trips**.  

    התפקיד שלה:
    - לטעון את רשימת הטיולים מהשרת דרך  
      API Client  
    - להציג אותם ב־  
      View  
    - לפתוח חלון של פרטי טיול (  
      TripDetailView  
      ) כשמשתמש לוחץ פעמיים על טיול מסוים
    """

    def __init__(self, view, session_manager):
        # שמירה של ה־View
        self.view = view

        # שמירה של מנהל הסשן (כדי לדעת אם המשתמש מחובר ומי המשתמש)
        self.session = session_manager

        # שמירה של חלון פרטי טיול שנפתח
        # כדי שלא ייסגר מיידית על ידי ה־Garbage Collector
        self._detail_win = None  

        # חיבור אירועים מה־View
        # כפתור רענון מחובר לפונקציה refresh
        self.view.refresh_btn.clicked.connect(self.refresh)

        # לחיצה כפולה על פריט ברשימה פותחת פרטי טיול
        self.view.trips_list.itemDoubleClicked.connect(self.open_detail)

    def refresh(self):
        """
        טוענת מחדש את רשימת הטיולים של המשתמש מהשרת
        ומעדכנת את המסך.
        """
        if not self.session.is_logged_in():
            QMessageBox.warning(self.view, "Not logged in", "Please log in first.")
            return

        # שם המשתמש המחובר
        username = self.session.username

        # מציג את שם המשתמש במסך
        self.view.set_username(username)

        # מנקה רשימת טיולים ישנה
        self.view.clear_list()

        try:
            # בקשת הטיולים מהשרת דרך ה־API Client
            trips: List[Dict] = api_client.get_my_trips(username)
        except requests.RequestException as e:
            QMessageBox.critical(self.view, "Error", f"Failed to fetch trips: {e}")
            return

        # אם לא נמצאו טיולים
        if not trips:
            self.view.add_trip_item("No trips found for this user.", {"empty": True})
            return

        # יצירת שורת תיאור נעימה לכל טיול
        for t in trips:
            dest = t.get("destination", "Unknown")
            start = t.get("start_date", "?")
            end   = t.get("end_date", "?")
            notes = t.get("notes") or ""

            # מחרוזת: יעד | תאריכים | הערות
            line = f"{dest}  |  {start} → {end}" + (f"  —  {notes}" if notes else "")

            # הוספה לרשימה ב־View
            self.view.add_trip_item(line, t)

    def open_detail(self, item):
        """
        נפתחת בלחיצה כפולה על טיול.
        מציגה חלון חדש עם פרטי הטיול שנבחר.
        """
        trip = item.data(self.view.trips_list.UserRole)

        # אם זה לא טיול אמיתי (או הודעה ריקה) — לא לעשות כלום
        if not isinstance(trip, dict) or trip.get("empty"):
            return

        # יצירת חלון פרטי טיול חדש והצגתו
        self._detail_win = TripDetailView(trip)
        self._detail_win.show()
