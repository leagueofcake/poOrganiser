#!/usr/bin/env python3.5
import ast
from sqlalchemy import Column, Integer, Unicode, UnicodeText, String, Date, Boolean
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///porg.db', echo=False)
Base = declarative_base(bind=engine)

class EventUser(Base):
    __tablename__ = 'eventusers'
    eventuserid = Column(Integer, primary_key=True)
    eventid = Column(Integer)
    userid = Column(Integer)
    isgoing = Column(Boolean)
    roles = Column(Unicode(100))

    def __init__(self, eventid, userid, isgoing=False, roles=[]):
        self.eventuserid = None
        self.eventid = eventid
        self.userid = userid
        self.isgoing = isgoing
        self.roles = roles

    def get_isgoing(self):
        return self.isgoing

    def get_roles(self):
        return self.roles

    def debug_print(self):
        print("\tUSER GOING ", self.isgoing)
        print("\tUSER ROLES ", self.roles)

    def set_isgoing(self, isgoing):
        if isinstance(isgoing, bool):
            self.isgoing = isgoing
        else: # Not a boolean - return None
            return None

    def add_role(self, role):
        self.roles = ast.literal_eval(str(self.roles)) # Convert to list before appending
        self.roles.append(role)

    def remove_role(self, role):
        self.roles = ast.literal_eval(str(self.roles)) # Convert to list before appending
        if role in self.roles:
            self.roles.remove(role)
        else:
            return None

# Initialise SQLAlchemy session
Base.metadata.create_all()
Session = sessionmaker(bind=engine)
s = Session()

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
