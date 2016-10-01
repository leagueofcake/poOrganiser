class Event():
    def __init__(self, name, location, time):
        self.name = name
        self.location = location
        self.time = time

    def get_name(self):
        return self.name

    def get_location(self):
        return self.location
        
    def get_time(self):
        return self.time

    def set_name(self, name):
        self.name = name

    def set_location(self, location):
        self.location = location

    def set_time(self, time):
        self.time = time

# UNIT TESTS        
def run_tests():
    test_get_name()
    test_set_name()
    test_get_location()
    test_set_location()
    test_get_time()
    test_set_time()
    print("All tests passed!")

def test_get_name():
    e1 = Event("BBQ", "Parra Park", "01/10/2016")
    assert(e1.get_name() == "BBQ")
    e1 = Event("", "house", "01/10/2016")
    assert(e1.get_name() == "")
    
def test_set_name():
    e1 = Event("BBQ", "Parra Park", "01/10/2016")
    e1.set_name("name is wrong")
    assert(e1.get_name() == "name is wrong")
    e1.set_name("")
    assert(e1.get_name() == "")
    
def test_get_location():
    e1 = Event("BBQ", "Parra Park", "01/10/2016")
    assert(e1.get_location() == "Parra Park")
    e1 = Event("BBQ", "", "01/10/2016")
    assert(e1.get_location() == "")
    
def test_set_location():
    e1 = Event("BBQ", "Parra Park", "01/10/2016")
    e1.set_location("Parramatta Park")
    assert(e1.get_location() == "Parramatta Park")
    e1.set_location("")
    assert(e1.get_location() == "")
    
def test_get_time():
    e1 = Event("BBQ", "Parra Park", "01/10/2016")
    assert(e1.get_time() == "01/10/2016")
    e1 = Event("BBQ", "Parra Park", "")
    assert(e1.get_time() == "")
    
def test_set_time():
    e1 = Event("BBQ", "Parra Park", "01/10/2016")
    e1.set_time("02/10/2016")
    assert(e1.get_time() == "02/10/2016")
    e1.set_time("")
    assert(e1.get_time() == "")
    
run_tests()
