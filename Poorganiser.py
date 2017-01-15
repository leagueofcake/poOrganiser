from sqlalchemy import Column, Integer, Unicode, PickleType, Date
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


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer)
    name = Column(Unicode(40))
    location = Column(Unicode(40))
    time = Column(Date)
    attendee_ids = Column(PickleType)

    def __init__(self, owner_id, name, location, time):
        self.id = None
        self.owner_id = owner_id
        self.name = name
        self.location = location
        self.time = time
        self.attendee_ids = []

    def get_id(self):
        return self.id

    def get_owner_id(self):
        return self.owner_id

    def get_name(self):
        return self.name

    def get_location(self):
        return self.location

    def get_time(self):
        return self.time

    def get_attendee_ids(self):
        return self.attendee_ids

    def set_owner_id(self, owner_id):
        self.owner_id = owner_id

    def set_name(self, name):
        self.name = name

    def set_location(self, location):
        self.location = location

    def set_time(self, time):
        self.time = time

    def add_attendee(self, obj):
        attendee_id = obj

        if isinstance(obj, Attendee.Attendee):
            attendee_id = obj.id
        elif not isinstance(obj, int):
            raise TypeError("Invalid object type for add_event_attending: expected int or Event")

        if attendee_id not in self.attendee_ids:
            self.events_attending_ids.append(attendee_id)
