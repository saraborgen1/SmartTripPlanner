
# client/presenters/main_presenter.py
class MainPresenter:
    """
    Presenter עבור MainView עם וידאו רקע.
    """
    def __init__(self, view, session_manager, go_to_auth):
        self.view = view
        self.session = session_manager
        self._go_to_auth = go_to_auth

        # חיבור הכפתור LOGIN לפונקציה חיצונית
        self.view.auth_button.clicked.connect(self._go_to_auth)

