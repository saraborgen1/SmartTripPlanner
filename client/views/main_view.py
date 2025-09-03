#client/views/main_view.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QMovie

"""
    מחלקה שמגדירה את מסך הבית הראשי –
    MainView.  
    המסך מציג רקע וידאו בלופ (קובץ 
    GIF),  
    כותרת מרכזית, וכפתור התחלה שמוביל למסך ההתחברות.
"""
class MainView(QWidget):
   
    def __init__(self, go_to_auth_callback):
        super().__init__()
        # כותרת חלון
        self.setWindowTitle("Smart Trip Planner")
        self.setMinimumSize(500, 400)

        # --- רקע מונפש ---
        self.bg_label = QLabel(self)
        self.bg_label.setGeometry(self.rect())
        self.bg_label.setScaledContents(True)
        # שולחים אותו אחורה כך שיהיה מאחורי כל האלמנטים
        self.bg_label.lower()  

        # טעינת ה־
        # GIF  
        # כרקע מונפש
        self.movie = QMovie("client/assets/background.gif")
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie.setSpeed(100)
        self.bg_label.setMovie(self.movie)
        self.movie.start()

        # --- שכבת overlay שקופה מעל הרקע ---
        self.overlay = QWidget(self)
        self.overlay.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(self.overlay)
        layout.setAlignment(Qt.AlignCenter)

        # --- כותרת טקסט ---
        self.label = QLabel("Welcome to Smart Trip Planner")
        self.label.setObjectName("title")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: white; font-size: 28px; font-weight: bold;")
        layout.addWidget(self.label)

        # --- כפתור התחלה ---
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


    """
        פעולה שמוודאת שהרקע המונפש  
        (GIF)  
        ושכבת ה־
        overlay  
        יישארו פרוסים על כל המסך גם כאשר חלון התוכנה משתנה בגודל.
    """
    def resizeEvent(self, event):
        self.bg_label.setGeometry(self.rect())
        self.overlay.setGeometry(self.rect())
        super().resizeEvent(event)

