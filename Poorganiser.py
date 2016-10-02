#!/usr/bin/env python3.5
import datetime
from config import porg_config
from sqlalchemy import create_engine
from Event import Event
from User import User
from EventUser import EventUser
from Question import Question
from sqlalchemy.orm import sessionmaker

class Poorganiser():
    def __init__(self):
        self._engine = create_engine(porg_config.DB_URL)
        self.s = sessionmaker(bind=self._engine)()

    def update(self, obj):
        if isinstance(obj, EventUser): # Need to convert list to string before storing in db

            obj.roles = str(obj.roles)
        self.s.commit()
        return obj

    # User
    def add_user(self, username):
        u = User(username)
        self.s.add(u)
        self.s.commit()
        return u

     # Returns None if username not found
    def get_user(self, username):
        return self.s.query(User).filter(User.username == username).first()

    def remove_user(self, username):
        u = self.get_user(username)
        self.s.query(User).filter(User.username == username).delete()
        if u != None:
            self.s.commit()
            return True # Deleted
        else: # User not found
            return None

    # Event
    def add_event(self, ownerid, name, location, year=None, month=None, day=None):
        date = None
        if year and month and day:
            date = datetime.date(year, month, day)
        e = Event(ownerid, name, location, date)
        self.s.add(e)
        self.s.commit()
        return e

    def get_event(self, eventid):
        return self.s.query(Event).get(eventid)

    def remove_event(self, eventid):
        e = self.get_event(eventid)
        self.s.query(Event).filter(Event.id == eventid).delete()
        if e != None:
            self.s.commit()
            return True # deleted
        return None

    # EventUser
    def add_eventuser(self, eventid, userid, isgoing):
        eu = EventUser(eventid, userid, isgoing)
        eu.roles = str(eu.roles) # Convert to string
        self.s.add(eu)
        self.s.commit()
        return eu

    def get_eventuser(self, eventid, userid):
        return self.s.query(EventUser).filter(EventUser.eventid == eventid).filter(EventUser.userid == userid).first()

    def remove_eventuser(self, eventid, userid):
        eu = self.get_eventuser(eventid, userid)
        self.s.query(EventUser).filter(EventUser.eventid == eventid).filter(EventUser.userid == userid).delete()
        if eu != None:
            self.s.commit()
            return True # Deleted
        return None

    # Question
    def get_question(self, questionid):
        return self.s.query(Question).get(questionid)

    def add_question(self, eventid, text, yettovote, choices=1, pref=False):
        q = Question(eventid, text, yettovote, choices, pref)
        q.yettovote = str(q.yettovote)
        self.s.add(q)
        self.s.commit()
        return q
