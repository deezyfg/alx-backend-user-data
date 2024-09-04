#!/usr/bin/env python3
"""
Module of session authenticating views.
"""

import os
from typing import Tuple
from flask import abort, jsonify, request

from models.user import User
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    """Handle user login and create a new session.

    Endpoint: POST /api/v1/auth_session/login

    Returns:
        Tuple[str, int]: JSON representation of a User object
                         and HTTP status code.

    Raises:
        400: If email or password is missing.
        404: If no user is found for the given email.
        401: If the password is incorrect.
    """
    not_found_res = {"error": "no user found for this email"}
    email = request.form.get('email')
    if email is None or len(email.strip()) == 0:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if password is None or len(password.strip()) == 0:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify(not_found_res), 404
    if len(users) <= 0:
        return jsonify(not_found_res), 404
    if users[0].is_valid_password(password):
        from api.v1.app import auth
        session_id = auth.create_session(getattr(users[0], 'id'))
        res = jsonify(users[0].to_json())
        res.set_cookie(os.getenv("SESSION_NAME"), session_id)
        return res
    return jsonify({"error": "wrong password"}), 401


@app_views.route(
    '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout() -> Tuple[str, int]:
    """Handle user logout by destroying the session.

    Endpoint: DELETE /api/v1/auth_session/logout

    Returns:
        Tuple[str, int]: An empty JSON object and HTTP status code.

    Raises:
        404: If the session couldn't be destroyed.
    """
    from api.v1.app import auth
    is_destroyed = auth.destroy_session(request)
    if not is_destroyed:
        abort(404)
    return jsonify({}), 200
