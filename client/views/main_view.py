# # client/views/main_view.py
# from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
# from PySide6.QtCore import Qt


# class MainView(QWidget):
#     """
#     מחלקת View עבור מסך הבית הראשי.

#     כולל:
#     - כותרת "Welcome"
#     - כפתור יחיד למעבר למסך התחברות/הרשמה
#     """

#     def __init__(self, go_to_auth_callback):
#         super().__init__()
#         self.setWindowTitle("Smart Trip Planner")
#         self.setMinimumSize(400, 300)

#         # Layout ראשי אנכי
#         # QVBoxLayout
#         layout = QVBoxLayout()

#         # תווית כותרת
#         # QLabel
#         self.label = QLabel("Welcome")
#         self.label.setAlignment(Qt.AlignCenter)
#         layout.addWidget(self.label)

#         # כפתור יחיד שמוביל למסך התחברות/הרשמה
#         # QPushButton
#         self.auth_button = QPushButton("Login / Register")
#         layout.addWidget(self.auth_button)

#         # שמירת הפונקציה שקיבלנו מבחוץ
#         # callback
#         self._go_to_auth = go_to_auth_callback

#         # חיבור הכפתור לפעולה
#         self.auth_button.clicked.connect(self._go_to_auth)

#         # הצמדת ה־
#         # layout
#         self.setLayout(layout)


from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt

class MainView(QWidget):
    """
    מסך הבית הראשי (ברוך הבא)
    """
    def __init__(self, go_to_auth_callback):
        super().__init__()
        self.setWindowTitle("Smart Trip Planner")
        self.setMinimumSize(500, 400)
        self.setStyleSheet("""
            QWidget { background-color: #f0f2f5; font-family: 'Segoe UI', sans-serif; }
            QLabel#title { font-size: 28px; font-weight: bold; color: #333; }
            QLabel#subtitle { font-size: 16px; color: #555; }
            QPushButton { 
                background-color: #667eea; color: white; font-weight: bold; 
                border-radius: 10px; padding: 12px 20px;
            }
            QPushButton:hover { background-color: #5563d6; }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # כותרת
        self.label = QLabel("Welcome to Smart Trip Planner")
        self.label.setObjectName("title")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # תמונת רקע (אפשר להחליף ל-path שלכם)
        self.bg_label = QLabel()
        self.bg_label.setAlignment(Qt.AlignCenter)
        # self.bg_label.setStyleSheet("""
        #     QLabel { 
        #         background-image: url('path/to/your/background.jpg'); 
        #         background-position: center; 
        #         background-repeat: no-repeat; 
        #         min-height: 150px; 
        #     }
        # """)
        layout.addWidget(self.bg_label)

        # כפתור LOGIN
        self.auth_button = QPushButton("Login")
        layout.addWidget(self.auth_button)

        # כיתוב משני למי שלא רשום
        self.signup_label = QLabel("Don't have an account? Sign up below")
        self.signup_label.setObjectName("subtitle")
        self.signup_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.signup_label)

        # חיבור הכפתור לפעולה
        self._go_to_auth = go_to_auth_callback
        self.auth_button.clicked.connect(self._go_to_auth)


