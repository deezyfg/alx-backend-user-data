#!/usr/bin/env python3
"""Session authentication with expiration module for the API.
"""

import os
from flask import request
from datetime import datetime, timedelta

from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Session authentication class with expiration."""

    def __init__(self) -> None:
        """Initialize a new SessionExpAuth instance.

        Sets the session duration from the
        SESSION_DURATION environment variable.
        """
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', '0'))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create a session ID for the user.

        Args:
            user_id: The ID of the user.

        Returns:
            str: The created session ID or None if creation fails.
        """
        session_id = super().create_session(user_id)
        if not isinstance(session_id, str):
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now(),
        }
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """Retrieve the user ID associated with a given session ID.

        Args:
            session_id: The session ID to look up.

        Returns:
            str: The user ID associated with the session ID
                 or None if not found
                 or if the session has expired.
        """
        if session_id in self.user_id_by_session_id:
            session_dict = self.user_id_by_session_id[session_id]
            if self.session_duration <= 0:
                return session_dict['user_id']
            if 'created_at' not in session_dict:
                return None
            cur_time = datetime.now()
            time_span = timedelta(seconds=self.session_duration)
            exp_time = session_dict['created_at'] + time_span
            if exp_time < cur_time:
                return None
            return session_dict['user_id']
        return None
