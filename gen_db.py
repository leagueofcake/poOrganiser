#!/usr/bin/env python3.5
import sqlite3
conn = sqlite3.connect('porg.db')
c = conn.cursor()
try:
    c.execute('DROP TABLE events')
except:
    pass

c.execute('''CREATE TABLE events(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    location TEXT,
    time DATE);
''')

conn.commit()
conn.close()
