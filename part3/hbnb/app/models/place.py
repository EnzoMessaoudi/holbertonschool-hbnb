import uuid
from datetime import datetime
from app.extensions import db
from sqlalchemy.orm import validates
from .basemodel import BaseModel


class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    owner_id = db.Column(db.Integer)
    owner = None

    amenities = db.Column(db.String)
    reviews = db.Column(db.String)

    @validates("title")
    def validate_title(self, key, value):
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        self._title = value
        if value == "":
            raise ValueError("Title is required")
        if len(value) > 100:
            raise ValueError("Title must be under 100 Characters")

    @validates("description")
    def validate_description(self, key, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("Description must be a string or None")
        self._description = value or ""

    @validates("price")
    def validate_price(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("Price must be a number")
        value = float(value)
        if value < 0:
            raise ValueError("Price must be positive")
        self._price = value

    @validates("latitude")
    def latitude(self, value):
        if not isinstance(value, float):
            raise TypeError("Latitude must be a Float")
        if not (-90.0 <= value <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0")
        self._latitude = value

    @validates("longitude")
    def longitude(self, value):
        if not isinstance(value, float):
            raise TypeError("Longitude must be a Float")
        if not (-180.0 <= value <= 180.0):
            raise ValueError("longitude must be between -180.0 and 180.0")
        self._longitude = value

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
