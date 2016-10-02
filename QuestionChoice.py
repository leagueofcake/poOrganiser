#!/usr/bin/env python3.5
import ast
from sqlalchemy import Column, Integer, Unicode, UnicodeText, String, Date
from create_base import Base

class QuestionChoice(Base):
    __tablename__ = 'choices'
    choiceid = Column(Integer, primary_key=True)
    questionid = Column(Integer)
    choicetext = Column(Unicode(100))
    votes = Column(Unicode(100))

    def __init__(self, questionid, choicetext, votes=[]):
        self.choiceid = None
        self.questionid = questionid
        self.choicetext = choicetext
        self.votes = votes

    def get_id(self):
        return self.choiceid

    def get_questionid(self):
        return self.questionid

    def get_choicetext(self):
        return self.choicetext

    def get_votes(self):
        return self.votes

    def set_choicetext(self, choicetext):
        self.choicetext = choicetext

    def add_vote(self, user):
        self.votes = ast.literal_eval(str(self.votes)) # Convert to list before appending
        if user in self.votes:
            return None
        self.votes.append(user)
        return True

    def remove_vote(self, user):
        self.votes = ast.literal_eval(str(self.votes)) # Convert to list before appending
        if user in self.votes:
            self.votes.remove(user)
        else:
            return None
