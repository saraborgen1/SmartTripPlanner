class SessionManager:
    def __init__(self):
        self.user_token = None

    def is_logged_in(self):
        return self.user_token is not None

    def login(self, token):
        self.user_token = token

    def logout(self):
        self.user_token = None
