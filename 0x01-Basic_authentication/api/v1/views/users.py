#!/usr/bin/env python3
"""Module of User views for the API."""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """Retrieve a list of all User objects.

    Returns:
        JSON: List of all User objects.
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """Retrieve a User object by ID.

    Args:
        user_id (str): The ID of the User.

    Returns:
        JSON: The User object if found, else 404 error.
    """
    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """Delete a User object by ID.

    Args:
        user_id (str): The ID of the User.

    Returns:
        JSON: Empty JSON if deleted, else 404 error.
    """
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """Create a new User object.

    Returns:
        JSON: The created User object, or error message if creation fails.
    """
    try:
        rj = request.get_json()
        if not rj:
            return jsonify({'error': "Wrong format"}), 400
        if not rj.get("email"):
            return jsonify({'error': "email missing"}), 400
        if not rj.get("password"):
            return jsonify({'error': "password missing"}), 400

        user = User()
        user.email = rj.get("email")
        user.password = rj.get("password")
        user.first_name = rj.get("first_name")
        user.last_name = rj.get("last_name")
        user.save()
        return jsonify(user.to_json()), 201
    except Exception as e:
        return jsonify({'error': f"Can't create User: {e}"}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """Update a User object by ID.

    Args:
        user_id (str): The ID of the User.

    Returns:
        JSON: The updated User object, or error message if update fails.
    """
    user = User.get(user_id)
    if user is None:
        abort(404)

    try:
        rj = request.get_json()
        if not rj:
            return jsonify({'error': "Wrong format"}), 400

        if 'first_name' in rj:
            user.first_name = rj.get('first_name')
        if 'last_name' in rj:
            user.last_name = rj.get('last_name')
        user.save()
        return jsonify(user.to_json()), 200
    except Exception as e:
        return jsonify({'error': f"Can't update User: {e}"}), 400
