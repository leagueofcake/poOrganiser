# poOrganiser
Event organisation framework written in Python. Winning project of the 2016 UNSW CSESoc Hackathon!

# Dependencies
* Python 3.5+
* [SQLAlchemy](http://www.sqlalchemy.org/)
* [Discord.py](https://github.com/Rapptz/discord.py) (optional, for Discord interface)

# Setup
Install dependencies: 

    make init
    or
    pip install -r requirements.txt
 
Run tests: 

    make tests

# Usage
Poorganiser.py defines classes for Event, User, Attendance etc, while database interfacing (query/update/delete) is handled by the DbInterface class. 

For convenience, the PorgWrapper class implements common functionality (registering users, creating events etc.)

Using PorgWrapper to register a user with username "Bob": 

```python
from PorgWrapper import PorgWrapper
p = PorgWrapper()
p.register_user("Bob")
```
    
If you would like to implement your own versions of the classes/methods you may bypass PorgWrapper and use the classes within Poorganiser.py directly. The following code snippet is functionally equivalent to the above code. 

```python
from Poorganiser import User
from DbInterface import DbInterface
d = DbInterface()
u = User("Bob")
d.add(u)
```

# Todo
* Update unit tests for latest version
* Finish Discord interface
* Redesign class file structure
* Implement web interface
