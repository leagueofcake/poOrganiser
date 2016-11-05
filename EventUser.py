import ast
from create_base import Base
from sqlalchemy import Column, Integer, Unicode, UnicodeText, String, Date, Boolean


class EventUser(Base):
    __tablename__ = 'eventusers'
    eventuserid = Column(Integer, primary_key=True)
    eventid = Column(Integer)
    userid = Column(Integer)
    isgoing = Column(Unicode(20))
    roles = Column(Unicode(100))

    def __init__(self, eventid, userid, isgoing='Invited', roles=[]):
        self.eventuserid = None
        self.eventid = eventid
        self.userid = userid
        self.isgoing = isgoing
        self.roles = roles

    def get_eventuserid(self):
        return self.eventuserid

    def get_isgoing(self):
        return self.isgoing

    def get_roles(self):
        return self.roles

    def get_userid(self):
        return self.userid

    def debug_print(self):
        print("\tUSER GOING ", self.isgoing)
        print("\tUSER ROLES ", self.roles)

    def set_isgoing(self, isgoing):
        self.isgoing = isgoing

    def add_role(self, role):
        self.roles = ast.literal_eval(str(self.roles)) # Convert to list before appending
        self.roles.append(role)

    def remove_role(self, role):
        self.roles = ast.literal_eval(str(self.roles)) # Convert to list before appending
        if role in self.roles:
            self.roles.remove(role)
        else:
            return None
