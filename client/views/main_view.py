# client/views/main_view.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt


class MainView(QWidget):
    """
    מחלקת View עבור מסך הבית הראשי.

    כולל:
    - כותרת "Welcome"
    - כפתור יחיד למעבר למסך התחברות/הרשמה
    """

    def __init__(self, go_to_auth_callback):
        super().__init__()
        self.setWindowTitle("Smart Trip Planner")
        self.setMinimumSize(400, 300)

        # Layout ראשי אנכי
        # QVBoxLayout
        layout = QVBoxLayout()

        # תווית כותרת
        # QLabel
        self.label = QLabel("Welcome")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # כפתור יחיד שמוביל למסך התחברות/הרשמה
        # QPushButton
        self.auth_button = QPushButton("Login / Register")
        layout.addWidget(self.auth_button)

        # שמירת הפונקציה שקיבלנו מבחוץ
        # callback
        self._go_to_auth = go_to_auth_callback

        # חיבור הכפתור לפעולה
        self.auth_button.clicked.connect(self._go_to_auth)

        # הצמדת ה־
        # layout
        self.setLayout(layout)
