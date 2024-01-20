class Field:
    def __init__(self, display_name, options=None):
        self.display_name = display_name
        self.name = None  # Name will be set by the metaclass
        self.value = None

    def __get__(self, instance, owner):
        return self.value

    def to_string(self):
        return f"{{\n    displayName: '{self.display_name}',\n    name: '{self.name}',\n    type: 'string',\n}}"


class StringField(Field):
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise ValueError("Value must be a string")
        self.value = value

    def to_string(self):
        return f"{{\n    displayName: '{self.display_name}',\n    name: '{self.name}',\n    type: 'string',\n}}"


class NumberField(Field):
    def __set__(self, instance, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Value must be an integer or a float")
        self.value = value

    def to_string(self):
        return f"{{\n    displayName: '{self.display_name}',\n    name: '{self.name}',\n    type: 'number',\n}}"


class BooleanField(Field):
    def __set__(self, instance, value):
        if not isinstance(value, bool):
            raise ValueError("Value must be a boolean")
        self.value = value

    def to_string(self):
        return f"{{\n    displayName: '{self.display_name}',\n    name: '{self.name}',\n    type: 'boolean',\n}}"


class DateField(Field):
    def __set__(self, instance, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Value must be a timestamp in milliseconds")
        self.value = value

    def to_string(self):
        return f"{{\n    displayName: '{self.display_name}',\n    name: '{self.name}',\n    type: 'date',\n}}"


class OptionsField(Field):
    def __init__(self, display_name, options=None):
        super().__init__(display_name)
        self.options = options

    def __set__(self, instance, value):
        if not isinstance(value, list):
            raise ValueError("Value must be a list")
        self.value = value

    def to_table_meta(self):
        if self.options is None:
            return self.to_string()
        return f"{{\n    displayName: '{self.display_name}',\n    name: '{self.name}',\n    type: 'options',\n    " \
               f"options: {self.options}\n}}"

    def to_string(self):
        return f"{{\n    displayName: '{self.display_name}',\n    name: '{self.name}',\n    type: 'options',\n}}"
