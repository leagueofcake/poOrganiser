class Event():
    def __init__(self, name, location, time):
        self.name = name
        self.location = location
        self.time = time

    def get_name(self):
        return self.name
