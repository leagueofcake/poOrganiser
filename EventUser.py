import ast
from create_base import Base
from sqlalchemy import Column, Integer, Unicode, UnicodeText, String, Date, Boolean


class EventUser(Base):
    __tablename__ = 'eventusers'
    event_user_id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    user_id = Column(Integer)
    is_going = Column(Unicode(20))
    roles = Column(Unicode(100))

    def __init__(self, event_id, user_id, is_going='Invited', roles=[]):
        self.event_user_id = None
        self.event_id = event_id
        self.user_id = user_id
        self.is_going = is_going
        self.roles = roles

    def get_event_user_id(self):
        return self.event_user_id

    def get_is_going(self):
        return self.is_going

    def get_roles(self):
        return self.roles

    def get_userid(self):
        return self.user_id

    def debug_print(self):
        print("\tUSER GOING ", self.is_going)
        print("\tUSER ROLES ", self.roles)

    def set_is_going(self, is_going):
        self.is_going = is_going

    def add_role(self, role):
        self.roles = ast.literal_eval(str(self.roles)) # Convert to list before appending
        self.roles.append(role)

    def remove_role(self, role):
        self.roles = ast.literal_eval(str(self.roles)) # Convert to list before appending
        if role in self.roles:
            self.roles.remove(role)
        else:
            return None
