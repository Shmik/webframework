DATABASE_SETTINGS = {
    'user': 'myuser',
    'password': 'mypassword',
    'database_name': 'dbname'
}


try:
    from .local_settings import *
except ImportError:
    pass
