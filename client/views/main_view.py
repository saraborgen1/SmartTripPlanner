#client/views/main_view.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QMovie

class MainView(QWidget):
    """
    מסך הבית הראשי (ברוך הבא) עם רקע וידאו בלופ ושקיפות
    """
    def __init__(self, go_to_auth_callback):
        super().__init__()
        self.setWindowTitle("Smart Trip Planner")
        self.setMinimumSize(500, 400)

        # רקע GIF מונפש
        self.bg_label = QLabel(self)
        self.bg_label.setGeometry(self.rect())
        self.bg_label.setScaledContents(True)
        self.bg_label.lower()  # שיהיה מאחורי הכל

        self.movie = QMovie("client/assets/background.gif")
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie.setSpeed(100)
        self.bg_label.setMovie(self.movie)
        self.movie.start()

        # overlay עם כל התוכן (שקוף)
        self.overlay = QWidget(self)
        self.overlay.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(self.overlay)
        layout.setAlignment(Qt.AlignCenter)

        # כותרת
        self.label = QLabel("Welcome to Smart Trip Planner")
        self.label.setObjectName("title")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: white; font-size: 28px; font-weight: bold;")
        layout.addWidget(self.label)

        # כפתור START
        self.auth_button = QPushButton("Start Planning")
        self.auth_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(102, 126, 234, 200);
                color: white; font-weight: bold; border-radius: 10px; padding: 12px 20px;
            }
            QPushButton:hover { background-color: rgba(85, 99, 214, 200); }
        """)
        layout.addWidget(self.auth_button)

        # חיבור הכפתור
        self._go_to_auth = go_to_auth_callback
        self.auth_button.clicked.connect(self._go_to_auth)

    def resizeEvent(self, event):
        """וידאו יתפרס על כל המסך בעת שינוי גודל"""
        self.bg_label.setGeometry(self.rect())
        self.overlay.setGeometry(self.rect())
        super().resizeEvent(event)

