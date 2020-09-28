from datetime import datetime


class Deadline:
    def __init__(self, name: str, date_time: datetime, notes: str = ""):
        """
        docstring
        """
        self.name = name
        self.until = date_time
        self.notes = notes
