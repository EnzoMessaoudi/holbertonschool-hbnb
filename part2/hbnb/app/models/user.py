import uuid
from datetime import datetime
from .basemodel import BaseModel
import re


class User(BaseModel):
    def __init__(self,
                 first_name,
                 last_name,
                 email,
                 is_admin=False,
                 places=None
                 ):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.places = []
        self.reviews = []

    @property
    def first_name(self):
        """
        Check if the user name is a string, non empty and less than 50 char
        """
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError("First Name must be a string")

        if value == "":
            raise ValueError("First Name requiered")

        if len(value) > 50:
            raise ValueError("Line over 50 characters")
        self._first_name = value

    @property
    def last_name(self):
        """
        Check if the user last name is nom-empty string and less than 50 chars
        """
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not isinstance(value, str):
            raise TypeError("Last Name must be a string")

        if value == "":
            raise ValueError("Last Name requiered")

        if len(value) > 50:
            raise ValueError("Line over 50 characters")
        self._last_name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        """
        Check if the email is a string, non empty and in the good format.
        """
        regex = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}"

        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        if value == "":
            raise ValueError("Email is required")
        if not re.fullmatch(regex, value):
            raise ValueError("Email must be in format: myemail@address.com")
        self._email = value

    def add_place(self, place):
        """
        Adds a place
        """
        self.places.append(place)
