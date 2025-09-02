# client/views/ai_consult_view.py

# הקובץ הזה מגדיר מחלקת 
# View
# שמציגה חלון צ'אט
# לתקשורת עם הסוכן החכם –
# AI Assistant.

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTextEdit, QLineEdit, QPushButton
)
from PySide6.QtCore import Qt

"""
  מחלקת
  View
  שמציגה חלון צ'אט לתקשורת עם הסוכן החכם.
  כוללת:
    - אזור היסטוריית שיחה (קריאה בלבד) 
    - שורת קלט לשאלה 
    - כפתור שליחה 
    - כפתור חזרה למסך קודם 
  """
class AIChatView(QWidget):

    def __init__(self, back_callback):
        super().__init__()
        self.setWindowTitle("Smart Trip Planner - AI Assistant")
        self.setMinimumSize(560, 420)

        # יצירת פריסה אנכית ראשית –
        root = QVBoxLayout()

        # כותרת עליונה –
        title = QLabel("AI Assistant")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        root.addWidget(title)

        # אזור היסטוריית השיחה
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

        # חיבור ה־
        # Layout
        # הראשי למסך
        self.setLayout(root)


    """
      הוספת שורת משתמש להיסטוריית הצ'אט.
    """
    def append_user(self, text: str):
      
      self.history.append(f"<b>You:</b> {text}")


    """
      הוספת תשובת הסוכן להיסטוריית הצ'אט.
    """
    def append_assistant(self, text: str):
       
      self.history.append(f"<b>AI:</b> {text}")


    """
     ניקוי שורת הקלט  
    """
    def clear_input(self):
       
      self.input.clear()


    """
      הפעלת/ביטול קלט בזמן שליחת בקשה לשרת.
      האם לאפשר אינטראקציה 
      (True) 
      או לנעול 
      (False).
    """
    def set_enabled(self, enabled: bool):
      
      self.input.setEnabled(enabled)
      self.send_btn.setEnabled(enabled)

