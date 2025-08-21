# client/presenters/search_presenter.py

from services.api_client import get_trips
from views.search_view import SearchView
from views.trip_detail_view import TripDetailView


class SearchPresenter:
    """
    מחלקת
    Presenter
    האחראית על חיפוש טיולים לפי עיר.

    התפקידים:
    - לקרוא את קלט המשתמש מה־
      SearchView
    - לשלוח בקשה ל־
      API Client
      (פונקציה
      get_trips)
    - להציג את התוצאות ברשימה
    - לפתוח חלון פרטי טיול חדש כאשר לוחצים על פריט
    """

    def __init__(self, view: SearchView):
        # שמירה על הפניה ל־
        # SearchView
        self.view = view

        # חיבור הכפתור "Search" מה־
        # View
        # לפונקציית החיפוש
        self.view.search_button.clicked.connect(self.search)

        # שמירה על חלון פרטי טיול כדי שלא ייסגר מיד ע"י
        # Garbage Collector
        self.detail_view = None

    def search(self):
        """
        מופעל כאשר המשתמש לוחץ על כפתור החיפוש.

        זרימה:
        - קולט שם עיר מה־
          QLineEdit
        - שולח בקשה ל־
          get_trips
        - מנקה את הרשימה וממלא אותה בתוצאות חדשות
        - מחבר את האירוע של לחיצה על פריט → הצגת פרטי טיול
        """
        city = self.view.search_input.text()
        if not city:
            return

        trips = get_trips(city)
        # שמירה פנימית כדי לדעת איזה
        # Trip
        # נבחר
        self.trips = trips

        # איפוס הרשימה והכנסה מחדש
        self.view.results_list.clear()

        for trip in trips:
            place = trip.get("place", {})
            name = place.get("name", "Unknown")
            category = place.get("category", "Unknown")

            # מוסיפים שורה עם שם וקטגוריה
            self.view.results_list.addItem(f"{name} ({category})")

        # כל פריט שנלחץ יוביל להצגת פרטי הטיול
        self.view.results_list.itemClicked.connect(self.show_trip_detail)

    def show_trip_detail(self, item):
        """
        מציג חלון חדש עם פרטי טיול שנבחר מהרשימה.
        """
        index = self.view.results_list.row(item)
        trip_data = self.trips[index]

        # שמירה במשתנה כדי שהחלון לא ייסגר מיד
        self.detail_view = TripDetailView(trip_data)
        self.detail_view.show()
