# # client/views/dashboard_view.py

# from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
# from PySide6.QtCore import Qt
# from client.utils.ai_button import add_ai_button


# class DashboardView(QWidget):
#     """
#     מחלקת View שמציגה את מסך ה־
#     Dashboard

#     תפקידה:
#     - להראות כפתורים עיקריים:
#       Current trip,
#       Past trips,
#       New trip,
#       AI Assistant
#     - להציג כותרת מותאמת אישית עם שם המשתמש המחובר.
#     """

#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Smart Trip Planner - Dashboard")
#         self.setMinimumSize(500, 360)

#         # Layout ראשי אנכי
#         # QVBoxLayout
#         layout = QVBoxLayout()

#         # כותרת ברוכים הבאים
#         # QLabel
#         self.title = QLabel("Welcome")
#         self.title.setAlignment(Qt.AlignCenter)
#         self.title.setStyleSheet("font-size: 20px; font-weight: bold;")
#         layout.addWidget(self.title)

#         # כפתורים עיקריים
#         # QPushButton
#         self.current_trip_btn = QPushButton("Current trip")
#         self.past_trips_btn   = QPushButton("Past trips")
#         self.new_trip_btn     = QPushButton("New trip")
#         self.ai_btn           = QPushButton("AI Assistant")

#         # הוספת הכפתורים ל־Layout
#         layout.addWidget(self.current_trip_btn)
#         layout.addWidget(self.past_trips_btn)
#         layout.addWidget(self.new_trip_btn)
#         layout.addWidget(self.ai_btn)

#         # חיבור ה־Layout למסך
#         self.setLayout(layout)

#     def set_username(self, username: str):
#         """
#         עדכון הכותרת עם שם המשתמש המחובר.

#         username –
#         str
#         שם המשתמש.
#         """
#         self.title.setText(f"Welcome, {username}")

#     def set_ai_callback(self, cb):
#         """
#         שמירה של פונקציית callback
#         שתופעל כאשר לוחצים על כפתור ה־
#         AI Assistant
#         """
#         self._ai_callback = cb


from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel,
    QStackedWidget, QFrame, QDialog, QScrollArea, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QColor, QFont

# ייבוא דפי תוכן
from client.views.currenttrip_view import CurrentTripView
from client.views.past_trips_view import PastTripsView
from client.views.newtrip_view import NewTripView
from client.views.ai_consult_view import AIChatView


class DashboardView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Trip Planner")
        self.setMinimumSize(1200, 800)
        
        # אפקט מעבר עמודים
        self.page_animation = None
        
        # הגדרת סגנונות מודרניים
        self.setup_modern_styles()
        
        # Layout ראשי
        root_layout = QHBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)
        
        # יצירת התפריט הצדי
        self.create_modern_sidebar(root_layout)
        
        # יצירת אזור התוכן הראשי
        self.create_modern_main_content(root_layout)
        
        # כפתור AI צף מודרני
        self.create_modern_floating_ai_button()
        
        # התחלה עם דף נוכחי
        self.current_page = None
        self.select_page("current")

    def setup_modern_styles(self):
        """הגדרת סגנונות מודרניים לאפליקציה"""
        self.setStyleSheet("""
            QWidget { 
                background-color: #f8fafc; 
                font-family: 'Inter', 'Segoe UI', system-ui, sans-serif; 
                color: #2d3748;
            }
            
            QFrame#modern_sidebar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #1e2026, 
                    stop:1 #2c3e50);
                min-width: 280px; 
                max-width: 280px; 
                border: none;
                border-top-right-radius: 20px;
                border-bottom-right-radius: 20px;
            }
            
            QLabel#brand_title {
                color: #ffffff; 
                font-size: 28px; 
                font-weight: 700;
                padding: 30px 20px 10px 20px;
                letter-spacing: -0.5px;
            }
            
            QLabel#brand_subtitle {
                color: #a0aec0; 
                font-size: 14px; 
                font-weight: 400;
                padding: 0 20px 30px 20px;
                letter-spacing: 0.5px;
            }
            
            QLabel#welcome_label {
                color: #cbd5e0; 
                font-size: 14px; 
                font-weight: 500;
                margin: 0 20px 20px 20px;
                padding: 12px 16px;
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                text-align: center;
            }
            
            QPushButton#nav_button {
                background: transparent;
                border: none;
                color: #e2e8f0;
                font-size: 16px;
                font-weight: 500;
                padding: 18px 24px;
                text-align: left;
                border-radius: 14px;
                margin: 4px 16px;
                transition: all 0.3s ease;
            }
            
            QPushButton#nav_button:hover {
                background-color: rgba(255, 255, 255, 0.15);
                color: #ffffff;
                transform: translateX(4px);
            }
            
            QPushButton#nav_button:checked {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #667eea, 
                    stop:1 #3498db);
                color: white;
                font-weight: 600;
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
            }
            
            QPushButton#nav_button:pressed { 
                background-color: #2980b9; 
            }
            
            QFrame#main_content_frame {
                background-color: #ffffff;
                border-radius: 20px;
                margin: 20px 20px 20px 0;
                border: 1px solid #e2e8f0;
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            }
            
            QPushButton#ai_floating_btn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #667eea, 
                    stop:1 #764ba2);
                border: none;
                border-radius: 32px;
                color: white;
                font-size: 20px;
                font-weight: bold;
                min-width: 64px;
                min-height: 64px;
                max-width: 64px;
                max-height: 64px;
            }
            
            QPushButton#ai_floating_btn:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #5563d6, 
                    stop:1 #553c9a);
            }
            
            QPushButton#ai_floating_btn:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #4c51bf, 
                    stop:1 #4c1d95);
            }
        """)

    def create_modern_sidebar(self, root_layout):
        """יצירת תפריט צדי מודרני"""
        sidebar_frame = QFrame()
        sidebar_frame.setObjectName("modern_sidebar")
        sidebar_layout = QVBoxLayout(sidebar_frame)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # כותרת המותג
        brand_title = QLabel("Smart Trip")
        brand_title.setObjectName("brand_title")
        brand_title.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(brand_title)
        
        # תת-כותרת
        brand_subtitle = QLabel("PLANNER")
        brand_subtitle.setObjectName("brand_subtitle")
        brand_subtitle.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(brand_subtitle)
        
        # קו מפריד אלגנטי
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.2);
                max-height: 1px;
                margin: 20px 40px;
            }
        """)
        sidebar_layout.addWidget(separator)
        
        # ברכת משתמש
        self.welcome_label = QLabel("Welcome, Guest")
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
        
        # מרווח גמיש
        sidebar_layout.addStretch()
        
        # מידע גרסה (אופציונלי)
        version_label = QLabel("v1.0.0")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("""
            color: rgba(255, 255, 255, 0.4);
            font-size: 12px;
            padding: 20px;
        """)
        sidebar_layout.addWidget(version_label)
        
        root_layout.addWidget(sidebar_frame)

    def create_modern_main_content(self, root_layout):
        """יצירת אזור התוכן הראשי המודרני"""
        main_frame = QFrame()
        main_frame.setObjectName("main_content_frame")
        main_layout = QVBoxLayout(main_frame)
        main_layout.setContentsMargins(32, 32, 32, 32)
        main_layout.setSpacing(20)
        
        # כותרת דף דינמית
        self.page_title = QLabel("Current Trip")
        self.page_title.setStyleSheet("""
            font-size: 32px;
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 10px;
            letter-spacing: -0.5px;
        """)
        main_layout.addWidget(self.page_title)
        
        # תת-כותרת דף
        self.page_subtitle = QLabel("Manage your current travel plans")
        self.page_subtitle.setStyleSheet("""
            font-size: 16px;
            color: #718096;
            margin-bottom: 20px;
        """)
        main_layout.addWidget(self.page_subtitle)
        
        # קו מפריד
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet("""
            background-color: #e2e8f0;
            max-height: 1px;
            margin: 0 0 20px 0;
        """)
        main_layout.addWidget(divider)
        
        # Stack של הדפים
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("""
            QStackedWidget {
                background-color: transparent;
                border: none;
            }
        """)
        
        # יצירת הדפים
        self.pages = {
            "current": CurrentTripView(),
            "past": PastTripsView(),
            "new": NewTripView(),
        }
        
        for page in self.pages.values():
            self.content_stack.addWidget(page)
        
        main_layout.addWidget(self.content_stack, stretch=1)
        root_layout.addWidget(main_frame, stretch=1)

    def create_modern_floating_ai_button(self):
        """יצירת כפתור AI צף מודרני עם אפקטים"""
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

    def position_ai_button(self):
        """מיקום הכפתור הצף"""
        margin = 30
        size = self.ai_button.width()
        x = self.width() - size - margin
        y = self.height() - size - margin
        self.ai_button.move(x, y)
        self.ai_button.raise_()

    def resizeEvent(self, event):
        """טיפול בשינוי גודל החלון"""
        super().resizeEvent(event)
        self.position_ai_button()

    def select_page(self, page_key):
        """מעבר בין דפים עם אנימציה"""
        if page_key not in self.pages:
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
        
        # מעבר לדף החדש
        page_index = list(self.pages.keys()).index(page_key)
        self.content_stack.setCurrentIndex(page_index)
        self.current_page = page_key

    def set_username(self, username: str):
        """עדכון שם המשתמש"""
        self.welcome_label.setText(f"Welcome, {username}")

    def set_ai_callback(self, callback):
        """הגדרת קריאה חוזרת לכפתור AI"""
        self.ai_button.clicked.disconnect()  # ניתוק חיבור קודם
        self.ai_button.clicked.connect(callback)

    def open_ai_dialog(self):
        """פתיחת דיאלוג AI מעוצב"""
        dialog = QDialog(self)
        dialog.setWindowTitle("AI Assistant")
        dialog.setMinimumSize(600, 700)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                border-radius: 20px;
            }
        """)
        
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(0, 0, 0, 0)
        
        ai_view = AIChatView(back_callback=dialog.close)
        layout.addWidget(ai_view)
        
        dialog.exec()