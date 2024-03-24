#!/usr/bin/python3
"""defines a database based storage engine"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.base_model import BaseModel
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.user import User
from os import getenv


class DBStorage:
    """defines a database storage"""

    __engine = None
    __session = None

    def __init__(self):
        """initiates a dbEngine"""
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")

        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}"
            .format(user, passwd, host, db),
            pool_pre_ping=True
        )
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current db session all objects of a class"""
        if cls is None:
            lst = self.__session.query(City).all()
            lst.extend(self.__session.query(State).all())
            lst.extend(self.__session.query(User).all())
            lst.extend(self.__session.query(Review).all())
            lst.extend(self.__session.query(Amenity).all())
            lst.extend(self.__session.query(Place).all())
        else:
            if type(cls) is str:
                cls = eval(cls)
            lst = self.__session.query(cls)
        result = {"{}.{}".format(type(i).__name__, i.id): i for i in lst}
        return result

    def new(self, obj):
        """add an object to the curerent db session"""
        self.__session.merge(obj)

    def save(self):
        """commit all changes of the current db session"""
        self.__session.commit()


    def delete(self, obj=None):
        """delete form the current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database"""
        try:
            Base.metadata.create_all(self.__engine)
            session_factory = sessionmaker(bind=self.__engine,
                                           expire_on_commit=False)
            Session = scoped_session(session_factory)
            self.__session = Session()
        except Exception as E:
            print(E)

    def close(self):
        """Closes the current DBStorage session"""
        self.__session.close()
        # self.__session.remove()
