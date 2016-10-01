#!/usr/bin/env python3.5
from sqlalchemy import Column, Integer, Unicode, UnicodeText, String, Date, ForeignKey
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
    isgoing = Column(Unicode(40))

    def __init__(self, eventid, userid, isgoing):
        self.eventuserid = None
        self.eventid = eventid
        self.userid = userid
        self.isgoing = isgoing
        self.roles = []

    def get_isgoing(self):
        return self.isgoing

    def get_roles(self):
        return self.roles

    def debug_print(self):
        print("\tUSER GOING ", self.isgoing)
        print("\tUSER ROLES ", self.roles)

    def set_isgoing(self, isgoing):
        self.isgoing = isgoing

    def add_role(self, role):
        self.roles.append(role)

# Initialise SQLAlchemy session
Base.metadata.create_all()
Session = sessionmaker(bind=engine)
s = Session()

def add_eventuser(eventid, userid, isgoing):
    eu = EventUser(eventid, userid, isgoing)
    s.add(eu)
    s.commit()
    return eu
