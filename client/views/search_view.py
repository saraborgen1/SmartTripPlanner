from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QLabel

class SearchView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Trips")
        self.setMinimumSize(400, 300)

        layout = QVBoxLayout()

        self.label = QLabel("Enter a city to search trips:")
        layout.addWidget(self.label)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("City name...")
        layout.addWidget(self.search_input)

        self.search_button = QPushButton("Search")
        layout.addWidget(self.search_button)

        self.results_list = QListWidget()
        layout.addWidget(self.results_list)

        self.setLayout(layout)
