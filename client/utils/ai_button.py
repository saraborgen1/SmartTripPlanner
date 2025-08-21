# client/utils/ai_button.py
from PySide6.QtWidgets import QPushButton, QHBoxLayout, QWidget


def add_ai_button(container_layout, on_ai_click) -> QPushButton:
    """
    פונקציה שמוסיפה כפתור עזר לפתיחת שיחה עם סוכן 
    AI Assistant
    
    container_layout –
    ה־
    Layout
    הראשי של המסך או החלון שבו רוצים להוסיף את הכפתור.

    on_ai_click –
    פונקציה שתיקרא כאשר לוחצים על הכפתור 
    (בדרך כלל 
    App.show_ai_chat
    ).
    """

    # יוצרים שורת כפתורים אופקית 
    # HBoxLayout
    strip = QHBoxLayout()
    
    # מוסיפים ריווח מתוח (stretch) בצד שמאל
    # כך שהכפתור יידחף לצד ימין
    strip.addStretch(1)

    # יוצרים את הכפתור עצמו
    # QPushButton
    btn = QPushButton("AI Assistant")

    # מחברים את הכפתור לפונקציה שתופעל בלחיצה
    if on_ai_click:
        btn.clicked.connect(on_ai_click)

    # מוסיפים את הכפתור ל־
    # strip
    strip.addWidget(btn)

    # עוטפים את ה־
    # layout
    # בתוך 
    # QWidget
    # כדי לשמור על מבנה נכון של הריווחים
    w = QWidget()
    w.setLayout(strip)

    # מוסיפים את ה־
    # QWidget
    # ל־
    # container_layout
    container_layout.addWidget(w)

    return btn
