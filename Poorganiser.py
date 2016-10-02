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
    def __init__(self):
        self._engine = create_engine(porg_config.DB_URL)
        self.s = sessionmaker(bind=self._engine)()

    def update(self, obj):
        if isinstance(obj, EventUser): # Need to convert list to string before storing in db
            obj.roles = str(obj.roles)
        self.s.commit()
        return obj

    # User
    def add_user(self, username):
        u = User(username)
        self.s.add(u)
        self.s.commit()
        return u

     # Returns None if username not found
    def get_user(self, username):
        return self.s.query(User).filter(User.username == username).first()

    def remove_user(self, username):
        u = self.get_user(username)
        self.s.query(User).filter(User.username == username).delete()
        if u != None:
            self.s.commit()
            return True # Deleted
        else: # User not found
            return None

    # Event
    def add_event(self, ownerid, name, location, year=None, month=None, day=None):
        date = None
        if year and month and day:
            date = datetime.date(year, month, day)
        e = Event(ownerid, name, location, date)
        self.s.add(e)
        self.s.commit()
        return e

    def get_event(self, eventid):
        return self.s.query(Event).get(eventid)

    def remove_event(self, eventid):
        e = self.get_event(eventid)
        self.s.query(Event).filter(Event.id == eventid).delete()
        if e != None:
            self.s.commit()
            return True # deleted
        return None

    def get_events(self):
        return self.s.query(Event).all()

    def get_curr_events(self):
        today = datetime.date.today()
        return self.s.query(Event).filter(Event.time > today).all()

    def get_events_by_user(self, userid):
        res = []
        eventids = self.s.query(EventUser).with_entities(EventUser.eventid).filter(EventUser.userid == userid).all()
        for eventid in eventids:
            print(eventid[0])
            res.append(self.get_event(eventid[0]))
        return res

    # EventUser
    def add_eventuser(self, eventid, userid, isgoing):
        eu = EventUser(eventid, userid, isgoing)
        eu.roles = str(eu.roles) # Convert to string
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
        if eu != None:
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
        if q != None:
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
        choices = self.get_questionchoice(questionid)
        ans = None
        count = 0

        for choice in choices:
            if len(choice.get_votes()) > count:
                ans = choice
                count = len(choice.get_votes())

        return ans
