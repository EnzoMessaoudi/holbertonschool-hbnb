import uuid
from datetime import datetime
from .basemodel import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False, places=None):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.places = []
        self.reviews = []

    @property
    def First_name(self):
        """
        Check if the user name is good
        """
        return self.first_name
    
    @First_name.setter
    def First_name(self, value):
        if not isinstance(value, str):
            raise TypeError ("First Name must be a string")
        
        if value == "":
            raise ValueError ("First Name requiered")

        if len(value) > 50:
            raise ValueError ("Line over 50 characters")
        
        self.first_name = value

    @property
    def Last_name(self):
        """
        Check if the user last name is good
        """
        return self.last_name
    
    @Last_name.setter
    def Last_name(self, value):
        if not isinstance(value, str):
            raise TypeError ("Last Name must be a string")

        if value == "":
            raise ValueError ("Last Name requiered")

        if len(value) > 50:
            raise ValueError ("Line over 50 characters")
        
        self.last_name = value

    def add_place(self, place):
        """
        Adds a place
        """
        self.places.append(place)