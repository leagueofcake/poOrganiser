from sqlalchemy import Column, Integer, Unicode, PickleType
from create_base import Base
from Event import Event


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

    def add_event_organised(self, obj):
        """obj may be an int denoting an Event id or an Event object. Event is not added if it already exists.
        Raises TypeError if obj is not either type."""
        event_id = obj
        if isinstance(obj, Event):
            event_id = obj.id
        elif not isinstance(obj, int):
            raise TypeError("Invalid object type for add_event_organised: expected int or Event")

        if event_id not in self.events_organised_ids:
            self.events_organised_ids.append(event_id)

    def add_event_attending(self, obj):
        """obj may be an int denoting an Event id or an Event object. Event is not added if it already exists.
        Raises TypeError if obj is not either type."""
        event_id = obj

        if isinstance(obj, Event):
            event_id = obj.id
        elif not isinstance(obj, int):
            raise TypeError("Invalid object type for add_event_attending: expected int or Event")

        if event_id not in self.events_attending_ids:
            self.events_attending_ids.append(event_id)

    def remove_event_organised(self, obj):
        """obj may be an int denoting an Event id or an Event object. Raises TypeError if obj is not either type."""
        if isinstance(obj, int):
            self.events_organised_ids.remove(obj)
        elif isinstance(obj, Event):
            self.events_organised_ids.remove(obj.id)
        else:
            raise TypeError("Invalid object type for remove_event_organised: expected int or Event")

    def remove_event_attending(self, obj):
        """obj may be an int denoting an Event id or an Event object. Raises TypeError if obj is not either type."""
        if isinstance(obj, int):
            self.events_attending_ids.remove(obj)
        elif isinstance(obj, Event):
            self.events_attending_ids.remove(obj.id)
        else:
            raise TypeError("Invalid object type for remove_event_attending: expected int or Event")
