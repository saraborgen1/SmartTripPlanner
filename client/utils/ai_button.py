# client/utils/ai_button.py
# client/utils/ai_button.py
# הקובץ הזה מספק פונקציית עזר להוספת כפתור
# AI Assistant
# למסכים שונים בצד ה־
# Client.
# הוא משתמש בספריית
# PySide6
# ובמחלקות:
# QPushButton – כפתור לחיץ,
# QHBoxLayout – פריסת רכיבים אופקית,
# QWidget – מכולה לרכיבים.
from PySide6.QtWidgets import QPushButton, QHBoxLayout, QWidget

# פונקציה שמוסיפה כפתור עזר לפתיחת שיחה עם סוכן
# AI Assistant
def add_ai_button(container_layout, on_ai_click) -> QPushButton:
    """
    container_layout –
    ה־
    Layout
    הראשי של המסך או החלון שבו רוצים להוסיף את הכפתור.

    on_ai_click –
    פונקציה שתופעל כאשר לוחצים על הכפתור
    (למשל:
    App.show_ai_chat).
    """

     # יוצרים פריסת רכיבים אופקית –
    # QHBoxLayout
    strip = QHBoxLayout()
    
    # מוסיפים ריווח מתוח (stretch) בצד שמאל
    # כך שהכפתור יידחף לצד ימין
    strip.addStretch(1)

    # יוצרים את הכפתור עצמו
    # QPushButton
    # עם טקסט "AI Assistant"
    btn = QPushButton("AI Assistant")

    # מחברים את הכפתור לפונקציה שהועברה
    # כך שכאשר לוחצים עליו – הפונקציה תופעל
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

    # מחזירים את הכפתור עצמו החוצה
    # כדי שאפשר יהיה להשתמש בו אם צריך
    return btn
