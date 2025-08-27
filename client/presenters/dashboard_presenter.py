# client/presenters/dashboard_presenter.py
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
