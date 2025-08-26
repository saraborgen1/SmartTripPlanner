# # client/presenters/dashboard_presenter.py

# class DashboardPresenter:
#     """
#     מחלקה שאחראית על החיבור בין ה־
#     View  
#     של מסך הדשבורד  
#     לבין הלוגיקה של ה־
#     App  

#     היא משמשת כ־
#     Presenter  
#     שתפקידו "לתווך" בין הכפתורים שמוצגים למשתמש  
#     לבין הפונקציות (קולבקים) שמבצע ה־
#     App  

#     מצפה לקבל ארבעה קולבקים עיקריים:
#     - on_current_trip  → פתיחת טיול נוכחי
#     - on_past_trips    → הצגת רשימת טיולים קודמים
#     - on_new_trip      → יצירת טיול חדש
#     - on_ai_chat       → פתיחת צ'אט עם ה־AI
#     """

#     def __init__(
#         self,
#         view,              # ה־View של הדשבורד (המסך עצמו עם הכפתורים)
#         session_manager,   # אובייקט שמנהל את מצב ההתחברות (Session)
#         on_current_trip,   # פונקציה שנטענת מבחוץ ומטפלת בלחיצה על כפתור "טיול נוכחי"
#         on_past_trips,     # פונקציה שנטענת מבחוץ ומטפלת בלחיצה על כפתור "טיולים קודמים"
#         on_new_trip,       # פונקציה שנטענת מבחוץ ומטפלת בלחיצה על כפתור "טיול חדש"
#         on_ai_chat,        # פונקציה שנטענת מבחוץ ומטפלת בלחיצה על כפתור "צ'אט AI"
#     ):
#         # שמירת ה־View
#         self.view = view
#         # שמירת מנהל הסשן (משמש כדי לדעת מי המשתמש המחובר כרגע)
#         self.session = session_manager

#         # חיבור הכפתורים ב־View לפונקציות (קולבקים) שהועברו מה־App
#         self.view.current_trip_btn.clicked.connect(on_current_trip)
#         self.view.past_trips_btn.clicked.connect(on_past_trips)
#         self.view.new_trip_btn.clicked.connect(on_new_trip)
#         self.view.ai_btn.clicked.connect(on_ai_chat)

class DashboardPresenter:
    def __init__(self, view: "DashboardView"):
        self.view = view

        # חיבור כפתורי ניווט פנימיים בלבד
        self.view.nav_buttons["current"].clicked.connect(lambda: self.view.select_page("current"))
        self.view.nav_buttons["past"].clicked.connect(lambda: self.view.select_page("past"))
        self.view.nav_buttons["new"].clicked.connect(lambda: self.view.select_page("new"))

        # התחלה עם דף נוכחי
        self.select_page("current")

    def select_page(self, page_key: str):
        self.view.select_page(page_key)

    def set_username(self, username: str):
        self.view.set_username(username)
