import requests
from server.models.user import User  # מייבא את מחלקת User שמכילה שם משתמש וסיסמה

class LoginPresenter:
    def __init__(self, view):
        self.view = view  # שומר הפניה למסך (LoginView)

    def login(self, username, password):
        user = User(username=username, password=password)  # יוצר אובייקט מסוג User

        try:
            # שולח בקשת POST לשרת
            response = requests.post("http://127.0.0.1:8000/login", json=user.dict(), timeout=10)
            print("RESPONSE STATUS:", response.status_code)
            print("RESPONSE BODY:", response.text)

            if response.status_code == 200:
                data = response.json()
                token = data.get("access_token")  # קבלת הטוקן מהשרת

                if token:
                    self.view.go_to_main_view(token, username)
                else:
                    self.view.show_error("Login failed: Token not received.")
            else:
                error_message = response.json().get("detail", "Login failed.")
                self.view.show_error(error_message)

        except requests.exceptions.RequestException as e:
            self.view.show_error(f"Server error: {e}")
