from User import User
from create_base import Base
from sqlalchemy import Column, Integer, Unicode, UnicodeText, String, Date

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    ownerid = Column(Integer)
    name = Column(Unicode(40))
    location = Column(Unicode(40))
    time = Column(Date)

    def __init__(self, ownerid, name, location, time):
        self.id = None
        self.ownerid = ownerid
        self.name = name
        self.location = location
        self.time = time

    def get_id(self):
        return self.id

    def get_ownerid(self):
        return self.ownerid

    def get_name(self):
        return self.name

    def get_location(self):
        return self.location

    def get_time(self):
        return self.time

    def set_ownerid(self, ownerid):
        self.ownerid = ownerid

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
