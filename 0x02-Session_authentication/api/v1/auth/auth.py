#!/usr/bin/env python3
"""
Module for handling API authentication.
"""
import os
import re
from typing import List, TypeVar
from flask import request


class Auth:
    """
    Authentication class for handling API authentication.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if authentication is required for a given path.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): List of paths
                                        exempt from authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        path = path.rstrip('/') + '/'  # Ensure path ends with exactly one '/'

        for excluded_path in map(lambda x: x.strip(), excluded_paths):
            if excluded_path.endswith('*'):
                pattern = f"^{re.escape(excluded_path[:-1])}.*$"
            elif excluded_path.endswith('/'):
                pattern = f"^{re.escape(excluded_path[:-1])}/?.*$"
            else:
                pattern = f"^{re.escape(excluded_path)}/?$"
            if re.match(pattern, path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Get the Authorization header from the request.

        Args:
            request: The Flask request object.

        Returns:
            str: The Authorization header value or None if not present.
        """
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar("User"):
        """Get the current authenticated user.

        Args:
            request: The Flask request object.

        Returns:
            User: The current authenticated user or None.
        """
        return None

    def session_cookie(self, request=None) -> str:
        """
        Get the value of the cookie named SESSION_NAME.

        Args:
            request: The Flask request object.

        Returns:
            str: The value of the session cookie or None if not present.
        """
        if request is None:
            return None

        cookie_name = os.getenv('SESSION_NAME')
        if cookie_name is None:
            return None

        return request.cookies.get(cookie_name)
