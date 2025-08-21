# client/presenters/trip_detail_presenter.py

class TripDetailPresenter:
    """
    מחלקת
    Presenter
    עבור חלון פרטי טיול.

    התפקיד:
    - אחראית על חיבור אירועי ממשק מה־
      View
    - במקרה הזה: לחיצה על כפתור "Close"
      תסגור את החלון
    """

    def __init__(self, view):
        # שמירה על הפניה ל־
        # View
        self.view = view

        # חיבור כפתור ה־
        # close_button
        # לאירוע סגירת חלון ה־
        # View
        self.view.close_button.clicked.connect(self.view.close)
