# client/views/past_trips_view.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem, QHBoxLayout
from PySide6.QtCore import Qt

class PastTripsView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Trip Planner - My Trips")
        self.setMinimumSize(560, 420)

        root = QVBoxLayout()

        # שורת כותרת + כפתורי פעולה
        header = QHBoxLayout()

        self.title = QLabel("My Trips")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 20px; font-weight: bold;")
        header.addWidget(self.title, 1)

        self.refresh_btn = QPushButton("Refresh")
        header.addWidget(self.refresh_btn, 0)

        # כפתור חזרה
        self.back_btn = QPushButton("Back")
        header.addWidget(self.back_btn, 0)

        root.addLayout(header)

        # רשימת הטיולים
        self.trips_list = QListWidget()
        root.addWidget(self.trips_list)

        self.setLayout(root)

    def set_username(self, username: str):
        self.title.setText(f"My Trips — {username}")

    def clear_list(self):
        self.trips_list.clear()

    def add_trip_item(self, text: str, trip_obj: dict):
        item = QListWidgetItem(text)
        item.setData(Qt.UserRole, trip_obj)
        self.trips_list.addItem(item)
