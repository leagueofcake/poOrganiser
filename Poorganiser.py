from config import porg_config
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, Unicode, PickleType, DateTime
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(porg_config.DB_URL, echo=False)
Base = declarative_base(bind=engine)


class User(Base):
    """Usernames are assumed to be unique (e.g. Discord user id)."""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Unicode(40))
    events_organised_ids = Column(MutableList.as_mutable(PickleType))
    events_attending_ids = Column(MutableList.as_mutable(PickleType))
    survey_ids = Column(MutableList.as_mutable(PickleType))
    question_ids = Column(MutableList.as_mutable(PickleType))

    def __init__(self, username):
        assert isinstance(username, str)

        self.id = None
        self.username = username
        self.events_organised_ids = []
        self.events_attending_ids = []
        self.survey_ids = []
        self.question_ids = []

    def __str__(self):
        return '{\n' + \
               '    id: {},\n'.format(self.id) + \
               '    username: {},\n'.format(self.username) + \
               '    events_organised_ids: {},\n'.format(self.events_organised_ids) + \
               '    events_attending_ids: {},\n'.format(self.events_attending_ids) + \
               '    survey_ids: {},\n'.format(self.survey_ids) + \
               '    question_ids: {},\n'.format(self.question_ids) + \
               '}'

    def get_id(self):
        return self.id

    def get_username(self):
        return self.username

    def get_events_organised_ids(self):
        return self.events_organised_ids

    def get_events_attending_ids(self):
        return self.events_attending_ids

    def get_survey_ids(self):
        return self.survey_ids

    def get_question_ids(self):
        return self.question_ids

    def set_username(self, username):
        assert isinstance(username, str)
        self.username = username

    def add_event_organised(self, event_obj):
        """event_obj may be an int denoting an Event id or an Event object. Event is not added
        if it already exists. Raises TypeError if event_obj is not either type."""
        if isinstance(event_obj, Event):
            event_obj = event_obj.get_id()
        elif not isinstance(event_obj, int):
            raise TypeError("Invalid object type for add_event_organised: expected int or Event")

        if event_obj not in self.events_organised_ids:
            self.events_organised_ids.append(event_obj)

    def add_event_attending(self, event_obj):
        """event_obj may be an int denoting an Event id or an Event object. Event is not added if it
        already exists. Raises TypeError if event_obj is not either type."""
        if isinstance(event_obj, Event):
            event_obj = event_obj.get_id()
        elif not isinstance(event_obj, int):
            raise TypeError("Invalid object type for add_event_attending: expected int or Event")

        if event_obj not in self.events_attending_ids:
            self.events_attending_ids.append(event_obj)

    def remove_event_organised(self, event_obj):
        """event_obj may be an int denoting an Event id or an Event object. Raises TypeError if
        event_obj is not either type. Returns None if the event id is not found in
        self.events_organised_ids."""
        if isinstance(event_obj, Event):
            event_obj = event_obj.get_id()
        elif not isinstance(event_obj, int):
            raise TypeError("Invalid object type for remove_event_organised: expected int or Event")

        if event_obj in self.events_organised_ids:
            self.events_organised_ids.remove(event_obj)

    def remove_event_attending(self, event_obj):
        """event_obj may be an int denoting an Event id or an Event object. Raises TypeError if
        event_obj is not either type. Returns None if the event id is not found in
        self.events_attending_ids."""
        if isinstance(event_obj, Event):
            event_obj = event_obj.get_id()
        elif not isinstance(event_obj, int):
            raise TypeError("Invalid object type for remove_event_attending: expected int or Event")

        if event_obj in self.events_attending_ids:
            self.events_attending_ids.remove(event_obj)

    def add_survey_id(self, survey_obj):
        if isinstance(survey_obj, Survey):
            survey_obj = survey_obj.get_id()
        elif not isinstance(survey_obj, int):
            raise TypeError("Invalid object type for add_survey_id: expected int or Survey")

        if survey_obj not in self.survey_ids:
            self.survey_ids.append(survey_obj)

    def add_question_id(self, question_obj):
        if isinstance(question_obj, Question):
            question_obj = question_obj.get_id()
        elif not isinstance(question_obj, int):
            raise TypeError("Invalid object type for add_question_id: expected int or Question")

        if question_obj not in self.question_ids:
            self.question_ids.append(question_obj)

    def remove_survey_id(self, survey_obj):
        if isinstance(survey_obj, Survey):
            survey_obj = survey_obj.get_id()
        elif not isinstance(survey_obj, int):
            raise TypeError("Invalid object type for remove_survey_id: expected int or Survey")

        if survey_obj in self.survey_ids:
            self.survey_ids.remove(survey_obj)

    def remove_question_id(self, question_obj):
        if isinstance(question_obj, Question):
            question_obj = question_obj.get_id()
        elif not isinstance(question_obj, int):
            raise TypeError("Invalid object type for remove_question_id: expected int or Question")

        if question_obj in self.question_ids:
            self.question_ids.remove(question_obj)


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(40))
    owner_id = Column(Integer)
    location = Column(Unicode(40))
    time = Column(DateTime)
    attendance_ids = Column(MutableList.as_mutable(PickleType))
    survey_ids = Column(MutableList.as_mutable(PickleType))

    def __init__(self, name, owner_id, location=None, time=None, survey_ids=[]):
        assert isinstance(name, str)
        assert isinstance(owner_id, int)  # Cannot be None on creation, but may later be
        assert isinstance(location, str) or location is None
        assert isinstance(time, datetime) or time is None
        assert isinstance(survey_ids, list)
        for survey_id in survey_ids:
            assert isinstance(survey_id, int)

        self.id = None
        self.name = name
        self.owner_id = owner_id
        self.location = location
        self.time = time
        self.attendance_ids = []
        self.survey_ids = survey_ids

    def __str__(self):
        return '{\n' + \
               '    id: {},\n'.format(self.id) + \
               '    name: {},\n'.format(self.name) + \
               '    owner_id: {},\n'.format(self.owner_id) + \
               '    location: {},\n'.format(self.location) + \
               '    time: {}\n'.format(self.time) + \
               '    attendance_ids: {}\n'.format(self.attendance_ids) + \
               '    survey_ids: {}\n'.format(self.survey_ids) + \
               '}'

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_owner_id(self):
        return self.owner_id

    def get_location(self):
        return self.location

    def get_time(self):
        return self.time

    def get_attendance_ids(self):
        return self.attendance_ids

    def get_survey_ids(self):
        return self.survey_ids

    def set_name(self, name):
        assert isinstance(name, str)
        self.name = name

    def set_owner_id(self, owner_id):
        assert isinstance(owner_id, int) or owner_id is None
        self.owner_id = owner_id

    def set_location(self, location):
        assert isinstance(location, str)
        self.location = location

    def set_time(self, time):
        assert isinstance(time, datetime)
        self.time = time

    def add_attendance_id(self, attendance_obj):
        """attendance_obj may be an int denoting an Attendance id or an Attendance object.
        Attendance id is not added if it already exists. Raises TypeError if attendance_obj is
        not either type."""
        if isinstance(attendance_obj, Attendance):
            attendance_obj = attendance_obj.get_id()
        elif not isinstance(attendance_obj, int):
            raise TypeError("Invalid object type for add_attendance_id: expected int or Attendance")

        if attendance_obj not in self.attendance_ids:
            self.attendance_ids.append(attendance_obj)

    def remove_attendance_id(self, attendance_obj):
        """attendance_obj may be an int denoting an Attendance id or an Attendance object. Raises
        TypeError if attendance_obj is not either type."""
        if isinstance(attendance_obj, Attendance):
            attendance_obj = attendance_obj.get_id()
        elif not isinstance(attendance_obj, int):
            raise TypeError("Invalid object type for remove_attendance_id: expected int or Attendance")

        if attendance_obj in self.attendance_ids:
            self.attendance_ids.remove(attendance_obj)

    def add_survey_id(self, survey_obj):
        if isinstance(survey_obj, Survey):
            survey_obj = survey_obj.get_id()
        elif not isinstance(survey_obj, int):
            raise TypeError("Invalid object type for add_survey_id: expected int or Survey")

        if survey_obj not in self.survey_ids:
            self.survey_ids.append(survey_obj)

    def remove_survey_id(self, survey_obj):
        if isinstance(survey_obj, Survey):
            survey_obj = survey_obj.get_id()
        elif not isinstance(survey_obj, int):
            raise TypeError("Invalid object type for remove_survey_id: expected int or Survey")

        if survey_obj in self.survey_ids:
            self.survey_ids.remove(survey_obj)


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

    def __str__(self):
        return '{\n' + \
               '    id: {},\n'.format(self.id) + \
               '    question_id: {},\n'.format(self.question_id) + \
               '    choice: {},\n'.format(self.choice) + \
               '}'

    def get_id(self):
        return self.id

    def get_question_id(self):
        return self.question_id

    def get_choice(self):
        return self.choice

    def set_question_id(self, question_obj):
        if isinstance(question_obj, Question):
            question_obj = question_obj.get_id()
        elif not isinstance(question_obj, int):
            raise TypeError("Invalid object type for set_question_id: expected int or Question")
        self.question_id = question_obj

    def set_choice(self, choice):
        assert isinstance(choice, str)
        self.choice = choice


class Response(Base):
    __tablename__ = 'responses'
    id = Column(Integer, primary_key=True)
    response_text = Column(Unicode(40))
    responder_id = Column(Integer)
    question_id = Column(Integer)
    choice_ids = Column(MutableList.as_mutable(PickleType))

    def __init__(self, responder_id, question_id, response_text=None, choice_ids=[]):
        assert isinstance(responder_id, int)
        assert isinstance(question_id, int)
        assert isinstance(choice_ids, list)
        assert isinstance(response_text, str) or response_text is None
        for choice_id in choice_ids:
            assert isinstance(choice_id, int)

        self.id = None
        self.response_text = response_text
        self.responder_id = responder_id
        self.question_id = question_id
        self.choice_ids = choice_ids

    def __str__(self):
        return '{\n' + \
               '    id: {},\n'.format(self.id) + \
               '    responder_id: {},\n'.format(self.responder_id) + \
               '    question_id: {},\n'.format(self.question_id) + \
               '    response_text: {},\n'.format(self.response_text) + \
               '    choice_ids: {},\n'.format(self.choice_ids) + \
               '}'

    def get_id(self):
        return self.id

    def get_responder_id(self):
        return self.responder_id

    def get_question_id(self):
        return self.question_id

    def get_response_text(self):
        return self.response_text

    def get_choice_ids(self):
        return self.choice_ids

    def set_response_text(self, response_text):
        assert isinstance(response_text, str)
        self.response_text = response_text

    def add_choice_id(self, choice_obj):
        if isinstance(choice_obj, Choice):
            choice_obj = choice_obj.get_id()
        elif not isinstance(choice_obj, int):
            raise TypeError("Invalid object type for add_choice_id: expected int or Choice")

        if choice_obj not in self.choice_ids:
            self.choice_ids.append(choice_obj)

    def remove_choice_id(self, choice_obj):
        if isinstance(choice_obj, Choice):
            choice_obj = choice_obj.get_id()
        elif not isinstance(choice_obj, int):
            raise TypeError("Invalid object type for remove_choice_id: expected int or Choice")

        if choice_obj in self.choice_ids:
            self.choice_ids.remove(choice_obj)


class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer)
    question = Column(Unicode(40))
    question_type = Column(Unicode(40))
    survey_id = Column(Integer)
    allowed_choice_ids = Column(MutableList.as_mutable(PickleType))
    response_ids = Column(MutableList.as_mutable(PickleType))

    def __init__(self, owner_id, question, question_type, survey_id=None, allowed_choice_ids=[]):
        assert isinstance(owner_id, int)
        assert isinstance(question, str)
        assert isinstance(question_type, str)
        assert isinstance(survey_id, int) or survey_id is None
        assert isinstance(allowed_choice_ids, list)
        for choice_id in allowed_choice_ids:
            assert isinstance(choice_id, int)

        self.id = None
        self.owner_id = owner_id
        self.question = question
        self.question_type = question_type
        self.survey_id = survey_id
        self.allowed_choice_ids = allowed_choice_ids
        self.response_ids = []

    def __str__(self):
        return '{\n' + \
               '    id: {},\n'.format(self.id) + \
               '    owner_id: {}\n'.format(self.owner_id) + \
               '    question: {},\n'.format(self.question) + \
               '    question_type: {},\n'.format(self.question_type) + \
               '    survey_id: {},\n'.format(self.survey_id) + \
               '    allowed_choice_ids: {},\n'.format(self.allowed_choice_ids) + \
               '    response_ids: {},\n'.format(self.response_ids) + \
               '}'

    def get_id(self):
        return self.id

    def get_owner_id(self):
        return self.owner_id

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

    def set_owner_id(self, owner_id):
        assert isinstance(owner_id, int)
        self.owner_id = owner_id

    def set_survey_id(self, survey_obj):
        if isinstance(survey_obj, Survey):
            survey_obj = survey_obj.get_id()
        elif not isinstance(survey_obj, int):
            raise TypeError("Invalid object type for set_survey_id: expected int or Survey")

        self.survey_id = survey_obj

    def set_question(self, question):
        assert isinstance(question, str)
        self.question = question

    def set_question_type(self, question_type):
        assert isinstance(question_type, str)
        self.question_type = question_type

    def add_allowed_choice_id(self, choice_obj):
        if isinstance(choice_obj, Choice):
            choice_obj = choice_obj.get_id()
        elif not isinstance(choice_obj, int):
            raise TypeError("Invalid object type for add_allowed_choice_id: expected int or Choice")

        if choice_obj not in self.allowed_choice_ids:
            self.allowed_choice_ids.append(choice_obj)

    def remove_allowed_choice_id(self, choice_obj):
        if isinstance(choice_obj, Choice):
            choice_obj = choice_obj.get_id()
        elif not isinstance(choice_obj, int):
            raise TypeError("Invalid object type for remove_allowed_choice_id: expected int or Choice")

        if choice_obj in self.allowed_choice_ids:
            self.allowed_choice_ids.remove(choice_obj)

    def add_response_id(self, response_obj):
        if isinstance(response_obj, Response):
            response_obj = response_obj.get_id()
        elif not isinstance(response_obj, int):
            raise TypeError("Invalid object type for add_response_id: expected int or Response")

        if response_obj not in self.response_ids:
            self.response_ids.append(response_obj)

    def remove_response_id(self, response_obj):
        if isinstance(response_obj, Response):
            response_obj = response_obj.get_id()
        elif not isinstance(response_obj, int):
            raise TypeError("Invalid object type for remove_response_id: expected int or Response")

        if response_obj in self.response_ids:
            self.response_ids.remove(response_obj)


class Survey(Base):
    __tablename__ = 'surveys'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer)
    name = Column(Unicode(40))
    event_id = Column(Integer)
    question_ids = Column(MutableList.as_mutable(PickleType))

    def __init__(self, name, owner_id, question_ids=[], event_id=None):
        assert isinstance(name, str)
        assert isinstance(owner_id, int)
        assert isinstance(question_ids, list)
        for question_id in question_ids:
            assert isinstance(question_id, int)
        assert isinstance(event_id, int) or event_id is None

        self.id = None
        self.name = name
        self.owner_id = owner_id
        self.event_id = event_id
        self.question_ids = question_ids

    def __str__(self):
        return '{\n' + \
               '    id: {},\n'.format(self.id) + \
               '    name: {},\n'.format(self.name) + \
               '    owner_id: {},\n'.format(self.owner_id) + \
               '    event_id: {},\n'.format(self.event_id) + \
               '    question_ids: {},\n'.format(self.question_ids) + \
               '}'

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_owner_id(self):
        return self.owner_id

    def get_question_ids(self):
        return self.question_ids

    def get_event_id(self):
        return self.event_id

    def set_name(self, name):
        assert isinstance(name, str)
        self.name = name

    def set_owner_id(self, owner_id):
        assert isinstance(owner_id, int)
        self.owner_id = owner_id

    def add_question_id(self, question_obj):
        if isinstance(question_obj, Question):
            question_obj = question_obj.get_id()
        elif not isinstance(question_obj, int):
            raise TypeError("Invalid object type for add_question_id: expected int or Question")

        if question_obj not in self.question_ids:
            self.question_ids.append(question_obj)

    def remove_question_id(self, question_obj):
        if isinstance(question_obj, Question):
            question_obj = question_obj.get_id()
        elif not isinstance(question_obj, int):
            raise TypeError("Invalid object type for remove_question_id: expected int or Question")

        if question_obj in self.question_ids:
            self.question_ids.remove(question_obj)

    def set_event_id(self, event_obj):
        if isinstance(event_obj, Event):
            event_obj = event_obj.get_id()
        elif not isinstance(event_obj, int):
            raise TypeError("Invalid object type for set_event_id: expected int or Event")

        self.event_id = event_obj
