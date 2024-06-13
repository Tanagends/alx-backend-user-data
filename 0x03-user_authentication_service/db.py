#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from typing import Dict

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """adds user to database"""
        usr = User(email=email, hashed_password=hashed_password)
        self._session.add(usr)
        self._session.commit()
        return usr

    def find_user_by(self, **kwargs) -> User:
        """returns first row of keyword arguments"""
        try:
            usr = self._session.query(User).filter_by(**kwargs).first()
        except AttributeError:
            raise InvalidRequestError

        if usr is None:
            raise NoResultFound
        return usr

    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates usr"""
        usr = self.find_user_by(id=user_id)

        for key, update in kwargs.items():
            if key in User.__table__.columns:
                setattr(self, key, update)
            else:
                raise ValueError
        self._session.commit
