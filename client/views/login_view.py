from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt
from client.presenters.login_presenter import LoginPresenter


class LoginView(QWidget):
    def __init__(self, go_to_main_view_callback, go_to_register_view_callback):
        super().__init__()
        self.setWindowTitle("Login")  # כותרת לחלון
        self.setMinimumSize(400, 200)  # קובע גודל מינימלי לחלון

        self.presenter = LoginPresenter(self)  # יוצר אובייקט Presenter ושומר עליו

        # פונקציות שיעברו למסכים אחרים
        self.go_to_main_view = go_to_main_view_callback  # פונקציה שמעבירה למסך הראשי לאחר התחברות
        self.go_to_register_view = go_to_register_view_callback  # פונקציה שמעבירה למסך הרשמה

        layout = QVBoxLayout(self)  # יוצר פריסת אנכית

        # כותרת עליונה
        title = QLabel("Login to Your Account")  # טקסט כותרת
        title.setAlignment(Qt.AlignCenter)  # ממרכז את הכותרת
        title.setStyleSheet("font-size: 20px; font-weight: bold;")  # עיצוב לכותרת
        layout.addWidget(title)  # מוסיף את הכותרת לפריסה

        # שדה קלט לשם משתמש
        self.username_input = QLineEdit()  # שדה קלט רגיל
        self.username_input.setPlaceholderText("Username")  # טקסט רקע
        layout.addWidget(self.username_input)  # מוסיף לפריסה

        # שדה קלט לסיסמה
        self.password_input = QLineEdit()  # שדה קלט רגיל
        self.password_input.setPlaceholderText("Password")  # טקסט רקע
        self.password_input.setEchoMode(QLineEdit.Password)  # מסתיר את הסיסמה (••••)
        layout.addWidget(self.password_input)  # מוסיף לפריסה

        # כפתור התחברות
        login_button = QPushButton("Login")  # יוצר כפתור
        login_button.clicked.connect(self.handle_login)  # מקשר את הכפתור לפונקציה שמטפלת בהתחברות
        layout.addWidget(login_button)  # מוסיף לפריסה

        # כפתור למעבר להרשמה
        register_button = QPushButton("Don't have an account? Sign up")  # כפתור לעבור למסך הרשמה
        register_button.clicked.connect(self.go_to_register_view)  # מקשר לפונקציה שמעבירה למסך הרשמה
        layout.addWidget(register_button)  # מוסיף לפריסה

    def handle_login(self):
        # לוקח את הנתונים מהשדות ושולח אותם ל־Presenter
        username = self.username_input.text()
        password = self.password_input.text()
        self.presenter.login(username, password)

    def show_error(self, message):
        # מציג חלונית שגיאה עם ההודעה מהשרת
        QMessageBox.critical(self, "Login Failed", message)

    def show_success(self, token):
        # מציג הודעת הצלחה ועובר למסך הראשי עם הטוקן ושם המשתמש
        QMessageBox.information(self, "Login Success", f"Welcome!")
        self.go_to_main_view(token, self.username_input.text())
