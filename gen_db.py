#!/usr/bin/env python3.5
import sqlite3
conn = sqlite3.connect('porg.db')
c = conn.cursor()
try:
    c.execute('DROP TABLE events')
    c.execute('DROP TABLE users')
    c.execute('DROP TABLE eventusers')
    c.execute('DROP TABLE questions')
    c.execute('DROP TABLE choices')
except:
    pass

c.execute('''CREATE TABLE events(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    location TEXT,
    time DATE);
''')

c.execute('''CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL);
''')

c.execute('''CREATE TABLE eventusers(
    eventuserid INTEGER PRIMARY KEY,
    eventid INTEGER NOT NULL,
    userid INTEGER NOT NULL,
    isgoing BOOLEAN NOT NULL,
    roles TEXT);
''')

c.execute('''CREATE TABLE questions(
    quesionid INTEGER PRIMARY KEY,
    text TEXT NOT NULL,
    numchoices INTEGER NOT NULL,
    preferential BOOLEAN NOT NULL,
    yettovote TEXT);
''')

c.execute('''CREATE TABLE choices(
    choice INTEGER PRIMARY KEY,
    questionid INTEGER NOT NULL,
    choicetext text NOT NULL,
    votes TEXT);
''')

conn.commit()
conn.close()
