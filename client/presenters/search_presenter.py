# from models.trip_model import Trip
# from views.trip_detail_view import TripDetailView
# from presenters.trip_detail_presenter import TripDetailPresenter

# class SearchPresenter:
#     def __init__(self, view):
#         self.view = view
#         self.view.search_button.clicked.connect(self.on_search)
#         self.view.results_list.itemClicked.connect(self.on_item_clicked)
#         self.trips = []
#         self.detail_windows = []  # <-- רשימה לשמירת חלונות פתוחים

#     def on_search(self):
#         city = self.view.search_input.text().strip()
#         if not city:
#             self.view.results_list.clear()
#             self.view.results_list.addItem("Please enter a city name.")
#             return

#         # יצירת אובייקטי Trip מדומים
#         self.trips = [
#             Trip(1, f"{city} Museum Tour", "Visit famous museums", city),
#             Trip(2, f"{city} Nature Hike", "Explore natural parks", city),
#             Trip(3, f"{city} Food Trip", "Taste local cuisine", city),
#         ]

#         self.view.results_list.clear()
#         for trip in self.trips:
#             self.view.results_list.addItem(f"{trip.name} - {trip.location}")

#     def on_item_clicked(self, item):
#         index = self.view.results_list.currentRow()
#         trip = self.trips[index]

#         # יצירת חלון Detail
#         detail_view = TripDetailView(trip)
#         TripDetailPresenter(detail_view)

#         # שמירה ברשימה כדי שלא ייסגר מיד
#         self.detail_windows.append(detail_view)
#         detail_view.show()


from services.api_client import get_trips
from views.search_view import SearchView
from views.trip_detail_view import TripDetailView

class SearchPresenter:
    def __init__(self, view: SearchView):
        self.view = view
        self.view.search_button.clicked.connect(self.search)
        self.detail_view = None  # כדי שהחלון לא ייסגר מיד

    def search(self):
        city = self.view.search_input.text()
        if not city:
            return

        trips = get_trips(city)
        self.trips = trips  # שמירה פנימית כדי לדעת איזה trip נבחר
        self.view.results_list.clear()

        for trip in trips:
            place = trip.get("place", {})
            name = place.get("name", "Unknown")
            category = place.get("category", "Unknown")
            self.view.results_list.addItem(f"{name} ({category})")

        self.view.results_list.itemClicked.connect(self.show_trip_detail)

    def show_trip_detail(self, item):
        index = self.view.results_list.row(item)
        trip_data = self.trips[index]
        # שמירה במשתנה כדי שהחלון לא ייסגר מיד
        self.detail_view = TripDetailView(trip_data)
        self.detail_view.show()
