# client/views/search_view.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QLabel


class SearchView(QWidget):
    """
    View שאחראי על מסך החיפוש.

    במסך זה המשתמש יכול:
    - להזין שם עיר
    - ללחוץ על כפתור חיפוש
    - לראות תוצאות חיפוש ברשימה

    כל הרכיבים מוגדרים כאן כ־
    QWidget
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Trips")
        self.setMinimumSize(400, 300)

        # פריסת מסך אנכית
        # QVBoxLayout
        layout = QVBoxLayout()

        # תווית הסבר
        # QLabel
        self.label = QLabel("Enter a city to search trips:")
        layout.addWidget(self.label)

        # שדה קלט לעיר
        # QLineEdit
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("City name...")
        layout.addWidget(self.search_input)

        # כפתור חיפוש
        # QPushButton
        self.search_button = QPushButton("Search")
        layout.addWidget(self.search_button)

        # רשימת תוצאות
        # QListWidget
        self.results_list = QListWidget()
        layout.addWidget(self.results_list)

        # החלת הפריסה על המסך
        self.setLayout(layout)
