import uuid
from datetime import datetime
from .basemodel import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value):
        if not isinstance(value, str):
            raise TypeError ("Text must be a string")
        if value == "":
            raise ValueError ("Text is required")
        self._text = value

    @property
    def rating(self):
        return self._rating
    
    @rating.setter
    def rating(self, value):
        if not isinstance(value, int) or not 1 <= value >= 5:
            raise TypeError ("Rating must an integer between 1 and 5")
        self._rating = value