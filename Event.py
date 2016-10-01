#!/usr/bin/env python3.5
from User import User
import datetime
from sqlalchemy import Column, Integer, Unicode, UnicodeText, String, Date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///porg.db', echo=False)
Base = declarative_base(bind=engine)

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

    def set_id(self, id):
        self.id = id

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

# Initialise SQLAlchemy session
Base.metadata.create_all()
Session = sessionmaker(bind=engine)
s = Session()

def add_event(name, location, year=None, month=None, day=None):
    if year and month and day:
        date = datetime.date(year, month, day)
    e = Event(name, location, date)
    s.add(e)
    s.commit()
    return e

def get_event(id):
    return s.query(Event).get(id)

def update_name(id, name):
    e = get_event(id)
    e.set_name(name)
    s.commit()
    return e

def update_location(id, location):
    e = get_event(id)
    get_event(id).set_location(location)
    s.commit()
    return e

def update_time(id, year, month, day):
    date = datetime.date(year, month, day)
    e = get_event(id)
    e.set_time(date)
    s.commit()
    return e

# UNIT TESTS
def run_tests():
    test_get_name()
    test_set_name()
    test_get_location()
    test_set_location()
    test_get_time()
    test_set_time()
    test_get_attendee()
    test_get_attendees()
    test_add_attendee()

def test_get_name():
    e1 = Event("BBQ", "Parra Park", "01/10/2016")
    assert(e1.get_name() == "BBQ")
    e1 = Event("", "house", "01/10/2016")
    assert(e1.get_name() == "")

def test_set_name():
    e1 = Event("BBQ", "Parra Park", "01/10/2016")
    e1.set_name("name is wrong")
    assert(e1.get_name() == "name is wrong")
    e1.set_name("")
    assert(e1.get_name() == "")

def test_get_location():
    e1 = Event("BBQ", "Parra Park", "01/10/2016")
    assert(e1.get_location() == "Parra Park")
    e1 = Event("BBQ", "", "01/10/2016")
    assert(e1.get_location() == "")

def test_get_attendee():
    e1 = Event("BBQ", "Parra Park", "01/10/2016")
    assert(e1.get_attendee('Bob') == None)
    e1 = Event("", "", "")
    assert(e1.get_attendee('Jane') == None)

def test_get_attendees():
    e1 = Event("BBQ", "Parra Park", "01/10/2016")
    assert(e1.get_attendees() == {})
    e1 = Event("", "", "")
    assert(e1.get_attendees() == {})

def test_add_attendee():
    e1 = Event("BBQ", "Parra Park", "01/10/2016")
    assert(e1.get_attendee('Bob') == None)
    e1.add_attendee('Bob')
    assert(e1.get_attendee('Bob').get_name() == 'Bob')
    assert(e1.get_attendee('Bob').get_going() == False)
    assert(e1.get_attendee('Bob').get_roles() == [])
    assert(e1.get_attendees() != {})

    e1.add_attendee('Jane')
    assert(e1.get_attendee('Jane').get_name() == 'Jane')
    assert(e1.get_attendee('Jane').get_going() == False)
    assert(e1.get_attendee('Jane').get_roles() == [])

def test_set_location():
    e1 = Event("BBQ", "Parra Park", "01/10/2016")
    e1.set_location("Parramatta Park")
    assert(e1.get_location() == "Parramatta Park")
    e1.set_location("")
    assert(e1.get_location() == "")

def test_get_time():
    e1 = Event("BBQ", "Parra Park", "01/10/2016")
    assert(e1.get_time() == "01/10/2016")
    e1 = Event("BBQ", "Parra Park", "")
    assert(e1.get_time() == "")

def test_set_time():
    e1 = Event("BBQ", "Parra Park", "01/10/2016")
    e1.set_time("02/10/2016")
    assert(e1.get_time() == "02/10/2016")
    e1.set_time("")
    assert(e1.get_time() == "")

run_tests()
