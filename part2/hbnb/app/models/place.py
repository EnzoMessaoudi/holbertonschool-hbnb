import uuid
from datetime import datetime
from .basemodel import BaseModel

class Place(BaseModel):
    def __init__(self, title, price, latitude, longitude, description=None, owner_id = None, amenities=None):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.reviews = []
        self.amenities = []

    @property
    def title(self):
        """
        Check if the title is non empy, a string and less than 100 chars
        """
        return self._title
        
    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise TypeError ("Title must be a string")
        self._title = value
        if value == "":
            raise ValueError ("Title is required")
        if len(value) > 100:
            raise ValueError ("Title must be under 100 Characters")

            
    @property
    def description(self):
        """
        Check if the description is a string
        """
        return self._description
        
    @description.setter
    def description(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("Description must be a string or None")
        self._description = value or ""

    @property
    def price(self):
        """
        Check if the price is positive and a float or an int
        """
        return self._price
        
    @price.setter
    def price(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("Price must be a number")
        value = float(value)
        if value < 0:
            raise ValueError("Price must be positive")
        self._price = value
            
    @property
    def latitude(self):
        """
        Check if the latitude is a float, non empty and exists
        """
        return self._latitude
        
    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, float):
            raise TypeError ("Latitude must be a Float")
        if not (-90.0 <= value <= 90.0):
            raise ValueError ("Latitude must be between -90.0 and 90.0")
        self._latitude = value
            
    @property
    def longitude(self):
        """
        Check if the longitude is a float, non empty and exists
        """
        return self._longitude
        
    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, float):
            raise TypeError ("Longitude must be a Float")
        if not (-180.0 <= value <= 180.0):
            raise ValueError ("longitude must be between -180.0 and 180.0")
        self._longitude = value

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
