from User import User
from create_base import Base
from sqlalchemy import Column, Integer, Unicode, UnicodeText, String, Date

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(40))
    location = Column(Unicode(40))
    time = Column(Date)

    def __init__(self, name, location, time):
        self.id = None
        self.name = name
        self.location = location
        self.time = time
        self.attendees = {}

    def get_name(self):
        return self.name

    def get_location(self):
        return self.location

    def get_time(self):
        return self.time

    def get_attendee(self, name):
        if name in self.attendees: # Check if in attendee dict
            return self.attendees[name]
        return None # User not found

    def get_attendees(self):
        return self.attendees

    def set_name(self, name):
        self.name = name

    def set_location(self, location):
        self.location = location

    def set_time(self, time):
        self.time = time

    def add_attendee(self, name):
        user = User(name)
        if user not in self.attendees:
            self.attendees[name] = user # Add to dict
        else:
            return None # User already exists!

    def debug_print(self):
        print("EVENT NAME = ", self.name)
        print("EVENT LOCATION = ", self.location)
        print("EVENT TIME = ", self.time)
        print("ATTENDEES: ")
        for key in self.attendees:
            attendee = self.attendees[key]
            attendee.debug_print()
