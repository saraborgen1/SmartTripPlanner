# client/presenters/register_presenter.py

from PySide6.QtCore import QTimer
import requests
from client.services import api_client  # שכבת השירות שמדברת עם ה־
                                        # Server
                                        # דרך ה־
                                        # API Client


class RegisterPresenter:
    """
    מחלקת
    Presenter
    שאחראית על זרימת ההרשמה.

    מחברת בין ה־
    View
    (טופס הרשמה)
    לבין שכבת השירות
    API Client
    ששולחת את הנתונים ל־
    Server
    ומחזירה תגובה.
    """

    def __init__(self, view):
        # שמירה על הפניה ל־
        # RegisterView
        self.view = view

    def register_user(self, username: str, password: str):
        """
        נקראת כאשר המשתמש לוחץ על כפתור "Register".

        מבצעת:
        - ולידציה בסיסית בצד ה־
          Client
        - קריאה ל־
          API Client
          לביצוע הרשמה ב־
          Server
        - הצגת הודעת הצלחה/שגיאה ב־
          View
        - מעבר חזרה למסך התחברות לאחר
          1.5s
          (באמצעות
          QTimer)
        """

        # בדיקה בסיסית בצד ה־
        # Client
        if not username or not password:
            self.view.show_error("Both fields are required.")
            return

        try:
            # קריאה ל־
            # API Client
            # כדי לבצע הרשמה ב־
            # Server
            data = api_client.register(username, password)

            # הודעת הצלחה:
            # ננסה לשלוף "message" מהתגובה;
            # אם אין — נשתמש בברירת מחדל באנגלית
            message = data.get("message", "User registered successfully.")
            self.view.show_message("Success", message)

            # חזרה למסך ההתחברות אחרי
            # 1500ms
            # באמצעות
            # QTimer.singleShot
            # חשוב: ב־
            # View
            # צריכה להיות פונקציה בשם
            # go_to_login_callback
            QTimer.singleShot(1500, self.view.go_to_login_callback)

        except requests.HTTPError as e:
            # שגיאת
            # HTTP
            # מהשרת (למשל
            # 400 / 409
            # וכו'):
            # ננסה להוציא
            # detail
            # מה־
            # JSON
            resp = e.response
            try:
                detail = resp.json().get("detail", resp.text)
            except Exception:
                detail = resp.text or str(e)

            # מציגים למשתמש הודעת שגיאה באנגלית
            self.view.show_error(detail or "Registration failed.")

        except requests.RequestException as e:
            # שגיאת רשת / timeout וכד'
            # (כל שגיאה שאינה
            # HTTPError
            # ספציפית)
            self.view.show_error(f"Server error: {e}")
