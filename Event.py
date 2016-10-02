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


    def debug_print(self):
        print("EVENT NAME = ", self.name)
        print("EVENT LOCATION = ", self.location)
        print("EVENT TIME = ", self.time)


    def print_info(self): #return string for discord output
        outputStr = "Event: " + self.name + "\n"
        outputStr += "Location: " + self.location + "\n"
        outputStr += "Date: " + self.time + "\n"
