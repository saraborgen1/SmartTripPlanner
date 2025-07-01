# client/main.py
import sys
import requests
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

response = requests.get("http://127.0.0.1:8000")
label.setText(response.json()["msg"])

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Smart Trip Planner")

layout = QVBoxLayout()
label = QLabel("ברוכים הבאים למערכת תכנון טיול חכם!")
layout.addWidget(label)

window.setLayout(layout)
window.show()

sys.exit(app.exec())
