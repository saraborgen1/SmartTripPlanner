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

        from PySide6.QtWidgets import QSizePolicy
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)



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
        # חיבור כפתור "טיולים קודמים" במסך הדשבורד
       # חיבור כפתור Trip History לתצוגה הנכונה
        if hasattr(self.dashboard_view, "nav_buttons") and "past" in self.dashboard_view.nav_buttons:
            self.dashboard_view.nav_buttons["past"].clicked.connect(self.show_past_trips)


        self.ai_chat_view = AIChatView(back_callback=self.show_dashboard)

        # --- Wire presenters ---
        self.main_presenter = MainPresenter(
            view=self.main_view,
            session_manager=self.session,
            go_to_auth=self.show_login,
        )
        self.dashboard_presenter = DashboardPresenter(view=self.dashboard_view)
        self.past_trips_presenter = PastTripsPresenter(
            view=self.dashboard_view.pages["past"], 
            session_manager=self.session,
        )
        self.ai_chat_presenter = AIChatPresenter(self.ai_chat_view)

      
        # --- Add to stacked widget ---
        self.addWidget(self.main_view)        # index 0
        self.addWidget(self.login_view)       # index 1
        self.addWidget(self.dashboard_view)   # index 2
        self.addWidget(self.ai_chat_view)     # index 3

        # ---- AI button callback hookup ----
        for v in (self.main_view, self.login_view, self.dashboard_view,
                    self.ai_chat_view):
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

        # צור את הדף רק אחרי ההתחברות
        self.newtrip_view = NewTripView(
            username=username,
            back_callback=self.show_dashboard,
            session_manager=self.session   
            )
        self.newtrip_presenter = NewTripPresenter(self.newtrip_view, session_manager=self.session)

        # הוסף את המסך ל-QStackedWidget אם עדיין לא הוסף
        if self.indexOf(self.newtrip_view) == -1:
            self.addWidget(self.newtrip_view)

        self.show_dashboard()
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
        """פתיחת מסך יצירת טיול חדש"""
        if not self.session.is_logged_in():
            QMessageBox.warning(self, "Not logged in", "Please login first.")
            self.show_login()
            return

        # אם קיים מסך ישן — נעדכן את המשתמש, אחרת נבנה מסך חדש
        if not hasattr(self, "newtrip_view") or self.newtrip_view is None:
            self.newtrip_view = NewTripView(
                username=self.session.username,
                back_callback=self.show_dashboard,
                session_manager=self.session
            )
            self.newtrip_presenter = NewTripPresenter(self.newtrip_view, session_manager=self.session)
            self.addWidget(self.newtrip_view)
        else:
            # **עדכון שם המשתמש תמידי**
            self.newtrip_view.username = self.session.username

        # מעבר למסך יצירת טיול
        self.setCurrentWidget(self.newtrip_view)

    def show_past_trips(self):
        if not self.session.is_logged_in():
            QMessageBox.warning(self, "Not logged in", "Please login first.")
            self.show_login()
            return

        # רענון הנתונים של הטיולים
        self.past_trips_presenter.refresh()

        # נבחר את דף ה-past בתוך הדשבורד
        self.dashboard_view.select_page("past")
        self.setCurrentWidget(self.dashboard_view)




if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("client/assets/style.qss", "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())

    window = App()
    window.showMaximized()
    sys.exit(app.exec())


