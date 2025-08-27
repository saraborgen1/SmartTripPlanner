from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
from PySide6.QtCore import Qt

class CurrentTripView(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # כותרת ראשית
        self.title = QLabel("Current Trip")
        self.title.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50;")
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)
        
        # תיבת טקסט להצגת פרטי הטיול
        self.trip_details = QTextEdit()
        self.trip_details.setReadOnly(True)
        self.trip_details.setAlignment(Qt.AlignLeft)
        self.trip_details.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                color: #2c3e50;
                border: 1px solid #dcdde1;
                border-radius: 8px;
                font-size: 15px;
                padding: 12px;
            }
        """)
        layout.addWidget(self.trip_details)
        
        # כפתור עריכת טיול (אופציונלי)
        self.btn_edit_trip = QPushButton("Edit Trip")
        self.btn_edit_trip.setStyleSheet("""
            QPushButton {
                background-color: #3498db; 
                color: white; 
                padding: 10px 20px; 
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        layout.addWidget(self.btn_edit_trip)
        
        self.setLayout(layout)

    def update_trip(self, trip_data: dict | None):
        """עדכון התצוגה עם נתוני הטיול הנוכחי"""
        if not trip_data:
            self.title.setText("No Current Trip")
            self.trip_details.setText("It looks like you don't have any upcoming trips.")
            return

        dest = trip_data.get("destination", "Unknown")
        start = trip_data.get("start_date", "?")
        end = trip_data.get("end_date", "?")
        sites = trip_data.get("selected_sites", [])
        transport = ", ".join(trip_data.get("transport", [])) if trip_data.get("transport") else "N/A"

        sites_text = "\n".join(f"• {s}" for s in sites) if sites else "No attractions selected"

        self.title.setText(f"Current Trip: {dest}")
        self.trip_details.setText(
            f"Destination: {dest}\n"
            f"Dates: {start} → {end}\n"
            f"Transport: {transport}\n"
            f"Selected Sites:\n{sites_text}"
        )
