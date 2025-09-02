# client/presenters/past_trips_presenter.py

from typing import List, Dict
import requests
from client.services import api_client
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt
from client.views.trip_detail_view import TripDetailView

""" 
    Presenter
    האחראי על מסך 
    'All Trips' (טיולים קודמים).
    מנהל את התקשורת בין ה-
    View 
    לבין ה-
    API.
"""
class PastTripsPresenter:
  

    def __init__(self, view, session_manager):
        # שמירת ה-View
        self.view = view
        # מנהל הסשן (שומר את פרטי המשתמש)
        self.session = session_manager
        # חלון פרטי טיול נפרד – נשמור כאן כדי שלא ייסגר מיד
        self._detail_win = None
        # חיבור כפתור רענון במסך לפונקציה refresh
        self.view.refresh_btn.clicked.connect(self.refresh)
        # חיבור לחיצה כפולה על טיול ברשימה לפתיחת פרטי הטיול
        self.view.trips_list.itemDoubleClicked.connect(self.open_detail)


    """ 
        טוען מחדש את רשימת הטיולים של המשתמש מהשרת ומעדכן את התצוגה במסך.
    """
    def refresh(self):
        # בדיקה שהמשתמש מחובר
        if not self.session.is_logged_in():
            QMessageBox.warning(self.view, "Not logged in", "Please log in first.")
            return

        username = self.session.username
        self.view.set_username(username)

        try:
            # בקשה לשרת לקבלת הטיולים של המשתמש
            trips: List[Dict] = api_client.get_my_trips(username)
        except requests.RequestException as e:
            QMessageBox.critical(self.view, "Error", f"Failed to fetch trips: {e}")
            return

        # עדכון הרשימה במסך
        self.view.set_trips(trips)


    """ 
        מופעל כשמשתמש לוחץ פעמיים על טיול ברשימה. 
        פותח חלון חדש עם פרטי הטיול.
    """
    def open_detail(self, item):
        trip = item.data(Qt.UserRole)


        # אם זה לא טיול אמיתי - לא עושים כלום
        if not isinstance(trip, dict) or trip.get("empty"):
            return

        # פתיחת חלון פרטי הטיול
        self._detail_win = TripDetailView(trip)
        self._detail_win.show()
