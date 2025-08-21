# client/views/ai_consult_view.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTextEdit, QLineEdit, QPushButton
)
from PySide6.QtCore import Qt


class AIChatView(QWidget):
    """
    מחלקת View שמציגה חלון צ'אט לתקשורת עם הסוכן החכם.

    כולל:
    - אזור היסטוריית שיחה (קריאה בלבד) — 
      QTextEdit
    - שורת קלט לשאלה — 
      QLineEdit
    - כפתור שליחה — 
      QPushButton
    - כפתור חזרה למסך קודם — 
      QPushButton
    """

    def __init__(self, back_callback):
        super().__init__()
        self.setWindowTitle("Smart Trip Planner - AI Assistant")
        self.setMinimumSize(560, 420)

        # Layout ראשי אנכי
        root = QVBoxLayout()

        # כותרת (Label גדול במרכז)
        # QLabel
        title = QLabel("AI Assistant")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        root.addWidget(title)

        # אזור היסטוריית השיחה
        # QTextEdit (קריאה בלבד)
        self.history = QTextEdit()
        self.history.setReadOnly(True)
        root.addWidget(self.history)

        # שורת קלט + כפתור שליחה
        # QHBoxLayout
        input_row = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("Ask me anything...")
        self.send_btn = QPushButton("Send")
        input_row.addWidget(self.input)
        input_row.addWidget(self.send_btn)
        root.addLayout(input_row)

        # כפתור חזרה
        # QPushButton
        self.back_btn = QPushButton("Back")
        self.back_btn.clicked.connect(back_callback)
        root.addWidget(self.back_btn)

        # חיבור Layout ראשי למסך
        self.setLayout(root)

    def append_user(self, text: str):
        """
        הוספת שורת משתמש להיסטוריית הצ'אט.

        text –
        str
        טקסט ההודעה של המשתמש.
        """
        self.history.append(f"<b>You:</b> {text}")

    def append_assistant(self, text: str):
        """
        הוספת תשובת הסוכן להיסטוריית הצ'אט.

        text –
        str
        תשובת ה־AI.
        """
        # ברירת מחדל: טקסט פשוט (אפשר להחליף ל־HTML מעוצב)
        self.history.append(f"<b>AI:</b> {text}")

    def clear_input(self):
        """
        ניקוי שורת הקלט (ה־
        QLineEdit
        ).
        """
        self.input.clear()

    def set_enabled(self, enabled: bool):
        """
        הפעלת/ביטול קלט בזמן שליחת בקשה לשרת.

        enabled –
        bool
        האם לאפשר אינטראקציה (True) או לנעול (False).
        """
        self.input.setEnabled(enabled)
        self.send_btn.setEnabled(enabled)
