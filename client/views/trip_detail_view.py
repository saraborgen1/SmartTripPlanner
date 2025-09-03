# client/views/trip_detail_view.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
from PySide6.QtCore import Qt
from client.utils.ai_button import add_ai_button

"""
    View 
    שאחראי להציג פרטי טיול. יכול להציג שני סוגים של מידע:
    1. תוצאות חיפוש שהגיעו מ־
       OpenTripMap
    2. טיול שנשמר במסד הנתונים
"""
class TripDetailView(QWidget):

    def __init__(self, data: dict):

        super().__init__()
        self.setMinimumSize(520, 420)

        # פריסת מסך
        layout = QVBoxLayout(self)

        # זיהוי סוג הנתונים:
        # האם מדובר בתוצאת חיפוש מאתר OpenTripMap
        is_search_result = "place" in data   
        # או שמדובר בטיול ששמור במסד הנתונים
        is_db_trip       = "start_date" in data and "end_date" in data

        # --- מצב 1: תוצאת חיפוש ---
        if is_search_result:
            place = data.get("place", {})
            route = data.get("route", {})
            # שליפת פרטים בסיסיים מהתוצאה
            name     = place.get("name", "Unknown")
            category = place.get("category", "Unknown")
            distance = data.get("distance", place.get("distance_meters", 0)) or 0
            self.setWindowTitle(f"Trip Details: {name}")
            layout.addWidget(QLabel(f"<b>{name}</b>"))
            layout.addWidget(QLabel(f"Category: {category}"))
            layout.addWidget(QLabel(f"Distance: {distance} meters"))

            # תיבת טקסט להצגת מסלול
            route_box = QTextEdit()
            route_box.setReadOnly(True)
            route_box.setText(self._format_route(route))
            layout.addWidget(route_box)

        # --- מצב 2: טיול מהמסד ---
        elif is_db_trip:
            self.setWindowTitle("Trip Details")

            # יעד
            dest = data.get("destination", "Unknown")
            layout.addWidget(QLabel(f"Destination: {dest}"))

            # תאריכים
            start_date = data.get("start_date", "N/A")
            end_date = data.get("end_date", "N/A")
            layout.addWidget(QLabel(f"Dates: {start_date} → {end_date}"))

            # תחבורה
            transport = ", ".join(data.get("transport", [])) or "N/A"
            layout.addWidget(QLabel(f"Transport: {transport}"))

            # אתרים נבחרים
            sites = data.get("selected_sites", [])
            layout.addWidget(QLabel("Selected Sites:"))
            sites_box = QTextEdit()
            sites_box.setReadOnly(True)
            sites_box.setText("\n".join(f"• {s}" for s in sites) if sites else "No selected sites.")
            layout.addWidget(sites_box)

            # מזג אוויר
            weather = data.get("weather")
            if weather:
                layout.addWidget(QLabel("Weather:"))
                w_box = QTextEdit()
                w_box.setReadOnly(True)
                w_box.setText(str(weather))
                layout.addWidget(w_box)

            # הערות
            notes = data.get("notes")
            if notes:
                layout.addWidget(QLabel("Notes:"))
                n_box = QTextEdit()
                n_box.setReadOnly(True)
                n_box.setText(notes)
                layout.addWidget(n_box)


        # --- מצב לא מזוהה ---
        else:
            self.setWindowTitle("Trip Details")
            warn = QLabel("Unsupported data format.")
            warn.setAlignment(Qt.AlignCenter)
            layout.addWidget(warn)

        # כפתור סגירה
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)


    #פונקציה שמציגה בצורה יפה את המסלול
    def _format_route(self, route: dict) -> str:
      
        if not route:
            return "No route information available."

        # --- צורה 1: routes+segments ---
        routes = route.get("routes")
        if isinstance(routes, list) and routes:
            out = []
            segments = routes[0].get("segments", [])
            if not segments:
                return "No route information available."

            for i, seg in enumerate(segments, 1):
                dist = seg.get("distance", 0)
                dur  = seg.get("duration", 0)
                out.append(f"Segment {i}: Distance {dist:.1f} m, Duration {dur:.1f} sec")
                # מעבר על כל הצעדים בתוך הסגמנט
                for j, step in enumerate(seg.get("steps", []) or [], 1):
                    instr = step.get("instruction", "-")
                    sdist = step.get("distance", 0)
                    sdur  = step.get("duration", 0)
                    out.append(f"  Step {j}: {instr} ({sdist:.1f} m, {sdur:.1f} sec)")
            return "\n".join(out)

        # --- צורה 2: steps בלבד ---
        steps = route.get("steps")
        if isinstance(steps, list) and steps:
            lines = []
            for j, step in enumerate(steps, 1):
                instr = step.get("instruction", "-")
                sdist = step.get("distance", 0)
                sdur  = step.get("duration", 0)
                lines.append(f"Step {j}: {instr} ({sdist:.1f} m, {sdur:.1f} sec)")
            return "\n".join(lines)

        return "No route information available."

    # חיבור אפשרות ל־
    # AI
    def set_ai_callback(self, cb):
        self._ai_callback = cb
