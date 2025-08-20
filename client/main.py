# # # # # # client/main.py
# # # # # import sys
# # # # # import requests
# # # # # from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

# # # # # response = requests.get("http://127.0.0.1:8000")
# # # # # label.setText(response.json()["msg"])

# # # # # app = QApplication(sys.argv)

# # # # # window = QWidget()
# # # # # window.setWindowTitle("Smart Trip Planner")

# # # # # layout = QVBoxLayout()
# # # # # label = QLabel("ברוכים הבאים למערכת תכנון טיול חכם!")
# # # # # layout.addWidget(label)

# # # # # window.setLayout(layout)
# # # # # window.show()

# # # # # sys.exit(app.exec())

# # # # import sys
# # # # from PySide6.QtWidgets import QApplication
# # # # from views.main_view import MainView
# # # # from presenters.main_presenter import MainPresenter
# # # # from utils.session import SessionManager

# # # # if __name__ == "__main__":
# # # #     app = QApplication(sys.argv)

# # # #     session = SessionManager()
# # # #     main_view = MainView()
# # # #     presenter = MainPresenter(main_view, session)

# # # #     main_view.show()
# # # #     sys.exit(app.exec())

# # # import sys
# # # from PySide6.QtWidgets import QApplication
# # # from views.main_view import MainView
# # # from presenters.main_presenter import MainPresenter
# # # from utils.session import SessionManager

# # # if __name__ == "__main__":
# # #     app = QApplication(sys.argv)

# # #     # Session – סימולציה של משתמש מחובר
# # #     session = SessionManager()
# # #     session.login("dummy_token")  # עכשיו SearchView ייפתח

# # #     # יצירת MainView + Presenter
# # #     main_view = MainView()
# # #     presenter = MainPresenter(main_view, session)

# # #     main_view.show()
# # #     sys.exit(app.exec())


# # import sys
# # from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QListWidget, QTextEdit

# # # =======================
# # # Session Manager
# # # =======================
# # class SessionManager:
# #     def __init__(self):
# #         self.user_token = None

# #     def login(self, token):
# #         self.user_token = token

# #     def is_logged_in(self):
# #         return self.user_token is not None

# # # =======================
# # # Models
# # # =======================
# # class Trip:
# #     def __init__(self, trip_id, name, description, location, image_url=None):
# #         self.trip_id = trip_id
# #         self.name = name
# #         self.description = description
# #         self.location = location
# #         self.image_url = image_url

# # # =======================
# # # Views
# # # =======================
# # class MainView(QWidget):
# #     def __init__(self):
# #         super().__init__()
# #         self.setWindowTitle("SmartTripPlanner - Main")
# #         self.setMinimumSize(300, 200)

# #         layout = QVBoxLayout()
# #         self.login_button = QPushButton("Login")
# #         self.register_button = QPushButton("Register")
# #         self.search_button = QPushButton("Search Trips")

# #         layout.addWidget(self.login_button)
# #         layout.addWidget(self.register_button)
# #         layout.addWidget(self.search_button)

# #         self.setLayout(layout)

# # class SearchView(QWidget):
# #     def __init__(self):
# #         super().__init__()
# #         self.setWindowTitle("Search Trips")
# #         self.setMinimumSize(400, 300)

# #         layout = QVBoxLayout()
# #         self.label = QLabel("Enter a city to search trips:")
# #         self.search_input = QLineEdit()
# #         self.search_input.setPlaceholderText("City name...")
# #         self.search_button = QPushButton("Search")
# #         self.results_list = QListWidget()

# #         layout.addWidget(self.label)
# #         layout.addWidget(self.search_input)
# #         layout.addWidget(self.search_button)
# #         layout.addWidget(self.results_list)
# #         self.setLayout(layout)

# # class TripDetailView(QWidget):
# #     def __init__(self, trip):
# #         super().__init__()
# #         self.setWindowTitle(f"Trip Details: {trip.name}")
# #         self.setMinimumSize(400, 300)

# #         layout = QVBoxLayout()
# #         self.name_label = QLabel(f"<b>{trip.name}</b>")
# #         self.location_label = QLabel(f"Location: {trip.location}")
# #         self.description_text = QTextEdit()
# #         self.description_text.setReadOnly(True)
# #         self.description_text.setText(trip.description)
# #         self.close_button = QPushButton("Close")

# #         layout.addWidget(self.name_label)
# #         layout.addWidget(self.location_label)
# #         layout.addWidget(self.description_text)
# #         layout.addWidget(self.close_button)
# #         self.setLayout(layout)

# # # =======================
# # # Presenters
# # # =======================
# # class TripDetailPresenter:
# #     def __init__(self, view):
# #         self.view = view
# #         self.view.close_button.clicked.connect(self.view.close)

# # class SearchPresenter:
# #     def __init__(self, view):
# #         self.view = view
# #         self.view.search_button.clicked.connect(self.on_search)
# #         self.view.results_list.itemClicked.connect(self.on_item_clicked)
# #         self.trips = []
# #         self.detail_windows = []

# #     def on_search(self):
# #         city = self.view.search_input.text().strip()
# #         if not city:
# #             self.view.results_list.clear()
# #             self.view.results_list.addItem("Please enter a city name.")
# #             return

# #         self.trips = [
# #             Trip(1, f"{city} Museum Tour", "Visit famous museums", city),
# #             Trip(2, f"{city} Nature Hike", "Explore natural parks", city),
# #             Trip(3, f"{city} Food Trip", "Taste local cuisine", city),
# #         ]

# #         self.view.results_list.clear()
# #         for trip in self.trips:
# #             self.view.results_list.addItem(f"{trip.name} - {trip.location}")

# #     def on_item_clicked(self, item):
# #         index = self.view.results_list.currentRow()
# #         trip = self.trips[index]

# #         detail_view = TripDetailView(trip)
# #         TripDetailPresenter(detail_view)
# #         self.detail_windows.append(detail_view)
# #         detail_view.show()

# # class MainPresenter:
# #     def __init__(self, view, session_manager):
# #         self.view = view
# #         self.session = session_manager
# #         self.search_window = None

# #         self.view.login_button.clicked.connect(self.go_to_login)
# #         self.view.register_button.clicked.connect(self.go_to_register)
# #         self.view.search_button.clicked.connect(self.go_to_search)

# #     def go_to_login(self):
# #         print("➡ Navigate to Login View")

# #     def go_to_register(self):
# #         print("➡ Navigate to Register View")

# #     def go_to_search(self):
# #         if self.session.is_logged_in():
# #             if self.search_window is None:
# #                 self.search_window = SearchView()
# #                 self.search_presenter = SearchPresenter(self.search_window)
# #             self.search_window.show()
# #         else:
# #             print("⚠ Please login first")

# # # =======================
# # # Main
# # # =======================
# # if __name__ == "__main__":
# #     app = QApplication(sys.argv)

# #     session = SessionManager()
# #     session.login("dummy_token")  # סימולציה של משתמש מחובר

# #     main_view = MainView()
# #     main_presenter = MainPresenter(main_view, session)

# #     main_view.show()
# #     sys.exit(app.exec())
# import sys
# from PySide6.QtWidgets import QApplication
# from views.search_view import SearchView
# from presenters.search_presenter import SearchPresenter

# app = QApplication(sys.argv)

# search_view = SearchView()
# presenter = SearchPresenter(search_view)
# search_view.show()

# sys.exit(app.exec())
from PySide6.QtWidgets import QApplication
from client.views.newtrip_view import NewTripView
from client.presenters.newtrip_presenter import NewTripPresenter
import sys

app = QApplication(sys.argv)

view = NewTripView(None)
presenter = NewTripPresenter(view)

view.show()
sys.exit(app.exec())
