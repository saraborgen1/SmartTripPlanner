# client/views/newtrip_view.py

from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QMessageBox, QDateEdit, QComboBox,
    QStackedWidget, QScrollArea, QFrame, QGridLayout, QSizePolicy, QDialog
)
from PySide6.QtCore import QDate, Qt, QSize
from PySide6.QtGui import QPixmap, QFont, QPalette

from client.presenters.newtrip_presenter import NewTripPresenter
from client.utils.ai_button import add_ai_button


class SiteCard(QFrame):
    """כרטיס אטרקציה מודרני"""
    
    def __init__(self, site_data, index, parent_view):
        super().__init__()
        self.site_data = site_data
        self.index = index
        self.parent_view = parent_view
        
        # עיצוב הכרטיס
        self.setFrameStyle(QFrame.StyledPanel)
        self.setStyleSheet("""
            SiteCard {
                border: 1px solid #e0e0e0;
                border-radius: 12px;
                background-color: white;
                margin: 4px;
            }
            SiteCard:hover {
                border: 2px solid #667eea;
                box-shadow: 0 4px 8px rgba(102, 126, 234, 0.1);
            }
        """)
        self.setMinimumHeight(120)
        self.setMaximumHeight(140)
        self.setCursor(Qt.PointingHandCursor)
        
        # Layout האופקי הראשי
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(12)
        
        # תמונה (משמאל)
        self.image_label = QLabel()
        self.image_label.setFixedSize(80, 80)
        self.image_label.setStyleSheet("""
            border: 1px solid #ddd;
            border-radius: 8px;
            background-color: #f8f9fa;
        """)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setText("📷")  # placeholder
        self.image_label.setScaledContents(True)
        main_layout.addWidget(self.image_label)
        
        # אזור הטקסט (באמצע)
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)
        
        place = site_data.get("place", {})
        name = place.get("name", "Unnamed Site")
        category = place.get("category", "Unknown")
        
        # כותרת
        title_label = QLabel(name)
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2d3748; margin-bottom: 2px;")
        title_label.setWordWrap(True)
        text_layout.addWidget(title_label)
        
        # קטגוריה
        category_label = QLabel(f"📍 {category}")
        category_label.setStyleSheet("color: #718096; font-size: 12px;")
        text_layout.addWidget(category_label)
        
        # דירוג (אם קיים)
        rating = place.get("rating")
        if rating:
            try:
                numeric_rating = float(str(rating).replace("h", "").strip())
                rating_text = "⭐" * min(int(numeric_rating), 5)
            except (ValueError, TypeError):
                rating_text = "⭐" * 0  # אין דירוג תקין

            rating_label = QLabel(f"{rating_text} ({rating})")
            rating_label.setStyleSheet("color: #f6ad55; font-size: 12px;")
            text_layout.addWidget(rating_label)
        
        # מידע מסלול
        route = site_data.get("route", {})
        if route.get("routes"):
            segments = route["routes"][0].get("segments", [])
            if segments:
                distance = segments[0].get("distance", 0)
                duration = segments[0].get("duration", 0)
                route_label = QLabel(f"🚗 {distance:.0f}m • {duration/60:.0f} min")
                route_label.setStyleSheet("color: #4a5568; font-size: 11px;")
                text_layout.addWidget(route_label)
        
        text_layout.addStretch()
        main_layout.addLayout(text_layout, stretch=1)
        
        # כפתור הוספה (מימין)
        add_btn = QPushButton("➕")
        add_btn.setFixedSize(40, 40)
        add_btn.setStyleSheet("""
            QPushButton {
                border-radius: 20px;
                background-color: #48bb78;
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #38a169;
            }
            QPushButton:pressed {
                background-color: #2f855a;
            }
        """)
        add_btn.clicked.connect(self._add_to_list)
        main_layout.addWidget(add_btn, alignment=Qt.AlignCenter)
        
        # טעינת תמונה
        self._load_image()
    
    def _load_image(self):
        """טעינת תמונה בצורה בטוחה עם טיפול בברירת מחדל"""
        place = self.site_data.get("place", {})
        image_url = place.get("image")

        # הדפסה דיבאגית לראות מה חוזר מהשרת
        print(f"[DEBUG] image_url for site '{place.get('name', 'Unknown')}' = {image_url}")

        # אם אין תמונה בכלל → ברירת מחדל
        if not image_url:
            self._set_default_image()
            return

        try:
            from urllib.request import urlopen
            data = urlopen(image_url).read()
            pixmap = QPixmap()
            if pixmap.loadFromData(data):
                scaled_pixmap = pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.image_label.setPixmap(scaled_pixmap)
                self.image_label.setText("")  # מנקה את האייקון 📷
            else:
                print(f"[DEBUG] טעינת תמונה נכשלה עבור {image_url}")
                self._set_default_image()
        except Exception as e:
            print(f"[ERROR] לא הצלחתי לטעון את התמונה: {e} | url={image_url}")
            self._set_default_image()

    def _set_default_image(self):
        """מציב תמונת ברירת מחדל אם אין תמונה זמינה"""
        try:
            # אם יש תמונת ברירת מחדל בתיקיית הנכסים
            default_path = "client/assets/default_image.png"
            pixmap = QPixmap(default_path)
            if not pixmap.isNull():
                self.image_label.setPixmap(
                    pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                )
                self.image_label.setText("")
            else:
                # fallback: אם אין קובץ תמונה, מציג את האייקון 📷
                self.image_label.setText("📷")
        except Exception:
            # fallback נוסף במקרה של בעיות בטעינת התמונה
            self.image_label.setText("📷")

    
    def _add_to_list(self):
        """הוספה לרשימת האטרקציות"""
        place = self.site_data.get("place", {})
        name = place.get("name", "Unnamed Site")
        self.parent_view.add_site_to_my_list(name)
        
        # אנימציה קטנה - שינוי צבע הכפתור
        btn = self.sender()
        btn.setText("✓")
        btn.setStyleSheet("""
            QPushButton {
                border-radius: 20px;
                background-color: #68d391;
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
        """)
    
    def mousePressEvent(self, event):
        """טיפול בלחיצה על הכרטיס - פתיחת פרטים"""
        if event.button() == Qt.LeftButton:
            self.parent_view.presenter.show_site_details(self.index)
        super().mousePressEvent(event)


class WeatherWidget(QWidget):
    """ווידג'ט מזג אוויר מעוצב"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        
        # כותרת
        title = QLabel("Weather Forecast")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #2d3748; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # אזור התוכן
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        layout.addWidget(self.content_widget)
        
        layout.addStretch()
    
    def update_weather(self, forecast_data):
        """עדכון תצוגת מזג האוויר"""
        # ניקוי תוכן קיים
        for i in reversed(range(self.content_layout.count())):
            self.content_layout.itemAt(i).widget().setParent(None)
        
        if not forecast_data or "error" in forecast_data:
            error_msg = forecast_data.get("error", "No weather data available") if forecast_data else "No weather data available"
            error_label = QLabel(f"❌ {error_msg}")
            error_label.setStyleSheet("color: #e53e3e; font-size: 14px; padding: 20px;")
            self.content_layout.addWidget(error_label)
            return
        
        dest = forecast_data.get("destination", "Unknown Location")
        location_label = QLabel(f"📍 {dest}")
        location_label.setStyleSheet("color: #4a5568; font-size: 16px; margin-bottom: 10px;")
        self.content_layout.addWidget(location_label)
        
        # יצירת כרטיסי מזג אוויר
        forecast_list = forecast_data.get("forecast", [])
        for day_data in forecast_list[:5]:  # מקסימום 5 ימים
            day_card = self._create_day_card(day_data)
            self.content_layout.addWidget(day_card)
    
    def _create_day_card(self, day_data):
        """יצירת כרטיס יום"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                background-color: #f7fafc;
                padding: 12px;
                margin: 2px 0;
            }
        """)
        
        layout = QHBoxLayout(card)
        
        # תאריך
        date_str = day_data.get("date", "")
        date_label = QLabel(date_str)
        date_label.setStyleSheet("font-weight: bold; color: #2d3748;")
        layout.addWidget(date_label)
        
        layout.addStretch()
        
        # אייקון מזג אוויר (פשוט לעכשיו)
        weather_icon = QLabel("☀️")  # ברירת מחדל - שמש
        weather_icon.setStyleSheet("font-size: 20px;")
        layout.addWidget(weather_icon)
        
        # טמפרטורות
        temp_min = day_data.get("temp_min", "?")
        temp_max = day_data.get("temp_max", "?")
        temp_label = QLabel(f"{temp_min}° - {temp_max}°C")
        temp_label.setStyleSheet("color: #4a5568; font-weight: bold;")
        layout.addWidget(temp_label)
        
        return card


class NewTripView(QWidget):
    def __init__(self, username: str | None = None, back_callback=None, session_manager=None):
        super().__init__()
        self.username = username
        self.session_manager = session_manager
        self.presenter = NewTripPresenter(self, session_manager)
        self._ai_callback = None

        self.setWindowTitle("Create New Trip")
        self.setStyleSheet("""
            QWidget {
                background-color: #f7fafc;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 13px;
            }
            QLabel { color: #2d3748; }
            QLineEdit, QComboBox, QDateEdit {
                border: 1px solid #cbd5e0;
                border-radius: 8px;
                padding: 8px 12px;
                background-color: white;
                min-height: 20px;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
                border: 2px solid #667eea;
                outline: none;
            }
            QPushButton {
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                background-color: #667eea;
                color: white;
                font-weight: 600;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #5a67d8;
            }
            QPushButton:pressed {
                background-color: #4c51bf;
            }
            QPushButton:checked {
                background-color: #4c51bf;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)

        self.setup_ui(back_callback)
        self.showMaximized()


    def setup_ui(self, back_callback):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)

        # כותרת ראשית
        title = QLabel("Create New Trip")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #2d3748; margin-bottom: 10px;")
        main_layout.addWidget(title)

        # כפתור Back (אם קיים)
        if back_callback:
            back_btn = QPushButton("← Back")
            back_btn.clicked.connect(back_callback)
            back_btn.setStyleSheet("""
                QPushButton {
                    background-color: #e2e8f0;
                    color: #4a5568;
                    border-radius: 6px;
                    padding: 6px 12px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #cbd5e0;
                }
            """)
            main_layout.addWidget(back_btn, alignment=Qt.AlignLeft)

        # כפתור AI
        # add_ai_button(main_layout, lambda: self._ai_callback and self._ai_callback())

        # תפריט ניווט
        nav_layout = QHBoxLayout()
        self.btn_search = QPushButton("🔍 Search Sites")
        self.btn_weather = QPushButton("🌤️ Weather")
        self.btn_list = QPushButton("📋 My List")
                # כפתור שמירה חדש - תמיד גלוי בתפריט
        self.btn_save_trip = QPushButton("💾 Save Trip")
        self.btn_save_trip.setMinimumHeight(45)
        self.btn_save_trip.setStyleSheet("""
            QPushButton {
                background-color: #38a169;
                font-weight: bold;
                font-size: 14px;
                padding: 8px 16px;
                border-radius: 8px;
                color: white;
            }
            QPushButton:hover {
                background-color: #2f855a;
            }
        """)
        self.btn_save_trip.clicked.connect(self.on_save_trip)


        for btn in (self.btn_search, self.btn_weather, self.btn_list, self.btn_save_trip):
            btn.setCheckable(btn in (self.btn_search, self.btn_weather, self.btn_list))
            btn.setMinimumHeight(45)
            nav_layout.addWidget(btn)
        main_layout.addLayout(nav_layout)

        # מסכים מוחלפים
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack, stretch=1)

        # יצירת המסכים
        self._create_search_page()
        self._create_weather_page()
        self._create_list_page()

        # חיבור ניווט
        self.btn_search.clicked.connect(lambda: self.set_page(0))
        self.btn_weather.clicked.connect(lambda: self.set_page(1))
        self.btn_list.clicked.connect(lambda: self.set_page(2))
        
        self.set_page(0)

    def _create_search_page(self):
        """יצירת עמוד החיפוש"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        page = QWidget()
        layout = QVBoxLayout(page)
        page.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.setSpacing(16)

        # טופס החיפוש
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 20px;
                border: 1px solid #e2e8f0;
            }
        """)
        form_layout = QVBoxLayout(form_frame)

        # שדות הטופס
        self._create_form_fields(form_layout)
        layout.addWidget(form_frame)

        # אזור התוצאות
        results_label = QLabel("Search Results")
        results_font = QFont()
        results_font.setPointSize(16)
        results_font.setBold(True)
        results_label.setFont(results_font)
        results_label.setStyleSheet("margin-top: 20px; color: #2d3748;")
        layout.addWidget(results_label)

        # אזור כרטיסי האטרקציות
        self.sites_container = QWidget()
        self.sites_layout = QVBoxLayout(self.sites_container)
        self.sites_layout.setSpacing(8)
        self.sites_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        layout.addWidget(self.sites_container)

        # רווח בסוף כדי למנוע חיתוך
        layout.addStretch()

        # הגדרת הדף בתוך ScrollArea
        scroll.setWidget(page)
        self.stack.addWidget(scroll)


    def _create_form_fields(self, layout):
        """יצירת שדות הטופס"""
        # עיר
        layout.addWidget(QLabel("Choose City/Region:"))
        self.city_entry = QLineEdit()
        self.city_entry.setPlaceholderText("e.g., Jerusalem, Tel Aviv, Haifa...")
        layout.addWidget(self.city_entry)

        # כתובת התחלה
        layout.addWidget(QLabel("Start Address:"))
        self.address_entry = QLineEdit()
        self.address_entry.setPlaceholderText("e.g., Jaffa St 1, Jerusalem")
        layout.addWidget(self.address_entry)

        # תאריכים בשורה אחת
        dates_layout = QHBoxLayout()
        
        # תאריך התחלה
        start_layout = QVBoxLayout()
        start_layout.addWidget(QLabel("Start Date:"))
        self.start_entry = QDateEdit()
        self.start_entry.setCalendarPopup(True)
        self.start_entry.setDate(QDate.currentDate())
        self.start_entry.setDisplayFormat("yyyy-MM-dd")
        start_layout.addWidget(self.start_entry)
        dates_layout.addLayout(start_layout)

        # תאריך סיום
        end_layout = QVBoxLayout()
        end_layout.addWidget(QLabel("End Date:"))
        self.end_entry = QDateEdit()
        self.end_entry.setCalendarPopup(True)
        self.end_entry.setDate(QDate.currentDate().addDays(1))
        self.end_entry.setDisplayFormat("yyyy-MM-dd")
        self.end_entry.setMinimumDate(self.start_entry.date())
        self.start_entry.dateChanged.connect(lambda d: self.end_entry.setMinimumDate(d))
        end_layout.addWidget(self.end_entry)
        dates_layout.addLayout(end_layout)

        layout.addLayout(dates_layout)

        # תחבורה
        layout.addWidget(QLabel("Transport Mode:"))
        self.transport_combo = QComboBox()
        self.transport_combo.addItems(["🚗 Car", "🚶 Walking", "🚴 Cycling"])
        layout.addWidget(self.transport_combo)

        # כפתור חיפוש
        self.create_btn = QPushButton("🔍 Search for Sites")
        self.create_btn.setMinimumHeight(50)
        self.create_btn.setStyleSheet("""
            QPushButton {
                background-color: #48bb78;
                font-size: 16px;
                font-weight: bold;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #38a169;
            }
            QPushButton:disabled {
                background-color: #a0aec0;
                color: #718096;
            }
        """)
        self.create_btn.clicked.connect(self.on_create_trip)
        layout.addWidget(self.create_btn)

        # קיצורי מקלדת
        self.address_entry.returnPressed.connect(self.create_btn.click)
        self.city_entry.returnPressed.connect(self.create_btn.click)

    def _create_weather_page(self):
        """יצירת עמוד מזג האוויר"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.weather_widget = WeatherWidget()
        scroll.setWidget(self.weather_widget)
        self.stack.addWidget(scroll)

    def _create_list_page(self):
        """יצירת עמוד הרשימה"""
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(10)

        # ScrollArea עם רשימת האטרקציות
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        page = QWidget()
        layout = QVBoxLayout(page)
        page.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.setSpacing(16)

        # כותרת
        title = QLabel("My Selected Attractions")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # רשימת האטרקציות
        self.my_sites_list = QListWidget()
        self.my_sites_list.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #f1f5f9;
                border-radius: 4px;
                margin: 2px 0;
            }
            QListWidget::item:hover {
                background-color: #f8fafc;
            }
            QListWidget::item:selected {
                background-color: #edf2f7;
                color: #2d3748;
            }
        """)
        layout.addWidget(self.my_sites_list, stretch=1)

        page.setLayout(layout)
        scroll.setWidget(page)

        # הוספת Scroll לאזור הראשי
        container_layout.addWidget(scroll, stretch=1)

        # הוספת הכל לסטאק
        self.stack.addWidget(container)


    def set_page(self, index: int):
        """מעבר בין עמודים"""
        self.stack.setCurrentIndex(index)
        buttons = [self.btn_search, self.btn_weather, self.btn_list]
        for i, btn in enumerate(buttons):
            btn.setChecked(i == index)

    def on_create_trip(self):
        """טיפול בבקשת חיפוש אטרקציות"""
        city = self.city_entry.text().strip()
        if not city:
            self.show_error("Please enter a city/destination.")
            return

        address = self.address_entry.text().strip() or city

        if self.end_entry.date() < self.start_entry.date():
            self.show_error("End date must be after start date.")
            return

        # מיפוי תחבורה
        mode_text = self.transport_combo.currentText()
        profile = {
            "🚗 Car": "driving-car",
            "🚶 Walking": "foot-walking",
            "🚴 Cycling": "cycling-regular",
        }.get(mode_text, "driving-car")

        # השבתת כפתור והפעלת חיפוש
        self.create_btn.setEnabled(False)
        self.create_btn.setText("🔍 Searching...")
        
        try:
            self.presenter.load_sites(city, address, profile, limit=20)
            self.presenter.update_weather(city)
        finally:
            self.create_btn.setEnabled(True)
            self.create_btn.setText("🔍 Search for Sites")

    def show_sites(self, sites: list[dict]):
        """הצגת רשימת האטרקציות בכרטיסים"""
        # ניקוי תוצאות קודמות
        for i in reversed(range(self.sites_layout.count())):
            child = self.sites_layout.itemAt(i).widget()
            if child:
                child.setParent(None)

        if not sites:
            no_results = QLabel("No sites found. Try a different city or search terms.")
            no_results.setStyleSheet("color: #718096; font-style: italic; padding: 20px; text-align: center;")
            no_results.setAlignment(Qt.AlignCenter)
            self.sites_layout.addWidget(no_results)
            return

        # יצירת כרטיסים
        for i, site in enumerate(sites):
            card = SiteCard(site, i, self)
            self.sites_layout.addWidget(card)

        # רווח בסוף
        spacer = QWidget()
        spacer.setFixedHeight(40)
        self.sites_layout.addWidget(spacer)

    def show_weather(self, forecast_data: dict | None):
        """הצגת מזג אוויר"""
        self.weather_widget.update_weather(forecast_data)

    def add_site_to_my_list(self, site_name: str):
        """הוספת אטרקציה לרשימה"""
        if not site_name:
            return
            
        # בדיקה שלא קיים כבר
        existing = [self.my_sites_list.item(i).text() for i in range(self.my_sites_list.count())]
        if site_name in existing:
            self.show_message(f"'{site_name}' is already in your list!")
            return

        self.my_sites_list.addItem(f"📍 {site_name}")
        self.show_message(f"Added '{site_name}' to your list!")

    def on_save_trip(self):
        """שמירת הטיול"""
        # אם אין שם משתמש גם במסך וגם בסשן → שגיאה
        username = self.username or (
        self.session_manager.username if self.session_manager else None
        )

        token = self.session_manager.user_token if self.session_manager else None

        if not username or not token:
            self.show_error("No logged-in user detected. Please log in first.")
            return


        selected_sites = []
        for i in range(self.my_sites_list.count()):
            item_text = self.my_sites_list.item(i).text()
            clean_name = item_text.replace("📍 ", "").strip()
            selected_sites.append(clean_name)

        if not selected_sites:
            self.show_error("Please add at least one site to your list.")
            return

        mode_text = self.transport_combo.currentText()
        transport = {
            "🚗 Car": ["car"],
            "🚶 Walking": ["foot"],
            "🚴 Cycling": ["bike"],
        }.get(mode_text, ["foot"])

        self.presenter.save_trip(
            username=username,
            start=self.start_entry.date().toString("yyyy-MM-dd"),
            end=self.end_entry.date().toString("yyyy-MM-dd"),
            city=self.city_entry.text().strip(),
            transport=transport,
            selected_sites=selected_sites,
        )
        self.reset_form()



    def on_site_clicked(self, item):
        """לא בשימוש - מוחלף בלחיצה על כרטיס"""
        pass

    def show_message(self, msg: str):
        """הצגת הודעת מידע"""
        QMessageBox.information(self, "Info", msg)

    def show_error(self, msg: str):
        """הצגת הודעת שגיאה"""
        QMessageBox.critical(self, "Error", msg)

    def set_ai_callback(self, cb):
        """הגדרת callback לכפתור AI"""
        self._ai_callback = cb

    def reset_form(self):
        """איפוס כל שדות הטופס אחרי שמירת טיול"""
        # איפוס שדות טקסט
        self.city_entry.clear()
        self.address_entry.clear()

        # איפוס תאריכים (ברירת מחדל - היום + מחר)
        self.start_entry.setDate(QDate.currentDate())
        self.end_entry.setDate(QDate.currentDate().addDays(1))

        # איפוס תחבורה
        self.transport_combo.setCurrentIndex(0)

        # ניקוי רשימת האתרים שנבחרו
        self.my_sites_list.clear()

        # ניקוי התוצאות הקודמות של החיפוש
        for i in reversed(range(self.sites_layout.count())):
            child = self.sites_layout.itemAt(i).widget()
            if child:
                child.setParent(None)

        # חזרה לעמוד החיפוש כברירת מחדל
        self.set_page(0)
