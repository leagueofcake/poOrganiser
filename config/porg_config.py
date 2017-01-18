env = 'test'
if env == 'test':
    DB_NAME = 'porg_test.db'
elif env == 'prod':
    DB_NAME = 'porg.db'
else:
    DB_NAME = None

DB_URL = 'sqlite:///' + DB_NAME

# Survey config
ALLOWED_QUESTION_TYPES = ['free']
