class User():
    def __init__(self, name):
        self.name = name
        self.going = False
        self.responsibilities = []

    def get_name(self):
        return self.name
