# from PySide6.QtWidgets import (
#     QWidget, QLabel, QLineEdit, QCheckBox, QPushButton,
#     QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
#     QMessageBox, QDateEdit, QTabWidget, QDialog
# )
# from PySide6.QtCore import QDate
# from presenters.newtrip_presenter import NewTripPresenter


# class NewTripView(QWidget):
#     def __init__(self, username=None):
#         super().__init__()
#         self.username = username
#         self.presenter = NewTripPresenter(self)

#         self.setWindowTitle("יצירת טיול חדש")
#         self.setGeometry(200, 200, 600, 500)

#         main_layout = QVBoxLayout()
#         self.tabs = QTabWidget()
#         main_layout.addWidget(self.tabs)

#         # ===== Tab חיפוש =====
#         search_tab = QWidget()
#         search_layout = QVBoxLayout()
#         search_tab.setLayout(search_layout)

#         search_layout.addWidget(QLabel("בחר עיר/אזור:"))
#         self.city_entry = QLineEdit()
#         search_layout.addWidget(self.city_entry)

#         search_layout.addWidget(QLabel("תאריך התחלה:"))
#         self.start_entry = QDateEdit()
#         self.start_entry.setCalendarPopup(True)
#         self.start_entry.setDate(QDate.currentDate())
#         search_layout.addWidget(self.start_entry)

#         search_layout.addWidget(QLabel("תאריך סיום:"))
#         self.end_entry = QDateEdit()
#         self.end_entry.setCalendarPopup(True)
#         self.end_entry.setDate(QDate.currentDate().addDays(1))
#         search_layout.addWidget(self.end_entry)

#         self.has_car = QCheckBox("יש לי רכב")
#         search_layout.addWidget(self.has_car)

#         self.create_btn = QPushButton("טען אתרים")
#         self.create_btn.clicked.connect(self.on_create_trip)
#         search_layout.addWidget(self.create_btn)

#         self.sites_list = QListWidget()
#         search_layout.addWidget(self.sites_list)

#         self.tabs.addTab(search_tab, "חיפוש")

#         # ===== Tab מזג אוויר =====
#         weather_tab = QWidget()
#         weather_layout = QVBoxLayout()
#         weather_tab.setLayout(weather_layout)
#         self.weather_label = QLabel("תחזית מזג אוויר תופיע כאן")
#         weather_layout.addWidget(self.weather_label)
#         self.tabs.addTab(weather_tab, "מזג אוויר")

#         # ===== Tab אטרקציות שנבחרו =====
#         my_sites_tab = QWidget()
#         my_sites_layout = QVBoxLayout()
#         my_sites_tab.setLayout(my_sites_layout)

#         self.my_sites_list = QListWidget()
#         my_sites_layout.addWidget(self.my_sites_list)
#         self.save_btn = QPushButton("שמור טיול")
#         self.save_btn.clicked.connect(self.on_save_trip)
#         my_sites_layout.addWidget(self.save_btn)

#         self.tabs.addTab(my_sites_tab, "רשימת אטרקציות שלי")

#         self.setLayout(main_layout)

#     # ===== View ↔ Presenter =====
#     def on_create_trip(self):
#         city = self.city_entry.text()
#         start = self.start_entry.date().toString("yyyy-MM-dd")
#         end = self.end_entry.date().toString("yyyy-MM-dd")
#         profile = "driving-car" if self.has_car.isChecked() else "foot-walking"
#         self.presenter.load_sites(city, "Default Address", profile)

#     def show_sites(self, sites):
#         self.sites_list.clear()
#         for index, site in enumerate(sites):
#             place = site.get("place", {})
#             name = place.get("name", "ללא שם")
#             category = place.get("category", "לא ידוע")
#             item_text = f"{name} ({category})"
#             item = QListWidgetItem(item_text)
#             self.sites_list.addItem(item)

#         self.sites_list.itemClicked.connect(self.on_site_clicked)

#     def on_site_clicked(self, item):
#         index = self.sites_list.row(item)
#         self.presenter.show_site_details(index)

#     def add_site_to_my_list(self, site_name):
#         # מוסיף רק אם לא קיים
#         existing = [self.my_sites_list.item(i).text() for i in range(self.my_sites_list.count())]
#         if site_name not in existing:
#             self.my_sites_list.addItem(site_name)

#     def on_save_trip(self):
#         selected_sites = [self.my_sites_list.item(i).text() for i in range(self.my_sites_list.count())]
#         if not selected_sites:
#             self.show_error("אנא הוסף לפחות אתר אחד לרשימה.")
#             return

#         self.presenter.save_trip(
#             username=self.username,
#             start=self.start_entry.date().toString("yyyy-MM-dd"),
#             end=self.end_entry.date().toString("yyyy-MM-dd"),
#             city=self.city_entry.text(),
#             has_car=self.has_car.isChecked(),
#             selected_sites=selected_sites
#         )

#     def show_message(self, msg):
#         QMessageBox.information(self, "מידע", msg)

#     def show_error(self, msg):
#         QMessageBox.critical(self, "שגיאה", msg)

from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QCheckBox, QPushButton,
    QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QMessageBox, QDateEdit, QTabWidget, QDialog
)
from PySide6.QtCore import QDate
from client.presenters.newtrip_presenter import NewTripPresenter


class NewTripView(QWidget):
    def __init__(self, username=None):
        super().__init__()
        self.username = username
        self.presenter = NewTripPresenter(self)

        self.setWindowTitle("יצירת טיול חדש")
        self.setGeometry(200, 200, 600, 500)

        main_layout = QVBoxLayout()
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # ===== Tab חיפוש =====
        search_tab = QWidget()
        search_layout = QVBoxLayout()
        search_tab.setLayout(search_layout)

        search_layout.addWidget(QLabel("בחר עיר/אזור:"))
        self.city_entry = QLineEdit()
        search_layout.addWidget(self.city_entry)

        search_layout.addWidget(QLabel("תאריך התחלה:"))
        self.start_entry = QDateEdit()
        self.start_entry.setCalendarPopup(True)
        self.start_entry.setDate(QDate.currentDate())
        search_layout.addWidget(self.start_entry)

        search_layout.addWidget(QLabel("תאריך סיום:"))
        self.end_entry = QDateEdit()
        self.end_entry.setCalendarPopup(True)
        self.end_entry.setDate(QDate.currentDate().addDays(1))
        search_layout.addWidget(self.end_entry)

        self.has_car = QCheckBox("יש לי רכב")
        search_layout.addWidget(self.has_car)

        self.create_btn = QPushButton("טען אתרים")
        self.create_btn.clicked.connect(self.on_create_trip)
        search_layout.addWidget(self.create_btn)

        self.sites_list = QListWidget()
        search_layout.addWidget(self.sites_list)

        self.tabs.addTab(search_tab, "חיפוש")

        # ===== Tab מזג אוויר =====
        weather_tab = QWidget()
        weather_layout = QVBoxLayout()
        weather_tab.setLayout(weather_layout)
        self.weather_label = QLabel("תחזית מזג אוויר תופיע כאן")
        weather_layout.addWidget(self.weather_label)
        self.tabs.addTab(weather_tab, "מזג אוויר")

        # ===== Tab אטרקציות שנבחרו =====
        my_sites_tab = QWidget()
        my_sites_layout = QVBoxLayout()
        my_sites_tab.setLayout(my_sites_layout)

        self.my_sites_list = QListWidget()
        my_sites_layout.addWidget(self.my_sites_list)
        self.save_btn = QPushButton("שמור טיול")
        self.save_btn.clicked.connect(self.on_save_trip)
        my_sites_layout.addWidget(self.save_btn)

        self.tabs.addTab(my_sites_tab, "רשימת אטרקציות שלי")

        self.setLayout(main_layout)

    # ===== View ↔ Presenter =====
    def on_create_trip(self):
        city = self.city_entry.text()
        start = self.start_entry.date().toString("yyyy-MM-dd")
        end = self.end_entry.date().toString("yyyy-MM-dd")
        profile = "driving-car" if self.has_car.isChecked() else "foot-walking"
        self.presenter.load_sites(city, "Default Address", profile)
        self.presenter.update_weather(city)  # <-- עדכון טאב מזג אוויר

    def show_sites(self, sites):
        self.sites_list.clear()
        for index, site in enumerate(sites):
            place = site.get("place", {})
            name = place.get("name", "ללא שם")
            category = place.get("category", "לא ידוע")
            item_text = f"{name} ({category})"
            item = QListWidgetItem(item_text)
            self.sites_list.addItem(item)

        self.sites_list.itemClicked.connect(self.on_site_clicked)

    def on_site_clicked(self, item):
        index = self.sites_list.row(item)
        self.presenter.show_site_details(index)

    def add_site_to_my_list(self, site_name):
        existing = [self.my_sites_list.item(i).text() for i in range(self.my_sites_list.count())]
        if site_name not in existing:
            self.my_sites_list.addItem(site_name)

    def on_save_trip(self):
        selected_sites = [self.my_sites_list.item(i).text() for i in range(self.my_sites_list.count())]
        if not selected_sites:
            self.show_error("אנא הוסף לפחות אתר אחד לרשימה.")
            return

        self.presenter.save_trip(
            username=self.username,
            start=self.start_entry.date().toString("yyyy-MM-dd"),
            end=self.end_entry.date().toString("yyyy-MM-dd"),
            city=self.city_entry.text(),
            has_car=self.has_car.isChecked(),
            selected_sites=selected_sites
        )

    def show_weather(self, forecast_data):
        if "error" in forecast_data:
            self.weather_label.setText(forecast_data["error"])
            return
        text = f"מזג אוויר ליעד: {forecast_data['destination']}\n"
        for day in forecast_data["forecast"]:
            text += f"{day['date']}: {day['temp_min']}°C - {day['temp_max']}°C\n"
        self.weather_label.setText(text)

    def show_message(self, msg):
        QMessageBox.information(self, "מידע", msg)

    def show_error(self, msg):
        QMessageBox.critical(self, "שגיאה", msg)
