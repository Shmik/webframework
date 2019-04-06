from models.fields import Field, PrimaryKeyField

class Model():
    id = PrimaryKeyField()

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls, *args, **kwargs)
        for name, field_class in cls.get_fields().items():
            setattr(obj, name, getattr(field_class, 'default', None))
        return obj

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


