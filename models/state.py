#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from os import getenv
from sqlalchemy.orm import relationship
import models


class State(BaseModel, Base):
    """State class definition
    Attributes:
    __tablename__: The name of the class State
    name: The nameof the states
    cities: The relationship of the states
    """
    __tablename__ = 'states'

    if getenv('HBNB_TYPE_STORAGE'):
        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='state',
                              cascade='all, delete-orphan')
    else:
        name = ''

        @property
        def cities(self):
            """Returns the list of `City` instances
            with `state_id` equals to the current
            """

            cities = list()

            for _id, city in models.storage.all(City).items():
                if city.state_id == self.id:
                    cities.append(city)

            return cities

    """ State class """
    name = ""
