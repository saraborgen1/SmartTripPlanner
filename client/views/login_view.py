# # client/views/login_view.py

from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QMovie

from client.presenters.login_presenter import LoginPresenter
# from client.utils.ai_button import add_ai_button

class LoginView(QWidget):
    def __init__(self, go_to_main_view_callback, go_to_register_view_callback=None, session_manager=None):
        super().__init__()
        self.setWindowTitle("Login / Register")
        self.setMinimumSize(420, 300)
        self._ai_callback = None
        self.mode = "login"
        self.presenter = LoginPresenter(self, session_manager)
        self.go_to_main_view = go_to_main_view_callback

        # רקע GIF מונפש
        self.bg_label = QLabel(self)
        self.bg_label.setGeometry(self.rect())
        self.bg_label.setScaledContents(True)
        self.bg_label.lower()

        self.movie = QMovie("client/assets/background.gif")
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie.setSpeed(100)
        self.bg_label.setMovie(self.movie)
        self.movie.start()

        # overlay שקוף עם טופס הלוגין
        self.overlay = QWidget(self)
        self.overlay.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(self.overlay)
        layout.setAlignment(Qt.AlignCenter)


        # # כפתור AI
        # add_ai_button(layout, lambda: self._ai_callback and self._ai_callback())

        # כותרת
        self.title = QLabel("Login to Your Account")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: white; font-size: 22px; font-weight: bold;")
        layout.addWidget(self.title)


        # שדות קלט
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet("""
            background: rgba(255,255,255,180);
            border-radius: 10px;
            padding: 8px 10px;
            font-size: 15px;
            qproperty-alignment: AlignLeft;
        """)
        self.username_input.setAlignment(Qt.AlignLeft)
        self.username_input.setTextMargins(0, 0, 290, 0)  # רווח קטן מהקצה השמאלי

        layout.addWidget(self.username_input, alignment=Qt.AlignHCenter)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            background: rgba(255,255,255,180);
            border-radius: 10px;
            padding: 8px 10px;
            font-size: 15px;
            qproperty-alignment: AlignLeft;
        """)
        self.password_input.setAlignment(Qt.AlignLeft)
        self.password_input.setTextMargins(0, 0, 290, 0)  # רווח קטן מהקצה השמאלי

        layout.addWidget(self.password_input, alignment=Qt.AlignHCenter)

        # כפתור ראשי
        self.primary_button = QPushButton("Login")
        self.primary_button.setFixedSize(435, 38)
        self.primary_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(102, 126, 234, 200);
                color: white;
                font-weight: bold;
                border-radius: 10px;
                font-size: 15px;
            }
            QPushButton:hover { background-color: rgba(85, 99, 214, 200); }
        """)
        self.primary_button.clicked.connect(self.handle_primary)
        layout.addWidget(self.primary_button, alignment=Qt.AlignHCenter)

        # כפתור להחלפת מצב
        self.toggle_button = QPushButton("Don't have an account? Sign up")
        self.toggle_button.setFixedSize(300, 38)
        self.toggle_button.setFlat(True)
        self.toggle_button.setStyleSheet("""
            QPushButton {
                color: white;
                font-weight: normal;
                font-size: 15px;
                background: transparent;
            }
            QPushButton:hover { text-decoration: underline; }
        """)
        self.toggle_button.clicked.connect(self.toggle_mode)
        layout.addWidget(self.toggle_button, alignment=Qt.AlignHCenter)

        # UX: Enter
        self.username_input.returnPressed.connect(self.primary_button.click)
        self.password_input.returnPressed.connect(self.primary_button.click)

    def resizeEvent(self, event):
            self.bg_label.setGeometry(self.rect())
            self.overlay.setGeometry(self.rect())
            super().resizeEvent(event)

    # def set_ai_callback(self, cb):
    #     self._ai_callback = cb

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
        self.go_to_main_view(token, self.username_input.text())

    def handle_loop(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.media_player.setPosition(0)
            self.media_player.play()

