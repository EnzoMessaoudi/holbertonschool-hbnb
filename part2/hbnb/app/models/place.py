import uuid
from datetime import datetime
from .basemodel import BaseModel

class Place(BaseModel):
    def __init__(self, title, price, latitude, longitude, owner, description=None,):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []

        @property
        def Title(self):
            """
            Check if the user gave a good title
            """
            return self._title
        
        @Title.setter
        def Title(self, value):
            if value == "":
                raise ValueError ("Title is required")
            if len(value) > 100:
                raise ValueError ("Title must be under 100 Characters")
            if not isinstance(value, str):
                raise TypeError ("Title must be a string")
            self._title = value
            
        @property
        def price(self):
            """
            Check if the user price is good
            """
            return self._price
        
        @price.setter
        def price(self, value):
            if value < 0:
                raise ValueError ("Price must be positive")
            if not isinstance(value, float):
                raise TypeError ("Price must be a float")
            
        @property
        def latitude(self):
            """
            Check if the user latitude is good
            """
            return self._latitude
        
        @latitude.setter
        def latitude(self, value):
            if not isinstance(value, float):
                raise TypeError ("Latitude must be a Float")
            if not -90.0 <= value >= 90.0:
                raise ValueError ("Latitude must be between -90.0 and 90.0")
            self._latitude = value
            
        @property
        def longitude(self):
            """
            Check if the user longitude is good
            """
            return self._longitude
        
        @longitude.setter
        def longitude(self, value):
            if not isinstance(value, float):
                raise TypeError ("Longitude must be a Float")
            if not -180.0 <= value >= 180.0:
                raise ValueError ("longitude must be between -180.0 and 180.0")
            self._longitude = value

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)
    
    def list_reviews(self):
        """Used to list the reviews of a place"""
        print(self.reviews)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def list_amenity(self):
        """Used to list the amenities of a place"""
        print(self.amenities)