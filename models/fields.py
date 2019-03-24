class Field():
    db_field = True

class CharField(Field):
    def __init__(self, max_length):
        self.max_length = max_length

class PrimaryKeyField(Field):
    pass

