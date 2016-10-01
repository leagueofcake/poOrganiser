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
            options[option] = 0

    def get_text(self):
        return self.question_text

    def set_text(self, text):
        self.question_text = text
