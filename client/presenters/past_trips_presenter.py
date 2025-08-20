from typing import List, Dict
import requests
from client.services import api_client
from PySide6.QtWidgets import QMessageBox
from client.views.trip_detail_view import TripDetailView

class PastTripsPresenter:
    """
    שולט במסך 'כל הטיולים' — טוען את הטיולים מהשרת ומציגם.
    לחיצה כפולה על פריט פותחת חלון פרטי טיול.
    """
    def __init__(self, view, session_manager):
        self.view = view
        self.session = session_manager
        self._detail_win = None  # שמירה כדי שלא ייסגר מיד

        # חיבור אירועים
        self.view.refresh_btn.clicked.connect(self.refresh)
        self.view.trips_list.itemDoubleClicked.connect(self.open_detail)

    def refresh(self):
        if not self.session.is_logged_in():
            QMessageBox.warning(self.view, "Not logged in", "אנא התחברי קודם.")
            return

        username = self.session.username
        self.view.set_username(username)
        self.view.clear_list()

        try:
            trips: List[Dict] = api_client.get_my_trips(username)
        except requests.RequestException as e:
            QMessageBox.critical(self.view, "Error", f"שגיאה בשליפת טיולים: {e}")
            return

        if not trips:
            self.view.add_trip_item("לא נמצאו טיולים עבור המשתמש.", {"empty": True})
            return

        # בניית שורת תיאור נעימה לכל טיול
        for t in trips:
            dest = t.get("destination", "Unknown")
            start = t.get("start_date", "?")
            end   = t.get("end_date", "?")
            notes = t.get("notes") or ""
            line = f"{dest}  |  {start} → {end}" + (f"  —  {notes}" if notes else "")
            self.view.add_trip_item(line, t)

    def open_detail(self, item):
        trip = item.data(self.view.trips_list.UserRole)
        if not isinstance(trip, dict) or trip.get("empty"):
            return
        self._detail_win = TripDetailView(trip)
        self._detail_win.show()
