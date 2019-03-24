DNS = 'dbname=dbname user=myuser password=mypassword'

INSTALLED_MODELS = [
    'person.Person',
]

try:
    from .local_settings import *
except ImportError:
    pass
