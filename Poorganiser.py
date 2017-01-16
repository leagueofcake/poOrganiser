from sqlalchemy import Column, Integer, Unicode, PickleType, Date
from create_base import Base
from datetime import datetime


class User(Base):
    """Usernames are assumed to be unique (e.g. Discord user id)."""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Unicode(40))
    events_organised_ids = Column(PickleType)
    events_attending_ids = Column(PickleType)

    def __init__(self, username):
        assert(isinstance(username, str))

        self.id = None
        self.username = username
        self.events_organised_ids = []
        self.events_attending_ids = []

    def __str__(self):
        return '{\n' + \
               '    id: {},\n'.format(self.id) + \
               '    username: {},\n'.format(self.username) + \
               '    events_organised_ids: {},\n'.format(self.events_organised_ids) + \
               '    events_attending_ids: {},\n'.format(self.events_attending_ids) + \
               '}'

    def get_id(self):
        return self.id

    def get_username(self):
        return self.username

    def get_events_organised_ids(self):
        return self.events_organised_ids

    def get_events_attending_ids(self):
        return self.events_attending_ids

    def set_username(self, username):
        assert(isinstance(username, str))
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
        """obj may be an int denoting an Event id or an Event object. Raises TypeError if obj is not either type.
        Returns None if the event id is not found in self.events_organised_ids."""
        event_id = obj

        if isinstance(obj, Event):
            event_id = obj.id
        elif not isinstance(obj, int):
            raise TypeError("Invalid object type for remove_event_organised: expected int or Event")

        if event_id in self.events_organised_ids:
            self.events_organised_ids.remove(event_id)
        else:
            return None

    def remove_event_attending(self, obj):
        """obj may be an int denoting an Event id or an Event object. Raises TypeError if obj is not either type.
        Returns None if the event id is not found in self.events_attending_ids."""
        event_id = obj

        if isinstance(obj, Event):
            event_id = obj.id
        elif not isinstance(obj, int):
            raise TypeError("Invalid object type for remove_event_attending: expected int or Event")

        if event_id in self.events_attending_ids:
            self.events_attending_ids.remove(event_id)
        else:
            return None


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer)
    name = Column(Unicode(40))
    location = Column(Unicode(40))
    time = Column(Date)
    attendance_ids = Column(PickleType)

    def __init__(self, owner_id, name, location='', time=None):
        assert(isinstance(owner_id, int))
        assert(isinstance(name, str))
        assert(isinstance(location, str))
        assert(isinstance(time, datetime) or time is None)

        self.id = None
        self.owner_id = owner_id
        self.name = name
        self.location = location
        self.time = time
        self.attendance_ids = []

    def __str__(self):
        return '{\n' + \
               '    id: {},\n'.format(self.id) + \
               '    owner_id: {},\n'.format(self.owner_id) + \
               '    name: {},\n'.format(self.name) + \
               '    location: {},\n'.format(self.location) + \
               '    time: {}\n'.format(self.time) + \
               '    attendance_ids: {}\n'.format(self.attendance_ids) + \
               '}'

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

    def get_attendance_ids(self):
        return self.attendance_ids

    def set_owner_id(self, owner_id):
        assert(isinstance(owner_id, int))
        self.owner_id = owner_id

    def set_name(self, name):
        assert (isinstance(name, str))
        self.name = name

    def set_location(self, location):
        assert (isinstance(location, str))
        self.location = location

    def set_time(self, time):
        assert (isinstance(time, datetime))
        self.time = time

    def add_attendance(self, obj):
        """obj may be an int denoting an Attendance id or an Attendance object. Attendance id is not added if it
        already exists. Raises TypeError if obj is not either type."""
        attendance_id = obj

        if isinstance(obj, Attendance):
            attendance_id = obj.id
        elif not isinstance(obj, int):
            raise TypeError("Invalid object type for add_attendance: expected int or Attendance")

        if attendance_id not in self.attendance_ids:
            self.attendance_ids.append(attendance_id)

    def remove_attendance(self, obj):
        """obj may be an int denoting an Attendance id or an Attendance object. Raises TypeError if obj is not
        either type."""
        if isinstance(obj, int):
            self.attendance_ids.remove(obj)
        elif isinstance(obj, Attendance):
            self.attendance_ids.remove(obj.id)
        else:
            raise TypeError("Invalid object type for remove_attendance: expected int or Attendance")


class Attendance(Base):
    __tablename__ = 'attendance'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    event_id = Column(Integer)
    going_status = Column(Unicode(40))
    roles = Column(PickleType)

    def __init__(self, user_id, event_id, going_status="invited", roles=list()):
        self.id = None
        self.user_id = user_id
        self.event_id = event_id
        self.going_status = going_status
        self.roles = roles

    def __str__(self):
        return '{\n' + \
               '    id: {},\n'.format(self.id) + \
               '    user_id: {},\n'.format(self.user_id) + \
               '    event_id: {},\n'.format(self.event_id) + \
               '    going_status: {},\n'.format(self.going_status) + \
               '    roles: {}\n'.format(self.roles) + \
               '}'

    def get_id(self):
        return self.id

    def get_user_id(self):
        return self.user_id

    def get_event_id(self):
        return self.event_id

    def get_going_status(self):
        return self.going_status

    def get_roles(self):
        return self.roles

    def set_going_status(self, status):
        self.going_status = status

    def add_role(self, role):
        self.roles.append(role)

    def remove_role(self, role):
        if role in self.roles:
            self.roles.remove(role)
        else:
            return None
