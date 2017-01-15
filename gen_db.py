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
    owner_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    location TEXT,
    time DATE);
''')

c.execute('''CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL);
''')

c.execute('''CREATE TABLE eventusers(
    event_user_id INTEGER PRIMARY KEY,
    event_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    is_going TEXT NOT NULL,
    roles TEXT);
''')

c.execute('''CREATE TABLE questions(
    question_id INTEGER PRIMARY KEY,
    event_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    num_choices INTEGER NOT NULL,
    preferential BOOLEAN NOT NULL,
    yet_to_vote TEXT);
''')

c.execute('''CREATE TABLE choices(
    choice_id INTEGER PRIMARY KEY,
    question_id INTEGER NOT NULL,
    choice_text text NOT NULL,
    votes TEXT);
''')

conn.commit()
conn.close()
