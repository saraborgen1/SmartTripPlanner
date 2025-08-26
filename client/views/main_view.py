############גרסה מקורית
# # # client/views/main_view.py
# # from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
# # from PySide6.QtCore import Qt


# # class MainView(QWidget):
# #     """
# #     מחלקת View עבור מסך הבית הראשי.

# #     כולל:
# #     - כותרת "Welcome"
# #     - כפתור יחיד למעבר למסך התחברות/הרשמה
# #     """

# #     def __init__(self, go_to_auth_callback):
# #         super().__init__()
# #         self.setWindowTitle("Smart Trip Planner")
# #         self.setMinimumSize(400, 300)

# #         # Layout ראשי אנכי
# #         # QVBoxLayout
# #         layout = QVBoxLayout()

# #         # תווית כותרת
# #         # QLabel
# #         self.label = QLabel("Welcome")
# #         self.label.setAlignment(Qt.AlignCenter)
# #         layout.addWidget(self.label)

# #         # כפתור יחיד שמוביל למסך התחברות/הרשמה
# #         # QPushButton
# #         self.auth_button = QPushButton("Login / Register")
# #         layout.addWidget(self.auth_button)

# #         # שמירת הפונקציה שקיבלנו מבחוץ
# #         # callback
# #         self._go_to_auth = go_to_auth_callback

# #         # חיבור הכפתור לפעולה
# #         self.auth_button.clicked.connect(self._go_to_auth)

# #         # הצמדת ה־
# #         # layout
# #         self.setLayout(layout)

#########לפני הסרטון
# from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
# from PySide6.QtCore import Qt

# class MainView(QWidget):
#     """
#     מסך הבית הראשי (ברוך הבא)
#     """
#     def __init__(self, go_to_auth_callback):
#         super().__init__()
#         self.setWindowTitle("Smart Trip Planner")
#         self.setMinimumSize(500, 400)
#         self.setStyleSheet("""
#             QWidget { background-color: #f0f2f5; font-family: 'Segoe UI', sans-serif; }
#             QLabel#title { font-size: 28px; font-weight: bold; color: #333; }
#             QLabel#subtitle { font-size: 16px; color: #555; }
#             QPushButton { 
#                 background-color: #667eea; color: white; font-weight: bold; 
#                 border-radius: 10px; padding: 12px 20px;
#             }
#             QPushButton:hover { background-color: #5563d6; }
#         """)

#         layout = QVBoxLayout(self)
#         layout.setAlignment(Qt.AlignCenter)

#         # כותרת
#         self.label = QLabel("Welcome to Smart Trip Planner")
#         self.label.setObjectName("title")
#         self.label.setAlignment(Qt.AlignCenter)
#         layout.addWidget(self.label)

#         # תמונת רקע (אפשר להחליף ל-path שלכם)
#         self.bg_label = QLabel()
#         self.bg_label.setAlignment(Qt.AlignCenter)
#         # self.bg_label.setStyleSheet("""
#         #     QLabel { 
#         #         background-image: url('path/to/your/background.jpg'); 
#         #         background-position: center; 
#         #         background-repeat: no-repeat; 
#         #         min-height: 150px; 
#         #     }
#         # """)
#         layout.addWidget(self.bg_label)

#         # כפתור LOGIN
#         self.auth_button = QPushButton("Login")
#         layout.addWidget(self.auth_button)

#         # כיתוב משני למי שלא רשום
#         self.signup_label = QLabel("Don't have an account? Sign up below")
#         self.signup_label.setObjectName("subtitle")
#         self.signup_label.setAlignment(Qt.AlignCenter)
#         layout.addWidget(self.signup_label)

#         # חיבור הכפתור לפעולה
#         self._go_to_auth = go_to_auth_callback
#         self.auth_button.clicked.connect(self._go_to_auth)

######עם סרטון
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QGraphicsView, QGraphicsScene
from PySide6.QtCore import Qt, QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QGraphicsVideoItem

class MainView(QWidget):
    """
    מסך הבית הראשי (ברוך הבא) עם רקע וידאו בלופ ושקיפות
    """
    def __init__(self, go_to_auth_callback):
        super().__init__()
        self.setWindowTitle("Smart Trip Planner")
        self.setMinimumSize(500, 400)

        # יצירת סצנה ווידאו עם שקיפות
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

        # # כיתוב משני
        # self.signup_label = QLabel("Don't have an account? Sign up below")
        # self.signup_label.setAlignment(Qt.AlignCenter)
        # self.signup_label.setStyleSheet("color: white; font-size: 16px;")
        # layout.addWidget(self.signup_label)

        # חיבור הכפתור
        self._go_to_auth = go_to_auth_callback
        self.auth_button.clicked.connect(self._go_to_auth)

    def resizeEvent(self, event):
        """וידאו יתפרס על כל המסך בעת שינוי גודל"""
        self.view.setGeometry(self.rect())
        self.overlay.setGeometry(self.rect())
        self.scene.setSceneRect(0, 0, self.width(), self.height())
        self.video_item.setSize(self.rect().size())
        super().resizeEvent(event)

    def handle_loop(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.media_player.setPosition(0)
            self.media_player.play()

