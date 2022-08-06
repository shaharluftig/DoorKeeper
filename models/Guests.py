from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class Guests:
    """Class for keeping track for who is in the door in a given time"""
    names: List[str]
    timestamp: datetime

    def format_message(self):
        return f"{','.join(self.names)} in the door! timestamp: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
