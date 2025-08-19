import requests
from PySide6.QtCore import QTimer

class RegisterPresenter:
    def __init__(self, view):
        self.view = view

    def register_user(self, username, password):
        if not username or not password:
            self.view.show_error("Both fields are required.")
            return

        try:
            response = requests.post(
                "http://127.0.0.1:8000/register",
                json={"username": username, "password": password},
                timeout=10
            )

            print("Status code:", response.status_code)
            print("Response text:", response.text)

            if response.status_code == 200:
                self.view.show_message("Success", "User registered successfully.")
                # מעבר חזרה למסך התחברות אחרי 1.5 שניות
                QTimer.singleShot(1500, self.view.go_to_login_callback)
            else:
                # ניסיון לקרוא JSON ואם נכשל מדפיס טקסט
                try:
                    error_msg = response.json().get("detail", "Registration failed.")
                except ValueError:
                    error_msg = f"Registration failed: {response.text}"
                self.view.show_error(error_msg)

        except requests.RequestException as e:
            self.view.show_error(f"Server error: {e}")
