# client/views/newtrip_view.py
from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QListWidget, QListWidgetItem, QMessageBox, QDateEdit, QTabWidget, QComboBox
)
from PySide6.QtCore import QDate, Qt

from client.presenters.newtrip_presenter import NewTripPresenter
from client.utils.ai_button import add_ai_button


class NewTripView(QWidget):
    """
    מחלקת View ליצירת טיול חדש.

    כוללת:
    - טפסים לבחירת עיר, כתובת התחלה ותאריכים
    - בחירת אמצעי תחבורה
    - טעינת אתרים
    - לשונית תחזית מזג אוויר
    - רשימת אתרים שנבחרו
    - שמירה של הטיול
    - כפתור AI לתקשורת עם הסוכן
    """

    def __init__(self, username: str | None = None, back_callback=None):
        super().__init__()
        self.username = username
        self.presenter = NewTripPresenter(self)
        self._ai_callback = None  # ימולא ע"י main.py

        # כותרת חלון
        self.setWindowTitle("Create New Trip")
        self.setGeometry(200, 200, 600, 520)

        # Layout ראשי
        # QVBoxLayout
        main_layout = QVBoxLayout(self)

        # כפתור Back אופציונלי
        # QPushButton
        if back_callback:
            back_btn = QPushButton("Back")
            back_btn.clicked.connect(back_callback)
            main_layout.addWidget(back_btn, alignment=Qt.AlignLeft)

        # כפתור AI למעלה
        add_ai_button(main_layout, lambda: self._ai_callback and self._ai_callback())

        # Tabs ראשיות
        # QTabWidget
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # ===== לשונית חיפוש =====
        search_tab = QWidget()
        search_layout = QVBoxLayout(search_tab)

        # עיר/אזור
        self.city_entry = QLineEdit()
        self.city_entry.setPlaceholderText("e.g., Jerusalem")
        search_layout.addWidget(QLabel("Choose City/Region:"))
        search_layout.addWidget(self.city_entry)

        # כתובת התחלה
        self.address_entry = QLineEdit()
        self.address_entry.setPlaceholderText("e.g., Jaffa St 1, Jerusalem")
        search_layout.addWidget(QLabel("Start address (origin for routes):"))
        search_layout.addWidget(self.address_entry)

        # תאריך התחלה
        self.start_entry = QDateEdit()
        self.start_entry.setCalendarPopup(True)
        self.start_entry.setDate(QDate.currentDate())
        self.start_entry.setDisplayFormat("yyyy-MM-dd")
        search_layout.addWidget(QLabel("Start Date:"))
        search_layout.addWidget(self.start_entry)

        # תאריך סיום
        self.end_entry = QDateEdit()
        self.end_entry.setCalendarPopup(True)
        self.end_entry.setDate(QDate.currentDate().addDays(1))
        self.end_entry.setDisplayFormat("yyyy-MM-dd")
        self.end_entry.setMinimumDate(self.start_entry.date())
        self.start_entry.dateChanged.connect(lambda d: self.end_entry.setMinimumDate(d))
        search_layout.addWidget(QLabel("End Date:"))
        search_layout.addWidget(self.end_entry)

        # בחירת אמצעי תחבורה
        # QComboBox
        self.transport_combo = QComboBox()
        self.transport_combo.addItems(["Car", "Walking", "Cycling"])
        search_layout.addWidget(self.transport_combo)

        # כפתור טעינת אתרים
        self.create_btn = QPushButton("Load Sites")
        self.create_btn.clicked.connect(self.on_create_trip)
        search_layout.addWidget(self.create_btn)

        # רשימת אתרים לחיפוש
        # QListWidget
        self.sites_list = QListWidget()
        self.sites_list.itemClicked.connect(self.on_site_clicked)
        search_layout.addWidget(self.sites_list)

        self.tabs.addTab(search_tab, "Search")

        # ===== לשונית מזג אוויר =====
        weather_tab = QWidget()
        weather_layout = QVBoxLayout(weather_tab)
        self.weather_label = QLabel("Weather forecast will appear here")
        self.weather_label.setWordWrap(True)
        weather_layout.addWidget(self.weather_label)
        self.tabs.addTab(weather_tab, "Weather")

        # ===== לשונית האטרקציות שלי =====
        my_sites_tab = QWidget()
        my_sites_layout = QVBoxLayout(my_sites_tab)

        self.my_sites_list = QListWidget()
        my_sites_layout.addWidget(self.my_sites_list)

        self.save_btn = QPushButton("Save Trip")
        self.save_btn.clicked.connect(self.on_save_trip)
        my_sites_layout.addWidget(self.save_btn)

        self.tabs.addTab(my_sites_tab, "My Attractions List")

        self.setLayout(main_layout)

        # UX: Enter מפעיל טעינה
        self.address_entry.returnPressed.connect(self.create_btn.click)
        self.city_entry.returnPressed.connect(self.create_btn.click)

    # ---------- View ↔ Presenter ----------

    def on_create_trip(self):
        """
        פונקציה שמופעלת בלחיצה על כפתור טעינת אתרים.
        שולחת נתונים ל־
        Presenter
        """
        city = self.city_entry.text().strip()
        if not city:
            self.show_error("Please enter a city/destination.")
            return

        address = self.address_entry.text().strip() or city

        if self.end_entry.date() < self.start_entry.date():
            self.show_error("End date must be after start date.")
            return

        # מיפוי מצב תחבורה לפרופיל של השרת
        mode = self.transport_combo.currentText()
        profile = {
            "Car": "driving-car",
            "Walking": "foot-walking",
            "Cycling": "cycling-regular",
        }[mode]

        # קריאה לפונקציות של ה־Presenter
        self.create_btn.setEnabled(False)
        try:
            self.presenter.load_sites(city, address, profile)
            self.presenter.update_weather(city)
        finally:
            self.create_btn.setEnabled(True)

    def show_sites(self, sites: list[dict]):
        """
        מציג את רשימת האתרים שהתקבלו מהשרת.
        """
        self.sites_list.clear()
        for site in sites:
            place = site.get("place", {})
            name = place.get("name", "Unnamed")
            category = place.get("category", "Unknown")

            # סיכום קצר של מסלול אם קיים
            route = site.get("route") or {}
            summary_txt = ""
            routes = route.get("routes") or []
            if routes:
                segs = routes[0].get("segments") or []
                if segs:
                    dist = segs[0].get("distance", 0)
                    dur = segs[0].get("duration", 0)
                    summary_txt = f" — {dist:.0f} m, {dur/60:.0f} min"

            self.sites_list.addItem(QListWidgetItem(f"{name} ({category}){summary_txt}"))

    def on_site_clicked(self, item):
        """
        טיפול בלחיצה על אתר מהרשימה.
        """
        index = self.sites_list.row(item)
        self.presenter.show_site_details(index)

    def add_site_to_my_list(self, site_name: str):
        """
        מוסיף אתר לרשימת האטרקציות שלי אם עוד לא קיים שם.
        """
        existing = [self.my_sites_list.item(i).text() for i in range(self.my_sites_list.count())]
        if site_name and site_name not in existing:
            self.my_sites_list.addItem(site_name)

    def on_save_trip(self):
        """
        שומר את פרטי הטיול מול השרת.
        """
        if not self.username:
            self.show_error("No logged-in user detected. Please log in first.")
            return

        selected_sites = [self.my_sites_list.item(i).text() for i in range(self.my_sites_list.count())]
        if not selected_sites:
            self.show_error("Please add at least one site to your list.")
            return

        # המרה של מצב תחבורה לערך שמתאים לשרת
        mode = self.transport_combo.currentText()
        transport = {
            "Car": ["car"],
            "Walking": ["foot"],
            "Cycling": ["bike"],
        }[mode]

        self.presenter.save_trip(
            username=self.username,
            start=self.start_entry.date().toString("yyyy-MM-dd"),
            end=self.end_entry.date().toString("yyyy-MM-dd"),
            city=self.city_entry.text().strip(),
            transport=transport,
            selected_sites=selected_sites,
        )

    def show_weather(self, forecast_data: dict | None):
        """
        מציג תחזית מזג אוויר בלשונית המתאימה.
        """
        if not forecast_data:
            self.weather_label.setText("No weather data received.")
            return
        if "error" in forecast_data:
            self.weather_label.setText(forecast_data['error'])
            return

        lines = []
        dest = forecast_data.get("destination") or self.city_entry.text().strip()
        lines.append(f"Weather for: {dest}")
        for day in forecast_data.get("forecast", []):
            lines.append(f"{day.get('date','')}: {day.get('temp_min','?')}°C - {day.get('temp_max','?')}°C")
        self.weather_label.setText("\n".join(lines) if lines else "No forecast available")

    def show_message(self, msg: str):
        QMessageBox.information(self, "Info", msg)

    def show_error(self, msg: str):
        QMessageBox.critical(self, "Error", msg)

    # יחובר מ־main.py
    def set_ai_callback(self, cb):
        self._ai_callback = cb
