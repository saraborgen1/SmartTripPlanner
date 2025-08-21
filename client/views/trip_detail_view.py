# client/views/trip_detail_view.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
from PySide6.QtCore import Qt
from client.utils.ai_button import add_ai_button


class TripDetailView(QWidget):
    """
    View שאחראי להציג פרטי טיול.

    יכול להציג שני סוגים של מידע:
    1. תוצאות חיפוש שהגיעו מ־
       OpenTripMap
    2. טיול שנשמר במסד הנתונים
    """
    def __init__(self, data: dict):
        super().__init__()
        self.setMinimumSize(520, 420)

        # פריסת מסך
        # QVBoxLayout
        layout = QVBoxLayout(self)

        # זיהוי סוג הנתונים:
        is_search_result = "place" in data       # תוצאת חיפוש מ־ OpenTripMap
        is_db_trip       = "destination" in data # טיול שנשמר במסד הנתונים

        # --- מצב 1: תוצאת חיפוש ---
        if is_search_result:
            place = data.get("place", {})
            route = data.get("route", {})

            name     = place.get("name", "Unknown")
            category = place.get("category", "Unknown")
            distance = data.get("distance", place.get("distance_meters", 0)) or 0

            self.setWindowTitle(f"Trip Details: {name}")

            layout.addWidget(QLabel(f"<b>{name}</b>"))
            layout.addWidget(QLabel(f"Category: {category}"))
            layout.addWidget(QLabel(f"Distance: {distance} meters"))

            # תיבת טקסט להצגת מסלול
            # QTextEdit
            route_box = QTextEdit()
            route_box.setReadOnly(True)
            route_box.setText(self._format_route(route))
            layout.addWidget(route_box)

        # --- מצב 2: טיול מהמסד ---
        elif is_db_trip:
            dest       = data.get("destination", "Unknown")
            start_date = data.get("start_date", "")
            end_date   = data.get("end_date", "")
            sites      = data.get("selected_sites") or []
            transport  = data.get("transport") or []
            notes      = data.get("notes") or ""
            weather    = data.get("weather") or ""

            self.setWindowTitle(f"Trip Details: {dest}")

            layout.addWidget(QLabel(f"<b>{dest}</b>"))
            layout.addWidget(QLabel(f"Dates: {start_date} → {end_date}"))
            layout.addWidget(QLabel(f"Transport: {', '.join(transport) if transport else 'N/A'}"))

            layout.addWidget(QLabel("Selected Sites:"))
            sites_box = QTextEdit()
            sites_box.setReadOnly(True)
            sites_box.setText("\n".join(f"• {s}" for s in sites) if sites else "No selected sites.")
            layout.addWidget(sites_box)

            if weather:
                layout.addWidget(QLabel("Weather:"))
                w_box = QTextEdit()
                w_box.setReadOnly(True)
                w_box.setText(str(weather))
                layout.addWidget(w_box)

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
        # QPushButton
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

    # ---------- פונקציית עזר ----------
    def _format_route(self, route: dict) -> str:
        """
        מדפיסה בצורה יפה את המסלול.

        תומכת בשני מבנים:
        1. {routes:[{segments:[{steps:...}]}]}
        2. {steps:[...]}
        """
        if not route:
            return "No route information available."

        # --- צורה A: routes+segments ---
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

                for j, step in enumerate(seg.get("steps", []) or [], 1):
                    instr = step.get("instruction", "-")
                    sdist = step.get("distance", 0)
                    sdur  = step.get("duration", 0)
                    out.append(f"  Step {j}: {instr} ({sdist:.1f} m, {sdur:.1f} sec)")
            return "\n".join(out)

        # --- צורה B: steps בלבד ---
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

    # חיבור אפשרות ל־AI
    def set_ai_callback(self, cb):
        self._ai_callback = cb
