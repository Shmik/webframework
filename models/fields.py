from psycopg2 import sql

class Field():
    db_field = True

class CharField(Field):
    udt_name='varchar'
    create_sql = sql.SQL('VARCHAR')
    def __init__(self, max_length, default=None):
        self.max_length = max_length
        self.default = None


class TextField(Field):
    udt_name='text'
    create_sql = sql.SQL('TEXT')
    def __init__(self, default=None):
        self.max_length = None
        self.default = None

class DateTimeField(Field):
    udt_name='timestamp'
    create_sql = sql.SQL('TIMESTAMP')
    def __init__(self, default=None):
        self.default = None


class PrimaryKeyField(Field):
    defaut=None
    udt_name='int4'
    create_sql = sql.SQL('serial PRIMARY KEY')

