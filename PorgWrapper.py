import datetime
from sqlalchemy import or_
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
        return u

    def unregister_user(self, obj):
        username = obj
        if isinstance(obj, User):
            u = self.db_interface.get_by_id(obj.get_id(), User)
            username = obj.get_username()
        else:
            u = self.get_user_by_username(obj)

        if not u:
            raise UserNotFoundError("User \"{}\" could not be found".format(username))

        self.db_interface.delete(u)

    def get_help(self):
        help_output = "TODO HELP SECTION"
        return help_output

    def get_curr_events(self):
        today = datetime.date.today()
        curr_filter = or_(Event.time >= today, Event.time == None)
        return self.db_interface.query(Event, curr_filter, num='all')

    def get_events_by_user(self, obj):
        if isinstance(obj, User):
            u = self.db_interface.get_by_id(obj.get_id(), User)
        else:
            u = self.db_interface.get_by_id(obj, User)

        # Check user exists in the database
        if not u:
            raise UserNotFoundError("User could not be found")

        res = []
        for event_id in u.get_events_organised_ids():
            e = self.db_interface.get_by_id(event_id, Event)
            res.append(e)
        return res

    def get_all_events(self):
        return self.db_interface.query(Event, True, num='all')

    def create_event(self, owner_id, name, location='', time=None):
        owner = self.db_interface.get_by_id(owner_id, User)

        # Check owner exists in the database
        if not owner:
            raise UserNotFoundError("Owner (user id {}) could not be found".format(owner_id))

        # Create event and insert into database
        e = Event(owner_id, name, location, time)
        self.db_interface.add(e)

        # Add event id to User.events_organised_ids
        owner.add_event_organised(e)
        self.db_interface.update(owner)

        # Add Attendance
        a = Attendance(owner_id, e.get_id(), going_status="going", roles=["organiser"])
        self.db_interface.add(a)
        e.add_attendance(a)
        self.db_interface.update(e)

        return e

    def delete_event(self, obj):
        if isinstance(obj, Event):
            e = self.db_interface.get_by_id(obj.get_id(), Event)
        else:
            e = self.db_interface.get_by_id(obj, Event)

        if not e:
            raise EventNotFoundError("Event could not be found for deletion")

        # Delete event
        event_owner_id = e.get_owner_id()
        self.db_interface.delete(e)

        # Remove event id from User.events_organised_ids
        owner = self.db_interface.get_by_id(event_owner_id, User)

        # Check owner exists in the database
        if not owner:
            raise UserNotFoundError("Event owner (id {}) could not be found".format(event_owner_id))

        owner.remove_event_organised(e)
        self.db_interface.update(owner)

    def get_attendance(self, user_id, event_id):
        return self.db_interface.query(Attendance, Attendance.user_id == user_id and
                                       Attendance.event_id == event_id, num='one')

    def get_attendances(self, event_id):
        res = []
        e = self.db_interface.get_by_id(event_id, Event)
        for attendance_id in e.get_attendance_ids():
            a = self.db_interface.get_by_id(attendance_id, Attendance)
            res.append(a)
        return res

    def create_attendance(self, user_id, event_id, going_status='invited', roles=list()):
        u = self.db_interface.get_by_id(user_id, User)
        e = self.db_interface.get_by_id(event_id, Event)

        # Check user and event exists in database
        if not e:
            raise EventNotFoundError("Event with event id {} could not be found".format(event_id))
        if not u:
            raise UserNotFoundError("User with id {} could not be found".format(user_id))

        # Create attendance
        a = Attendance(user_id, event_id, going_status, roles)
        self.db_interface.add(a)

        # Add event id to User.events_attending_ids
        u.add_event_attending(e)
        self.db_interface.update(u)

        # Add attendance id to Event
        e.add_attendance(a)
        self.db_interface.update(e)

        return a

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
