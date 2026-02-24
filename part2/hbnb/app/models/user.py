import uuid
from datetime import datetime
from basemodel import BaseModel

class user(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin, places, reviews):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.places = []
        self.reviews = []

    def add_place(self, place):
        """
        Adds a place
        """
        self.places.append(place)