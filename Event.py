class Event():
    def __init__(self, name, location, time):
        self.name = name
        self.location = location
        self.time = time

    def get_name(self):
        return self.name

    def get_location(self):
        return self.location
        
    def get_time(self):
        return self.time

    def set_name(self, name):
        self.name = name

    def set_location(self, location):
        self.location = location

    def set_time(self, time):
        self.time = time
