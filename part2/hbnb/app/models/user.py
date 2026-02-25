import uuid
from datetime import datetime
from .basemodel import BaseModel
import re

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
        Check if the user name is a string, non empty and less than 50 char
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
        Check if the user last name is a string, non empty and less than 50 chars
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

    @property
    def Email(self):
        return self.email
    
    @Email.setter
    def Email(self, value):
        """
        Check if the email is a string, non empty and in the good format. !!!!!! Need to check if it's already used !!!!!!
        """
        regex = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}"
        if not isinstance(value, str):
            raise TypeError ("Email must be a string")
        if value == "":
            raise ValueError ("Email is required")
        if  not re.fullmatch(regex, value):
            raise ValueError("Email must be in format: myemail@address.com")
        self.email = value

    def add_place(self, place):
        """
        Adds a place
        """
        self.places.append(place)