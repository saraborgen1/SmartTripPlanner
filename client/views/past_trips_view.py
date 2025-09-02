# client/views/past_trips_view.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem, QHBoxLayout
from PySide6.QtCore import Qt

# ---------- תצוגת טיולים קודמים ----------
class PastTripsView(QWidget):

    def __init__(self):
        super().__init__()
        # הגדרות חלון
        self.setWindowTitle("Smart Trip Planner - My Trips")
        self.setMinimumSize(560, 420)

        # לייאאוט ראשי אנכי
        root = QVBoxLayout()

        # לייאאוט עליון (כותרת + כפתורים)
        header = QHBoxLayout()

        # כותרת ראשית
        self.title = QLabel("My Trips")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 20px; font-weight: bold;")
        header.addWidget(self.title, 1)

        # כפתור רענון
        self.refresh_btn = QPushButton("Refresh")
        header.addWidget(self.refresh_btn, 0)

        # הוספת שורת הכותרת ללייאאוט הראשי
        root.addLayout(header)

        # רשימת טיולים
        self.trips_list = QListWidget()
        root.addWidget(self.trips_list)

        # חיבור הלייאאוט הראשי למסך
        self.setLayout(root)


    #עדכון הכותרת לשם המשתמש הנוכחי
    def set_username(self, username: str):

        self.title.setText(f"My Trips — {username}")


    # ניקוי כל הפריטים מהרשימה
    def clear_list(self):

        self.trips_list.clear()


    # הוספת פריט חדש לרשימה
    def add_trip_item(self, text: str, trip_obj: dict):

        item = QListWidgetItem(text)
        item.setData(Qt.UserRole, trip_obj)
        self.trips_list.addItem(item)


    # עדכון רשימת הטיולים בתצוגה
    def set_trips(self, trips: list):

        self.clear_list()
        self.trips = []  

        # אם אין טיולים כלל
        if not trips:
            self.trips_list.addItem(QListWidgetItem("No past trips found."))
            return

        # מעבר על כל טיול שהתקבל מהשרת
        for trip in trips:
            trip_data = {
                "start_date": trip.get("start_date"),
                "end_date": trip.get("end_date"),
                "selected_sites": trip.get("selected_sites", []),
                "transport": trip.get("transport", []),
                "weather": trip.get("weather"),
                "notes": trip.get("notes", "")
            }

            self.trips.append(trip_data)

            # טקסט להצגה ברשימה
            display_text = (
                f"Dates: {trip_data['start_date']} → {trip_data['end_date']} | "
                f"Sites: {', '.join(trip_data['selected_sites']) if trip_data['selected_sites'] else 'None'} | "
                f"Transport: {', '.join(trip_data['transport']) if trip_data['transport'] else 'None'} | "
                f"Weather: {trip_data['weather'] if trip_data['weather'] else 'N/A'} | "
                f"Notes: {trip_data['notes'] if trip_data['notes'] else 'None'}"
            )
            item = QListWidgetItem(display_text)
            item.setData(Qt.UserRole, trip_data)   
            self.trips_list.addItem(item)

        # עדכון טבלה במידה ויש כזו
        if hasattr(self, "update_trips_table"):
            self.update_trips_table(self.trips)
