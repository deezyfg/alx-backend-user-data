#!/usr/bin/env python3
"""
Module of Index views for the API.
"""

from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """Get the status of the API.

    Endpoint: GET /api/v1/status

    Returns:
        str: JSON response containing the API status.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """Get the count of objects in the API.

    Endpoint: GET /api/v1/stats

    Returns:
        str: JSON response containing the count of each object type.
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route('/unauthorized/', strict_slashes=False)
def unauthorized() -> None:
    """Raise a 401 Unauthorized error.

    Endpoint: GET /api/v1/unauthorized

    Raises:
        werkzeug.exceptions.Unauthorized: 401 Unauthorized error.
    """
    abort(401)


@app_views.route('/forbidden/', strict_slashes=False)
def forbidden() -> None:
    """Raise a 403 Forbidden error.

    Endpoint: GET /api/v1/forbidden

    Raises:
        werkzeug.exceptions.Forbidden: 403 Forbidden error.
    """
    abort(403)
