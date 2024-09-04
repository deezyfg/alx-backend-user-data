#!/usr/bin/env python3
"""Session authentication with expiration
and storage support module for the API.
"""

from flask import request
from datetime import datetime, timedelta

from models.user_session import UserSession
from .session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """Session authentication class with expiration and storage support."""

    def create_session(self, user_id=None) -> str:
        """Create and store a session ID for the user.

        Args:
            user_id: The ID of the user.

        Returns:
            str: The created session ID or None if creation fails.
        """
        session_id = super().create_session(user_id)
        if isinstance(session_id, str):
            kwargs = {
                'user_id': user_id,
                'session_id': session_id,
            }
            user_session = UserSession(**kwargs)
            user_session.save()
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """Retrieve the user ID associated with a given session ID.

        Args:
            session_id: The session ID to look up.

        Returns:
            str: The user ID associated with the session ID
                 or None if not found
                 or if the session has expired.
        """
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None
        cur_time = datetime.now()
        time_span = timedelta(seconds=self.session_duration)
        exp_time = sessions[0].created_at + time_span
        if exp_time < cur_time:
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None) -> bool:
        """Destroy an authenticated session.

        Args:
            request: The Flask request object.

        Returns:
            bool: True if the session was successfully destroyed,
                  False otherwise.
        """
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(sessions) <= 0:
            return False
        sessions[0].remove()
        return True
