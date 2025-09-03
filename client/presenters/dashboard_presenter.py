# client/presenters/dashboard_presenter.py

# הקובץ הזה מגדיר מחלקה בשם –
# DashboardPresenter –
# שתפקידה לחבר בין כפתורי הניווט בלוח הבקרה
# DashboardView –
# לבין הפונקציות שמחליפות דפים במסך.

from client.views.dashboard_view import DashboardView

class DashboardPresenter:

    def __init__(self, view: DashboardView):

        # שמירה של הפניה אל ה־
        # View –
        # כלומר, הממשק הגרפי של לוח הבקרה
        self.view = view

        # חיבור כפתורי הניווט הפנימיים בלבד:
        # כל כפתור במילון –
        # nav_buttons –
        # מקושר לפעולה שמפעילה את הפונקציה –
        # select_page –
        # עם המפתח המתאים 
        #("current", "past", "new").
        self.view.nav_buttons["current"].clicked.connect(lambda: self.view.select_page("current"))
        self.view.nav_buttons["past"].clicked.connect(lambda: self.view.select_page("past"))
        self.view.nav_buttons["new"].clicked.connect(lambda: self.view.select_page("new"))

        # מתחילים את המסך עם דף ה־
        # current
        self.select_page("current")


    # פונקציה שמקבלת מפתח מחרוזת –
    # page_key –
    # ומעבירה אותו ל־
    # View.select_page
    # כדי להציג את הדף המתאים במסך
    def select_page(self, page_key: str):
        self.view.select_page(page_key)


    # פונקציה שמעבירה את שם המשתמש ל־
    # View –
    # כדי להציגו בממשק (לדוגמה: "שלום, שרה")
    def set_username(self, username: str):
        self.view.set_username(username)
