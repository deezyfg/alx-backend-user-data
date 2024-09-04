#!/usr/bin/env python3
"""User session module for managing user session data."""

from models.base import Base


class UserSession(Base):
    """User session class for representing and managing user sessions."""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a UserSession instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
