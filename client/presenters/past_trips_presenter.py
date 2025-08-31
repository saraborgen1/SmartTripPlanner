# client/presenters/past_trips_presenter.py

from typing import List, Dict
import requests
from client.services import api_client
from PySide6.QtWidgets import QMessageBox
from client.views.trip_detail_view import TripDetailView


class PastTripsPresenter:
    """ Presenter האחראי על מסך 'All Trips' (טיולים קודמים).
        מנהל את התקשורת בין ה-View לבין ה-API.
    """

    def __init__(self, view, session_manager):
        # שמירת ה-View
        self.view = view
        # מנהל הסשן (שומר את פרטי המשתמש)
        self.session = session_manager
        # שמירה על חלון פרטי הטיול כדי למנוע סגירה מוקדמת
        self._detail_win = None

        # חיבור אירועים מה-View
        self.view.refresh_btn.clicked.connect(self.refresh)
        self.view.trips_list.itemDoubleClicked.connect(self.open_detail)

    def refresh(self):
        """ טוען מחדש את רשימת הטיולים של המשתמש מהשרת ומעדכן את המסך. """
        if not self.session.is_logged_in():
            QMessageBox.warning(self.view, "Not logged in", "Please log in first.")
            return

        # שם המשתמש
        username = self.session.username
        # מציג את שם המשתמש במסך
        self.view.set_username(username)

        try:
            # בקשה לשרת לקבלת הטיולים של המשתמש
            trips: List[Dict] = api_client.get_my_trips(username)
        except requests.RequestException as e:
            QMessageBox.critical(self.view, "Error", f"Failed to fetch trips: {e}")
            return

        # עדכון הרשימה במסך
        self.view.set_trips(trips)

    def open_detail(self, item):
        """ נפתח בלחיצה כפולה על טיול. מציג חלון חדש עם פרטי הטיול. """
        trip = item.data(self.view.trips_list.UserRole)

        # אם זה לא טיול אמיתי - לא עושים כלום
        if not isinstance(trip, dict) or trip.get("empty"):
            return

        # פתיחת חלון פרטי הטיול
        self._detail_win = TripDetailView(trip)
        self._detail_win.show()
