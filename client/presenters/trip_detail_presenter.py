class TripDetailPresenter:
    def __init__(self, view):
        self.view = view
        self.view.close_button.clicked.connect(self.view.close)
