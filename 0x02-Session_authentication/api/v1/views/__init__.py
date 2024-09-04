#!/usr/bin/env python3
"""
Blueprint initialization module for the API views.

This module sets up the Blueprint for the API views and imports
the necessary view modules to register routes.
"""

from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import views after creating the Blueprint to avoid circular imports
from api.v1.views.index import *  # noqa: E402
from api.v1.views.users import *  # noqa: E402
from api.v1.views.session_auth import *  # noqa: E402

# Load user data from file
User.load_from_file()
