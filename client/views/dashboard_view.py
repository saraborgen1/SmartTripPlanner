# client/views/dashboard_view.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
from client.utils.ai_button import add_ai_button


class DashboardView(QWidget):
    """
    מחלקת View שמציגה את מסך ה־
    Dashboard

    תפקידה:
    - להראות כפתורים עיקריים:
      Current trip,
      Past trips,
      New trip,
      AI Assistant
    - להציג כותרת מותאמת אישית עם שם המשתמש המחובר.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Trip Planner - Dashboard")
        self.setMinimumSize(500, 360)

        # Layout ראשי אנכי
        # QVBoxLayout
        layout = QVBoxLayout()

        # כותרת ברוכים הבאים
        # QLabel
        self.title = QLabel("Welcome")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(self.title)

        # כפתורים עיקריים
        # QPushButton
        self.current_trip_btn = QPushButton("Current trip")
        self.past_trips_btn   = QPushButton("Past trips")
        self.new_trip_btn     = QPushButton("New trip")
        self.ai_btn           = QPushButton("AI Assistant")

        # הוספת הכפתורים ל־Layout
        layout.addWidget(self.current_trip_btn)
        layout.addWidget(self.past_trips_btn)
        layout.addWidget(self.new_trip_btn)
        layout.addWidget(self.ai_btn)

        # חיבור ה־Layout למסך
        self.setLayout(layout)

    def set_username(self, username: str):
        """
        עדכון הכותרת עם שם המשתמש המחובר.

        username –
        str
        שם המשתמש.
        """
        self.title.setText(f"Welcome, {username}")

    def set_ai_callback(self, cb):
        """
        שמירה של פונקציית callback
        שתופעל כאשר לוחצים על כפתור ה־
        AI Assistant
        """
        self._ai_callback = cb
