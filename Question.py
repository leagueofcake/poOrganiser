class Question():
    def __init__(self, text, users, choices=1, pref=False):
        self.question_text = text
        self.choices = choices
        self.preferential = pref
        self.yet_to_vote = users
        self.options = {}

    def get_options(self): #return options as text
        options_text = []
        for key in self.options:
            options_text.append(key)
        return self.options

    def add_option(self, option):
        if option not in self.options:
            self.options[option] = []

    def remove_option(self, option):
        if option in self.options:
            del(self.options[option])

    def get_text(self):
        return self.question_text

    def set_text(self, text):
        self.question_text = text

    def make_vote(self, user, option):
        self.options[option].append(user)
#print(self.options) #debug

    def get_result(self):
        for key in sorted(self.options, key=lambda k: len(self.options[k]), reverse = True): #sorted(self.options, key = len, reverse=False): #DEBUG PRINTING
            print (key, self.options[key], len(self.options[key]))
        ## FIX UP RETURN

    def has_voted(self, user):
        self.yet_to_vote.remove(user)
        if len(self.yet_to_vote) == 0: #everyone has voted
            self.get_result() #get the result



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


# run_tests()

q = Question("Please answer", ["Dom", "Dennis", "Jeremy"], 1, False)
q.add_option("A")
q.add_option("B")
q.add_option("C")
q.make_vote("Dom", "C")
q.has_voted("Dom")
q.make_vote("Jeremy", "B")
q.has_voted("Jeremy")
q.make_vote("Dennis", "B")
q.has_voted("Dennis")
