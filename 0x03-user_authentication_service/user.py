#!/usr/bin/env python3
"""User module for defining the User model."""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    """
    Represents a record from the `users` table.

    Attributes:
        id (int): The primary key of the user.
        email (str): The email address of the user.
        hashed_password (str): The hashed password of the user.
        session_id (str): The session ID for the user's current session.
        reset_token (str): The token used for password reset.
    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    def __repr__(self) -> str:
        """
        Return a string representation of the User instance.

        Returns:
            str: A string containing the user's ID.
        """
        return f"User: id={self.id}"
