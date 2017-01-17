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

For convenience, the PorgWrapper class implements common functionality (registering users, creating events etc.). If you are only using the PorgWrapper implemented methods you do not need to import DbInterface.

Using PorgWrapper to register a user with username "Bob": 

```python
from PorgWrapper import PorgWrapper
p = PorgWrapper()
p.register_user("Bob")
```
    
If you would like more fine-grained control over the classes/methods you may bypass PorgWrapper and use the classes within Poorganiser.py directly. The following code snippet is almost functionally equivalent to the above code, with the previous code also performing duplicate checking. 

```python
from Poorganiser import User
from DbInterface import DbInterface
d = DbInterface()
u = User("Bob")
d.add(u)
```

Database insertion is performed by the generic add() method of DbInterface. The above code snippet is an example of this. 

DbInterface provides the get_obj() and query() methods to get an object within the database.

```python
d = DbInterface()
u = d.get_obj(3, User)  # d.get_obj(obj_id, obj_type)
u = d.query(User, User.username == "Bob", num="all")  # d.query(obj_type, filter, num)
```

To update an object in the database, simply modify it as you wish, then call DbInterface.update() on it to commit the changes.

```python
u.set_username("Dave")
d.update(u)
```

Database deletion is performed via the delete() method. 

```python
d.delete(u)
```

# Todo
* Update unit tests for latest version
* Finish Discord interface
* Redesign class file structure
* Implement web interface
