from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt
from client.presenters.login_presenter import LoginPresenter

class LoginView(QWidget):
    def __init__(self, go_to_main_view_callback, go_to_register_view_callback=None, session_manager=None):
        super().__init__()
        self.setWindowTitle("Login / Register")
        self.setMinimumSize(420, 240)

        # מצב התחלתי: התחברות
        self.mode = "login"  # או "register"

        self.presenter = LoginPresenter(self, session_manager)

        self.go_to_main_view = go_to_main_view_callback

        layout = QVBoxLayout(self)

        self.title = QLabel("Login to Your Account")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(self.title)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # כפתור ראשי – משתנה לפי מצב
        self.primary_button = QPushButton("Login")
        self.primary_button.clicked.connect(self.handle_primary)
        layout.addWidget(self.primary_button)

        # "קישור" קטן להחלפת מצב (Login <-> Sign up)
        self.toggle_button = QPushButton("Don't have an account? Sign up")
        self.toggle_button.setFlat(True)
        self.toggle_button.clicked.connect(self.toggle_mode)
        layout.addWidget(self.toggle_button)

    def toggle_mode(self):
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
        username = self.username_input.text().strip()
        password = self.password_input.text()
        if self.mode == "login":
            self.presenter.login(username, password)
        else:
            self.presenter.register(username, password)

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)

    def show_success(self, token):
        QMessageBox.information(self, "Success", "Welcome!")
        self.go_to_main_view(token, self.username_input.text())
