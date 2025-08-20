from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTextEdit, QLineEdit, QPushButton
)
from PySide6.QtCore import Qt

class AIChatView(QWidget):
    """
    חלון צ'אט לתקשורת עם הסוכן:
    - אזור היסטוריית שיחה (קריאה בלבד)
    - שורת קלט לשאלה
    - כפתור שליחה
    - כפתור חזרה
    """
    def __init__(self, back_callback):
        super().__init__()
        self.setWindowTitle("Smart Trip Planner - AI Assistant")
        self.setMinimumSize(560, 420)

        root = QVBoxLayout()

        # כותרת
        title = QLabel("AI Assistant")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        root.addWidget(title)

        # אזור היסטוריית השיחה (רק לקריאה)
        self.history = QTextEdit()
        self.history.setReadOnly(True)
        root.addWidget(self.history)

        # שורת קלט + כפתור שליחה
        input_row = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("Ask me anything...")
        self.send_btn = QPushButton("Send")
        input_row.addWidget(self.input)
        input_row.addWidget(self.send_btn)
        root.addLayout(input_row)

        # כפתור חזרה
        self.back_btn = QPushButton("Back")
        self.back_btn.clicked.connect(back_callback)
        root.addWidget(self.back_btn)

        self.setLayout(root)

    def append_user(self, text: str):
        """מוסיף שורת משתמש להיסטוריה."""
        self.history.append(f"<b>You:</b> {text}")

    def append_assistant(self, text: str):
        """מוסיף תשובת הסוכן להיסטוריה."""
        # ברירת מחדל: טקסט פשוט (אפשר להחליף ל-HTML מעוצב בהמשך)
        self.history.append(f"<b>AI:</b> {text}")

    def clear_input(self):
        self.input.clear()

    def set_enabled(self, enabled: bool):
        """נעילת קלט וכפתור בזמן שליחת בקשה."""
        self.input.setEnabled(enabled)
        self.send_btn.setEnabled(enabled)
