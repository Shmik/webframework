from models.fields import Field, PrimaryKeyField

class Model():
    id = PrimaryKeyField()
    @classmethod
    def get_name(cls):
        return cls.__name__.lower()

    @classmethod
    def get_table(cls):
        return cls.get_name()

    @classmethod
    def get_fields(cls):
        fields_dict = {}
        for field_name in dir(cls):
            field = getattr(cls, field_name)
            if getattr(field, 'db_field', None):
                fields_dict[field_name] = field
        return fields_dict


