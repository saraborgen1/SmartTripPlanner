#client/views/dashboard_view.py

# הקובץ הזה מגדיר את המחלקה הראשית –
# DashboardView –
# שהיא הממשק הגרפי  של לוח הבקרה.
# כאן נבנים כל רכיבי המסך הראשי:
# Sidebar (תפריט צדי),
# Main Content (תוכן מרכזי),
# וכפתור צף (Floating Button).

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel,
    QStackedWidget, QFrame, QDialog, QGraphicsDropShadowEffect, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPixmap

from client.views.currenttrip_view import CurrentTripView
from client.views.past_trips_view import PastTripsView
from client.views.ai_consult_view import AIChatView

class DashboardView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Trip Planner")
        self.setMinimumSize(1200, 800)

        # --- הוספת רקע תמונה ---
        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(QPixmap("client/assets/background.png"))  
        self.bg_label.setScaledContents(True)
        self.bg_label.setGeometry(self.rect())
        self.bg_label.lower()  
        
        # אפקט מעבר עמודים
        self.page_animation = None
        
        # יצירת 
        # Layout 
        # ראשי 
        root_layout = QHBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)
        
        # קריאה לפונקציות עזר שמרכיבות את המבנה
        self.create_modern_sidebar(root_layout)
        self.create_modern_main_content(root_layout)
        self.create_modern_floating_ai_button()
        
        # התחלה עם דף ברירת מחדל –
        self.current_page = None
        self.select_page("current")

    def create_modern_sidebar(self, root_layout):
        # יצירת תפריט צדי מודרני
        sidebar_frame = QFrame()
        sidebar_frame.setObjectName("modern_sidebar")
        sidebar_frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)  
        sidebar_layout = QVBoxLayout(sidebar_frame)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        # כותרת המותג
        brand_title = QLabel("Smart Trip")
        brand_title.setObjectName("brand_title")
        brand_title.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(brand_title)

        # תת-כותרת
        brand_subtitle = QLabel("PLANNER✈️")
        brand_subtitle.setObjectName("brand_subtitle")
        brand_subtitle.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(brand_subtitle)

        # קו מפריד אלגנטי
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        sidebar_layout.addWidget(separator)

        # ברכת משתמש
        self.welcome_label = QLabel("Welcome, Guest🏃‍➡️")
        self.welcome_label.setObjectName("welcome_label")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(self.welcome_label)

        # כפתורי ניווט מעוצבים
        self.nav_buttons = {}
        nav_items = [
            ("current", "🏠 Current Trip"),
            ("past", "📋 Trip History"),
            ("new", "✨ New Adventure"),
        ]

        for key, text in nav_items:
            btn = QPushButton(text)
            btn.setObjectName("nav_button")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, k=key: self.select_page(k))
            self.nav_buttons[key] = btn
            sidebar_layout.addWidget(btn)

        #כדי לדחוף את הכפתורים למעלה
        sidebar_layout.addStretch()

        # מידע גרסה (אופציונלי)
        version_label = QLabel("v1.0.0")
        version_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(version_label)

        root_layout.insertWidget(0, sidebar_frame)  


    """יצירת אזור התוכן הראשי המודרני"""
    def create_modern_main_content(self, root_layout):

        main_frame = QFrame()
        main_frame.setObjectName("main_content_frame")
        main_layout = QVBoxLayout(main_frame)
        main_layout.setContentsMargins(32, 32, 32, 32)
        main_layout.setSpacing(20)

        # כותרת דף דינמית
        self.page_title = QLabel("Current Trip")
        main_layout.addWidget(self.page_title)

        # תת-כותרת דף
        self.page_subtitle = QLabel("Manage your current travel plans")
        main_layout.addWidget(self.page_subtitle)

        # קו מפריד
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        main_layout.addWidget(divider)

        # Stack של הדפים
        self.content_stack = QStackedWidget()

        # יוצרים רק את שני המסכים הראשיים כרגע
        self.pages = {
            "current": CurrentTripView(edit_trip_callback=self.handle_edit_trip),
            "past": PastTripsView(),
            "new": None    # placeholder – יוחלף מבחוץ
        }

        # הוספת הדפים הקיימים ל־stack
        self.content_stack.addWidget(self.pages["current"])
        self.content_stack.addWidget(self.pages["past"])
        main_layout.addWidget(self.content_stack, stretch=1)
        root_layout.addWidget(main_frame, stretch=1)

    """יצירת כפתור 
    AI
    צף מודרני עם אפקטים"""
    def create_modern_floating_ai_button(self):
       
        self.ai_button = QPushButton("🤖")
        self.ai_button.setObjectName("ai_floating_btn")
        self.ai_button.setParent(self)
        self.ai_button.setFixedSize(64, 64)
        
        # הוספת צל מתקדם
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(102, 126, 234, 100))
        self.ai_button.setGraphicsEffect(shadow)
        
        self.ai_button.clicked.connect(self.open_ai_dialog)
        self.position_ai_button()
        self.ai_button.raise_()


    def position_ai_button(self):
        """מיקום הכפתור הצף"""
        margin = 30
        size = self.ai_button.width()
        main_window = self.window()
        if main_window:
            x = main_window.width() - size - margin
            y = main_window.height() - size - margin
        else:
            x = self.width() - size - margin
            y = self.height() - size - margin

        self.ai_button.move(x, y)
        self.ai_button.raise_()


    # טיפול בשינוי גודל חלון –
    # עדכון רקע + מיקום כפתור AI
    def resizeEvent(self, event):
       
        super().resizeEvent(event)
        self.bg_label.setGeometry(self.rect())
        self.position_ai_button()
        self.ai_button.raise_()


    # מעבר לדף חדש לפי מפתח –
    # current, past, new
    def select_page(self, page_key):
        
        if page_key == "new" and self.pages["new"] is None:
            from client.utils.session import SessionManager
            from client.views.newtrip_view import NewTripView
            session = getattr(self.parentWidget(), "session", None)
            username = session.username if session else None
            self.pages["new"] = NewTripView(username=username, session_manager=session)
            self.content_stack.addWidget(self.pages["new"])

        if page_key not in self.pages or self.pages[page_key] is None:
            return

        # עדכון כפתורי הניווט
        for key, btn in self.nav_buttons.items():
            btn.setChecked(key == page_key)

        # עדכון כותרות הדף
        page_titles = {
            "current": ("Current Trip", "Manage your current travel plans"),
            "past": ("Trip History", "Review your past adventures"),
            "new": ("New Adventure", "Plan your next amazing journey")
        }
        if page_key in page_titles:
            title, subtitle = page_titles[page_key]
            self.page_title.setText(title)
            self.page_subtitle.setText(subtitle)

        self.content_stack.setCurrentWidget(self.pages[page_key])
        self.current_page = page_key

        
    """עדכון שם המשתמש"""
    def set_username(self, username: str):

        self.welcome_label.setText(f"Welcome, {username}")


    """הגדרת קריאה חוזרת לכפתור AI"""
    def set_ai_callback(self, callback):
        
        self.ai_button.clicked.disconnect()  
        self.ai_button.clicked.connect(callback)


    """פתיחת דיאלוג AI מעוצב"""
    def open_ai_dialog(self):

        dialog = QDialog(self)
        dialog.setWindowTitle("AI Assistant")
        dialog.setMinimumSize(1200, 800)
        
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(0, 0, 0, 0)
        
        ai_view = AIChatView(back_callback=dialog.close)
        layout.addWidget(ai_view)
        
        dialog.exec()

    # פתיחת מסך 
    # New Trip 
    # עם נתוני טיול לעריכה
    def handle_edit_trip(self, trip_data):
      
        if self.pages["new"] is None:
            from client.utils.session import SessionManager
            from client.views.newtrip_view import NewTripView
            session = getattr(self.parentWidget(), "session", None)
            username = session.username if session else None
            self.pages["new"] = NewTripView(username=username, session_manager=session)
            self.content_stack.addWidget(self.pages["new"])

        self.pages["new"].load_trip(trip_data)
        self.select_page("new")

     
        

        
