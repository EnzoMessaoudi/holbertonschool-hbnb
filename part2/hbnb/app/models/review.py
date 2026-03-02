import uuid
from datetime import datetime
from .basemodel import BaseModel


class Review(BaseModel):
    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        """
        Check if the text is a string and non empty
        """
        if not isinstance(value, str):
            raise TypeError("Text must be a string")
        if value == "":
            raise ValueError("Text is required")
        self._text = value

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        """
        Check if the rating is an int between 1 or 5
        """
        if not isinstance(value, int):
            raise TypeError("Rating must an integer")
        if not 1 <= value <= 5:
            raise ValueError("Rating must be an integer bewteen 1 and 5")
        self._rating = value

    def to_dict(self):
        data = super().to_dict()  # récupère id, created_at, updated_at
        data.update({
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place_id,
            "user_id": self.user_id
        })
        return data
