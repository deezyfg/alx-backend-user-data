#!/usr/bin/env python3
"""Module for authentication handling."""
from typing import List, TypeVar
from flask import request


class Auth:
    """Authentication class for handling API authentication."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if authentication is required for a given path.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): List of paths
                                        exempt from authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != "/":
            path += "/"

        return path not in excluded_paths

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
