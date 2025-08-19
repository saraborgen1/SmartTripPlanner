# from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton

# class TripDetailView(QWidget):
#     def __init__(self, trip):
#         super().__init__()
#         self.setWindowTitle(f"Trip Details: {trip.name}")
#         self.setMinimumSize(400, 300)

#         layout = QVBoxLayout()

#         self.name_label = QLabel(f"<b>{trip.name}</b>")
#         self.location_label = QLabel(f"Location: {trip.location}")
#         self.description_text = QTextEdit()
#         self.description_text.setReadOnly(True)
#         self.description_text.setText(trip.description)

#         self.close_button = QPushButton("Close")

#         layout.addWidget(self.name_label)
#         layout.addWidget(self.location_label)
#         layout.addWidget(self.description_text)
#         layout.addWidget(self.close_button)

#         self.setLayout(layout)

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton

class TripDetailView(QWidget):
    def __init__(self, trip: dict):
        super().__init__()
        place = trip.get("place", {})
        route = trip.get("route", {})

        self.setWindowTitle(f"Trip Details: {place.get('name', 'Unknown')}")
        self.setMinimumSize(500, 400)

        layout = QVBoxLayout()

        # פרטי המקום
        self.name_label = QLabel(f"<b>{place.get('name', 'Unknown')}</b>")
        self.category_label = QLabel(f"Category: {place.get('category', 'Unknown')}")
        self.distance_label = QLabel(f"Distance: {place.get('distance_meters', 0)} meters")

        # הצגת המסלול בצורה קריאה
        self.route_text = QTextEdit()
        self.route_text.setReadOnly(True)
        self.route_text.setText(self.format_route(route))

        # כפתור סגירה
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)

        layout.addWidget(self.name_label)
        layout.addWidget(self.category_label)
        layout.addWidget(self.distance_label)
        layout.addWidget(self.route_text)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

    def format_route(self, route: dict) -> str:
        """
        ממיר את ה-route למחרוזת קריאה:
        לכל segment ולכל step מציג instruction, מרחק וזמן
        """
        text_lines = []

        routes = route.get("routes", [])
        if not routes:
            return "No route information available."

        # נסתכל על המסלול הראשון בלבד
        first_route = routes[0]
        segments = first_route.get("segments", [])
        for i, segment in enumerate(segments, 1):
            text_lines.append(f"Segment {i}: Distance {segment.get('distance',0):.1f} m, Duration {segment.get('duration',0):.1f} sec")
            steps = segment.get("steps", [])
            for j, step in enumerate(steps, 1):
                instr = step.get("instruction", "-")
                dist = step.get("distance", 0)
                dur = step.get("duration", 0)
                text_lines.append(f"  Step {j}: {instr} ({dist:.1f} m, {dur:.1f} sec)")

        return "\n".join(text_lines)
