#!/usr/bin/env python3.5
from sqlalchemy import Column, Integer, Unicode, UnicodeText, String, Date
from create_session import Base
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Unicode(40))

    def __init__(self, username):
        self.id = None
        self.username = username

    def get_username(self):
        return self.username

    def get_id(self):
        return self.id

    def set_username(self, username):
        self.username = username
