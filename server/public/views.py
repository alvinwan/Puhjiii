from flask import Blueprint
from server.views import render

# setup Blueprint
mod_public = Blueprint('public', __name__)