from sqlalchemy import Column, Integer, Unicode, PickleType
from create_base import Base


class User(Base):
    """Usernames are assumed to be unique (e.g. Discord user id)."""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Unicode(40))
    events_organised_ids = Column(PickleType)
    events_attending_ids = Column(PickleType)

    def __init__(self, username):
        self.id = None
        self.username = username
        self.events_organised_ids = []
        self.events_attending_ids = []

    def get_id(self):
        return self.id

    def get_username(self):
        return self.username

    def get_events_organised_ids(self):
        return self.events_organised_ids

    def get_events_attending_ids(self):
        return self.events_attending_ids

    def set_username(self, username):
        self.username = username

    def add_event_organised(self, event_id):
        self.events_organised_ids.append(event_id)

    def add_event_attending(self, event_id):
        self.events_attending_ids.append(event_id)

    def remove_event_organised(self, event_id):
        self.events_organised_ids.remove(event_id)

    def remove_event_attending(self, event_id):
        self.events_attending_ids.remove(event_id)