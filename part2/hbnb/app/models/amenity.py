import uuid
from datetime import datetime
from .basemodel import BaseModel


class Amenity(BaseModel):
    def __init__(self, name, places=None):
        super().__init__()
        self.name = name
        self.places = []

    @property
    def name(self):
        """
        Check if the name is a non empty string and is less than 50 chars
        """
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if value == "":
            raise ValueError("Name is required")
        if len(value) > 50:
            raise ValueError("Name must be less than 50 character")
        self._name = value
