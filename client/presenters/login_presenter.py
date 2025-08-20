from client.services import api_client
import requests

class LoginPresenter:
    def __init__(self, view, session_manager):
        self.view = view
        self.session = session_manager

    def login(self, username: str, password: str):
        try:
            data = api_client.login(username, password)
            token = data.get("access_token")
            if not token:
                self.view.show_error("Login failed: Token not received.")
                return
            # שומרים סשן וממשיכים למסך הראשי
            if self.session:
                self.session.login(token, username)
            self.view.show_success(token)
        except requests.HTTPError as e:
            resp = e.response
            try:
                detail = resp.json().get("detail", resp.text)
            except Exception:
                detail = resp.text or str(e)
            self.view.show_error(detail or "Login failed.")
        except requests.RequestException as e:
            self.view.show_error(f"Server error: {e}")

    def register(self, username: str, password: str):
        if not username or not password:
            self.view.show_error("Both fields are required.")
            return
        try:
            data = api_client.register(username, password)
            # אחרי הרשמה מוצלחת—ננסה להתחבר אוטומטית
            self.login(username, password)
        except requests.HTTPError as e:
            resp = e.response
            try:
                detail = resp.json().get("detail", resp.text)
            except Exception:
                detail = resp.text or str(e)
            self.view.show_error(detail or "Registration failed.")
        except requests.RequestException as e:
            self.view.show_error(f"Server error: {e}")
