# client/views/login_view.py

from PySide6.QtWidgets import (
    QWidget, 
    QLabel, 
    QLineEdit, 
    QPushButton, 
    QVBoxLayout, 
    QMessageBox
)
from PySide6.QtCore import Qt

from client.presenters.login_presenter import LoginPresenter
from client.utils.ai_button import add_ai_button


class LoginView(QWidget):
    """
    מחלקת View שמציגה את מסך ההתחברות/הרשמה.

    כולל:
    - קלט לשם משתמש
    - קלט לסיסמה
    - כפתור ראשי (Login/Register)
    - כפתור להחלפת מצב (Login ↔ Sign up)
    - כפתור AI Assistant למעלה
    """

    def __init__(self, go_to_main_view_callback, go_to_register_view_callback=None, session_manager=None):
        super().__init__()
        self.setWindowTitle("Login / Register")
        self.setMinimumSize(420, 240)

        # Callback עבור AI (יוזן ע"י ה-App)
        self._ai_callback = None

        # מצב התחלתי
        # login או register
        self.mode = "login"

        # Presenter
        # LoginPresenter
        self.presenter = LoginPresenter(self, session_manager)

        # Callback שנקרא אחרי התחברות מוצלחת
        self.go_to_main_view = go_to_main_view_callback

        # Layout ראשי אנכי
        # QVBoxLayout
        layout = QVBoxLayout(self)

        # כפתור AI בצד עליון
        # add_ai_button
        add_ai_button(layout, lambda: self._ai_callback and self._ai_callback())

        # כותרת (ברירת מחדל: Login)
        # QLabel
        self.title = QLabel("Login to Your Account")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(self.title)

        # שדה קלט לשם משתמש
        # QLineEdit
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        # שדה קלט לסיסמה
        # QLineEdit
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # כפתור ראשי (Login/Register)
        # QPushButton
        self.primary_button = QPushButton("Login")
        self.primary_button.clicked.connect(self.handle_primary)
        layout.addWidget(self.primary_button)

        # כפתור להחלפת מצב (Login ↔ Sign up)
        # QPushButton
        self.toggle_button = QPushButton("Don't have an account? Sign up")
        self.toggle_button.setFlat(True)
        self.toggle_button.clicked.connect(self.toggle_mode)
        layout.addWidget(self.toggle_button)

    def set_ai_callback(self, cb):
        """
        מאפשר ל-App לחבר פונקציית 
        callback
        עבור כפתור ה־
        AI
        """
        self._ai_callback = cb

    def toggle_mode(self):
        """
        החלפת מצב בין:
        login ↔ register
        משנה טקסט בכותרת ובכפתורים בהתאם.
        """
        if self.mode == "login":
            self.mode = "register"
            self.title.setText("Create Your Account")
            self.primary_button.setText("Create account")
            self.toggle_button.setText("Already have an account? Log in")
        else:
            self.mode = "login"
            self.title.setText("Login to Your Account")
            self.primary_button.setText("Login")
            self.toggle_button.setText("Don't have an account? Sign up")

    def handle_primary(self):
        """
        פעולה כאשר לוחצים על כפתור ראשי.
        - במצב login → קריאה ל־
        presenter.login
        - במצב register → קריאה ל־
        presenter.register
        """
        username = self.username_input.text().strip()
        password = self.password_input.text()
        if self.mode == "login":
            self.presenter.login(username, password)
        else:
            self.presenter.register(username, password)

    def show_error(self, message):
        """
        מציג הודעת שגיאה למשתמש.
        QMessageBox.critical
        """
        QMessageBox.critical(self, "Error", message)

    def show_success(self, token):
        """
        מציג הודעת הצלחה אחרי התחברות מוצלחת
        QMessageBox.information

        ואז ממשיך ל־
        MainView
        דרך ה־
        callback
        """
        QMessageBox.information(self, "Success", "Welcome!")
        self.go_to_main_view(token, self.username_input.text())
