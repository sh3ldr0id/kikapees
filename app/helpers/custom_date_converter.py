from werkzeug.routing import BaseConverter
from datetime import datetime

class CustomDateConverter(BaseConverter):
    def to_python(self, value):
        try:
            return datetime.strptime(value, '%Y-%m-%d').date()
        
        except ValueError:
            return None

    def to_url(self, value):
        return value.strftime('%Y-%m-%d')