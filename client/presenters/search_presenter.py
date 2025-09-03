# client/presenters/search_presenter.py

from services.api_client import get_trips
from views.search_view import SearchView
from views.trip_detail_view import TripDetailView

#מחלקה עבורת חיפוש טיולים
class SearchPresenter:
    
    def __init__(self, view: SearchView):
      # שמירה על הפניה ל־
      # SearchView
      self.view = view

      # חיבור הכפתור לחיפוש
      self.view.search_button.clicked.connect(self.search)

      # שמירה על חלון פרטי טיול כדי שלא ייסגר מיד ע"י
      # Garbage Collector
      self.detail_view = None


    #מופעל כאשר המשתמש לוחץ על כפתור החיפוש
    def search(self):

      city = self.view.search_input.text()
      if not city:
        return

      trips = get_trips(city)

      # שמירת התוצאות במשתנה פנימי כדי לדעת איזה טיול נבחר אחר כך
      self.trips = trips

      # איפוס הרשימה והכנסה מחדש
      self.view.results_list.clear()

      # הוספת התוצאות החדשות לרשימה
      for trip in trips:
        place = trip.get("place", {})
        name = place.get("name", "Unknown")
        category = place.get("category", "Unknown")

        # מוסיפים שורה לרשימת התוצאות עם שם האתר והקטגוריה
        self.view.results_list.addItem(f"{name} ({category})")

      # חיבור כל פריט ברשימה כך שלחיצה עליו תציג את פרטי הטיול
      self.view.results_list.itemClicked.connect(self.show_trip_detail)


    # מציג את פרטי הטיול שנבחר
    def show_trip_detail(self, item):
       
      index = self.view.results_list.row(item)
      trip_data = self.trips[index]

      # שמירה במשתנה כדי שהחלון לא ייסגר מיד
      self.detail_view = TripDetailView(trip_data)
      self.detail_view.show()
