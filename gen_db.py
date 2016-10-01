#!/usr/bin/env python3.5
import sqlite3
conn = sqlite3.connect('porg.db')
c = conn.cursor()
try:
    c.execute('DROP TABLE events')
    c.execute('DROP TABLE users')
    c.execute('DROP TABLE eventusers')
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
    id INTEGER PRIMARY KEY,
    eventid INTEGER NOT NULL,
    userid INTEGER NOT NULL,
    isgoing BOOLEAN NOT NULL,
    role TEXT);
''')

conn.commit()
conn.close()
