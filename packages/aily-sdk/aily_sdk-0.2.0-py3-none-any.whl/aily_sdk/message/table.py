from .record import MetaModel


class Table(metaclass=MetaModel):
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return self.to_string()

    def to_string(self):
        fields_str = ', '.join(
            field.to_table_meta() if hasattr(field, 'to_table_meta') else field.to_string()
            for field in self._fields.values()
        )

        def format_js_object(data):

            def format_js_value(value):
                if isinstance(value, bool):
                    return str(value).lower()
                elif isinstance(value, str):
                    return f"'{value}'"
                else:
                    return str(value)

            formatted_items = []
            for item in data:
                formatted_item = ',\n'.join(f" {key}: {format_js_value(value)}" for key, value in item.items())
                formatted_items.append(f"{{{formatted_item}\n}}")

            return f"{', '.join(formatted_items)}"

        data_str = format_js_object(self.data)
        return f"<table\ncolumns = [\n{fields_str}\n]\ndata = [\n    {data_str}\n] />"
