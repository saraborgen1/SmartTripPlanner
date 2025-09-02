# client/views/search_view.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QLabel

#אחראי על מסך החיפוש
class SearchView(QWidget):
 
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Trips")
        self.setMinimumSize(400, 300)

        # פריסת מסך אנכית
        layout = QVBoxLayout()

        # תווית הסבר למשתמש
        self.label = QLabel("Enter a city to search trips:")
        layout.addWidget(self.label)

        # שדה קלט שבו המשתמש מזין את שם העיר
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("City name...")
        layout.addWidget(self.search_input)

        # כפתור חיפוש — בלחיצה עליו יבוצע החיפוש
        self.search_button = QPushButton("Search")
        layout.addWidget(self.search_button)

        # רשימת תוצאות שבה יוצגו כל הטיולים שנמצאו
        self.results_list = QListWidget()
        layout.addWidget(self.results_list)

        self.setLayout(layout)
