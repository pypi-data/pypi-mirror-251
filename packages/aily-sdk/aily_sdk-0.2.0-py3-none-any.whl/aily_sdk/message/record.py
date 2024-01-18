# my_package/message/record.py

from .fields import Field, StringField


class MetaModel(type):
    def __new__(mcs, name, bases, namespace):
        fields = {}
        for key, value in namespace.items():
            if isinstance(value, Field):
                value.name = key  # Set the name of the field based on the attribute name
                fields[key] = value
        namespace['_fields'] = fields
        return super().__new__(mcs, name, bases, namespace)


class Record(metaclass=MetaModel):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key in self._fields:
                setattr(self, key, value)
            else:
                raise ValueError(f"Field {key} does not exist in {type(self).__name__}")

    def __str__(self):
        return self.to_string()

    def to_string(self):
        fields_str = ', '.join(field.to_string() for field in self._fields.values())
        data_str = ',\n    '.join(f"{name}: {repr(getattr(self, name))}" for name in self._fields)
        return f"<record\nfields = [\n{fields_str}\n]\ndata = {{\n    {data_str}\n}}\n/>"
