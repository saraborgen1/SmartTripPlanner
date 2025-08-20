class MainPresenter:
    def __init__(self, view, session_manager, go_to_auth):
        self.view = view
        self.session = session_manager
        self._go_to_auth = go_to_auth  # פונקציה שמחליפה למסך ההתחברות/הרשמה

        # יש כפתור יחיד במסך הבית: auth_button
        self.view.auth_button.clicked.connect(self._go_to_auth)
