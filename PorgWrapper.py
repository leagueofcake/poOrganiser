import datetime
from sqlalchemy import or_, and_
from config import porg_config
from DbInterface import DbInterface
from Poorganiser import User, Event, Attendance, Survey, Question, Choice, Response
from PorgExceptions import *


class PorgWrapper:
    def __init__(self):
        self.db_interface = DbInterface()

    def check_obj_exists(self, obj, obj_type):
        o = self.db_interface.get_obj(obj, obj_type)

        if o:
            return o
        elif obj_type is User:
            raise UserNotFoundError("User could not be found")
        elif obj_type is Event:
            raise EventNotFoundError("Event could not be found")
        elif obj_type is Attendance:
            raise AttendanceNotFoundError("Attendance could not be found")
        elif obj_type is Question:
            raise QuestionNotFoundError("Question could not be found")
        elif obj_type is Survey:
            raise SurveyNotFoundError("Survey could not be found")

    def get_user_by_username(self, username):
        return self.db_interface.s.query(User).filter(User.username == username).first()

    def register_user(self, username):
        if self.get_user_by_username(username):
            raise UserRegisteredError("User \"{}\" is already registered".format(username))

        u = User(username)
        self.db_interface.add(u)
        return u

    def unregister_user(self, obj, delete_events=False):
        username = obj
        if isinstance(obj, User):
            u = self.db_interface.get_obj(obj, User)
            username = obj.get_username()
        else:
            u = self.get_user_by_username(obj)

        if not u:
            raise UserNotFoundError("User \"{}\" could not be found".format(username))

        # Remove Attendance objects from database - use set() to remove duplicates
        events_participating = set(u.get_events_organised_ids() + u.get_events_attending_ids())
        for event_id in events_participating:
            a = self.get_attendance(u.get_id(), event_id)
            self.delete_attendance(a)

        # Remove organiser id from organised events
        for event in self.get_events_by_user(u):
            event.set_owner_id(None)

        if delete_events:
            for e in self.get_events_by_user(u):
                self.delete_event(e)

        self.db_interface.delete(u)

    def get_help(self):
        help_output = "TODO HELP SECTION"
        return help_output

    def get_curr_events(self):
        today = datetime.date.today()
        curr_filter = or_(Event.time >= today, Event.time == None)
        return self.db_interface.query(Event, curr_filter, num='all')

    def get_events_by_user(self, user_obj):
        u = self.check_obj_exists(user_obj, User)

        res = []
        for event_id in u.get_events_organised_ids():
            e = self.db_interface.get_obj(event_id, Event)
            res.append(e)
        return res

    def get_all_events(self):
        return self.db_interface.query(Event, True, num='all')

    def create_event(self, name, owner_obj, location=None, time=None):
        owner = self.check_obj_exists(owner_obj, User)
        owner_id = owner.get_id()
        # Create event and insert into database
        e = Event(name, owner_id, location, time)
        self.db_interface.add(e)

        # Add event id to User.events_organised_ids and User.events_attending_ids
        owner.add_event_organised(e)
        owner.add_event_attending(e)
        self.db_interface.update(owner)

        # Add Attendance
        a = Attendance(owner_id, e.get_id(), going_status="going", roles=["organiser"])
        self.db_interface.add(a)
        e.add_attendance_id(a)
        self.db_interface.update(e)

        return e

    def delete_event(self, event_obj):
        e = self.check_obj_exists(event_obj, Event)

        # Remove attendances from database
        for attendance_id in e.get_attendance_ids():
            a = self.db_interface.get_obj(attendance_id, Attendance)
            self.delete_attendance(a.get_id())

        # Delete event
        event_owner_id = e.get_owner_id()
        self.db_interface.delete(e)

        # Remove event id from User.events_organised_ids and User.events_attending_ids
        # NB: owner may not exist if they unregistered instead of deleting user
        owner = self.db_interface.get_obj(event_owner_id, User)
        if owner:
            owner.remove_event_organised(e)
            owner.remove_event_attending(e)  # May not be present if organising but not attending
            self.db_interface.update(owner)

    def get_attendance(self, user_obj, event_obj):
        u = self.db_interface.get_obj(user_obj, User)
        e = self.db_interface.get_obj(event_obj, Event)

        if not e or not u:
            return None

        attendance_filter = and_(Attendance.user_id == u.get_id(), Attendance.event_id == e.get_id())
        return self.db_interface.query(Attendance, attendance_filter, num='one')

    def get_attendances(self, obj):
        res = []
        if isinstance(obj, Event):
            e = self.db_interface.get_obj(obj.get_id(), Event)
            for attendance_id in e.get_attendance_ids():
                a = self.db_interface.get_obj(attendance_id, Attendance)
                res.append(a)
        elif isinstance(obj, User):
            u = self.db_interface.get_obj(obj.get_id(), User)
            for event_id in u.get_events_attending_ids():
                a = self.get_attendance(u.get_id(), event_id)
                res.append(a)
        else:
            raise TypeError("Invalid object type for get_attendances: expected Event or User")

        return res

    def create_attendance(self, user_obj, event_obj, going_status='invited', roles=list()):
        u = self.check_obj_exists(user_obj, User)
        e = self.check_obj_exists(event_obj, Event)

        # Create attendance
        a = Attendance(u.get_id(), e.get_id(), going_status, roles)
        self.db_interface.add(a)

        # Add event id to User.events_attending_ids
        u.add_event_attending(e)
        self.db_interface.update(u)

        # Add attendance id to Event
        e.add_attendance_id(a)
        self.db_interface.update(e)

        return a

    def delete_attendance(self, attendance_obj):
        a = self.check_obj_exists(attendance_obj, Attendance)
        e = self.check_obj_exists(a.get_event_id(), Event)
        u = self.check_obj_exists(a.get_user_id(), User)

        # Remove event id from Users.events_attending_ids
        u.remove_event_attending(e)
        self.db_interface.update(u)

        # Remove attendance id from Event.attendance_ids
        e.remove_attendance_id(a)
        self.db_interface.update(e)

        # Delete attendance object
        self.db_interface.delete(a)

    def create_choice(self, question_obj, choice):
        q = self.check_obj_exists(question_obj, Question)
        c = Choice(q.get_id(), choice)
        self.db_interface.add(c)

        # Add choice id to Question.allowed_choice_ids
        q.add_allowed_choice_id(c.get_id())
        self.db_interface.update(q)

        return c

    def create_question(self, owner_obj, question, question_type, survey_obj=None):
        """Specifying allowed_choice_ids is forbidden here - since create_choice requires an
        existing question, we cannot have choices existing before questions."""
        if question_type not in porg_config.ALLOWED_QUESTION_TYPES:
            raise InvalidQuestionTypeError("Invalid Question type: {}".format(question_type))

        owner = self.check_obj_exists(owner_obj, User)

        # TODO: add User.question_ids

        survey_id = None
        if survey_obj:
            survey_obj = self.check_obj_exists(survey_obj, Survey)
            survey_id = survey_obj.get_id()

        q = Question(owner.get_id(), question, question_type, survey_id)

        self.db_interface.add(q)

        # Add question id to Survey.question_ids
        if survey_id:
            survey_obj.add_question_id(q.get_id())
            self.db_interface.update(survey_obj)

        return q

    def create_response(self, responder_obj, question_obj, response_text=[], choice_ids=[]):
        # TODO: add User.response_ids
        pass

    def create_survey(self, name, owner_obj, question_ids=[], event_obj=None):
        owner = self.check_obj_exists(owner_obj, User)

        # TODO: Add User.survey_ids

        # Check each question_id can be found in the database
        questions = []
        if question_ids:
            for question_id in question_ids:
                q = self.check_obj_exists(question_id, Question)
                questions.append(q)

        # Check each event_id can be found in the database
        if event_obj:
            event_obj = self.check_obj_exists(event_obj, Event)
            event_obj = event_obj.get_id()

        s = Survey(name, owner.get_id(), question_ids=question_ids, event_id=event_obj)
        self.db_interface.add(s)

        # Set survey_id for each Question
        for q in questions:
            q.set_survey_id(s.get_id())
            self.db_interface.update(q)

        return s
