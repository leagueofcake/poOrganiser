import datetime
from DbInterface import DbInterface
from Poorganiser import User, Event, Attendance
from PorgExceptions import *


class PorgWrapper:
    def __init__(self):
        self.db_interface = DbInterface()

    def get_user_by_username(self, username):
        return self.db_interface.s.query(User).filter(User.username == username).first()

    def register_user(self, username):
        if self.get_user_by_username(username):
            raise UserRegisteredError("User \"{}\" is already registered".format(username))

        u = User(username)
        self.db_interface.add(u)

    def unregister_user(self, username):
        u = self.get_user_by_username(username)
        if u:
            raise UserNotFoundError("User \"{}\" could not be found".format(username))

        self.db_interface.delete(u)

    def get_help(self):
        help_output = "TODO HELP SECTION"
        return help_output

    def get_curr_events(self):
        today = datetime.date.today()
        return self.db_interface.query(Event, Event.time > today, num='all')

    def create_event(self, owner_id, name, location='', time=None):
        e = Event(owner_id, name, location, time)
        self.db_interface.add(e)

        # Add event id to User.events_organised_ids
        owner = self.db_interface.get_by_id(owner_id, User)
        owner.add_event_organised(e)
        self.db_interface.update(owner)

    def delete_event(self, event_id):
        e = self.db_interface.get_by_id(event_id, Event)

        # Remove event id from User.events_organised_ids
        owner = self.db_interface.get_by_id(e.get_owner_id(), User)
        owner.remove_event_organised(e)
        self.db_interface.update(owner)
        self.db_interface.delete(e)

    def create_attendance(self, user_id, event_id, going_status='invited', roles=list()):
        a = Attendance(user_id, event_id, going_status, roles)
        self.db_interface.add(a)

        e = self.db_interface.get_by_id(event_id, Event)

        # Add event id to User.events_attending_ids
        u = self.db_interface.get_by_id(user_id, User)
        u.add_event_attending(e)
        self.db_interface.update(u)

        # Add attendance id to Event
        e.add_attendance(a)
        self.db_interface.update(e)

    def delete_attendance(self, attendance_id):
        a = self.db_interface.get_by_id(attendance_id, Attendance)
        e = self.db_interface.get_by_id(a.get_event_id(), Event)
        u = self.db_interface.get_by_id(a.get_user_id(), User)

        # Remove event id from Users.events_attending_ids
        u.remove_event_attending(e)
        self.db_interface.update(u)

        # Remove attendance id from Event.attendance_ids
        e.remove_attendance(a)
        self.db_interface.update(e)

        # Delete attendance object
        self.db_interface.delete(a)
