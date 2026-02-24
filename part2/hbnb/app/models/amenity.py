import uuid
from datetime import datetime

class amenity:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """
        Update the attribute update_at.
        """
        self.updated_at = datetime.now()

    def update(self, data):
        """
        Use if the user want to update info about something that belongs to him
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save
