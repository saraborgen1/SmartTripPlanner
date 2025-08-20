# client/presenters/dashboard_presenter.py

class DashboardPresenter:
    """
    Presenter למסך הדשבורד – מחבר את הכפתורים לקולבקים שה-App מספק.
    מצפה ל-4 קולבקים:
      on_current_trip, on_past_trips, on_new_trip, on_ai_chat
    """
    def __init__(
        self,
        view,
        session_manager,
        on_current_trip,
        on_past_trips,
        on_new_trip,
        on_ai_chat,
    ):
        self.view = view
        self.session = session_manager

        # חיבור הכפתורים לקולבקים
        self.view.current_trip_btn.clicked.connect(on_current_trip)
        self.view.past_trips_btn.clicked.connect(on_past_trips)
        self.view.new_trip_btn.clicked.connect(on_new_trip)
        self.view.ai_btn.clicked.connect(on_ai_chat)
