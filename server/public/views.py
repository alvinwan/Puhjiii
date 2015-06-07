from flask import Blueprint
from server.views import render

# setup Blueprint
mod_public = Blueprint('public', __name__)


@mod_public.route("/")
def index():
	return render('index.html', mod='public')