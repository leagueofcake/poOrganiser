#!/usr/bin/env python3.5
class User():
    def __init__(self, name):
        self.name = name
        self.going = False
        self.roles = []

    def get_name(self):
        return self.name

    def get_going(self):
        return self.going

    def get_roles(self):
        return self.roles

    def debug_print(self):
        print("\tUSER NAME ", self.name)
        print("\tUSER GOING ", self.going)
        print("\tUSER ROLES ", self.roles)

    def set_name(self, name):
        self.name = name

    def set_going(self, going):
        self.going = going

    def add_role(self, role):
        self.roles.append(role)


def run_tests():
    test_get_name()
    test_get_going()
    test_get_roles()
    test_set_name()
    test_set_going()
    test_add_role()
    

def test_get_name():
    u1 = User("") # Empty case
    assert(u1.get_name() == "")

    u1 = User(" ") # Whitespace case
    assert(u1.get_name() == " ")

    u1 = User("Jeremy") # Whitespace case
    assert(u1.get_name() == "Jeremy")

def test_get_going():
    u1 = User("")
    assert(u1.get_going() == False)

    u1 = User("Jeremy")
    assert(u1.get_going() == False)

def test_get_roles():
    u1 = User("")
    assert(u1.get_roles() == [])

    u1 = User("Jeremy")
    assert(u1.get_roles() == [])

def test_set_name():
    u1 = User("test")
    u1.set_name("Dennis")
    assert(u1.get_name() == "Dennis")
    u1.set_name(" ")
    assert(u1.get_name() == " ")
    u1.set_name("")
    assert(u1.get_name() == "")

def test_set_going():
    u1 = User("test")
    u1.set_going(True)
    assert(u1.get_going() == True)
    u1.set_going(False)
    assert(u1.get_going() == False)

def test_add_role():
    u1 = User("test")
    assert(u1.get_roles() == [])
    u1.add_role("Showerwatcher")
    assert(u1.get_roles() == ["Showerwatcher"])
    u1.add_role("CivV")
    assert(u1.get_roles() == ["Showerwatcher", "CivV"])

    
    
run_tests()
