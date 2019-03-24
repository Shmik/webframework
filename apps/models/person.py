from models import Model
from models.fields import CharField

class Person(Model):
    first_name = CharField(max_length=55)
    last_name = CharField(max_length=55)

