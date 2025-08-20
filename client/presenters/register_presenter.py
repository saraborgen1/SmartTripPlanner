# client/presenters/register_presenter.py
from PySide6.QtCore import QTimer
import requests
from client.services import api_client  # שכבת השירות שמדברת עם השרת

class RegisterPresenter:
    def __init__(self, view):
        self.view = view  # שמירה על הפניה ל-RegisterView

    def register_user(self, username: str, password: str):
        # בדיקה בסיסית בצד הלקוח
        if not username or not password:
            self.view.show_error("Both fields are required.")
            return

        try:
            # קריאה לשרת דרך שכבת השירות
            data = api_client.register(username, password)

            # הודעת הצלחה (מקבל מהשרת או ברירת מחדל)
            message = data.get("message", "User registered successfully.")
            self.view.show_message("Success", message)

            # חזרה למסך ההתחברות אחרי 1.5 שניות
            QTimer.singleShot(1500, self.view.go_to_login_callback)

        except requests.HTTPError as e:
            # שגיאת HTTP מהשרת (400/409 וכו') – ננסה להוציא detail
            resp = e.response
            try:
                detail = resp.json().get("detail", resp.text)
            except Exception:
                detail = resp.text or str(e)
            self.view.show_error(detail or "Registration failed.")

        except requests.RequestException as e:
            # שגיאת רשת/timeout וכו'
            self.view.show_error(f"Server error: {e}")
