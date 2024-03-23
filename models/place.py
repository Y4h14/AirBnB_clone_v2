#!/usr/bin/python3
""" Place Module for HBNB project """
import os
import models
from models.review import Review
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy import Table
from sqlalchemy.orm import relationship

place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', ForeignKey('amenities.id'),
                             primary_key=True, nullable=False))


class Place (BaseModel, Base):
    __tablename__ = 'places'
    """ A place to stay """
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    reviews = relationship('Review', backref='place', cascade='delete')
    amenities = relationship('Amenity', secondary=place_amenity,
                             viewonly=False, back_populates="place_amenities")
    amenity_ids = []

    if os.getenv("HBNB_TYPE_STORAGE", None) != 'db':
        @property
        def reviews(self):
            """reviews getter"""
            review_list = []
            for review in list(models.storage.all(Review).values()):
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            """amenities getter"""
            return self.amenity_ids

        @amenities.setter
        def amenities(self, obj=None):
            """amenities setter"""
            if type(obj) is models.Amenity and obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)
