# # client/views/login_view.py

# from PySide6.QtWidgets import (
#     QWidget, 
#     QLabel, 
#     QLineEdit, 
#     QPushButton, 
#     QVBoxLayout, 
#     QMessageBox
# )
# from PySide6.QtCore import Qt

# from client.presenters.login_presenter import LoginPresenter
# from client.utils.ai_button import add_ai_button


# class LoginView(QWidget):
#     """
#     מחלקת View שמציגה את מסך ההתחברות/הרשמה.

#     כולל:
#     - קלט לשם משתמש
#     - קלט לסיסמה
#     - כפתור ראשי (Login/Register)
#     - כפתור להחלפת מצב (Login ↔ Sign up)
#     - כפתור AI Assistant למעלה
#     """

#     def __init__(self, go_to_main_view_callback, go_to_register_view_callback=None, session_manager=None):
#         super().__init__()
#         self.setWindowTitle("Login / Register")
#         self.setMinimumSize(420, 240)

#         # Callback עבור AI (יוזן ע"י ה-App)
#         self._ai_callback = None

#         # מצב התחלתי
#         # login או register
#         self.mode = "login"

#         # Presenter
#         # LoginPresenter
#         self.presenter = LoginPresenter(self, session_manager)

#         # Callback שנקרא אחרי התחברות מוצלחת
#         self.go_to_main_view = go_to_main_view_callback

#         # Layout ראשי אנכי
#         # QVBoxLayout
#         layout = QVBoxLayout(self)

#         # כפתור AI בצד עליון
#         # add_ai_button
#         add_ai_button(layout, lambda: self._ai_callback and self._ai_callback())

#         # כותרת (ברירת מחדל: Login)
#         # QLabel
#         self.title = QLabel("Login to Your Account")
#         self.title.setAlignment(Qt.AlignCenter)
#         self.title.setStyleSheet("font-size: 20px; font-weight: bold;")
#         layout.addWidget(self.title)

#         # שדה קלט לשם משתמש
#         # QLineEdit
#         self.username_input = QLineEdit()
#         self.username_input.setPlaceholderText("Username")
#         layout.addWidget(self.username_input)

#         # שדה קלט לסיסמה
#         # QLineEdit
#         self.password_input = QLineEdit()
#         self.password_input.setPlaceholderText("Password")
#         self.password_input.setEchoMode(QLineEdit.Password)
#         layout.addWidget(self.password_input)

#         # כפתור ראשי (Login/Register)
#         # QPushButton
#         self.primary_button = QPushButton("Login")
#         self.primary_button.clicked.connect(self.handle_primary)
#         layout.addWidget(self.primary_button)

#         # כפתור להחלפת מצב (Login ↔ Sign up)
#         # QPushButton
#         self.toggle_button = QPushButton("Don't have an account? Sign up")
#         self.toggle_button.setFlat(True)
#         self.toggle_button.clicked.connect(self.toggle_mode)
#         layout.addWidget(self.toggle_button)

#     def set_ai_callback(self, cb):
#         """
#         מאפשר ל-App לחבר פונקציית 
#         callback
#         עבור כפתור ה־
#         AI
#         """
#         self._ai_callback = cb

#     def toggle_mode(self):
#         """
#         החלפת מצב בין:
#         login ↔ register
#         משנה טקסט בכותרת ובכפתורים בהתאם.
#         """
#         if self.mode == "login":
#             self.mode = "register"
#             self.title.setText("Create Your Account")
#             self.primary_button.setText("Create account")
#             self.toggle_button.setText("Already have an account? Log in")
#         else:
#             self.mode = "login"
#             self.title.setText("Login to Your Account")
#             self.primary_button.setText("Login")
#             self.toggle_button.setText("Don't have an account? Sign up")

#     def handle_primary(self):
#         """
#         פעולה כאשר לוחצים על כפתור ראשי.
#         - במצב login → קריאה ל־
#         presenter.login
#         - במצב register → קריאה ל־
#         presenter.register
#         """
#         username = self.username_input.text().strip()
#         password = self.password_input.text()
#         if self.mode == "login":
#             self.presenter.login(username, password)
#         else:
#             self.presenter.register(username, password)

#     def show_error(self, message):
#         """
#         מציג הודעת שגיאה למשתמש.
#         QMessageBox.critical
#         """
#         QMessageBox.critical(self, "Error", message)

#     def show_success(self, token):
#         """
#         מציג הודעת הצלחה אחרי התחברות מוצלחת
#         QMessageBox.information

#         ואז ממשיך ל־
#         MainView
#         דרך ה־
#         callback
#         """
#         QMessageBox.information(self, "Success", "Welcome!")
#         self.go_to_main_view(token, self.username_input.text())

#############לפני סרטון
# from PySide6.QtWidgets import (
#     QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
# )
# from PySide6.QtCore import Qt

# from client.presenters.login_presenter import LoginPresenter
# from client.utils.ai_button import add_ai_button

# class LoginView(QWidget):
#     def __init__(self, go_to_main_view_callback, go_to_register_view_callback=None, session_manager=None):
#         super().__init__()
#         self.setWindowTitle("Login / Register")
#         self.setMinimumSize(420, 300)
#         self._ai_callback = None
#         self.mode = "login"
#         self.presenter = LoginPresenter(self, session_manager)
#         self.go_to_main_view = go_to_main_view_callback

#         # עיצוב כולל
#         self.setStyleSheet("""
#             QWidget { background-color: #f0f2f5; font-family: 'Segoe UI', sans-serif; }
#             QLabel#title { font-size: 22px; font-weight: bold; color: #333; }
#             QLineEdit { border: 1px solid #ccc; border-radius: 8px; padding: 6px; }
#             QPushButton { 
#                 border-radius: 10px; padding: 10px 15px; 
#                 background-color: #667eea; color: white; font-weight: bold;
#             }
#             QPushButton:hover { background-color: #5563d6; }
#             QPushButton:flat { color: #667eea; font-weight: normal; }
#         """)

#         layout = QVBoxLayout(self)
#         layout.setAlignment(Qt.AlignCenter)

#         # כפתור AI למעלה
#         add_ai_button(layout, lambda: self._ai_callback and self._ai_callback())

#         # כותרת
#         self.title = QLabel("Login to Your Account")
#         self.title.setObjectName("title")
#         self.title.setAlignment(Qt.AlignCenter)
#         layout.addWidget(self.title)

#         # שדות קלט
#         self.username_input = QLineEdit()
#         self.username_input.setPlaceholderText("Username")
#         layout.addWidget(self.username_input)

#         self.password_input = QLineEdit()
#         self.password_input.setPlaceholderText("Password")
#         self.password_input.setEchoMode(QLineEdit.Password)
#         layout.addWidget(self.password_input)

#         # כפתור ראשי
#         self.primary_button = QPushButton("Login")
#         self.primary_button.clicked.connect(self.handle_primary)
#         layout.addWidget(self.primary_button)

#         # כפתור להחלפת מצב
#         self.toggle_button = QPushButton("Don't have an account? Sign up")
#         self.toggle_button.setFlat(True)
#         self.toggle_button.clicked.connect(self.toggle_mode)
#         layout.addWidget(self.toggle_button)

#         # UX: Enter
#         self.username_input.returnPressed.connect(self.primary_button.click)
#         self.password_input.returnPressed.connect(self.primary_button.click)

#     def set_ai_callback(self, cb):
#         self._ai_callback = cb

#     def toggle_mode(self):
#         if self.mode == "login":
#             self.mode = "register"
#             self.title.setText("Create Your Account")
#             self.primary_button.setText("Create account")
#             self.toggle_button.setText("Already have an account? Log in")
#         else:
#             self.mode = "login"
#             self.title.setText("Login to Your Account")
#             self.primary_button.setText("Login")
#             self.toggle_button.setText("Don't have an account? Sign up")

#     def handle_primary(self):
#         username = self.username_input.text().strip()
#         password = self.password_input.text()
#         if self.mode == "login":
#             self.presenter.login(username, password)
#         else:
#             self.presenter.register(username, password)

#     def show_error(self, message):
#         QMessageBox.critical(self, "Error", message)

#     def show_success(self, token):
#         QMessageBox.information(self, "Success", "Welcome!")
#         self.go_to_main_view(token, self.username_input.text())


###########עם סרטון
from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QGraphicsView, QGraphicsScene
)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QGraphicsVideoItem

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

        # ווידאו כרקע עם שקיפות
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(self.rect())
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setFrameShape(QGraphicsView.NoFrame)
        self.view.setStyleSheet("background: transparent; border: none;")

        self.video_item = QGraphicsVideoItem()
        self.video_item.setOpacity(0.9)  # שקיפות הווידאו
        self.scene.addItem(self.video_item)

        self.media_player = QMediaPlayer(self)
        self.media_player.setVideoOutput(self.video_item)
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setSource(QUrl.fromLocalFile("client/assets/background.mp4"))
        self.media_player.play()
        self.media_player.mediaStatusChanged.connect(self.handle_loop)

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
        self.view.setGeometry(self.rect())
        self.overlay.setGeometry(self.rect())
        self.scene.setSceneRect(0, 0, self.width(), self.height())
        self.video_item.setSize(self.rect().size())
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
        QMessageBox.information(self, "Success", "Welcome!")
        self.go_to_main_view(token, self.username_input.text())

    def handle_loop(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.media_player.setPosition(0)
            self.media_player.play()

