# client/views/newtrip_view.py

from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QMessageBox, QDateEdit, QComboBox,
    QStackedWidget, QScrollArea, QFrame, QGridLayout, QSizePolicy, QDialog
)
from PySide6.QtCore import QDate, Qt, QSize
from PySide6.QtGui import QPixmap, QFont, QPalette, QIcon

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
        title_label.setWordWrap(True)
        text_layout.addWidget(title_label)
        
        # קטגוריה
        category_label = QLabel(f"📍 {category}")
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
            text_layout.addWidget(rating_label)
        
        # מידע מסלול
        route = site_data.get("route", {})
        if route.get("routes"):
            segments = route["routes"][0].get("segments", [])
            if segments:
                distance = segments[0].get("distance", 0)
                duration = segments[0].get("duration", 0)
                route_label = QLabel(f"🚗 {distance:.0f}m • {duration/60:.0f} min")
                text_layout.addWidget(route_label)
        
        text_layout.addStretch()
        main_layout.addLayout(text_layout, stretch=1)
        
        # כפתור הוספה (מימין)
     
        self.add_btn = QPushButton(self)
        self.add_btn.setIcon(QIcon("client/assets/plus.png"))  # פלוס מתוך הקובץ המקומי
        self.add_btn.setIconSize(QSize(24, 24))
        self.add_btn.setFixedSize(40, 40)

        self.add_btn.clicked.connect(self._toggle_site)
        main_layout.addWidget(self.add_btn, 0, Qt.AlignRight | Qt.AlignVCenter)

        
        # טעינת תמונה
        self._load_image()
    
    def _load_image(self):
        """טעינת תמונה בצורה בטוחה עם טיפול בברירת מחדל"""
        place = self.site_data.get("place", {})
        image_url = place.get("image")



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

    
    def _toggle_site(self):
        place = self.site_data.get("place", {})
        name = place.get("name", "Unnamed Site")

        if name in [self.parent_view.my_sites_list.item(i).text().replace("📍 ", "") 
                    for i in range(self.parent_view.my_sites_list.count())]:
            # אם כבר קיים → נסיר
            items = self.parent_view.my_sites_list.findItems(f"📍 {name}", Qt.MatchExactly)
            for item in items:
                row = self.parent_view.my_sites_list.row(item)
                self.parent_view.my_sites_list.takeItem(row)

            # חזרה למצב פלוס סגול
            self.add_btn.setIcon(QIcon("client/assets/plus.png"))
        else:
            # מוסיפים לרשימה
            self.parent_view.add_site_to_my_list(name)

            # מעבר למצב וי ירוק
            self.add_btn.setIcon(QIcon("client/assets/check.png"))
            self.add_btn.setStyleSheet("""
                            QPushButton {
                                border-radius: 20px;
                                background-color: #10B981;
                            }
                            QPushButton:hover {
                                background-color: #059669;
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
            self.content_layout.addWidget(error_label)
            return
        
        dest = forecast_data.get("destination", "Unknown Location")
        location_label = QLabel(f"📍 {dest}")
        self.content_layout.addWidget(location_label)
        
        # יצירת כרטיסי מזג אוויר
        forecast_list = forecast_data.get("forecast", [])
        for day_data in forecast_list[:5]:  # מקסימום 5 ימים
            day_card = self._create_day_card(day_data)
            self.content_layout.addWidget(day_card)
    
    def _create_day_card(self, day_data):
        """יצירת כרטיס יום"""
        card = QFrame()
        layout = QHBoxLayout(card)
        
        # תאריך
        date_str = day_data.get("date", "")
        date_label = QLabel(date_str)
        layout.addWidget(date_label)
        
        layout.addStretch()
        
        # אייקון מזג אוויר (פשוט לעכשיו)
        weather_icon = QLabel("☀️")  # ברירת מחדל - שמש
        layout.addWidget(weather_icon)
        
        # טמפרטורות
        temp_min = day_data.get("temp_min", "?")
        temp_max = day_data.get("temp_max", "?")
        temp_label = QLabel(f"{temp_min}° - {temp_max}°C")
        layout.addWidget(temp_label)
        
        return card


class NewTripView(QWidget):
    def __init__(self, username: str | None = None, back_callback=None, session_manager=None, on_save_callback=None):
        super().__init__()
        self.username = username
        self.session_manager = session_manager
        self.presenter = NewTripPresenter(self, session_manager)
        self._ai_callback = None
        self.on_save_callback = on_save_callback  
        self._back_btn = None   # נשמור כאן את הכפתור כדי שנוכל לשנות אותו אחר כך



        self.setWindowTitle("Create New Trip")

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
        main_layout.addWidget(title)

        # כפתור Back (אם קיים)
        if back_callback:
            self._back_btn = QPushButton("← Back")
            self._back_btn.clicked.connect(lambda: self._handle_back(back_callback))
            main_layout.addWidget(self._back_btn, alignment=Qt.AlignLeft)


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

    def _handle_back(self, callback):
        """ניקוי טופס וחזרה למסך הקודם"""
        self.reset_form()   # מנקה את כל מה שהוזן
        callback()          # מבצע את החזרה

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

        # 👇 נגדיר פונקציה שתקרה אחרי הצלחה
        def on_success():
            self.reset_form()
            if self.on_save_callback:
                self.on_save_callback()

        trip_id = getattr(self, "current_trip_id", None)

        # נעביר את ה־callback ל־presenter
        self.presenter.save_trip(
            username=username,
            start=self.start_entry.date().toString("yyyy-MM-dd"),
            end=self.end_entry.date().toString("yyyy-MM-dd"),
            city=self.city_entry.text().strip(),
            transport=transport,
            selected_sites=selected_sites,
            on_success=on_success,
            trip_id=trip_id
        )

    def set_back_callback(self, callback):
        """עדכון פעולה של כפתור Back בזמן ריצה"""
        if self._back_btn:
            try:
                self._back_btn.clicked.disconnect()
            except Exception:
                pass
            # נעטוף את הקריאה עם reset_form
            self._back_btn.clicked.connect(lambda: self._handle_back(callback))




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

    def load_trip(self, trip_data: dict):
        self.current_trip = trip_data
        self.current_trip_id = trip_data.get("id")

        """מילוי טופס העריכה לפי נתוני טיול קיים"""
        if not trip_data:
            return

        # יעד
        self.city_entry.setText(trip_data.get("destination", ""))

        # כתובת התחלה – אם לא קיים ניקח את שם העיר
        self.address_entry.setText(trip_data.get("address", trip_data.get("destination", "")))

        # תאריכים
        start_date = trip_data.get("start_date")
        end_date = trip_data.get("end_date")
        if start_date:
            self.start_entry.setDate(QDate.fromString(start_date, "yyyy-MM-dd"))
        if end_date:
            self.end_entry.setDate(QDate.fromString(end_date, "yyyy-MM-dd"))

        # תחבורה
        transport_map = {
            "car": "🚗 Car",
            "foot": "🚶 Walking",
            "bike": "🚴 Cycling"
        }
        transport_list = trip_data.get("transport", [])
        if transport_list:
            mode = transport_map.get(transport_list[0], "🚗 Car")
            index = self.transport_combo.findText(mode)
            if index >= 0:
                self.transport_combo.setCurrentIndex(index)

        # אתרים נבחרים
        self.my_sites_list.clear()
        for site in trip_data.get("selected_sites", []):
            self.my_sites_list.addItem(f"📍 {site}")

        # מעבר אוטומטי לדף הרשימה כדי לראות את האטרקציות
        self.set_page(2)