#!/usr/bin/env python3
"""
A simple end-to-end (E2E) integration test suite for `app.py`.

This module contains a series of tests that simulate user interactions
with the application, including registration, login, profile access,
logout, and password reset functionalities. It ensures that the API
endpoints behave as expected under various scenarios.
"""
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """
    Test user registration functionality.

    This function attempts to register a new user and then tries to
    register the same user again to check for proper error handling.

    Args:
        email (str): The email address for the new user.
        password (str): The password for the new user.

    Raises:
        AssertionError: If any of the assertions fail.
    """
    url = "{}/users".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    res = requests.post(url, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "user created"}
    res = requests.post(url, data=body)
    assert res.status_code == 400
    assert res.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Test login functionality with an incorrect password.

    This function attempts to log in with a valid email but an incorrect
    password to ensure proper error handling.

    Args:
        email (str): A valid user email address.
        password (str): An incorrect password for the given email.

    Raises:
        AssertionError: If the assertion fails.
    """
    url = "{}/sessions".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    res = requests.post(url, data=body)
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Test login functionality with correct credentials.

    This function attempts to log in with valid credentials and returns
    the session ID upon successful login.

    Args:
        email (str): A valid user email address.
        password (str): The correct password for the given email.

    Returns:
        str: The session ID cookie value.

    Raises:
        AssertionError: If any of the assertions fail.
    """
    url = "{}/sessions".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    res = requests.post(url, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "logged in"}
    return res.cookies.get('session_id')


def profile_unlogged() -> None:
    """
    Test profile access when not logged in.

    This function attempts to access the user profile without being
    logged in to ensure proper access control.

    Raises:
        AssertionError: If the assertion fails.
    """
    url = "{}/profile".format(BASE_URL)
    res = requests.get(url)
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Test profile access when logged in.

    This function attempts to access the user profile with a valid
    session ID to ensure authorized access is granted.

    Args:
        session_id (str): A valid session ID obtained from successful login.

    Raises:
        AssertionError: If any of the assertions fail.
    """
    url = "{}/profile".format(BASE_URL)
    req_cookies = {
        'session_id': session_id,
    }
    res = requests.get(url, cookies=req_cookies)
    assert res.status_code == 200
    assert "email" in res.json()


def log_out(session_id: str) -> None:
    """
    Test logout functionality.

    This function attempts to log out a user with a valid session ID.

    Args:
        session_id (str): A valid session ID obtained from successful login.

    Raises:
        AssertionError: If any of the assertions fail.
    """
    url = "{}/sessions".format(BASE_URL)
    req_cookies = {
        'session_id': session_id,
    }
    res = requests.delete(url, cookies=req_cookies)
    assert res.status_code == 200
    assert res.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """
    Test password reset token request.

    This function attempts to request a password reset token for a given email.

    Args:
        email (str): The email address for which to request a reset token.

    Returns:
        str: The reset token received from the server.

    Raises:
        AssertionError: If any of the assertions fail.
    """
    url = "{}/reset_password".format(BASE_URL)
    body = {'email': email}
    res = requests.post(url, data=body)
    assert res.status_code == 200
    assert "email" in res.json()
    assert res.json()["email"] == email
    assert "reset_token" in res.json()
    return res.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Test password update functionality.

    This function attempts to update a user's password using a valid
    reset token.

    Args:
        email (str): The email address of the user.
        reset_token (str): A valid reset token obtained
                           from reset_password_token.
        new_password (str): The new password to set.

    Raises:
        AssertionError: If any of the assertions fail.
    """
    url = "{}/reset_password".format(BASE_URL)
    body = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password,
    }
    res = requests.put(url, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
