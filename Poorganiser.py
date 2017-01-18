from datetime import datetime
from sqlalchemy import Column, Integer, Unicode, PickleType, DateTime
from sqlalchemy.ext.mutable import MutableList
from create_base import Base


class User(Base):
    """Usernames are assumed to be unique (e.g. Discord user id)."""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Unicode(40))
    events_organised_ids = Column(MutableList.as_mutable(PickleType))
    events_attending_ids = Column(MutableList.as_mutable(PickleType))

    def __init__(self, username):
        assert isinstance(username, str)

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
        assert isinstance(username, str)
        self.username = username

    def add_event_organised(self, obj):
        """obj may be an int denoting an Event id or an Event object. Event is not added
        if it already exists. Raises TypeError if obj is not either type."""
        if isinstance(obj, Event):
            obj = obj.id
        elif not isinstance(obj, int):
            raise TypeError("Invalid object type for add_event_organised: expected int or Event")

        if obj not in self.events_organised_ids:
            self.events_organised_ids.append(obj)

    def add_event_attending(self, obj):
        """obj may be an int denoting an Event id or an Event object. Event is not added if it
        already exists. Raises TypeError if obj is not either type."""
        if isinstance(obj, Event):
            obj = obj.id
        elif not isinstance(obj, int):
            raise TypeError("Invalid object type for add_event_attending: expected int or Event")

        if obj not in self.events_attending_ids:
            self.events_attending_ids.append(obj)

    def remove_event_organised(self, obj):
        """obj may be an int denoting an Event id or an Event object. Raises TypeError if obj is
        not either type. Returns None if the event id is not found in self.events_organised_ids."""
        if isinstance(obj, Event):
            obj = obj.id
        elif not isinstance(obj, int):
            raise TypeError("Invalid object type for remove_event_organised: expected int or Event")

        if obj in self.events_organised_ids:
            self.events_organised_ids.remove(obj)

    def remove_event_attending(self, obj):
        """obj may be an int denoting an Event id or an Event object. Raises TypeError if obj is
        not either type. Returns None if the event id is not found in self.events_attending_ids."""
        if isinstance(obj, Event):
            obj = obj.id
        elif not isinstance(obj, int):
            raise TypeError("Invalid object type for remove_event_attending: expected int or Event")

        if obj in self.events_attending_ids:
            self.events_attending_ids.remove(obj)


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer)
    name = Column(Unicode(40))
    location = Column(Unicode(40))
    time = Column(DateTime)
    attendance_ids = Column(MutableList.as_mutable(PickleType))

    def __init__(self, owner_id, name, location=None, time=None):
        assert isinstance(owner_id, int)  # Cannot be None on creation, but may later be
        assert isinstance(name, str)
        assert isinstance(location, str) or location is None
        assert isinstance(time, datetime) or time is None

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
        assert isinstance(owner_id, int) or owner_id is None
        self.owner_id = owner_id

    def set_name(self, name):
        assert isinstance(name, str)
        self.name = name

    def set_location(self, location):
        assert isinstance(location, str)
        self.location = location

    def set_time(self, time):
        assert isinstance(time, datetime)
        self.time = time

    def add_attendance_id(self, obj):
        """obj may be an int denoting an Attendance id or an Attendance object. Attendance id is
        not added if it already exists. Raises TypeError if obj is not either type."""
        if isinstance(obj, Attendance):
            obj = obj.id
        elif not isinstance(obj, int):
            raise TypeError("Invalid object type for add_attendance_id: expected int or Attendance")

        if obj not in self.attendance_ids:
            self.attendance_ids.append(obj)

    def remove_attendance_id(self, obj):
        """obj may be an int denoting an Attendance id or an Attendance object. Raises TypeError
        if obj is not either type."""
        if isinstance(obj, Attendance):
            obj = obj.get_id()
        elif not isinstance(obj, int):
            raise TypeError("Invalid object type for remove_attendance_id: expected int or Attendance")

        if obj in self.attendance_ids:
            self.attendance_ids.remove(obj)


class Attendance(Base):
    __tablename__ = 'attendance'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    event_id = Column(Integer)
    going_status = Column(Unicode(40))
    roles = Column(MutableList.as_mutable(PickleType))

    def __init__(self, user_id, event_id, going_status="invited", roles=list()):
        assert isinstance(user_id, int)
        assert isinstance(event_id, int)
        assert isinstance(going_status, str)
        assert isinstance(roles, list)
        for role in roles:
            assert isinstance(role, str)

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
        assert isinstance(status, str)
        self.going_status = status

    def add_role(self, role):
        assert isinstance(role, str)
        if role not in self.roles:
            self.roles.append(role)

    def remove_role(self, role):
        if role in self.roles:
            self.roles.remove(role)


class Choice(Base):
    __tablename__ = 'choices'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer)
    choice = Column(Unicode(40))

    def __init__(self, question_id, choice):
        assert isinstance(question_id, int)
        assert isinstance(choice, str)

        self.id = None
        self.question_id = question_id
        self.choice = choice

    def get_id(self):
        return self.id

    def get_question_id(self):
        return self.question_id

    def get_choice(self):
        return self.choice

    def set_question_id(self, question_id):
        assert isinstance(question_id, int)
        self.question_id = question_id

    def set_choice(self, choice):
        assert isinstance(choice, str)
        self.choice = choice


class Response(Base):
    __tablename__ = 'responses'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer)
    choice_ids = Column(MutableList.as_mutable(PickleType))

    def __init__(self, responder_id, question_id, choice_ids=[]):
        assert isinstance(responder_id, int)
        assert isinstance(question_id, int)
        assert isinstance(choice_ids, list)
        for choice_id in choice_ids:
            assert isinstance(choice_id, int)

        self.id = None
        self.responder_id = responder_id
        self.question_id = question_id
        self.choice_ids = choice_ids

    def get_id(self):
        return self.id

    def get_responder_id(self):
        return self.responder_id

    def get_question_id(self):
        return self.question_id

    def get_choice_ids(self):
        return self.choice_ids

    def add_choice_id(self, choice_id):
        assert isinstance(choice_id, int)
        if choice_id not in self.choice_ids:
            self.choice_ids.append(choice_id)

    def remove_choice_id(self, choice_id):
        assert isinstance(choice_id, int)
        if choice_id in self.choice_ids:
            self.choice_ids.remove(choice_id)


class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    question = Column(Unicode(40))
    question_type = Column(Unicode(40))
    survey_id = Column(Integer)
    allowed_choice_ids = Column(MutableList.as_mutable(PickleType))
    response_ids = Column(MutableList.as_mutable(PickleType))

    def __init__(self, question, question_type, survey_id=None, allowed_choice_ids=[]):
        assert isinstance(question, str)
        assert isinstance(question_type, str)
        assert isinstance(survey_id, int) or survey_id is None
        assert isinstance(allowed_choice_ids, list)
        for choice_id in allowed_choice_ids:
            assert isinstance(choice_id, int)

        self.id = None
        self.question = question
        self.question_type = question_type
        self.survey_id = survey_id
        self.allowed_choice_ids = allowed_choice_ids
        self.response_ids = []

    def get_id(self):
        return self.id

    def get_question(self):
        return self.question

    def get_question_type(self):
        return self.question_type

    def get_survey_id(self):
        return self.survey_id

    def get_allowed_choice_ids(self):
        return self.allowed_choice_ids

    def get_response_ids(self):
        return self.response_ids

    def set_survey_id(self, survey_id):
        self.survey_id = survey_id

    def set_question(self, question):
        assert isinstance(question, str)
        self.question = question

    def set_question_type(self, question_type):
        assert isinstance(question_type, str)
        self.question_type = question_type

    def add_allowed_choice_id(self, choice_id):
        assert isinstance(choice_id, int)
        if choice_id not in self.allowed_choice_ids:
            self.allowed_choice_ids.append(choice_id)

    def remove_allowed_choice_id(self, choice_id):
        assert isinstance(choice_id, int)
        if choice_id in self.allowed_choice_ids:
            self.allowed_choice_ids.remove(choice_id)
