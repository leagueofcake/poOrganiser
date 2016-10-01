class Question():
    def __init__(self, text):
        self.question_text = text
        self.options = {}

    def get_options(self):
        options_text = []
        for key in self.options:
            options_text.append(key)
        return self.options

    def add_option(self, option):
        if option not in self.options:
            self.options[option] = 0

    def get_text(self):
        return self.question_text

    def set_text(self, text):
        self.question_text = text

 #tests

def run_tests():
    test_get_text()
    test_set_text()
    test_add_option()
    test_get_options()
    

def test_get_text():
    q1 = Question("") # Empty case
    assert(q1.get_text() == "")

    q1 = Question(" ") # Whitespace case
    assert(q1.get_text() == " ")

    q1 = Question("Do you lickadickaday?") # normal case
    assert(q1.get_text() == "Do you lickadickaday?")


def test_set_text():
    q1 = Question("test")
    q1.set_text("Do you lickadickaday?")
    assert(q1.get_text() == "Do you lickadickaday?")
    q1.set_text(" ")
    assert(q1.get_text() == " ")
    q1.set_text("")
    assert(q1.get_text() == "")

def test_add_option():
    q1 = Question("test")
    assert(q1.get_options() == {})
    q1.add_option("Yes")
    assert(q1.get_options()["Yes"] == 0)
    q1.add_option("No")
    assert(q1.get_options()["No"] == 0)

def test_get_options():
    q1 = Question("")
    assert(q1.get_options() == {})

    q1 = Question("test")
    assert(q1.get_options() == {})
    
    
run_tests()