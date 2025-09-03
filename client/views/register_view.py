# client/views/register_view.py
from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)
from client.presenters.register_presenter import RegisterPresenter

# ---------- מסך הרשמה למשתמש חדש ----------
class RegisterView(QWidget):

    def __init__(self, go_to_login_callback):

        super().__init__()
        self.setWindowTitle("Register")

        # callback שמאפשר לחזור למסך ההתחברות
        self.go_to_login_callback = go_to_login_callback

        # חיבור ל־
        # RegisterPresenter
        self.presenter = RegisterPresenter(self)

        # ---------- רכיבי טופס ----------
        # שדה שם משתמש
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        # שדה סיסמה (עם מצב סיסמה מוסתרת)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        # כפתור הרשמה
        self.register_button = QPushButton("Sign Up")
        self.register_button.clicked.connect(self._register)

        # כפתור חזרה למסך התחברות
        self.back_button = QPushButton("Back to Login")
        self.back_button.clicked.connect(self.go_to_login_callback)

        # ---------- פריסת המסך ----------
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Register"))
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.register_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)


    #פונקציה שמופעלת בעת לחיצה על כפתור ההרשמה
    def _register(self):
    
        username = self.username_input.text()
        password = self.password_input.text()
        self.presenter.register_user(username, password)


    # פונקציות להצגת הודעות למשתמש
    def show_message(self, title, message):
      
        QMessageBox.information(self, title, message)

    #פונקציה להצגת הודעת שגיאה
    def show_error(self, message):
     
        QMessageBox.critical(self, "Error", message)
