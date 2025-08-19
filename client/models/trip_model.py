class Trip:
    def __init__(self, trip_id, name, description, location, image_url=None):
        self.trip_id = trip_id
        self.name = name
        self.description = description
        self.location = location
        self.image_url = image_url

    def __repr__(self):
        return f"<Trip {self.name} in {self.location}>"
