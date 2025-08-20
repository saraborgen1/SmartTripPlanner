# client/main.py
import sys
from PySide6.QtWidgets import QApplication, QStackedWidget, QMessageBox

# ניהול סשן (אצלך המחלקה בקובץ client/session.py)
from client.utils.session import SessionManager

# --- Views ---
from client.views.main_view import MainView                 # דף הבית ("Welcome" + כפתור Login/Register)
from client.views.login_view import LoginView               # מסך משולב: Login/Register (כפתור ראשי יחיד)
from client.views.dashboard_view import DashboardView       # דשבורד אחרי התחברות (3 כפתורים)
from client.views.past_trips_view import PastTripsView      # מסך "כל הטיולים" (כולל כפתור חזרה)
from client.views.trip_detail_view import TripDetailView    # חלון פרטי טיול
from client.views.ai_consult_view import AIChatView            # מסך תקשורת עם הסוכן (AI)
from client.views.newtrip_view import NewTripView


# --- Presenters ---
from client.presenters.main_presenter import MainPresenter
from client.presenters.dashboard_presenter import DashboardPresenter
from client.presenters.past_trips_presenter import PastTripsPresenter
from client.presenters.ai_consult_presenter import AIChatPresenter
from client.presenters.newtrip_presenter import NewTripPresenter


# --- שירותים/עזר ---
from client.services import api_client
from client.utils.trip_select import select_current_or_next


class App(QStackedWidget):
    """
    ניווט בין:
      0) MainView (Home)
      1) LoginView (Login/Register)
      2) DashboardView (אחרי התחברות)
      3) PastTripsView (כל הטיולים)
      4) AIChatView (צ'אט עם הסוכן)
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Trip Planner")
        self.setFixedSize(560, 420)

        # מצב התחברות
        self.session = SessionManager()

        # --- יצירת המסכים ---
        self.main_view = MainView(go_to_auth_callback=self.show_login)

        self.login_view = LoginView(
            go_to_main_view_callback=self.on_login_success,  # יקרא אחרי Login מוצלח
            go_to_register_view_callback=None,               # הכל משולב באותו מסך
            session_manager=self.session,
        )

        self.dashboard_view = DashboardView()
        self.past_trips_view = PastTripsView()
        self.ai_chat_view = AIChatView(back_callback=self.show_dashboard)

        # --- חיבור פרזנטרים ---
        self.main_presenter = MainPresenter(
            view=self.main_view,
            session_manager=self.session,
            go_to_auth=self.show_login,
        )

        self.dashboard_presenter = DashboardPresenter(
            view=self.dashboard_view,
            session_manager=self.session,
            on_current_trip=self.go_to_current_trip,
            on_past_trips=self.go_to_past_trips,
            on_new_trip=self.go_to_new_trip,   # כרגע TODO
            on_ai_chat=self.show_ai_chat
        )

        self.past_trips_presenter = PastTripsPresenter(
            view=self.past_trips_view,
            session_manager=self.session,
        )

        self.ai_chat_presenter = AIChatPresenter(self.ai_chat_view)

        # כפתור חזרה במסך "כל הטיולים" → דשבורד
        self.past_trips_view.back_btn.clicked.connect(self.show_dashboard)

        # --- הוספה ל-Stack ---
        self.addWidget(self.main_view)       # index 0
        self.addWidget(self.login_view)      # index 1
        self.addWidget(self.dashboard_view)  # index 2
        self.addWidget(self.past_trips_view) # index 3
        self.addWidget(self.ai_chat_view)    # index 4

        # מסך פתיחה: דף הבית
        self.setCurrentWidget(self.main_view)

        # רפרנס לחלון פרטי טיול (למנוע סגירה ע"י GC)
        self._current_trip_window = None

        self.new_trip_view = NewTripView(username=self.session.username)
        self.new_trip_presenter = NewTripPresenter(self.new_trip_view)

        # הוספה לסטאק
        self.addWidget(self.new_trip_view)  # index 5


    # ---------- ניווטים ----------
    def show_home(self):
        self.setCurrentWidget(self.main_view)

    def show_login(self):
        self.setCurrentWidget(self.login_view)

    def show_dashboard(self):
        # עדכון כותרת עם שם המשתמש (אם קיים)
        if getattr(self.session, "username", None):
            self.dashboard_view.set_username(self.session.username)
        self.setCurrentWidget(self.dashboard_view)

    def show_ai_chat(self):
        # ניתן לקרוא למתודה זו מתוך כפתור בדשבורד (אם תוסיפי כזה)
        self.setCurrentWidget(self.ai_chat_view)

    # ---------- נקרא אחרי התחברות מוצלחת ----------
    def on_login_success(self, token: str, username: str):
        self.session.login(token, username)
        self.show_dashboard()

    # ---------- פעולות הדשבורד ----------
    def go_to_current_trip(self):
        """מציג טיול שמתקיים היום, ואם אין – את הטיול העתידי הקרוב ביותר."""
        if not self.session.is_logged_in():
            QMessageBox.warning(self, "Not logged in", "אנא התחברי קודם.")
            self.show_login()
            return

        try:
            trips = api_client.get_my_trips(self.session.username)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"שגיאה בשליפת טיולים: {e}")
            return

        trip = select_current_or_next(trips)
        if not trip:
            QMessageBox.information(self, "אין טיול זמין", "לא נמצא טיול נוכחי או עתידי עבור המשתמש.")
            return

        self._current_trip_window = TripDetailView(trip)
        self._current_trip_window.show()

    def go_to_past_trips(self):
        """ניווט למסך 'כל הטיולים' + רענון הרשימה."""
        if not self.session.is_logged_in():
            QMessageBox.warning(self, "Not logged in", "אנא התחברי קודם.")
            self.show_login()
            return

        self.past_trips_presenter.refresh()
        self.setCurrentWidget(self.past_trips_view)

    def go_to_new_trip(self):
        """מעביר למסך יצירת טיול חדש."""
        if not self.session.is_logged_in():
            QMessageBox.warning(self, "Not logged in", "אנא התחברי קודם.")
            self.show_login()
            return

        # נעדכן ל־view את שם המשתמש הנוכחי (אם נכנסת אחרי init)
        self.new_trip_view.username = self.session.username
        self.setCurrentWidget(self.new_trip_view)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())
