# client/views/past_trips_view.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem, QHBoxLayout
from PySide6.QtCore import Qt
from client.utils.ai_button import add_ai_button


class PastTripsView(QWidget):
    """
    View שאחראי להציג את מסך 'הטיולים שלי'.

    כולל:
    - כותרת עם שם המשתמש
    - כפתורי רענון וחזרה
    - רשימת טיולים שנמשכת מהשרת
    - חיבור אופציונלי לכפתור AI
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Trip Planner - My Trips")
        self.setMinimumSize(560, 420)

        # Layout ראשי
        # QVBoxLayout
        root = QVBoxLayout()

        # שורת כותרת + כפתורים
        # QHBoxLayout
        header = QHBoxLayout()

        # כותרת ראשית
        # QLabel
        self.title = QLabel("My Trips")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 20px; font-weight: bold;")
        header.addWidget(self.title, 1)

        # כפתור רענון
        # QPushButton
        self.refresh_btn = QPushButton("Refresh")
        header.addWidget(self.refresh_btn, 0)

        # כפתור חזרה
        # QPushButton
        self.back_btn = QPushButton("Back")
        header.addWidget(self.back_btn, 0)

        # הוספת השורה ל־Layout הראשי
        root.addLayout(header)

        # רשימת טיולים
        # QListWidget
        self.trips_list = QListWidget()
        root.addWidget(self.trips_list)

        # חיבור ה־Layout לחלון
        self.setLayout(root)

    # ---------- מתודות עזר ----------

    def set_username(self, username: str):
        """
        עדכון הכותרת לשם המשתמש הנוכחי.
        """
        self.title.setText(f"My Trips — {username}")

    def clear_list(self):
        """
        ניקוי כל הפריטים מהרשימה.
        """
        self.trips_list.clear()

    def add_trip_item(self, text: str, trip_obj: dict):
        """
        מוסיף פריט חדש לרשימת הטיולים.
        text - טקסט שמוצג ברשימה
        trip_obj - אובייקט הטיול המלא נשמר ב־
        UserRole
        כדי שנוכל לגשת אליו בלחיצה.
        """
        item = QListWidgetItem(text)
        item.setData(Qt.UserRole, trip_obj)
        self.trips_list.addItem(item)

    def set_ai_callback(self, cb):
        """
        מאפשר ל־App לחבר את כפתור ה־AI למסך זה.
        """
        self._ai_callback = cb
