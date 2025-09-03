# client/presenters/register_presenter.py

from PySide6.QtCore import QTimer
import requests
from client.services import api_client  

"""
    Presenter
     עבור תהליך ההרשמה.
    מחבר בין ה־
    View
    (טופס הרשמה)
    לבין שכבת השירות 
    (api_client).
"""
class RegisterPresenter:

    def __init__(self, view):
        # שמירה על הפניה ל־
        self.view = view


    # פונקציה לקריאה כאשר המשתמש לוחץ על כפתור ההרשמה
    def register_user(self, username: str, password: str):
    
        # בדיקה: האם המשתמש מילא את כל השדות
        if not username or not password:
            self.view.show_error("Both fields are required.")
            return

        try:
            # קריאה ל־
            # API Client
            # כדי לבצע הרשמה ב־
            # Server
            data = api_client.register(username, password)

            # אם ההרשמה הצליחה – מציגים הודעת הצלחה
            message = data.get("message", "User registered successfully.")
            self.view.show_message("Success", message)
            # מעבר אוטומטי חזרה למסך ההתחברות אחרי 1.5 שניות
            QTimer.singleShot(1500, self.view.go_to_login_callback)

        except requests.HTTPError as e:
            # שגיאת HTTP ספציפית מהשרת
            resp = e.response
            try:
                detail = resp.json().get("detail", resp.text)
            except Exception:
                detail = resp.text or str(e)

            # מציג הודעת שגיאה למשתמש
            self.view.show_error(detail or "Registration failed.")
        except requests.RequestException as e:
            # שגיאה כללית ברשת  
            self.view.show_error(f"Server error: {e}")
