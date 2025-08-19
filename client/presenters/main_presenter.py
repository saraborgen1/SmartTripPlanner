# from views.search_view import SearchView
# from presenters.search_presenter import SearchPresenter

# class MainPresenter:
#     def __init__(self, view, session_manager):
#         self.view = view
#         self.session = session_manager
#         self.search_window = None  # נשתמש כאן למסך חיפוש

#         self.view.login_button.clicked.connect(self.go_to_login)
#         self.view.register_button.clicked.connect(self.go_to_register)
#         self.view.search_button.clicked.connect(self.go_to_search)

#     def go_to_login(self):
#         print("➡ Navigate to Login View")

#     def go_to_register(self):
#         print("➡ Navigate to Register View")

#     def go_to_search(self):
#         if self.session.is_logged_in():
#             if self.search_window is None:
#                 self.search_window = SearchView()
#                 self.search_presenter = SearchPresenter(self.search_window)
#             self.search_window.show()
#         else:
#             print("⚠ Please login first")


from views.search_view import SearchView
from presenters.search_presenter import SearchPresenter

class MainPresenter:
    def __init__(self, view, session_manager):
        self.view = view
        self.session = session_manager
        self.search_window = None

        self.view.login_button.clicked.connect(self.go_to_login)
        self.view.register_button.clicked.connect(self.go_to_register)
        self.view.search_button.clicked.connect(self.go_to_search)

    def go_to_login(self):
        print("➡ Navigate to Login View")

    def go_to_register(self):
        print("➡ Navigate to Register View")

    def go_to_search(self):
        if self.session.is_logged_in():
            if self.search_window is None:
                self.search_window = SearchView()
                self.search_presenter = SearchPresenter(self.search_window)
            self.search_window.show()
        else:
            print("⚠ Please login first")
