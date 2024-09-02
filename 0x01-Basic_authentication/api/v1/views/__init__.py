#!/usr/bin/env python3
"""Blueprint initialization for the API views."""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Views are imported here to avoid circular imports
from api.v1.views.index import *
from api.v1.views.users import *

# Load user data from file
User.load_from_file()
