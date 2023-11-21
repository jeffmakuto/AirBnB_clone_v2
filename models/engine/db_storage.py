#!/usr/bin/python3
"""The DB Storage for our AirBnB project"""
from models.base_model import BaseModel, Base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from os import getenv
from models.city import City
from models.state import State
from sqlalchemy import create_engine
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models.review import Review

the_classes = {"State", "City", "Amenity", "Review", "Place", "User"}

class DBStorage:
    """
    Attributes:
    __engine: The DBStorage's Engine with SQLAlchemy
    __session: The DBStorage's Session Maker with SQLAlchemy
    """
    __storage = None
    __engine = None
    
    def __init__(self):
        """Start the connection with MySQL
        and set it up -> Create different tables
        """
        db_uri = "{0}+{1}://{2}:{3}@{4}:3306/{5}".format(
            'mysql', 'mysqldb', getenv('HBNB_MYSQL_USER'),
            getenv('HBNB_MYSQL_PWD'), getenv('HBNB_MYSQL_HOST'),
            getenv('HBNB_MYSQL_DB'))

        self.__engine = create_engine(db_uri, pool_pre_ping=True)
        self.reload()

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):

        entities = dict()
        if cls:
            return self.get_data_from_table(cls, entities)
        
        for entity in the_classes:
            entities = self.get_data_from_table((entity), entities)

            return entities
    def new(self, obj):
        if obj:
            self.__session.add(obj)

    def save(self):
            self.__session.commit()

    def delete(self, obj=None):
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database (feature of SQLAlchemy)"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def get_data_from_table(self, cls, structure):
        """Fetch the data from a MySQL Table
        """

        if type(structure) is dict:
            query = self.__session.query(cls)

            for _row in query.all():
                key = "{}.{}".format(cls.__name__, _row.id)
                structure[key] = _row

            return structure

    def close(self):
        """Close the Session
        """
        self.__session.close()