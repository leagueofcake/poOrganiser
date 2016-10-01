#!/usr/bin/env python3.5
from sqlalchemy import Column, Integer, Unicode, UnicodeText, String, Date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///porg.db', echo=False)
Base = declarative_base(bind=engine)

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

# Initialise SQLAlchemy session
Base.metadata.create_all()
Session = sessionmaker(bind=engine)
s = Session()

def add_user(username):
    u = User(username)
    s.add(u)
    s.commit()
    return u

 # Returns None if username not found
def get_user(username):
    return s.query(User).filter(User.username == username).first()

def update_user(obj):
    s.commit()
    return obj

def run_tests():
    test_get_username()
    test_set_username()


def test_get_username():
    u1 = User("") # Empty case
    assert(u1.get_username() == "")

    u1 = User(" ") # Whitespace case
    assert(u1.get_username() == " ")

    u1 = User("Jeremy") # Whitespace case
    assert(u1.get_username() == "Jeremy")

def test_set_username():
    u1 = User("test")
    u1.set_username("Dennis")
    assert(u1.get_username() == "Dennis")
    u1.set_username(" ")
    assert(u1.get_username() == " ")
    u1.set_username("")
    assert(u1.get_username() == "")

run_tests()
