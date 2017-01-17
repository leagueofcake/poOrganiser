env = 'test'
if env == 'test':
    DB_NAME = 'porg_test.db'
elif env == 'prod':
    DB_NAME = 'porg.db'

DB_URL = 'sqlite:///' + DB_NAME
