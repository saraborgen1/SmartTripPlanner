# # client/main.py
# import sys
# from PySide6.QtWidgets import QApplication, QStackedWidget, QMessageBox

# # Session
# from client.utils.session import SessionManager

# # --- Views ---
# from client.views.main_view import MainView                 # Home
# from client.views.login_view import LoginView               # Login/Register combined
# from client.views.dashboard_view import DashboardView       # Dashboard after login
# from client.views.past_trips_view import PastTripsView      # All trips (has Back)
# from client.views.trip_detail_view import TripDetailView    # Trip details popup
# from client.views.ai_consult_view import AIChatView         # AI chat view
# from client.views.newtrip_view import NewTripView           # Create New Trip view

# # --- Presenters ---
# from client.presenters.main_presenter import MainPresenter
# from client.presenters.dashboard_presenter import DashboardPresenter
# from client.presenters.past_trips_presenter import PastTripsPresenter
# from client.presenters.ai_consult_presenter import AIChatPresenter
# from client.presenters.newtrip_presenter import NewTripPresenter

# # --- Services/Utils ---
# from client.services import api_client
# from client.utils.trip_select import select_current_or_next


# class App(QStackedWidget):
#     """
#     Navigation between:
#       0) MainView (Home)
#       1) LoginView (Login/Register)
#       2) DashboardView (after login)
#       3) PastTripsView (all trips)
#       4) AIChatView (chat with AI)
#       5) NewTripView (create new trip)
#     """
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Smart Trip Planner")
#         self.setFixedSize(560, 420)

#         # Session state
#         self.session = SessionManager()

#         # --- Create views ---
#         self.main_view = MainView(go_to_auth_callback=self.show_login)

#         self.login_view = LoginView(
#             go_to_main_view_callback=self.on_login_success,  # called after successful login
#             go_to_register_view_callback=None,               # combined screen
#             session_manager=self.session,
#         )

#         self.dashboard_view = DashboardView()
#         self.past_trips_view = PastTripsView()
#         self.ai_chat_view = AIChatView(back_callback=self.show_dashboard)

#         # Create New Trip view (+ presenter). Back → dashboard
#         self.newtrip_view = NewTripView(username=None, back_callback=self.show_dashboard)
#         self.newtrip_presenter = NewTripPresenter(self.newtrip_view)

#         # --- Wire presenters ---
#         self.main_presenter = MainPresenter(
#             view=self.main_view,
#             session_manager=self.session,
#             go_to_auth=self.show_login,
#         )

#         self.dashboard_presenter = DashboardPresenter(
#             view=self.dashboard_view,
#             session_manager=self.session,
#             on_current_trip=self.go_to_current_trip,
#             on_past_trips=self.go_to_past_trips,
#             on_new_trip=self.go_to_new_trip,
#             on_ai_chat=self.show_ai_chat,
#         )

#         self.past_trips_presenter = PastTripsPresenter(
#             view=self.past_trips_view,
#             session_manager=self.session,
#         )

#         self.ai_chat_presenter = AIChatPresenter(self.ai_chat_view)

#         # Back button in "All trips" → Dashboard
#         self.past_trips_view.back_btn.clicked.connect(self.show_dashboard)

#         # --- Add to stacked widget ---
#         self.addWidget(self.main_view)        # index 0
#         self.addWidget(self.login_view)       # index 1
#         self.addWidget(self.dashboard_view)   # index 2
#         self.addWidget(self.past_trips_view)  # index 3
#         self.addWidget(self.ai_chat_view)     # index 4
#         self.addWidget(self.newtrip_view)     # index 5

#         # ---- AI button callback hookup (if views expose set_ai_callback) ----
#         for v in (self.main_view, self.login_view, self.dashboard_view,
#                   self.past_trips_view, self.newtrip_view, self.ai_chat_view):
#             if hasattr(v, "set_ai_callback"):
#                 v.set_ai_callback(self.show_ai_chat)

#         # Start at home
#         self.setCurrentWidget(self.main_view)

#         # Keep a reference for detail window (avoid GC)
#         self._current_trip_window = None

#     # ---------- Navigation ----------
#     def show_home(self):
#         self.setCurrentWidget(self.main_view)

#     def show_login(self):
#         self.setCurrentWidget(self.login_view)

#     def show_dashboard(self):
#         # Update greeting with username (if exists)
#         if getattr(self.session, "username", None):
#             self.dashboard_view.set_username(self.session.username)
#         self.setCurrentWidget(self.dashboard_view)

#     def show_ai_chat(self):
#         self.setCurrentWidget(self.ai_chat_view)

#     # ---------- After successful login ----------
#     def on_login_success(self, token: str, username: str):
#         self.session.login(token, username)
#         # sync username into NewTripView (used when saving a trip)
#         self.newtrip_view.username = username
#         self.show_dashboard()

#     # ---------- Dashboard actions ----------
#     def go_to_current_trip(self):
#         """Show a trip happening today, or the nearest upcoming one."""
#         if not self.session.is_logged_in():
#             QMessageBox.warning(self, "Not logged in", "Please login first.")
#             self.show_login()
#             return

#         try:
#             trips = api_client.get_my_trips(self.session.username)
#         except Exception as e:
#             QMessageBox.critical(self, "Error", f"Failed to fetch trips: {e}")
#             return

#         trip = select_current_or_next(trips)
#         if not trip:
#             QMessageBox.information(self, "No trip", "No current or upcoming trip found.")
#             return

#         # אם עדכנת את TripDetailView לתמוך ב-ai_callback, אפשר:
#         # self._current_trip_window = TripDetailView(trip, ai_callback=self.show_ai_chat)
#         self._current_trip_window = TripDetailView(trip)
#         self._current_trip_window.show()

#     def go_to_past_trips(self):
#         """Navigate to 'All trips' and refresh the list."""
#         if not self.session.is_logged_in():
#             QMessageBox.warning(self, "Not logged in", "Please login first.")
#             self.show_login()
#             return

#         self.past_trips_presenter.refresh()
#         self.setCurrentWidget(self.past_trips_view)

#     def go_to_new_trip(self):
#         """Navigate to 'Create New Trip'."""
#         if not self.session.is_logged_in():
#             QMessageBox.warning(self, "Not logged in", "Please login first.")
#             self.show_login()
#             return

#         self.newtrip_view.username = self.session.username
#         self.setCurrentWidget(self.newtrip_view)


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = App()
#     window.show()
#     sys.exit(app.exec())


# client/main.py
import sys
from PySide6.QtWidgets import QApplication, QStackedWidget, QMessageBox

# Session
from client.utils.session import SessionManager

# --- Views ---
from client.views.main_view import MainView
from client.views.login_view import LoginView
from client.views.dashboard_view import DashboardView
from client.views.past_trips_view import PastTripsView
from client.views.trip_detail_view import TripDetailView
from client.views.ai_consult_view import AIChatView
from client.views.newtrip_view import NewTripView

# --- Presenters ---
from client.presenters.main_presenter import MainPresenter
from client.presenters.dashboard_presenter import DashboardPresenter
from client.presenters.past_trips_presenter import PastTripsPresenter
from client.presenters.ai_consult_presenter import AIChatPresenter
from client.presenters.newtrip_presenter import NewTripPresenter

# --- Services/Utils ---
from client.services import api_client
from client.utils.trip_select import select_current_or_next


class App(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Trip Planner")
        self.resize(900, 700)
        self.setMinimumSize(600, 400)

        # Session state
        self.session = SessionManager()

        # --- Create views ---
        self.main_view = MainView(go_to_auth_callback=self.show_login)
        self.login_view = LoginView(
            go_to_main_view_callback=self.on_login_success,
            go_to_register_view_callback=None,
            session_manager=self.session,
        )
        self.dashboard_view = DashboardView()
        self.past_trips_view = PastTripsView()
        self.ai_chat_view = AIChatView(back_callback=self.show_dashboard)
        self.newtrip_view = NewTripView(username=None, back_callback=self.show_dashboard)

        # --- Wire presenters ---
        self.main_presenter = MainPresenter(
            view=self.main_view,
            session_manager=self.session,
            go_to_auth=self.show_login,
        )
        self.dashboard_presenter = DashboardPresenter(view=self.dashboard_view)
        self.past_trips_presenter = PastTripsPresenter(
            view=self.past_trips_view,
            session_manager=self.session,
        )
        self.ai_chat_presenter = AIChatPresenter(self.ai_chat_view)
        self.newtrip_presenter = NewTripPresenter(self.newtrip_view)

        # Back button in "All trips" → Dashboard
        self.past_trips_view.back_btn.clicked.connect(self.show_dashboard)

        # --- Add to stacked widget ---
        self.addWidget(self.main_view)        # index 0
        self.addWidget(self.login_view)       # index 1
        self.addWidget(self.dashboard_view)   # index 2
        self.addWidget(self.ai_chat_view)     # index 3
        self.addWidget(self.newtrip_view)     # index 4

        # ---- AI button callback hookup ----
        for v in (self.main_view, self.login_view, self.dashboard_view,
                  self.past_trips_view, self.newtrip_view, self.ai_chat_view):
            if hasattr(v, "set_ai_callback"):
                v.set_ai_callback(self.show_ai_chat)

        # Start at home
        self.setCurrentWidget(self.main_view)

        # Keep a reference for detail window (avoid GC)
        self._current_trip_window = None

    # ---------- Navigation ----------
    def show_home(self):
        self.setCurrentWidget(self.main_view)

    def show_login(self):
        self.setCurrentWidget(self.login_view)

    def show_dashboard(self):
        if getattr(self.session, "username", None):
            self.dashboard_view.set_username(self.session.username)
        self.setCurrentWidget(self.dashboard_view)

    def show_ai_chat(self):
        self.setCurrentWidget(self.ai_chat_view)

    # ---------- After successful login ----------
    def on_login_success(self, token: str, username: str):
        self.session.login(token, username)
        self.newtrip_view.username = username
        self.show_dashboard()
        # עדכון הדף CurrentTripView
        self.refresh_current_trip()

    # ---------- Dashboard update functions ----------
    def refresh_current_trip(self):
        """קבל נתוני טיול נוכחי מה-API ועדכן את הדף CurrentTripView"""
        if not self.session.is_logged_in():
            return

        try:
            trips = api_client.get_my_trips(self.session.username)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to fetch trips: {e}")
            return

        current_trip = select_current_or_next(trips)
        self.dashboard_view.pages["current"].update_trip(current_trip)
        self.dashboard_view.select_page("current")

    def refresh_past_trips(self):
        """עדכן את PastTripsView"""
        if not self.session.is_logged_in():
            return

        self.past_trips_presenter.refresh()
        self.dashboard_view.select_page("past")

    def go_to_new_trip(self):
        """בחר בדף יצירת טיול חדש בתוך הדשבורד"""
        if not self.session.is_logged_in():
            QMessageBox.warning(self, "Not logged in", "Please login first.")
            self.show_login()
            return

        self.newtrip_view.username = self.session.username
        self.dashboard_view.select_page("new")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("client/assets/style.qss", "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())

    window = App()
    window.show()
    sys.exit(app.exec())


