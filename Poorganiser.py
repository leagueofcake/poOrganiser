#!/usr/bin/env python3.5
import datetime
from config import porg_config
from sqlalchemy import create_engine
from Event import Event
from User import User
from EventUser import EventUser
from sqlalchemy.orm import sessionmaker

class Poorganiser():
    def __init__(self):
        self._engine = create_engine(porg_config.DB_URL)
        self.s = sessionmaker(bind=self._engine)()
    # User
    def add_user(self, username):
        u = User(username)
        self.s.add(u)
        self.s.commit()
        return u

     # Returns None if username not found
    def get_user(self, username):
        return self.s.query(User).filter(User.username == username).first()

    # Event
    def add_event(self, name, location, year=None, month=None, day=None):
        date = None
        if year and month and day:
            date = datetime.date(year, month, day)
        e = Event(name, location, date)
        self.s.add(e)
        self.s.commit()
        return e

    def get_event(self, id):
        return self.s.query(Event).get(id)

    # EventUser
    def add_eventuser(self, eventid, userid, isgoing):
        eu = EventUser(eventid, userid, isgoing)
        eu.roles = str(eu.roles) # Convert to string
        self.s.add(eu)
        self.s.commit()
        return eu

    def get_eventuser(self, ventid, userid):
        return self.s.query(EventUser).filter(EventUser.eventid == eventid).filter(EventUser.userid == userid).one()

    def update(self, obj):
        if isinstance(obj, EventUser): #handle array input 
            obj.roles = str(obj.roles)
        self.s.commit()
        return obj

    # EventUser
    def add_eventuser(self, eventid, userid, isgoing, roles=[]):
        eu = EventUser(eventid, userid, isgoing, roles)
        eu.roles = str(eu.roles) # Convert to string
        self.s.add(eu)
        self.s.commit()
        return eu

    def get_eventuser(self, eventid, userid):
        return self.s.query(EventUser).filter(EventUser.eventid == eventid).filter(EventUser.userid == userid).one()
