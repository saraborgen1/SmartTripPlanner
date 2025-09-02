# client/main.py

import sys
from PySide6.QtWidgets import QApplication, QStackedWidget, QMessageBox,QSizePolicy
from client.utils.session import SessionManager
from client.views.main_view import MainView
from client.views.login_view import LoginView
from client.views.dashboard_view import DashboardView
from client.views.ai_consult_view import AIChatView
from client.views.newtrip_view import NewTripView
from client.presenters.main_presenter import MainPresenter
from client.presenters.dashboard_presenter import DashboardPresenter
from client.presenters.past_trips_presenter import PastTripsPresenter
from client.presenters.ai_consult_presenter import AIChatPresenter
from client.presenters.newtrip_presenter import NewTripPresenter
from client.services import api_client
from client.utils.trip_select import select_current_or_next

#מחלקת האפליקציה הראשית
class App(QStackedWidget):

    def __init__(self):

        super().__init__()
        self.setWindowTitle("Smart Trip Planner")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # ניהול מצב משתמש
        self.session = SessionManager()

        # --- יצירת מסכים ---
        self.main_view = MainView(go_to_auth_callback=self.show_login)
        self.login_view = LoginView(
            go_to_main_view_callback=self.on_login_success,
            session_manager=self.session,
        )
        self.dashboard_view = DashboardView()
     
        # חיבור כפתור "טיולים קודמים" במסך הדשבורד
        if hasattr(self.dashboard_view, "nav_buttons") and "past" in self.dashboard_view.nav_buttons:
            self.dashboard_view.nav_buttons["past"].clicked.connect(self.show_past_trips)
        self.ai_chat_view = AIChatView(back_callback=self.show_dashboard)

        # --- יצירת פרזנטרים ---
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

        # --- הוספת מסכים ל־QStackedWidget ---
        self.addWidget(self.main_view)        
        self.addWidget(self.login_view)       
        self.addWidget(self.dashboard_view)   
        self.addWidget(self.ai_chat_view)     

        # חיבור כפתור ה־AI בכל מסך שמאפשר זאת
        for v in (self.main_view, self.login_view, self.dashboard_view,
                    self.ai_chat_view):
            if hasattr(v, "set_ai_callback"):
                v.set_ai_callback(self.show_ai_chat)

        # מתחילים במסך הראשי
        self.setCurrentWidget(self.main_view)

        # משתנה פנימי כדי למנוע סגירה מוקדמת של חלון טיול פתוח
        self._current_trip_window = None

    # ---------- ניווט בין מסכים ----------
    #מציג את המסך הראשי
    def show_home(self):
        self.setCurrentWidget(self.main_view)

    # מציג את מסך ההתחברות
    def show_login(self):
        self.setCurrentWidget(self.login_view)

    # מציג את מסך הלוח בקרה
    def show_dashboard(self):
        if getattr(self.session, "username", None):
            self.dashboard_view.set_username(self.session.username)
        self.setCurrentWidget(self.dashboard_view)

    # מציג את מסך הייעוץ של ה-AI
    def show_ai_chat(self):
        self.setCurrentWidget(self.ai_chat_view)

    # ---------- אחרי התחברות מוצלחת ----------
    # פונקציה שמופעלת אחרי התחברות מוצלחת
    # מקבלת טוקן ושם משתמש ומעדכנת את מצב ההתחברות
    def on_login_success(self, token: str, username: str):
        self.session.login(token, username)

        self.newtrip_view = NewTripView(
            username=username,
            back_callback=self.show_dashboard,
            session_manager=self.session,
            on_save_callback=self.refresh_current_trip   
        )
        self.newtrip_presenter = NewTripPresenter(self.newtrip_view, session_manager=self.session)

        # מוסיפים את מסך יצירת הטיול אם הוא לא קיים כבר
        if self.indexOf(self.newtrip_view) == -1:
            self.addWidget(self.newtrip_view)

        # מוסיפים את מסך יצירת הטיול למילון הדפים של הדשבורד
        self.dashboard_view.pages["new"] = self.newtrip_view
        if self.dashboard_view.content_stack.indexOf(self.newtrip_view) == -1:
            self.dashboard_view.content_stack.addWidget(self.newtrip_view)

        # חיבור כפתור "טיול חדש" במסך הדשבורד
        current_view = self.dashboard_view.pages["current"]
        current_view.edit_trip_callback = self.open_edit_trip    

        # מעבר לדשבורד ורענון נתוני הטיול הנוכחי
        self.show_dashboard()
        self.refresh_current_trip()


    # ---------- פונקציות עדכון דשבורד ----------
    # רענון נתוני הטיול הנוכחי
    def refresh_current_trip(self):

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


    # רענון נתוני הטיולים הקודמים
    def refresh_past_trips(self):

        if not self.session.is_logged_in():
            return

        self.past_trips_presenter.refresh()
        self.dashboard_view.select_page("past")

    # ---------- ניווט למסך יצירת טיול חדש ----------
    def go_to_new_trip(self):
        self.newtrip_view.set_back_callback(self.show_dashboard)
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
            self.newtrip_view.username = self.session.username

        # מעבר למסך יצירת טיול
        self.setCurrentWidget(self.newtrip_view)


    # ---------- ניווט למסך טיולים קודמים ----------
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


    # ---------- ניווט למסך עריכת טיול קיים ----------
    def open_edit_trip(self, trip_data):
        self.newtrip_view.set_back_callback(lambda: (
        self.dashboard_view.select_page("current"),
        self.setCurrentWidget(self.dashboard_view)
        ))

        if not hasattr(self, "newtrip_view"):
            QMessageBox.warning(self, "Error", "Trip editor not available.")
            return

        # טוענים את הנתונים למסך NewTripView
        self.newtrip_view.load_trip(trip_data)
        self.dashboard_view.select_page("new")
        self.setCurrentWidget(self.dashboard_view)


# ---------- נקודת כניסה ראשית ----------
if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("client/assets/style.qss", "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())

    window = App()
    window.showMaximized()
    sys.exit(app.exec())


