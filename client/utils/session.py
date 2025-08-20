# client/session/session_manager.py
class SessionManager:
    def __init__(self):
        self.user_token = None
        self.username = None  # אופציונלי – לשימוש ב־UI

    def is_logged_in(self):
        return self.user_token is not None

    def login(self, token, username=None):
        self.user_token = token
        self.username = username

    def logout(self):
        self.user_token = None
        self.username = None
