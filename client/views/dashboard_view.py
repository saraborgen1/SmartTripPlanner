from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt

class DashboardView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Trip Planner - Dashboard")
        self.setMinimumSize(500, 360)

        layout = QVBoxLayout()

        # כותרת (נעדכן לשם המשתמש אחרי התחברות)
        self.title = QLabel("Welcome")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(self.title)

        self.current_trip_btn = QPushButton("Current trip")
        self.past_trips_btn   = QPushButton("Past trips")
        self.new_trip_btn     = QPushButton("New trip")
        self.ai_btn = QPushButton("AI Assistant")

        layout.addWidget(self.current_trip_btn)
        layout.addWidget(self.past_trips_btn)
        layout.addWidget(self.new_trip_btn)
        layout.addWidget(self.ai_btn)

        self.setLayout(layout)

    def set_username(self, username: str):
        """מעדכן את הכותרת לשם המשתמש המחובר."""
        self.title.setText(f"Welcome, {username}")
