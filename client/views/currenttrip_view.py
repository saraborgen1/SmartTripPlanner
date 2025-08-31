#client/views/currenttrip_view.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QFrame
from PySide6.QtCore import Qt

class CurrentTripView(QWidget):
    def __init__(self, edit_trip_callback=None):
        super().__init__()
        
        self.current_trip = None
        self.edit_trip_callback = edit_trip_callback
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # כותרת ראשית
        self.title = QLabel("Current Trip")
        self.title.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50;")
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        # -------- יצירת כרטיס (Card) שיכיל גם את הטקסט וגם את הכפתור --------
        trip_card = QFrame()
        trip_card.setStyleSheet("""
            QFrame {
                border: 1px solid #dcdde1;
                border-radius: 8px;
                background-color: #f8f9fa;
            }
        """)
        card_layout = QVBoxLayout(trip_card)
        card_layout.setContentsMargins(12, 12, 12, 12)
        card_layout.setSpacing(10)

        # תיבת טקסט להצגת פרטי הטיול
        self.trip_details = QTextEdit()
        self.trip_details.setReadOnly(True)
        self.trip_details.setAlignment(Qt.AlignLeft)
        self.trip_details.setStyleSheet("""
            QTextEdit {
                background-color: white;
                color: #2c3e50;
                border: none;
                font-size: 15px;
                padding: 8px;
            }
        """)
        self.trip_details.setMaximumHeight(120)
        card_layout.addWidget(self.trip_details)

        # כפתור עריכת טיול
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
        self.btn_edit_trip.clicked.connect(self.on_edit_trip_clicked)
        card_layout.addWidget(self.btn_edit_trip)

        # הוספת ה־Card ל־layout הראשי
        layout.addWidget(trip_card)

        self.setLayout(layout)

    def update_trip(self, trip_data: dict | None):
        self.current_trip = trip_data
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

    def on_edit_trip_clicked(self):
        if self.current_trip and self.edit_trip_callback:
            self.edit_trip_callback(self.current_trip)
    
