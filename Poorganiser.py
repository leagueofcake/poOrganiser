#!/usr/bin/env python3.5
import datetime
from config import porg_config
from sqlalchemy import create_engine
from Event import Event
from User import User
from EventUser import EventUser
from Question import Question
from QuestionChoice import QuestionChoice
from sqlalchemy.orm import sessionmaker


class Poorganiser():
    """Main class for handling object representation and database interfacing."""
    def __init__(self):
        self._engine = create_engine(porg_config.DB_URL)
        self.s = sessionmaker(bind=self._engine)()

    def update(self, obj):
        """Commits any database changes performed by an interface module and performs any pre-commit processing
        (such as list object to string conversion).

        Args:
            obj (object): The object being updated.

        Returns:
            obj."""
        if isinstance(obj, EventUser):  # Need to convert list to string before storing in db
            obj.roles = str(obj.roles)
        self.s.commit()
        return obj

    # User
    def add_user(self, username):
        """Adds a user with a given username to the database.

        Args:
            username (str): Username for a user. Assumed to be unique.

        Returns:
             A User object with the specified username."""
        u = User(username)
        self.s.add(u)
        self.s.commit()
        return u

    def get_user(self, username):
        """Queries the database for a user with the given username.

        Args:
            username (str): Username to be searched for.

        Returns:
            A User object for the query results if the username is found in the database, otherwise None. """
        return self.s.query(User).filter(User.username == username).first()

    def remove_user(self, username):
        """Removes any users with the given username.

        Args:
            username (str): Username of the user to be deleted.

        Returns:
             True if a user was found, otherwise None."""
        u = self.get_user(username)
        self.s.query(User).filter(User.username == username).delete()
        if u is not None:
            self.s.commit()
            return True  # Deleted
        return None  # User not found

    # Event
    def add_event(self, ownerid, name, location, year=None, month=None, day=None):
        """Adds an event to the database. If the year, month and date parameters are specified, the Event is given
        that date.

        Args:
            ownerid  (int): ID corresponding to the user that created the event.
            name     (str): Name of the event.
            location (str): Location for the event.
            year     (int, optional): Year for the event. Defaults to None.
            month    (int, optional): Month for the event. Defaults to None.
            day      (int, optional): Day for the event. Defaults to None.

        Returns:
            An Event object with the specified parameters."""
        date = None
        if year and month and day:
            date = datetime.date(year, month, day)
        e = Event(ownerid, name, location, date)
        self.s.add(e)
        self.s.commit()
        return e

    def get_event(self, eventid):
        """Queries the database for an event with the given event ID.

        Args:
            eventid (int): Event ID for the event to be searched for.

        Returns:
            An Event object for the query results if the event is found in the database, otherwise None. """
        return self.s.query(Event).get(eventid)

    def remove_event(self, eventid):
        """Removes an event with the given event ID.

        Args:
            eventid (int): Event ID for the event to be deleted.

        Returns:
             True if the event was found, otherwise None."""
        e = self.get_event(eventid)
        self.s.query(Event).filter(Event.id == eventid).delete()
        if e is not None:
            self.s.commit()
            return True  # deleted
        return None  # Event ID not found

    def get_events(self):
        """Queries the database for all events.

        Returns:
             A list of all Event objects found."""
        return self.s.query(Event).all()

    def get_curr_events(self):
        """Queries the database for all events with date newer than today's date.

        Returns:
             A list of all Event objects found."""
        today = datetime.date.today()
        return self.s.query(Event).filter(Event.time > today).all()

    def get_events_by_user(self, userid):
        res = []
        eventids = self.s.query(EventUser).with_entities(EventUser.eventid).filter(EventUser.userid == userid).all()
        for eventid in eventids:
            res.append(self.get_event(eventid[0]))
        return res

    # EventUser
    def add_eventuser(self, eventid, userid, isgoing):
        eu = EventUser(eventid, userid, isgoing)
        eu.roles = str(eu.roles)  # Convert to string
        self.s.add(eu)
        self.s.commit()
        return eu

    def get_eventuser(self, eventid, userid):
        return self.s.query(EventUser).filter(EventUser.eventid == eventid).filter(EventUser.userid == userid).first()

    def get_eventusers(self, eventid):
        return self.s.query(EventUser).filter(EventUser.eventid == eventid).all()

    def remove_eventuser(self, eventid, userid):
        eu = self.get_eventuser(eventid, userid)
        self.s.query(EventUser).filter(EventUser.eventid == eventid).filter(EventUser.userid == userid).delete()
        if eu is not None:
            self.s.commit()
            return True # Deleted
        return None

    # Question
    def get_question(self, questionid):
        return self.s.query(Question).get(questionid)

    def get_questions(self, eventid):
        return self.s.query(Question).filter(Question.eventid == eventid).all()

    def add_question(self, eventid, text, yettovote, choices=1, pref=False):
        q = Question(eventid, text, yettovote, choices, pref)
        q.yettovote = str(q.yettovote)
        self.s.add(q)
        self.s.commit()
        return q

    def remove_question(self, questionid):
        q = self.get_question(questionid)
        self.s.query(Question).filter(Question.questionid == questionid).delete()
        if q is not None:
            self.s.commit()
            return True
        return None

    # QuestionChoice
    def add_questionchoice(self, questionid, choicetext, votes=[]):
        qc = QuestionChoice(questionid, choicetext, votes)
        qc.votes = str(qc.votes)
        self.s.add(qc)
        self.s.commit()
        return qc

    def get_questionchoice(self, choiceid):
        return self.s.query(QuestionChoice).filter(QuestionChoice.choiceid == choiceid).first()

    def get_questionchoices(self, questionid):
        return self.s.query(QuestionChoice).filter(QuestionChoice.questionid == questionid).all()

    def vote(self, userid, choiceid): # Add vote for user
        qc = self.get_questionchoice(choiceid)
        successful = qc.add_vote(userid)
        qc.votes = str(qc.votes)
        if successful:
            self.s.commit()
        return successful

    def get_result(self, questionid):
        choices = self.get_questionchoices(questionid)
        ans = None
        count = 0

        for choice in choices:
            if len(choice.get_votes()) > count:
                ans = choice
                count = len(choice.get_votes())

        return ans
