from .record import MetaModel


class Table(metaclass=MetaModel):
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
        return f"<table\ncolumns = [\n{fields_str}\n]\ndata = [\n    {data_str}\n]\n/>"
