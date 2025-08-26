from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

class CurrentTripView(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # כותרת
        title = QLabel("Current Trip")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # תוכן
        content = QLabel("Here you can see details about your current trip.\nStart planning your next adventure!")
        content.setAlignment(Qt.AlignCenter)
        content.setStyleSheet("font-size: 16px; color: #7f8c8d;")
        layout.addWidget(content)
        
        # דוגמה לכפתור לפעולה עתידית
        self.btn_edit_trip = QPushButton("Edit Trip")
        layout.addWidget(self.btn_edit_trip)
        # self.btn_edit_trip.setStyleSheet("""
        #     QPushButton {
        #         background-color: #3498db; 
        #         color: white; 
        #         padding: 10px 20px; 
        #         border-radius: 5px;
        #         font-size: 16px;
        #     }
        #     QPushButton:hover {
        #         background-color: #2980b9;
        #     }
        # """)