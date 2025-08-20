from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt

class MainView(QWidget):
    def __init__(self, go_to_auth_callback):
        super().__init__()
        self.setWindowTitle("Smart Trip Planner")
        self.setMinimumSize(400, 300)

        layout = QVBoxLayout()

        self.label = QLabel("Welcome")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # כפתור יחיד → למסך ההתחברות/הרשמה
        self.auth_button = QPushButton("Login / Register")
        layout.addWidget(self.auth_button)

        self._go_to_auth = go_to_auth_callback
        self.auth_button.clicked.connect(self._go_to_auth)

        self.setLayout(layout)
