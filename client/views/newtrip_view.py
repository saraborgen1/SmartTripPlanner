# client/views/newtrip_view.py

from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QListWidget, QMessageBox, QDateEdit, QComboBox,
    QStackedWidget, QScrollArea, QFrame, QSizePolicy,  QTextEdit
)
from PySide6.QtCore import QDate, Qt, QSize, QPointF
from PySide6.QtGui import QPixmap, QFont, QPainter, QIcon
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QCategoryAxis

from client.presenters.newtrip_presenter import NewTripPresenter
from client.utils.ai_button import add_ai_button

"""כרטיס אטרקציה מודרני שמציג אתר תיירות יחיד"""
class SiteCard(QFrame):
    
    def __init__(self, site_data, index, parent_view):
        super().__init__()
        self.site_data = site_data      # המידע על האתר (שם, קטגוריה, תמונה וכו')
        self.index = index              # המיקום שלו ברשימת האתרים
        self.parent_view = parent_view  # הפניה למסך הראשי כדי לעדכן ממנו
        
        # עיצוב כללי של הכרטיס
        self.setFrameStyle(QFrame.StyledPanel)
        self.setMinimumHeight(120)
        self.setMaximumHeight(140)
        self.setCursor(Qt.PointingHandCursor)
        
        # Layout ראשי אופקי (תמונה + טקסט + כפתור)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(12)
        
        # 📷 תמונה משמאל (אם אין - יוצג אייקון ברירת מחדל)
        self.image_label = QLabel()
        self.image_label.setFixedSize(80, 80)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setText("📷")  
        self.image_label.setScaledContents(True)
        main_layout.addWidget(self.image_label)
        
        # טקסט באמצע: שם האתר, קטגוריה, דירוג, מסלול
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)
        
        place = site_data.get("place", {})
        name = place.get("name", "Unnamed Site")
        category = place.get("category", "Unknown")
        
        # שם האתר (כותרת מודגשת)
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
        
        # דירוג (אם קיים - נציג כוכבים)
        rating = place.get("rating")
        if rating:
            try:
                numeric_rating = float(str(rating).replace("h", "").strip())
                rating_text = "⭐" * min(int(numeric_rating), 5)
            except (ValueError, TypeError):
                rating_text = "⭐" * 0  
            rating_label = QLabel(f"{rating_text} ({rating})")
            text_layout.addWidget(rating_label)
        
        # מידע על מסלול (מרחק + זמן)
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
        
        # כפתור ➕/✔️ להוספה או הסרה     
        self.add_btn = QPushButton(self)
        self.add_btn.setIcon(QIcon("client/assets/plus.png")) 
        self.add_btn.setIconSize(QSize(24, 24))
        self.add_btn.setFixedSize(40, 40)
        self.add_btn.clicked.connect(self._toggle_site)
        main_layout.addWidget(self.add_btn, 0, Qt.AlignRight | Qt.AlignVCenter)

        # טעינת תמונה אמיתית (אם יש URL)
        self._load_image()
    

    """ניסיון טעינת תמונה מתוך ה־URL אם קיים"""
    def _load_image(self):

        place = self.site_data.get("place", {})
        image_info = place.get("image")
        if not image_info:
            self._set_default_image()
            return
        try:
            import requests
            if isinstance(image_info, dict):
                url = image_info.get("url")
                headers = image_info.get("headers", {})
            else:
                url = str(image_info)
                headers = {}
            if not url:
                self._set_default_image()
                return
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                pixmap = QPixmap()
                if pixmap.loadFromData(resp.content):
                    scaled = pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.image_label.setPixmap(scaled)
                    self.image_label.setText("")
                    return
            self._set_default_image()
        except Exception as e:
            print(f"[ERROR] image load failed: {e}")
            self._set_default_image()


    """מציב תמונת ברירת מחדל אם אין תמונה זמינה"""
    def _set_default_image(self):

        try:
            default_path = "client/assets/default_image.png"
            pixmap = QPixmap(default_path)
            if not pixmap.isNull():
                self.image_label.setPixmap(
                    pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                )
                self.image_label.setText("")
            else:
                self.image_label.setText("📷")
        except Exception:
            self.image_label.setText("📷")

    
    """לחיצה על כפתור ➕ / ✔️ כדי להוסיף או להסיר מהרשימה"""
    def _toggle_site(self):

        place = self.site_data.get("place", {})
        name = place.get("name", "Unnamed Site")
        # אם כבר קיים ברשימה → מסירים
        if name in [self.parent_view.my_sites_list.item(i).text().replace("📍 ", "") 
                    for i in range(self.parent_view.my_sites_list.count())]:
            items = self.parent_view.my_sites_list.findItems(f"📍 {name}", Qt.MatchExactly)
            for item in items:
                row = self.parent_view.my_sites_list.row(item)
                self.parent_view.my_sites_list.takeItem(row)
            self.add_btn.setIcon(QIcon("client/assets/plus.png"))
        # מוסיפים לרשימה
        else:
            self.parent_view.add_site_to_my_list(name)
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

    
    """לחיצה על כל הכרטיס → פתיחת חלון פרטים מלאים"""
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parent_view.presenter.show_site_details(self.index)
        super().mousePressEvent(event)


"""ווידג'ט להצגת תחזית מזג אוויר"""
class WeatherWidget(QWidget):
    
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
        
        # אזור תוכן (שיתעדכן כל פעם מחדש)
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        layout.addWidget(self.content_widget, 1)  
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(8)

    
    """עדכון התחזית על המסך לפי נתונים מהשרת"""
    def update_weather(self, forecast_data):
        # ניקוי תוכן קיים
        for i in reversed(range(self.content_layout.count())):
            self.content_layout.itemAt(i).widget().setParent(None)
        # אם יש שגיאה
        if not forecast_data or "error" in forecast_data:
            if forecast_data:
                error_msg = forecast_data.get("error", "No weather data available")
            else:
                error_msg = "No weather data available"
            error_label = QLabel(f"❌ {error_msg}")
            self.content_layout.addWidget(error_label)
            return
        # שם יעד
        dest = forecast_data.get("destination", "Unknown Location")
        location_label = QLabel(f"📍 {dest}")
        self.content_layout.addWidget(location_label)
        
        # הוספת גרף תחזית
        forecast_list = forecast_data.get("forecast", [])
        if forecast_list:
            chart_view = WeatherChart(forecast_list[:7])
            self.content_layout.addWidget(chart_view)
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setWidget(chart_view)
            self.content_layout.addWidget(scroll, 1)


    """גרף טמפרטורות למספר ימים קדימה"""
    def _create_day_card(self, day_data):

        card = QFrame()
        layout = QHBoxLayout(card)
        
        # תאריך
        date_str = day_data.get("date", "")
        date_label = QLabel(date_str)
        layout.addWidget(date_label)
        layout.addStretch()
        
        # אייקון מזג אוויר (פשוט לעכשיו)
        weather_icon = QLabel("☀️")  
        layout.addWidget(weather_icon)
        
        # שני קווים: מינימום ומקסימום
        temp_min = day_data.get("temp_min", "?")
        temp_max = day_data.get("temp_max", "?")
        temp_label = QLabel(f"{temp_min}° - {temp_max}°C")
        layout.addWidget(temp_label)
        
        return card


"""גרף טמפרטורות למספר ימים קדימה"""
class WeatherChart(QChartView):

    def __init__(self, forecast_list):
        super().__init__()

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setFixedHeight(250)  

        # שני קווים: מינימום ומקסימום
        series_min = QLineSeries(name="Min Temp")
        series_max = QLineSeries(name="Max Temp")
        series_min.setColor(Qt.blue)
        series_max.setColor(Qt.red)
        series_min.setPointsVisible(True)
        series_max.setPointsVisible(True)

        # הוספת נקודות
        for i, day_data in enumerate(forecast_list):
            try:
                temp_min = float(str(day_data.get("temp_min", 0)).replace("°", ""))
                temp_max = float(str(day_data.get("temp_max", 0)).replace("°", ""))
                series_min.append(QPointF(i, temp_min))
                series_max.append(QPointF(i, temp_max))
            except Exception:
                continue

        # הגדרת הגרף
        chart = QChart()
        chart.addSeries(series_min)
        chart.addSeries(series_max)
        chart.setTitle("Weather Forecast")
        chart.createDefaultAxes()
        chart.legend().setVisible(True)

        # ציר X עם שמות הימים
        axisX = QCategoryAxis()
        axisX.setTitleText("Day")
        for i, day_data in enumerate(forecast_list):
            date_str = str(day_data.get("date", f"Day {i+1}"))
            axisX.append(date_str, i)
        chart.setAxisX(axisX, series_min)
        chart.setAxisX(axisX, series_max)

        # ציר Y = טמפרטורה
        axisY = QValueAxis()
        axisY.setTitleText("°C")
        chart.setAxisY(axisY, series_min)
        chart.setAxisY(axisY, series_max)

        self.setChart(chart)
        self.setRenderHint(QPainter.Antialiasing)


"""מסך יצירת טיול חדש: חיפוש אתרים, מזג אוויר, רשימה והערות"""
class NewTripView(QWidget):

    def __init__(self, username: str | None = None, back_callback=None,
             session_manager=None, on_save_callback=None):
        
        super().__init__()
        self.username = username
        self.session_manager = session_manager
        self.presenter = NewTripPresenter(self, session_manager)
        self._ai_callback = None
        self.on_save_callback = on_save_callback  
        self._back_btn = None   

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

        # כפתור Back 
        if back_callback:
            self._back_btn = QPushButton("← Back")
            self._back_btn.clicked.connect(lambda: self._handle_back(back_callback))
            main_layout.addWidget(self._back_btn, alignment=Qt.AlignLeft)

        # תפריט ניווט
        nav_layout = QHBoxLayout()
        self.btn_search = QPushButton("🔍 Search Sites")
        self.btn_weather = QPushButton("🌤️ Weather")
        self.btn_list = QPushButton("📋 My List")
        self.btn_notes = QPushButton("📝 Notes")
        self.btn_save_trip = QPushButton("💾 Save Trip")
        self.btn_save_trip.setMinimumHeight(45)
        self.btn_save_trip.clicked.connect(self.on_save_trip)

        # כל הכפתורים מתווספים ל־layout
        for btn in (self.btn_search, self.btn_weather, self.btn_list, self.btn_notes, self.btn_save_trip):
            btn.setCheckable(btn in (self.btn_search, self.btn_weather, self.btn_list, self.btn_notes))
            btn.setMinimumHeight(45)
            nav_layout.addWidget(btn)
        main_layout.addLayout(nav_layout)

        #להחלפת מסכים (חיפוש, מזג אוויר, רשימה, הערות)
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack, stretch=1)

        # יצירת המסכים
        self._create_search_page()
        self._create_weather_page()
        self._create_list_page()
        self._create_notes_page()

        # חיבור כפתורי הניווט למעבר בין המסכים
        self.btn_search.clicked.connect(lambda: self.set_page(0))
        self.btn_weather.clicked.connect(lambda: self.set_page(1))
        self.btn_list.clicked.connect(lambda: self.set_page(2))
        self.btn_notes.clicked.connect(lambda: self.set_page(3))
        
        self.set_page(0)


    """ניקוי טופס וחזרה למסך הקודם"""
    def _handle_back(self, callback):

        self.reset_form()  
        callback()          


    """יצירת עמוד החיפוש"""
    def _create_search_page(self):

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

        # יצירת השדות (עיר, כתובת, תאריכים, תחבורה)
        self._create_form_fields(form_layout)
        layout.addWidget(form_frame)

        # כותרת "תוצאות"
        results_label = QLabel("Search Results")
        results_font = QFont()
        results_font.setPointSize(16)
        results_font.setBold(True)
        results_label.setFont(results_font)
        layout.addWidget(results_label)

        # אזור התוצאות
        self.sites_container = QWidget()
        self.sites_layout = QVBoxLayout(self.sites_container)
        self.sites_layout.setSpacing(8)
        self.sites_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        layout.addWidget(self.sites_container)

        layout.addStretch()
        scroll.setWidget(page)
        self.stack.addWidget(scroll)


    """יוצר את שדות הטופס שבהם המשתמש ממלא פרטי טיול חדש:
        עיר, כתובת התחלה, תאריכי התחלה וסיום, אמצעי תחבורה,
        ולבסוף כפתור חיפוש אתרים.
    """
    def _create_form_fields(self, layout):

        # שדה להזנת עיר/אזור
        layout.addWidget(QLabel("Choose City/Region:"))
        self.city_entry = QLineEdit()
        self.city_entry.setPlaceholderText("e.g., Jerusalem, Tel Aviv, Haifa...")
        layout.addWidget(self.city_entry)

        # שדה להזנת כתובת התחלה
        layout.addWidget(QLabel("Start Address:"))
        self.address_entry = QLineEdit()
        self.address_entry.setPlaceholderText("e.g., Jaffa St 1, Jerusalem")
        layout.addWidget(self.address_entry)

        # יצירת לייאאוט אופקי לשדות תאריכים
        dates_layout = QHBoxLayout()
        
        # בחירת תאריך התחלה
        start_layout = QVBoxLayout()
        start_layout.addWidget(QLabel("Start Date:"))
        self.start_entry = QDateEdit()
        self.start_entry.setCalendarPopup(True)
        self.start_entry.setDate(QDate.currentDate())
        self.start_entry.setDisplayFormat("yyyy-MM-dd")
        start_layout.addWidget(self.start_entry)
        dates_layout.addLayout(start_layout)

        # בחירת תאריך סיום
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

        # הוספת לייאאוט התאריכים כולו לטופס
        layout.addLayout(dates_layout)

        # בחירת אמצעי תחבורה
        layout.addWidget(QLabel("Transport Mode:"))
        self.transport_combo = QComboBox()
        self.transport_combo.addItems(["🚗 Car", "🚶 Walking", "🚴 Cycling"])
        layout.addWidget(self.transport_combo)

        # כפתור חיפוש אתרים
        self.create_btn = QPushButton("🔍 Search for Sites")
        self.create_btn.setMinimumHeight(50)
        self.create_btn.clicked.connect(self.on_create_trip)
        layout.addWidget(self.create_btn)

        # קיצורי מקלדת: לחיצה על Enter מפעילה את החיפוש
        self.address_entry.returnPressed.connect(self.create_btn.click)
        self.city_entry.returnPressed.connect(self.create_btn.click)


    # יצירת עמוד מזג אוויר
    def _create_weather_page(self):

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.weather_widget = WeatherWidget()
        self.weather_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        scroll.setWidget(self.weather_widget)
        self.stack.addWidget(scroll)


    # יצירת עמוד רשימת האטרקציות שנבחרו
    def _create_list_page(self):

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(10)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # יצירת דף פנימי עם כותרת ורשימה
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
        container_layout.addWidget(scroll, stretch=1)
        self.stack.addWidget(container)


    # יצירת עמוד הערות
    def _create_notes_page(self):

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(16)
        layout.setContentsMargins(16, 16, 16, 16)

        # כותרת
        title = QLabel("Trip Notes")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # תיבת טקסט לערות
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Write your ideas or notes for this trip here...")
        layout.addWidget(self.notes_edit, stretch=1)

        scroll.setWidget(page)
        self.stack.addWidget(scroll)


    # מעבר בין עמודים
    def set_page(self, index: int):

        self.stack.setCurrentIndex(index)
        buttons = [self.btn_search, self.btn_weather, self.btn_list, self.btn_notes]
        for i, btn in enumerate(buttons):
            btn.setChecked(i == index)


    # טיפול בלחיצה על כפתור חיפוש אתרים
    def on_create_trip(self):

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
            # מחזיר את הכפתור למצב רגיל
            self.create_btn.setEnabled(True)
            self.create_btn.setText("🔍 Search for Sites")


    # הצגת רשימת האטרקציות שנמצאו
    def show_sites(self, sites: list[dict]):
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


    # הצגת תחזית מזג אוויר
    def show_weather(self, forecast_data: dict | None):

        self.weather_widget.update_weather(forecast_data)


    # הוספת אטרקציה לרשימה האישית
    def add_site_to_my_list(self, site_name: str):

        if not site_name:
            return
            
        # בדיקה שלא קיים כבר
        existing = [self.my_sites_list.item(i).text() for i in range(self.my_sites_list.count())]
        if site_name in existing:
            self.show_message(f"'{site_name}' is already in your list!")
            return

        self.my_sites_list.addItem(f"📍 {site_name}")
        self.show_message(f"Added '{site_name}' to your list!")


    # שמירת הטיול
    def on_save_trip(self):

        username = self.username or (
            self.session_manager.username if self.session_manager else None
        )
        token = self.session_manager.user_token if self.session_manager else None

        if not username or not token:
            self.show_error("No logged-in user detected. Please log in first.")
            return
        
        # איסוף אתרים שנבחרו
        selected_sites = []
        for i in range(self.my_sites_list.count()):
            item_text = self.my_sites_list.item(i).text()
            clean_name = item_text.replace("📍 ", "").strip()
            selected_sites.append(clean_name)

        if not selected_sites:
            self.show_error("Please add at least one site to your list.")
            return

        # מיפוי אמצעי תחבורה
        mode_text = self.transport_combo.currentText()
        transport = {
            "🚗 Car": ["car"],
            "🚶 Walking": ["foot"],
            "🚴 Cycling": ["bike"],
        }.get(mode_text, ["foot"])

        notes_text = self.notes_edit.toPlainText() if hasattr(self, "notes_edit") else ""

        #  נגדיר פונקציה שתקרה אחרי הצלחה
        def on_success():
            self.reset_form()
            if self.on_save_callback:
                self.on_save_callback()

        trip_id = getattr(self, "current_trip_id", None)

        # קריאה לשמירה דרך הפרזנטור
        self.presenter.save_trip(
            username=username,
            start=self.start_entry.date().toString("yyyy-MM-dd"),
            end=self.end_entry.date().toString("yyyy-MM-dd"),
            city=self.city_entry.text().strip(),
            transport=transport,
            selected_sites=selected_sites,
            notes=notes_text, 
            on_success=on_success,
            trip_id=trip_id
        )


    #כפתור Back - עדכון בזמן ריצה
    def set_back_callback(self, callback):

        if self._back_btn:
            try:
                self._back_btn.clicked.disconnect()
            except Exception:
                pass
            self._back_btn.clicked.connect(lambda: self._handle_back(callback))


    # הצגת הודעות מידע למשתמש
    def show_message(self, msg: str):
        QMessageBox.information(self, "Info", msg)

    # הצגת הודעות שגיאה למשתמש
    def show_error(self, msg: str):
        QMessageBox.critical(self, "Error", msg)

    # הגדרת פונקציית AI שתקרה בלחיצה על כפתור AI
    def set_ai_callback(self, cb):
        self._ai_callback = cb

    # איפוס כל שדות הטופס   
    def reset_form(self):

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

        if hasattr(self, "notes_edit"):
            self.notes_edit.clear()

        # חזרה לעמוד החיפוש כברירת מחדל
        self.set_page(0)

    # טעינת טיול קיים לעריכה
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

        # Notes (אם קיים בשמירה)
        if hasattr(self, "notes_edit"):
            self.notes_edit.clear()
            if "notes" in trip_data and isinstance(trip_data["notes"], str):
                self.notes_edit.setPlainText(trip_data["notes"])

        # מעבר אוטומטי לדף הרשימה כדי לראות את האטרקציות
        self.set_page(2)