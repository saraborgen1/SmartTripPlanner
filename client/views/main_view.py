from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

class MainView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Trip Planner")
        self.setMinimumSize(400, 300)

        layout = QVBoxLayout()

        self.label = QLabel("Welcome to SmartTripPlanner!")
        layout.addWidget(self.label)

        self.login_button = QPushButton("Login")
        self.register_button = QPushButton("Register")
        self.search_button = QPushButton("Search Trips")

        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)
        layout.addWidget(self.search_button)

        self.setLayout(layout)
