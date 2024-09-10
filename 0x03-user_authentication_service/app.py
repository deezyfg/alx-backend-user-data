#!/usr/bin/env python3
"""A simple Flask app with user authentication features."""
from auth import Auth
from flask import Flask, jsonify, request, abort, redirect
from typing import Tuple


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> Tuple[str, int]:
    """Handle GET request for the home page.

    Endpoint: GET /

    Returns:
        Tuple[str, int]: JSON response with a welcome message
                         and HTTP status code.
    """
    return jsonify({"message": "Bienvenue"}), 200


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> Tuple[str, int]:
    """Handle user registration.

    Endpoint: POST /users

    Returns:
        Tuple[str, int]: JSON response with user creation confirmation
                         or error message, and HTTP status code.

    Raises:
        400: If email is already registered.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> Tuple[str, int]:
    """Handle user login and create a new session.

    Endpoint: POST /sessions

    Returns:
        Tuple[str, int]: JSON response with login confirmation
                         and HTTP status code.

    Raises:
        401: If login credentials are invalid.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    valid_login = AUTH.valid_login(email, password)
    if valid_login:
        session_id = AUTH.create_session(email)
        response = jsonify({"email": f"{email}", "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> Tuple[str, int]:
    """Handle user logout by destroying the session.

    Endpoint: DELETE /sessions

    Returns:
        Tuple[str, int]: Redirect response to home route
                         and HTTP status code.

    Raises:
        403: If session is invalid.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        abort(403)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> Tuple[str, int]:
    """Retrieve the profile information of the logged-in user.

    Endpoint: GET /profile

    Returns:
        Tuple[str, int]: JSON response with user's email
                         and HTTP status code.

    Raises:
        403: If session is invalid.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> Tuple[str, int]:
    """Generate a password reset token for the given email.

    Endpoint: POST /reset_password

    Returns:
        Tuple[str, int]: JSON response with email and reset token
                         and HTTP status code.

    Raises:
        403: If email is invalid.
    """
    email = request.form.get("email")
    reset_token = None
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        reset_token = None
    if reset_token is None:
        abort(403)
    return jsonify({"email": email, "reset_token": reset_token}), 200


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> Tuple[str, int]:
    """Update the user's password using the provided reset token.

    Endpoint: PUT /reset_password

    Returns:
        Tuple[str, int]: JSON response confirming password update
                         and HTTP status code.

    Raises:
        403: If reset token is invalid.
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    is_password_changed = False
    try:
        AUTH.update_password(reset_token, new_password)
        is_password_changed = True
    except ValueError:
        is_password_changed = False
    if not is_password_changed:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
