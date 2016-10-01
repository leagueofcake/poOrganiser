#!/usr/bin/env python3.5
from create_session import s

# User
def add_user(username):
    u = User(username)
    s.add(u)
    s.commit()
    return u

 # Returns None if username not found
def get_user(username):
    return s.query(User).filter(User.username == username).first()

def update_user(obj):
    s.commit()
    return obj

# Event
def add_event(name, location, year=None, month=None, day=None):
    date = None
    if year and month and day:
        date = datetime.date(year, month, day)
    e = Event(name, location, date)
    s.add(e)
    s.commit()
    return e

def get_event(id):
    return s.query(Event).get(id)

def update_event(obj):
    s.commit()
    return obj

# EventUserdef add_eventuser(eventid, userid, isgoing):
    eu = EventUser(eventid, userid, isgoing)
    eu.roles = str(eu.roles) # Convert to string
    s.add(eu)
    s.commit()
    return eu

def get_eventuser(eventid, userid):
    return s.query(EventUser).filter(EventUser.eventid == eventid).filter(EventUser.userid == userid).one()

def update_eventuser(obj):
    obj.roles = str(obj.roles)
    s.commit()
    return obj

# EventUser
def add_eventuser(eventid, userid, isgoing):
    eu = EventUser(eventid, userid, isgoing)
    eu.roles = str(eu.roles) # Convert to string
    s.add(eu)
    s.commit()
    return eu

def get_eventuser(eventid, userid):
    return s.query(EventUser).filter(EventUser.eventid == eventid).filter(EventUser.userid == userid).one()

def update_eventuser(obj):
    obj.roles = str(obj.roles)
    s.commit()
    return obj
